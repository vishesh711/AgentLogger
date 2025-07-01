"""
Coordinator Agent for orchestrating the debugging process.
"""
import asyncio
import json
import uuid
from typing import Any, Dict, List, Optional, Union

from app.agents.base_agent import BaseAgent, Message
from app.services.ai.groq_client import GroqClient

class CoordinatorAgent(BaseAgent):
    """
    Coordinator Agent that orchestrates the debugging process.
    """
    def __init__(
        self, 
        agent_id: str, 
        llm_client: GroqClient,
        agent_registry: Dict[str, BaseAgent]
    ):
        super().__init__(agent_id=agent_id, agent_type="coordinator")
        self.llm_client = llm_client
        self.agent_registry = agent_registry
        self.active_sessions = {}
    
    async def process_message(self, message: Message) -> Optional[Message]:
        """Process incoming messages and coordinate the debugging workflow."""
        self.log(f"Processing message: {message.message_type} from {message.sender_id}")
        
        if message.message_type == "user_request":
            return await self.handle_user_request(message)
        elif message.message_type == "agent_response":
            return await self.handle_agent_response(message)
        elif message.message_type == "status_update":
            return await self.handle_status_update(message)
        else:
            self.log(f"Unknown message type: {message.message_type}", level="WARNING")
            return Message(
                message_type="error",
                sender_id=self.agent_id,
                recipient_id=message.sender_id,
                content={"error": f"Unknown message type: {message.message_type}"},
                parent_id=message.message_id
            )
    
    async def handle_user_request(self, message: Message) -> Message:
        """Handle a request from a user to debug code."""
        session_id = message.content.get("session_id") or str(uuid.uuid4())
        code = message.content.get("code")
        language = message.content.get("language")
        error_message = message.content.get("error_message")
        
        if not code:
            return Message(
                message_type="error",
                sender_id=self.agent_id,
                recipient_id=message.sender_id,
                content={"error": "No code provided"},
                parent_id=message.message_id
            )
        
        # Create a new debugging session
        self.active_sessions[session_id] = {
            "user_id": message.sender_id,
            "code": code,
            "language": language,
            "error_message": error_message,
            "state": "analyzing",
            "issues": [],
            "fixes": [],
            "plan": await self.create_debugging_plan(code, language, error_message)
        }
        
        # Send acknowledgment to user
        user_response = Message(
            message_type="status_update",
            sender_id=self.agent_id,
            recipient_id=message.sender_id,
            content={
                "session_id": session_id,
                "status": "started",
                "message": "Debugging session started. Analyzing code..."
            },
            parent_id=message.message_id
        )
        
        # Start the debugging workflow
        await self.execute_next_step(session_id)
        
        return user_response
    
    async def handle_agent_response(self, message: Message) -> Optional[Message]:
        """Handle a response from another agent."""
        session_id = message.content.get("session_id")
        if not session_id or session_id not in self.active_sessions:
            self.log(f"Unknown session ID: {session_id}", level="WARNING")
            return None
        
        session = self.active_sessions[session_id]
        current_state = session["state"]
        
        # Update session based on the agent's response
        if message.sender_id.startswith("analyzer"):
            await self.handle_analyzer_response(session_id, message)
        elif message.sender_id.startswith("explainer"):
            await self.handle_explainer_response(session_id, message)
        elif message.sender_id.startswith("fix_generator"):
            await self.handle_fix_generator_response(session_id, message)
        elif message.sender_id.startswith("test"):
            await self.handle_test_response(session_id, message)
        elif message.sender_id.startswith("pr"):
            await self.handle_pr_response(session_id, message)
        
        # Execute the next step in the workflow
        await self.execute_next_step(session_id)
        
        # If the state has changed, send an update to the user
        if session["state"] != current_state:
            return Message(
                message_type="status_update",
                sender_id=self.agent_id,
                recipient_id=session["user_id"],
                content={
                    "session_id": session_id,
                    "status": session["state"],
                    "message": f"Debugging session is now in state: {session['state']}"
                }
            )
        
        return None
    
    async def handle_status_update(self, message: Message) -> None:
        """Handle a status update from another agent."""
        # Just log it for now
        self.log(f"Status update from {message.sender_id}: {message.content.get('status')}")
        return None
    
    async def create_debugging_plan(self, code: str, language: str, error_message: Optional[str]) -> List[Dict[str, Any]]:
        """Create a plan for debugging the code."""
        # Start with a basic plan using actual available agents
        plan = [
            {"step": "analyze", "agent": "analyzer", "status": "pending"},
            {"step": "fix", "agent": "fix_generator", "status": "pending"}
        ]
        
        # If there's an error message, we can skip analysis and go straight to fixing
        if error_message:
            plan[0]["status"] = "skipped"
        
        # Note: We're not including explainer, test, and PR steps for now
        # since those agents are not implemented yet
        
        return plan
    
    async def execute_next_step(self, session_id: str):
        """Execute the next step in the debugging plan."""
        session = self.active_sessions[session_id]
        plan = session["plan"]
        
        # Find the next pending step
        next_step = next((step for step in plan if step["status"] == "pending"), None)
        if not next_step:
            # All steps are complete
            session["state"] = "completed"
            await self.send_final_report(session_id)
            return
        
        # Mark the step as in progress
        next_step["status"] = "in_progress"
        agent_type = next_step["agent"]
        
        # Find an available agent of the required type
        agent_id = f"{agent_type}_1"  # In a real system, we'd have a pool of agents
        if agent_id not in self.agent_registry:
            self.log(f"Agent {agent_id} not found", level="ERROR")
            next_step["status"] = "failed"
            session["state"] = "error"
            return
        
        # Prepare the message for the agent
        content = {
            "session_id": session_id,
            "code": session["code"],
            "language": session["language"],
            "error_message": session["error_message"],
            "issues": session["issues"],
            "fixes": session["fixes"],
            "step": next_step["step"]
        }
        
        # Send the message to the agent
        message = Message(
            message_type="task",
            sender_id=self.agent_id,
            recipient_id=agent_id,
            content=content
        )
        
        # Update session state
        session["state"] = next_step["step"]
        
        # Send the message
        await self.send_message(message)
    
    async def handle_analyzer_response(self, session_id: str, message: Message):
        """Handle a response from an analyzer agent."""
        session = self.active_sessions[session_id]
        issues = message.content.get("issues", [])
        
        # Update the session with the identified issues
        session["issues"] = issues
        
        # Mark the analysis step as complete
        for step in session["plan"]:
            if step["step"] == "analyze":
                step["status"] = "completed"
                break
    
    async def handle_explainer_response(self, session_id: str, message: Message):
        """Handle a response from an explainer agent."""
        session = self.active_sessions[session_id]
        explanations = message.content.get("explanations", [])
        
        # Update the issues with explanations
        for i, explanation in enumerate(explanations):
            if i < len(session["issues"]):
                session["issues"][i]["explanation"] = explanation
        
        # Mark the explain step as complete
        for step in session["plan"]:
            if step["step"] == "explain":
                step["status"] = "completed"
                break
    
    async def handle_fix_generator_response(self, session_id: str, message: Message):
        """Handle a response from a fix generator agent."""
        session = self.active_sessions[session_id]
        fixes = message.content.get("fixes", [])
        
        # Update the session with the generated fixes
        session["fixes"] = fixes
        
        # Mark the fix step as complete
        for step in session["plan"]:
            if step["step"] == "fix":
                step["status"] = "completed"
                break
    
    async def handle_test_response(self, session_id: str, message: Message):
        """Handle a response from a test agent."""
        session = self.active_sessions[session_id]
        test_results = message.content.get("test_results", [])
        
        # Update the fixes with test results
        for i, result in enumerate(test_results):
            if i < len(session["fixes"]):
                session["fixes"][i]["test_result"] = result
        
        # Mark the test step as complete
        for step in session["plan"]:
            if step["step"] == "test":
                step["status"] = "completed"
                break
    
    async def handle_pr_response(self, session_id: str, message: Message):
        """Handle a response from a PR agent."""
        session = self.active_sessions[session_id]
        pr_info = message.content.get("pr_info", {})
        
        # Update the session with PR information
        session["pr_info"] = pr_info
        
        # Mark the PR step as complete
        for step in session["plan"]:
            if step["step"] == "create_pr":
                step["status"] = "completed"
                break
    
    async def send_final_report(self, session_id: str):
        """Send a final report to the user."""
        session = self.active_sessions[session_id]
        
        # Create a summary of the debugging session
        summary = {
            "session_id": session_id,
            "issues": session["issues"],
            "fixes": session["fixes"],
            "pr_info": session.get("pr_info", {}),
            "final_state": session["state"],
            "plan_status": session["plan"]
        }
        
        # Log the final results for debugging
        self.log(f"🎉 Session {session_id} completed successfully!")
        self.log(f"Final summary: {summary}")
        
        # Send the summary to the user
        message = Message(
            message_type="final_report",
            sender_id=self.agent_id,
            recipient_id=session["user_id"],
            content=summary
        )
        
        await self.send_message(message)
        
        # For debugging: Store the final result before deletion
        session["_final_summary"] = summary
        session["_completed_at"] = "2025-07-01T03:30:00Z"  # Timestamp for debugging
        
        # Clean up the session after a delay to allow debugging
        # In a real system, we might archive it instead
        await asyncio.sleep(5)  # Keep session for 5 seconds for debugging
        
        if session_id in self.active_sessions:  # Check if still exists
            del self.active_sessions[session_id]
            self.log(f"Session {session_id} cleaned up") 