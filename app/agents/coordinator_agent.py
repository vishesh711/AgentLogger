"""
Coordinator Agent for orchestrating multi-agent debugging workflows.
"""
import asyncio
import uuid
from typing import Dict, Any, Optional, List
from datetime import datetime

from app.agents.base_agent import BaseAgent, Message


class CoordinatorAgent(BaseAgent):
    """
    Agent responsible for coordinating the entire debugging workflow.
    
    The coordinator receives user requests and orchestrates the workflow
    between analyzer, fix generator, and other specialized agents.
    """
    
    def __init__(self, agent_id: str, llm_client, agent_registry: Dict[str, BaseAgent]):
        super().__init__(agent_id, "coordinator")
        self.llm_client = llm_client
        self.agent_registry = agent_registry
        self.active_sessions: Dict[str, Dict[str, Any]] = {}
    
    async def process_message(self, message: Message) -> Optional[Message]:
        """Process incoming messages and coordinate the debugging workflow."""
        self.log(f"Processing message of type: {message.message_type}")
        
        if message.message_type == "user_request":
            return await self._handle_user_request(message)
        elif message.message_type == "analysis_result":
            return await self._handle_analysis_result(message)
        elif message.message_type == "fix_result":
            return await self._handle_fix_result(message)
        elif message.message_type == "error":
            return await self._handle_error(message)
        else:
            self.log(f"Unknown message type: {message.message_type}", level="WARNING")
            return None
    
    async def _handle_user_request(self, message: Message) -> Optional[Message]:
        """Handle a new user debugging request."""
        content = message.content
        session_id = content.get("session_id", str(uuid.uuid4()))
        code = content.get("code")
        language = content.get("language")
        error_message = content.get("error_message")
        
        # Initialize session
        self.active_sessions[session_id] = {
            "state": "analyzing",
            "user_id": message.sender_id,
            "code": code,
            "language": language,
            "error_message": error_message,
            "started_at": datetime.utcnow().isoformat(),
            "issues": [],
            "fixes": []
        }
        
        self.log(f"Starting debugging session {session_id}")
        
        # Send analysis request to analyzer agent
        analyzer_id = "analyzer_1"  # Assuming we have this agent
        if analyzer_id in self.agent_registry:
            analysis_message = Message(
                message_type="analyze_request",
                sender_id=self.agent_id,
                recipient_id=analyzer_id,
                content={
                    "session_id": session_id,
                    "code": code,
                    "language": language,
                    "error_message": error_message
                },
                parent_id=message.message_id
            )
            
            # Send to analyzer
            await self.send_message(analysis_message)
            
            # Return acknowledgment to user
            return Message(
                message_type="session_started",
                sender_id=self.agent_id,
                recipient_id=message.sender_id,
                content={
                    "session_id": session_id,
                    "status": "analyzing",
                    "message": "Code analysis started"
                },
                parent_id=message.message_id
            )
        else:
            self.log(f"Analyzer agent {analyzer_id} not found", level="ERROR")
            self.active_sessions[session_id]["state"] = "error"
            self.active_sessions[session_id]["error"] = "Analyzer agent not available"
            return None
    
    async def _handle_analysis_result(self, message: Message) -> Optional[Message]:
        """Handle analysis results from the analyzer agent."""
        content = message.content
        session_id = content.get("session_id")
        
        if session_id not in self.active_sessions:
            self.log(f"Session {session_id} not found", level="WARNING")
            return None
        
        session = self.active_sessions[session_id]
        issues = content.get("issues", [])
        session["issues"] = issues
        
        self.log(f"Received analysis for session {session_id}: {len(issues)} issues found")
        
        # If issues were found, send to fix generator
        if issues:
            session["state"] = "generating_fixes"
            
            fix_generator_id = "fix_generator_1"  # Assuming we have this agent
            if fix_generator_id in self.agent_registry:
                fix_message = Message(
                    message_type="fix_request",
                    sender_id=self.agent_id,
                    recipient_id=fix_generator_id,
                    content={
                        "session_id": session_id,
                        "code": session["code"],
                        "language": session["language"],
                        "issues": issues,
                        "error_message": session.get("error_message")
                    },
                    parent_id=message.message_id
                )
                
                await self.send_message(fix_message)
            else:
                self.log(f"Fix generator agent {fix_generator_id} not found", level="ERROR")
                session["state"] = "error"
                session["error"] = "Fix generator agent not available"
        else:
            # No issues found, mark as completed
            session["state"] = "completed"
            session["completed_at"] = datetime.utcnow().isoformat()
            
            # Notify user
            return Message(
                message_type="debugging_complete",
                sender_id=self.agent_id,
                recipient_id=session["user_id"],
                content={
                    "session_id": session_id,
                    "status": "completed",
                    "issues": [],
                    "fixes": [],
                    "message": "No issues found in the code"
                },
                parent_id=message.message_id
            )
        
        return None
    
    async def _handle_fix_result(self, message: Message) -> Optional[Message]:
        """Handle fix results from the fix generator agent."""
        content = message.content
        session_id = content.get("session_id")
        
        if session_id not in self.active_sessions:
            self.log(f"Session {session_id} not found", level="WARNING")
            return None
        
        session = self.active_sessions[session_id]
        fixes = content.get("fixes", [])
        session["fixes"] = fixes
        session["state"] = "completed"
        session["completed_at"] = datetime.utcnow().isoformat()
        
        self.log(f"Received fixes for session {session_id}: {len(fixes)} fixes generated")
        
        # Notify user of completion
        return Message(
            message_type="debugging_complete",
            sender_id=self.agent_id,
            recipient_id=session["user_id"],
            content={
                "session_id": session_id,
                "status": "completed",
                "issues": session["issues"],
                "fixes": fixes,
                "message": f"Debugging completed with {len(fixes)} fixes generated"
            },
            parent_id=message.message_id
        )
    
    async def _handle_error(self, message: Message) -> Optional[Message]:
        """Handle error messages from other agents."""
        content = message.content
        session_id = content.get("session_id")
        error = content.get("error", "Unknown error")
        
        if session_id and session_id in self.active_sessions:
            session = self.active_sessions[session_id]
            session["state"] = "error"
            session["error"] = error
            session["completed_at"] = datetime.utcnow().isoformat()
            
            self.log(f"Error in session {session_id}: {error}", level="ERROR")
            
            # Notify user of error
            return Message(
                message_type="debugging_error",
                sender_id=self.agent_id,
                recipient_id=session["user_id"],
                content={
                    "session_id": session_id,
                    "status": "error",
                    "error": error,
                    "message": f"Debugging failed: {error}"
                },
                parent_id=message.message_id
            )
        
        return None
    
    def get_session_status(self, session_id: str) -> Optional[Dict[str, Any]]:
        """Get the current status of a debugging session."""
        return self.active_sessions.get(session_id)
    
    def list_active_sessions(self) -> List[str]:
        """List all active session IDs."""
        return list(self.active_sessions.keys())
    
    def cleanup_completed_sessions(self, max_age_hours: int = 24):
        """Clean up old completed sessions."""
        current_time = datetime.utcnow()
        sessions_to_remove = []
        
        for session_id, session in self.active_sessions.items():
            if session.get("state") in ["completed", "error"]:
                completed_at = session.get("completed_at")
                if completed_at:
                    try:
                        completed_time = datetime.fromisoformat(completed_at)
                        age_hours = (current_time - completed_time).total_seconds() / 3600
                        if age_hours > max_age_hours:
                            sessions_to_remove.append(session_id)
                    except ValueError:
                        # Invalid timestamp, remove it
                        sessions_to_remove.append(session_id)
        
        for session_id in sessions_to_remove:
            del self.active_sessions[session_id]
            self.log(f"Cleaned up old session: {session_id}")
        
        return len(sessions_to_remove) 