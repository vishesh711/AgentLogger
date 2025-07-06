"""
Agent System for managing all agents and their communication.
"""
import asyncio
import logging
import uuid
from typing import Dict, List, Optional, Any

from app.agents.base_agent import BaseAgent, Message
from app.agents.coordinator_agent import CoordinatorAgent
from app.agents.analyzer_agent import AnalyzerAgent
from app.agents.fix_generator_agent import FixGeneratorAgent
from app.services.ai.groq_client import GroqClient
from app.utils.sandbox.code_runner import CodeRunner

class AgentSystem:
    """
    System for managing all agents and their communication.
    """
    def __init__(self, llm_client: GroqClient):
        self.llm_client = llm_client
        self.agents: Dict[str, BaseAgent] = {}
        self.logger = logging.getLogger("agent_system")
        self.message_queue: asyncio.Queue[Message] = asyncio.Queue()
        self.running = False
    
    def initialize_agents(self):
        """Initialize all agents in the system."""
        # Create a code runner for sandbox execution
        code_runner = CodeRunner()
        
        # Create analyzer agent
        analyzer = AnalyzerAgent(
            agent_id="analyzer_1",
            llm_client=self.llm_client,
            code_runner=code_runner
        )
        analyzer.logger = self.logger
        self.agents[analyzer.agent_id] = analyzer
        
        # Create fix generator agent
        fix_generator = FixGeneratorAgent(
            agent_id="fix_generator_1",
            llm_client=self.llm_client
        )
        fix_generator.logger = self.logger
        self.agents[fix_generator.agent_id] = fix_generator
        
        # Create coordinator agent
        coordinator = CoordinatorAgent(
            agent_id="coordinator_1",
            llm_client=self.llm_client,
            agent_registry=self.agents
        )
        coordinator.logger = self.logger
        self.agents[coordinator.agent_id] = coordinator
        
        # Set up message sending for all agents
        for agent in self.agents.values():
            agent.send_message = self.send_message
    
    async def start(self):
        """Start the agent system."""
        self.running = True
        
        # Start all agents
        agent_tasks = []
        for agent in self.agents.values():
            agent_tasks.append(asyncio.create_task(agent.start()))
        
        # Start the message dispatcher
        dispatcher_task = asyncio.create_task(self.message_dispatcher())
        
        try:
            # Wait for the dispatcher to finish (which it won't unless stopped)
            await dispatcher_task
        except asyncio.CancelledError:
            self.logger.info("Agent system shutting down")
        finally:
            # Cancel all agent tasks
            for task in agent_tasks:
                task.cancel()
            
            # Wait for all tasks to complete
            await asyncio.gather(*agent_tasks, return_exceptions=True)
            
            self.running = False
    
    async def stop(self):
        """Stop the agent system."""
        self.running = False
    
    async def message_dispatcher(self):
        """Dispatch messages to the appropriate agents."""
        while self.running:
            message = await self.message_queue.get()
            try:
                recipient_id = message.recipient_id
                
                if recipient_id in self.agents:
                    # Send the message to the specific agent
                    await self.agents[recipient_id].receive_message(message)
                elif recipient_id == "user" or not recipient_id.endswith("_1"):
                    # This is a message for the user (either explicit "user" or any non-agent ID)
                    await self.handle_user_message(message)
                else:
                    self.logger.warning(f"Message for unknown recipient: {recipient_id}")
            except Exception as e:
                self.logger.error(f"Error dispatching message: {str(e)}")
            finally:
                self.message_queue.task_done()
    
    async def send_message(self, message: Message):
        """Send a message to the appropriate recipient."""
        await self.message_queue.put(message)
    
    async def handle_user_message(self, message: Message):
        """Handle a message intended for the user."""
        # In a real system, this would send the message to the user interface
        self.logger.info(f"Message for user: {message.content}")
    
    async def submit_user_request(self, user_id: str, code: str, language: str, error_message: Optional[str] = None) -> str:
        """Submit a user request to debug code."""
        # Create a session ID
        session_id = str(uuid.uuid4())
        
        # Create a message for the coordinator
        message = Message(
            message_type="user_request",
            sender_id=user_id,
            recipient_id="coordinator_1",  # Assuming we have only one coordinator
            content={
                "session_id": session_id,
                "code": code,
                "language": language,
                "error_message": error_message
            }
        )
        
        # Send the message
        await self.send_message(message)
        
        return session_id 