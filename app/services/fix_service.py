from typing import Dict, List, Optional, Tuple, Any
from datetime import datetime
from sqlalchemy.orm import Session

from app.core.config import settings
from app.models.db.fix import FixRequest, FixStatus
from app.models.schemas.fix import (
    FixRequestCreate, 
    FixRequestResponse
)
from app.services.ai.groq_client import get_fix_from_groq
from app.utils.parsing.parser_factory import get_parser_for_language
from app.utils.sandbox.code_runner import run_code_in_sandbox

# Define types for clarity
CodeFix = Dict[str, Any]
ValidationResult = Tuple[bool, Optional[str]]

async def create_fix_request(
    db: Session, fix_data: FixRequestCreate, user_id: str, analysis_id: Optional[str] = None
) -> FixRequest:
    """
    Create a new fix request
    """
    db_fix = FixRequest(
        language=fix_data.language,
        code=fix_data.code,
        error_message=fix_data.error_message,
        context=fix_data.context,
        user_id=user_id,
        analysis_id=analysis_id,
    )
    db.add(db_fix)
    db.commit()
    db.refresh(db_fix)
    return db_fix

async def get_fix_request(db: Session, fix_id: str) -> Optional[FixRequestResponse]:
    """
    Get a fix request by ID
    """
    db_fix_request = db.query(FixRequest).filter(FixRequest.id == fix_id).first()
    if not db_fix_request:
        return None
    
    return FixRequestResponse.model_validate(db_fix_request)

async def get_user_fix_requests(db: Session, user_id: str, skip: int = 0, limit: int = 100) -> List[FixRequestResponse]:
    """
    Get all fix requests for a user
    """
    db_fix_requests = db.query(FixRequest).filter(
        FixRequest.user_id == user_id
    ).offset(skip).limit(limit).all()
    
    return [FixRequestResponse.model_validate(fr) for fr in db_fix_requests]

async def get_fix_requests_by_user(db: Session, user_id: str, skip: int = 0, limit: int = 100) -> List[FixRequestResponse]:
    """
    Get all fix requests for a user
    
    Args:
        db: Database session
        user_id: User ID
        skip: Number of records to skip
        limit: Maximum number of records to return
        
    Returns:
        List of fix request responses
    """
    db_fix_requests = db.query(FixRequest).filter(
        FixRequest.user_id == user_id
    ).offset(skip).limit(limit).all()
    
    return [FixRequestResponse.model_validate(fr) for fr in db_fix_requests]

async def get_fix_requests_by_analysis(db: Session, analysis_id: str) -> List[FixRequestResponse]:
    """
    Get all fix requests for a specific analysis
    
    Args:
        db: Database session
        analysis_id: Analysis ID
        
    Returns:
        List of fix request responses
    """
    db_fix_requests = db.query(FixRequest).filter(
        FixRequest.analysis_id == analysis_id
    ).all()
    
    return [FixRequestResponse.model_validate(fr) for fr in db_fix_requests]

async def process_fix_request(db: Session, fix_id: str) -> None:
    """
    Process a fix request by generating a fix using the agent system
    """
    # Get the fix request
    db_fix_request = db.query(FixRequest).filter(FixRequest.id == fix_id).first()
    if not db_fix_request:
        return
    
    # Update status
    db_fix_request.status = FixStatus.PROCESSING
    db.commit()
    
    try:
        # Try to use the agent system for comprehensive fix generation
        try:
            from app.main import get_agent_system
            agent_system = get_agent_system()
            fix_result = await process_fix_with_agents(db, db_fix_request, agent_system)
        except Exception as e:
            # Fallback to direct Groq if agent system is not available
            print(f"Agent system not available for fix generation, falling back to direct fix: {e}")
            fix_result = await process_fix_direct(db_fix_request)
        
        # Validate the fix
        is_valid, validation_message = await validate_fix(
            original_code=db_fix_request.code,
            fixed_code=fix_result["fixed_code"],
            language=db_fix_request.language
        )
        
        # Update the fix request
        db_fix_request.fixed_code = fix_result["fixed_code"]
        db_fix_request.explanation = fix_result["explanation"]
        db_fix_request.status = FixStatus.COMPLETED if is_valid else FixStatus.FAILED
        db_fix_request.validation_message = validation_message
        db_fix_request.completed_at = datetime.utcnow()
        
        db.commit()
        
    except Exception as e:
        # Handle errors
        db_fix_request.status = FixStatus.FAILED
        db_fix_request.validation_message = f"Error processing fix: {str(e)}"
        db.commit()

async def process_fix_with_agents(db: Session, fix_request: FixRequest, agent_system) -> Dict[str, str]:
    """
    Process a fix request using the multi-agent system
    """
    import asyncio
    
    # Submit the request to the agent system
    session_id = await agent_system.submit_user_request(
        user_id=str(fix_request.user_id),
        code=fix_request.code,
        language=fix_request.language,
        error_message=fix_request.error_message
    )
    
    # Store the session ID for tracking
    fix_request.session_id = session_id
    db.commit()
    
    # Get the coordinator agent to access active sessions
    coordinator = agent_system.agents.get("coordinator_1")
    if not coordinator:
        raise Exception("Coordinator agent not found")
    
    # Wait for the fix to complete (with timeout)
    max_wait_time = 90  # 90 seconds timeout for fix generation
    poll_interval = 3   # Check every 3 seconds
    waited_time = 0
    
    while waited_time < max_wait_time:
        # Check if the session has completed
        session_data = getattr(coordinator, 'active_sessions', {}).get(session_id)
        if session_data and session_data.get("state") == "completed":
            # Extract fixes from the session
            fixes = session_data.get("fixes", [])
            
            if fixes:
                # Use the first (best) fix
                best_fix = fixes[0]
                return {
                    "fixed_code": best_fix.get("fixed_code", ""),
                    "explanation": best_fix.get("explanation", "")
                }
            else:
                # No fixes generated
                return {
                    "fixed_code": fix_request.code,  # Return original code
                    "explanation": "No fixes were generated by the agent system"
                }
        
        elif session_data and session_data.get("state") == "error":
            # Fix generation failed
            error_msg = session_data.get("error", "Unknown error occurred")
            raise Exception(f"Agent system error: {error_msg}")
        
        # Wait before checking again
        await asyncio.sleep(poll_interval)
        waited_time += poll_interval
    
    # Timeout occurred
    raise Exception("Fix generation timed out after 90 seconds")

async def process_fix_direct(fix_request: FixRequest) -> Dict[str, str]:
    """
    Process a fix request directly using Groq (fallback method)
    """
    # Generate fix using Groq directly
    fix_result = await get_fix_from_groq(
        code=fix_request.code,
        language=fix_request.language,
        error_message=fix_request.error_message,
        context=fix_request.context
    )
    
    return fix_result

async def validate_fix(original_code: str, fixed_code: str, language: str) -> ValidationResult:
    """
    Validate a fix by running it in a sandbox
    """
    # Skip validation if sandbox is disabled
    if not settings.USE_DOCKER_SANDBOX:
        return True, "Sandbox validation skipped"
    
    try:
        # Run the fixed code in a sandbox
        result = await run_code_in_sandbox(fixed_code, language, timeout=settings.EXECUTION_TIMEOUT)
        
        if result["success"]:
            return True, "Code executed successfully"
        else:
            return False, f"Code execution failed: {result['error']}"
    
    except Exception as e:
        return False, f"Validation error: {str(e)}"

def create_diff(original_code: str, fixed_code: str) -> str:
    """
    Create a unified diff between original and fixed code
    """
    # In a real implementation, use a proper diff library
    # This is a simplified version
    parser = get_parser_for_language("python")  # Default to Python parser
    
    # Parse both code versions
    original_lines = original_code.splitlines()
    fixed_lines = fixed_code.splitlines()
    
    # Generate a simple diff
    diff_lines = []
    for i, (orig, fixed) in enumerate(zip(original_lines, fixed_lines)):
        if orig != fixed:
            diff_lines.append(f"Line {i+1}: - {orig}")
            diff_lines.append(f"Line {i+1}: + {fixed}")
    
    # Handle different lengths
    if len(original_lines) < len(fixed_lines):
        for i, line in enumerate(fixed_lines[len(original_lines):], start=len(original_lines)):
            diff_lines.append(f"Line {i+1}: + {line}")
    elif len(original_lines) > len(fixed_lines):
        for i, line in enumerate(original_lines[len(fixed_lines):], start=len(fixed_lines)):
            diff_lines.append(f"Line {i+1}: - {line}")
    
    return "\n".join(diff_lines)

async def generate_fix(db: Session, fix_id: str) -> Dict[str, str]:
    """
    Generate a fix for a code issue
    """
    # Get the fix request
    fix_request = await get_fix_request(db, fix_id)
    if not fix_request:
        raise ValueError(f"Fix request with ID {fix_id} not found")
    
    # Process the fix request
    await process_fix_request(db, fix_id)
    
    # Get the updated fix request
    updated_fix = await get_fix_request(db, fix_id)
    
    return {
        "fixed_code": updated_fix.fixed_code or "",
        "explanation": updated_fix.explanation or "",
        "status": updated_fix.status.value
    }

async def create_github_pr_for_fix(db: Session, fix_id: str, repo_name: str, file_path: Optional[str] = None) -> Dict[str, Any]:
    """
    Create a GitHub PR for a fix
    """
    # Import here to avoid circular imports
    from app.services.github_service import create_github_pr
    
    # Get the fix request
    db_fix = db.query(FixRequest).filter(FixRequest.id == fix_id).first()
    if not db_fix:
        raise ValueError(f"Fix request with ID {fix_id} not found")
    
    # Create the PR
    return await create_github_pr(
        db=db,
        fix_id=fix_id,
        repo_name=repo_name,
        file_path=file_path,
        fix_request=db_fix
    ) 