from typing import List, Optional
from uuid import UUID

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


async def analyze_code(db: Session, analysis_id: UUID) -> List[CodeIssue]:
    """
    Analyze code for bugs and issues
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