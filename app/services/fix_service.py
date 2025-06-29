from typing import Dict, List, Optional
from uuid import UUID

from sqlalchemy.orm import Session

from app.models.db.analysis import AnalysisRequest
from app.models.db.fix import FixRequest, FixStatus
from app.models.schemas.analysis import CodeIssue
from app.models.schemas.fix import FixRequestCreate
from app.services.ai.groq_client import GroqClient
from app.services.analysis_service import get_analysis_request
from app.services.github_service import create_github_pr
from app.utils.parsing.parser_factory import get_parser_for_language


async def create_fix_request(
    db: Session, fix_data: FixRequestCreate, user_id: UUID
) -> FixRequest:
    """
    Create a new fix request
    """
    # Get the analysis request to ensure it exists
    analysis = await get_analysis_request(db, fix_data.analysis_id)
    if not analysis:
        raise ValueError(f"Analysis request with ID {fix_data.analysis_id} not found")
    
    # Create the fix request
    db_fix = FixRequest(
        issue_id=fix_data.issue_id,
        create_pr=fix_data.create_pr,
        user_id=user_id,
        analysis_id=fix_data.analysis_id,
    )
    
    db.add(db_fix)
    db.commit()
    db.refresh(db_fix)
    return db_fix


async def get_fix_request(db: Session, fix_id: UUID) -> Optional[FixRequest]:
    """
    Get a fix request by ID
    """
    return db.query(FixRequest).filter(FixRequest.id == fix_id).first()


async def get_fix_requests_by_user(db: Session, user_id: UUID, skip: int = 0, limit: int = 100) -> List[FixRequest]:
    """
    Get all fix requests for a user
    """
    return (
        db.query(FixRequest)
        .filter(FixRequest.user_id == user_id)
        .order_by(FixRequest.created_at.desc())
        .offset(skip)
        .limit(limit)
        .all()
    )


async def get_fix_requests_by_analysis(db: Session, analysis_id: UUID) -> List[FixRequest]:
    """
    Get all fix requests for an analysis
    """
    return (
        db.query(FixRequest)
        .filter(FixRequest.analysis_id == analysis_id)
        .order_by(FixRequest.created_at.desc())
        .all()
    )


async def generate_fix(db: Session, fix_id: UUID) -> Dict[str, str]:
    """
    Generate a fix for a specific issue
    """
    # Get the fix request
    fix = await get_fix_request(db, fix_id)
    if not fix:
        raise ValueError(f"Fix request with ID {fix_id} not found")
    
    # Get the analysis request
    analysis = await get_analysis_request(db, fix.analysis_id)
    if not analysis:
        raise ValueError(f"Analysis request with ID {fix.analysis_id} not found")
    
    # Update status to processing
    fix.status = FixStatus.PROCESSING
    db.commit()
    
    try:
        # Find the issue in the analysis
        issue_dict = next(
            (issue for issue in analysis.issues if issue.get("id") == fix.issue_id),
            None
        )
        
        if not issue_dict:
            raise ValueError(f"Issue with ID {fix.issue_id} not found in analysis")
        
        # Convert the issue dict to a CodeIssue object
        issue = CodeIssue(**issue_dict)
        
        # Get the parser for the language
        parser = get_parser_for_language(analysis.language)
        
        # Pre-process the code if needed
        preprocessed_code = parser.preprocess(analysis.code)
        
        # Generate the fix using the LLM
        groq_client = GroqClient()
        fix_result = await groq_client.fix_issue(preprocessed_code, analysis.language, issue)
        
        # Post-process the fixed code if needed
        fixed_code = parser.process_fix_result(fix_result["fixed_code"])
        
        # Update the fix request with the results
        fix.fixed_code = fixed_code
        fix.explanation = fix_result["explanation"]
        fix.status = FixStatus.COMPLETED
        db.commit()
        
        # Create GitHub PR if requested
        if fix.create_pr and fix.github_pr:
            pr_url = await create_github_pr(db, fix_id)
            fix.pr_url = pr_url
            fix.pr_created = True
            db.commit()
        
        return {
            "fixed_code": fixed_code,
            "explanation": fix_result["explanation"],
            "pr_url": fix.pr_url,
        }
    
    except Exception as e:
        # Update status to failed
        fix.status = FixStatus.FAILED
        fix.error = str(e)
        db.commit()
        
        raise e 