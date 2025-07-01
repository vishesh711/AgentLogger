from typing import List, Optional
from uuid import UUID
import asyncio

from sqlalchemy.orm import Session

from app.models.db.analysis import AnalysisRequest, AnalysisStatus
from app.models.schemas.analysis import AnalysisRequestCreate, CodeIssue
from app.services.ai.groq_client import GroqClient
from app.utils.parsing.parser_factory import get_parser_for_language


async def create_analysis_request(
    db: Session, analysis_data: AnalysisRequestCreate, user_id: UUID
) -> AnalysisRequest:
    """
    Create a new analysis request
    """
    db_analysis = AnalysisRequest(
        language=analysis_data.language,
        code=analysis_data.code,
        user_id=user_id,
    )
    db.add(db_analysis)
    db.commit()
    db.refresh(db_analysis)
    return db_analysis


async def get_analysis_request(db: Session, analysis_id: UUID) -> Optional[AnalysisRequest]:
    """
    Get an analysis request by ID
    """
    return db.query(AnalysisRequest).filter(AnalysisRequest.id == analysis_id).first()


async def get_analysis_requests_by_user(db: Session, user_id: UUID, skip: int = 0, limit: int = 100) -> List[AnalysisRequest]:
    """
    Get all analysis requests for a user
    """
    return (
        db.query(AnalysisRequest)
        .filter(AnalysisRequest.user_id == user_id)
        .order_by(AnalysisRequest.created_at.desc())
        .offset(skip)
        .limit(limit)
        .all()
    )


async def analyze_code_with_agents(db: Session, analysis_id: UUID, agent_system) -> List[CodeIssue]:
    """
    Analyze code using the multi-agent system
    """
    # Get the analysis request
    analysis = await get_analysis_request(db, analysis_id)
    if not analysis:
        raise ValueError(f"Analysis request with ID {analysis_id} not found")
    
    # Update status to processing
    analysis.status = AnalysisStatus.PROCESSING
    db.commit()
    
    try:
        # Submit the request to the agent system
        session_id = await agent_system.submit_user_request(
            user_id=str(analysis.user_id),
            code=analysis.code,
            language=analysis.language,
            error_message=None  # No error message for basic analysis
        )
        
        # Store the session ID for tracking
        analysis.session_id = session_id
        db.commit()
        
        # Get the coordinator agent to access active sessions
        coordinator = agent_system.agents.get("coordinator_1")
        if not coordinator:
            raise Exception("Coordinator agent not found")
        
        # Wait for the analysis to complete (with timeout)
        max_wait_time = 60  # 60 seconds timeout
        poll_interval = 2   # Check every 2 seconds
        waited_time = 0
        
        while waited_time < max_wait_time:
            # Check if the session has completed
            session_data = coordinator.active_sessions.get(session_id)
            if session_data and session_data.get("state") == "completed":
                # Extract issues from the session
                issues = session_data.get("issues", [])
                
                # Convert to CodeIssue objects
                code_issues = []
                for issue in issues:
                    code_issues.append(CodeIssue(
                        type=issue.get("type", "unknown"),
                        message=issue.get("message", ""),
                        line_start=issue.get("line_start", 1),
                        line_end=issue.get("line_end"),
                        column_start=issue.get("column_start"),
                        column_end=issue.get("column_end"),
                        severity=issue.get("severity", "medium"),
                        confidence=issue.get("confidence", 0.5)
                    ))
                
                # Update the analysis request with the issues
                analysis.issues = [issue.dict() for issue in code_issues]
                analysis.status = AnalysisStatus.COMPLETED
                db.commit()
                
                return code_issues
            
            elif session_data and session_data.get("state") == "error":
                # Analysis failed
                error_msg = session_data.get("error", "Unknown error occurred")
                analysis.status = AnalysisStatus.FAILED
                analysis.error = error_msg
                db.commit()
                raise Exception(error_msg)
            
            # Wait before checking again
            await asyncio.sleep(poll_interval)
            waited_time += poll_interval
        
        # Timeout occurred
        analysis.status = AnalysisStatus.FAILED
        analysis.error = "Analysis timed out"
        db.commit()
        raise Exception("Analysis timed out after 60 seconds")
        
    except Exception as e:
        # Update status to failed
        analysis.status = AnalysisStatus.FAILED
        analysis.error = str(e)
        db.commit()
        
        raise e


async def analyze_code(db: Session, analysis_id: UUID, agent_system=None) -> List[CodeIssue]:
    """
    Analyze code for bugs and issues using agent system or fallback to direct LLM
    """
    if agent_system:
        return await analyze_code_with_agents(db, analysis_id, agent_system)
    else:
        # Fallback to direct LLM analysis if agent system is not available
        print("Agent system not provided, falling back to direct analysis")
        return await analyze_code_direct(db, analysis_id)


async def analyze_code_direct(db: Session, analysis_id: UUID) -> List[CodeIssue]:
    """
    Analyze code directly using LLM (fallback method)
    """
    # Get the analysis request
    analysis = await get_analysis_request(db, analysis_id)
    if not analysis:
        raise ValueError(f"Analysis request with ID {analysis_id} not found")
    
    # Update status to processing
    analysis.status = AnalysisStatus.PROCESSING
    db.commit()
    
    try:
        # Get the parser for the language
        parser = get_parser_for_language(analysis.language)
        
        # Pre-process the code if needed
        preprocessed_code = parser.preprocess(analysis.code)
        
        # Analyze the code using the LLM
        groq_client = GroqClient()
        issues = await groq_client.analyze_code(preprocessed_code, analysis.language)
        
        # Post-process the issues if needed
        processed_issues = parser.process_analysis_results(issues)
        
        # Update the analysis request with the issues
        analysis.issues = [issue.dict() for issue in processed_issues]
        analysis.status = AnalysisStatus.COMPLETED
        db.commit()
        
        return processed_issues
    
    except Exception as e:
        # Update status to failed
        analysis.status = AnalysisStatus.FAILED
        analysis.error = str(e)
        db.commit()
        
        raise e 