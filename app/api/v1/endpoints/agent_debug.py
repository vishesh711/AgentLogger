"""
API endpoints for agent-based debugging.
"""
from fastapi import APIRouter, Depends, HTTPException, BackgroundTasks
from sqlalchemy.orm import Session
from typing import Optional
import uuid
import asyncio

from app.core.db import get_db
from app.core.dependencies import get_agent_system_dependency
from app.agents.agent_system import AgentSystem
from app.services.ai.groq_client import GroqClient
from app.core.config import settings
from pydantic import BaseModel

router = APIRouter()

# Initialize the agent system
groq_client = GroqClient(api_key=settings.GROQ_API_KEY)
agent_system = AgentSystem(llm_client=groq_client)
agent_system.initialize_agents()

# Store for active debugging sessions
active_sessions = {}

class TestRequest(BaseModel):
    code: str
    language: str
    error_message: str = None

@router.post("/test-simple")
async def test_agent_simple():
    """Simple test without dependencies"""
    try:
        groq_client = GroqClient()
        return {"status": "ok", "groq_client": str(type(groq_client))}
    except Exception as e:
        return {"status": "error", "error": str(e)}

@router.post("/test-agent-system")
async def test_agent_system(agent_system: AgentSystem = Depends(get_agent_system_dependency)):
    """Test agent system dependency"""
    try:
        return {
            "status": "ok", 
            "agent_system": str(type(agent_system)),
            "agents": list(agent_system.agents.keys()) if hasattr(agent_system, 'agents') else "no agents"
        }
    except Exception as e:
        return {"status": "error", "error": str(e)}

@router.post("/test-submit")
async def test_submit_request(
    test_data: TestRequest,
    agent_system: AgentSystem = Depends(get_agent_system_dependency)
):
    """Test submitting a request to the agent system"""
    try:
        # Try to submit a simple request
        session_id = await agent_system.submit_user_request(
            user_id="test-user",
            code=test_data.code,
            language=test_data.language,
            error_message=test_data.error_message
        )
        
        return {
            "status": "ok",
            "session_id": session_id,
            "message": "Request submitted successfully"
        }
    except Exception as e:
        import traceback
        return {
            "status": "error", 
            "error": str(e),
            "traceback": traceback.format_exc()
        }

@router.post("/agent-debug")
async def start_agent_debug(
    background_tasks: BackgroundTasks,
    code: str,
    language: str,
    error_message: Optional[str] = None,
    db: Session = Depends(get_db)
):
    """
    Start an agent-based debugging session.
    """
    # Generate a user ID (in a real system, this would be authenticated)
    user_id = f"user_{uuid.uuid4()}"
    
    # Submit the request to the agent system
    session_id = await agent_system.submit_user_request(
        user_id=user_id,
        code=code,
        language=language,
        error_message=error_message
    )
    
    # Store the session
    active_sessions[session_id] = {
        "user_id": user_id,
        "status": "started",
        "updates": []
    }
    
    # Return the session ID
    return {
        "session_id": session_id,
        "status": "started",
        "message": "Debugging session started"
    }

@router.get("/agent-debug/{session_id}")
async def get_debug_status(session_id: str):
    """
    Get the status of a debugging session.
    """
    if session_id not in active_sessions:
        raise HTTPException(status_code=404, detail="Session not found")
    
    return active_sessions[session_id]

@router.post("/agent-debug/{session_id}/start")
async def start_agent_system(background_tasks: BackgroundTasks):
    """
    Start the agent system in the background.
    """
    background_tasks.add_task(agent_system.start)
    return {"status": "started", "message": "Agent system started in the background"}

@router.post("/agent-debug/{session_id}/stop")
async def stop_agent_system():
    """
    Stop the agent system.
    """
    await agent_system.stop()
    return {"status": "stopped", "message": "Agent system stopped"}

@router.post("/test-full-workflow")
async def test_full_workflow(
    test_data: TestRequest,
    agent_system: AgentSystem = Depends(get_agent_system_dependency)
):
    """Test the full agent workflow without database operations"""
    try:
        # Submit the request to the agent system
        session_id = await agent_system.submit_user_request(
            user_id="test-user",
            code=test_data.code,
            language=test_data.language,
            error_message=test_data.error_message
        )
        
        # Get the coordinator agent to access active sessions
        coordinator = agent_system.agents.get("coordinator_1")
        if not coordinator:
            return {"status": "error", "error": "Coordinator agent not found"}
        
        # Wait for completion (shorter timeout for testing)
        max_wait_time = 30  # 30 seconds timeout
        poll_interval = 2   # Check every 2 seconds
        waited_time = 0
        
        while waited_time < max_wait_time:
            # Check if the session has completed
            session_data = getattr(coordinator, 'active_sessions', {}).get(session_id)
            if session_data and session_data.get("state") == "completed":
                # Extract results from the session
                issues = session_data.get("issues", [])
                fixes = session_data.get("fixes", [])
                
                return {
                    "status": "completed",
                    "session_id": session_id,
                    "issues_count": len(issues),
                    "fixes_count": len(fixes),
                    "issues": issues[:3],  # Show first 3 issues
                    "fixes": fixes[:1] if fixes else []  # Show first fix
                }
            
            elif session_data and session_data.get("state") == "error":
                # Analysis failed
                error_msg = session_data.get("error", "Unknown error occurred")
                return {
                    "status": "error",
                    "session_id": session_id,
                    "error": error_msg
                }
            
            # Wait before checking again
            await asyncio.sleep(poll_interval)
            waited_time += poll_interval
        
        # Timeout occurred - but let's see the current state
        session_data = getattr(coordinator, 'active_sessions', {}).get(session_id, {})
        return {
            "status": "timeout",
            "session_id": session_id,
            "current_state": session_data.get("state", "unknown"),
            "waited_time": waited_time,
            "session_data": session_data
        }
        
    except Exception as e:
        import traceback
        return {
            "status": "error", 
            "error": str(e),
            "traceback": traceback.format_exc()
        } 

@router.post("/debug-coordinator")
async def debug_coordinator(
    agent_system: AgentSystem = Depends(get_agent_system_dependency)
):
    """Debug the coordinator state"""
    try:
        coordinator = agent_system.agents.get("coordinator_1")
        if not coordinator:
            return {"status": "error", "error": "Coordinator agent not found"}
        
        return {
            "status": "ok",
            "coordinator_type": str(type(coordinator)),
            "has_active_sessions": hasattr(coordinator, "active_sessions"),
            "active_sessions_count": len(coordinator.active_sessions) if hasattr(coordinator, "active_sessions") else "N/A",
            "active_sessions": dict(coordinator.active_sessions) if hasattr(coordinator, "active_sessions") else "N/A",
            "coordinator_attrs": dir(coordinator)
        }
    except Exception as e:
        import traceback
        return {
            "status": "error", 
            "error": str(e),
            "traceback": traceback.format_exc()
        }

@router.post("/test-simple-submit")
async def test_simple_submit(
    test_data: TestRequest,
    agent_system: AgentSystem = Depends(get_agent_system_dependency)
):
    """Just test submitting without waiting"""
    try:
        # Submit the request to the agent system
        session_id = await agent_system.submit_user_request(
            user_id="test-user",
            code=test_data.code,
            language=test_data.language,
            error_message=test_data.error_message
        )
        
        # Get the coordinator agent
        coordinator = agent_system.agents.get("coordinator_1")
        if not coordinator:
            return {"status": "error", "error": "Coordinator agent not found"}
        
        # Check immediate state
        await asyncio.sleep(1)  # Wait 1 second for processing to start
        
        session_data = getattr(coordinator, 'active_sessions', {}).get(session_id, {})
        
        return {
            "status": "submitted",
            "session_id": session_id,
            "immediate_state": session_data,
            "all_sessions": dict(getattr(coordinator, 'active_sessions', {})),
            "agent_system_running": agent_system.running
        }
        
    except Exception as e:
        import traceback
        return {
            "status": "error", 
            "error": str(e),
            "traceback": traceback.format_exc()
        } 

@router.post("/debug-agent-system")
async def debug_agent_system(
    agent_system: AgentSystem = Depends(get_agent_system_dependency)
):
    """Debug the agent system status"""
    try:
        return {
            "status": "ok",
            "agent_system_running": agent_system.running,
            "agents_count": len(agent_system.agents),
            "agents": list(agent_system.agents.keys()),
            "message_queue_size": agent_system.message_queue.qsize(),
            "coordinator_id": "coordinator_1" in agent_system.agents,
            "coordinator_attrs": dir(agent_system.agents.get("coordinator_1", {})) if "coordinator_1" in agent_system.agents else []
        }
    except Exception as e:
        import traceback
        return {
            "status": "error", 
            "error": str(e),
            "traceback": traceback.format_exc()
        }

@router.post("/force-start-agents")
async def force_start_agents(
    agent_system: AgentSystem = Depends(get_agent_system_dependency)
):
    """Force start the agent system if not running"""
    try:
        if not agent_system.running:
            # Try to start the agent system
            import asyncio
            asyncio.create_task(agent_system.start())
            await asyncio.sleep(2)  # Give it time to start
            
        return {
            "status": "ok",
            "agent_system_running": agent_system.running,
            "message": "Agent system start attempted"
        }
    except Exception as e:
        import traceback
        return {
            "status": "error", 
            "error": str(e),
            "traceback": traceback.format_exc()
        } 

@router.post("/test-message-dispatch")
async def test_message_dispatch(
    agent_system: AgentSystem = Depends(get_agent_system_dependency)
):
    """Test if message dispatching is working"""
    try:
        from app.agents.base_agent import Message
        
        # Create a test message
        test_message = Message(
            message_type="test",
            sender_id="test-user",
            recipient_id="coordinator_1",
            content={"test": "message dispatching"}
        )
        
        # Check queue size before
        queue_size_before = agent_system.message_queue.qsize()
        
        # Send the message
        await agent_system.send_message(test_message)
        
        # Check queue size after
        await asyncio.sleep(1)  # Give it time to process
        queue_size_after = agent_system.message_queue.qsize()
        
        # Get coordinator to check if it received anything
        coordinator = agent_system.agents.get("coordinator_1")
        
        return {
            "status": "ok",
            "queue_size_before": queue_size_before,
            "queue_size_after": queue_size_after,
            "message_sent": True,
            "coordinator_sessions": dict(getattr(coordinator, 'active_sessions', {})) if coordinator else "no coordinator"
        }
        
    except Exception as e:
        import traceback
        return {
            "status": "error", 
            "error": str(e),
            "traceback": traceback.format_exc()
        }

@router.post("/test-direct-coordinator")
async def test_direct_coordinator(
    test_data: TestRequest,
    agent_system: AgentSystem = Depends(get_agent_system_dependency)
):
    """Test calling the coordinator directly without message queue"""
    try:
        from app.agents.base_agent import Message
        
        # Get the coordinator
        coordinator = agent_system.agents.get("coordinator_1")
        if not coordinator:
            return {"status": "error", "error": "Coordinator not found"}
        
        # Create a message for the coordinator
        message = Message(
            message_type="user_request",
            sender_id="test-user",
            recipient_id="coordinator_1",
            content={
                "session_id": str(uuid.uuid4()),
                "code": test_data.code,
                "language": test_data.language,
                "error_message": test_data.error_message
            }
        )
        
        # Call the coordinator directly
        response = await coordinator.process_message(message)
        
        # Check the coordinator's active sessions after processing
        await asyncio.sleep(1)  # Give it time to process
        
        return {
            "status": "ok",
            "direct_call": True,
            "response": response.content if response else None,
            "coordinator_sessions": dict(getattr(coordinator, 'active_sessions', {}))
        }
        
    except Exception as e:
        import traceback
        return {
            "status": "error", 
            "error": str(e),
            "traceback": traceback.format_exc()
        } 

@router.post("/debug-step-by-step")
async def debug_step_by_step(
    test_data: TestRequest,
    agent_system: AgentSystem = Depends(get_agent_system_dependency)
):
    """Debug the coordinator workflow step by step"""
    try:
        from app.agents.base_agent import Message
        
        # Get the coordinator
        coordinator = agent_system.agents.get("coordinator_1")
        if not coordinator:
            return {"status": "error", "error": "Coordinator not found"}
        
        # Step 1: Create message and process it
        message = Message(
            message_type="user_request",
            sender_id="test-user",
            recipient_id="coordinator_1",
            content={
                "session_id": str(uuid.uuid4()),
                "code": test_data.code,
                "language": test_data.language,
                "error_message": test_data.error_message
            }
        )
        
        debug_info = []
        debug_info.append(f"Step 1: Created message with content: {message.content}")
        
        # Step 2: Check initial sessions
        initial_sessions = dict(getattr(coordinator, 'active_sessions', {}))
        debug_info.append(f"Step 2: Initial sessions count: {len(initial_sessions)}")
        
        # Step 3: Process the message
        response = await coordinator.process_message(message)
        debug_info.append(f"Step 3: Coordinator response: {response.content if response else 'None'}")
        
        # Step 4: Check sessions after processing
        sessions_after = dict(getattr(coordinator, 'active_sessions', {}))
        debug_info.append(f"Step 4: Sessions after processing: {len(sessions_after)}")
        debug_info.append(f"Step 4: Session data: {sessions_after}")
        
        # Step 5: Check agent registry
        agent_registry = list(coordinator.agent_registry.keys())
        debug_info.append(f"Step 5: Available agents in registry: {agent_registry}")
        
        # Step 6: Wait a bit and check again
        await asyncio.sleep(2)
        sessions_after_wait = dict(getattr(coordinator, 'active_sessions', {}))
        debug_info.append(f"Step 6: Sessions after 2s wait: {len(sessions_after_wait)}")
        debug_info.append(f"Step 6: Session data after wait: {sessions_after_wait}")
        
        return {
            "status": "ok",
            "debug_info": debug_info,
            "final_sessions": sessions_after_wait
        }
        
    except Exception as e:
        import traceback
        return {
            "status": "error", 
            "error": str(e),
            "traceback": traceback.format_exc()
        } 

@router.post("/check-session-status")
async def check_session_status(
    session_id: str,
    agent_system: AgentSystem = Depends(get_agent_system_dependency)
):
    """Check the status of a specific session"""
    try:
        # Check if the session has completed
        coordinator = agent_system.agents.get("coordinator_1")
        if coordinator and hasattr(coordinator, 'active_sessions'):
            session_data = coordinator.active_sessions.get(session_id, {})
            
            max_wait = 30  # 30 seconds timeout
            waited = 0
            
            while waited < max_wait:
                session_data = getattr(coordinator, 'active_sessions', {}).get(session_id, {})
                if session_data.get("state") in ["completed", "error"]:
                    break
                await asyncio.sleep(1)
                waited += 1
            
            return {
                "status": "ok",
                "session_id": session_id,
                "session_data": session_data,
                "all_sessions": dict(getattr(coordinator, 'active_sessions', {})),
                "waited_seconds": waited
            }
        else:
            return {
                "status": "error",
                "error": "Coordinator not found or doesn't have active_sessions attribute"
            }
    except Exception as e:
        import traceback
        return {
            "status": "error", 
            "error": str(e),
            "traceback": traceback.format_exc()
        } 