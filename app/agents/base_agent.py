"""
Base agent class that all specialized agents will inherit from.
"""
from abc import ABC, abstractmethod
import asyncio
import json
import uuid
from datetime import datetime
from typing import Any, Dict, List, Optional, Union

class Message:
    """
    Represents a message passed between agents.
    """
    def __init__(
        self,
        message_type: str,
        sender_id: str,
        recipient_id: str,
        content: Dict[str, Any],
        message_id: Optional[str] = None,
        parent_id: Optional[str] = None,
        timestamp: Optional[datetime] = None
    ):
        self.message_id = message_id or str(uuid.uuid4())
        self.message_type = message_type
        self.sender_id = sender_id
        self.recipient_id = recipient_id
        self.content = content
        self.parent_id = parent_id
        self.timestamp = timestamp or datetime.utcnow()
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert the message to a dictionary."""
        return {
            "message_id": self.message_id,
            "message_type": self.message_type,
            "sender_id": self.sender_id,
            "recipient_id": self.recipient_id,
            "content": self.content,
            "parent_id": self.parent_id,
            "timestamp": self.timestamp.isoformat()
        }
    
    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'Message':
        """Create a message from a dictionary."""
        timestamp = datetime.fromisoformat(data["timestamp"]) if isinstance(data["timestamp"], str) else data["timestamp"]
        return cls(
            message_id=data["message_id"],
            message_type=data["message_type"],
            sender_id=data["sender_id"],
            recipient_id=data["recipient_id"],
            content=data["content"],
            parent_id=data.get("parent_id"),
            timestamp=timestamp
        )

class BaseAgent(ABC):
    """
    Base class for all agents in the system.
    """
    def __init__(self, agent_id: str, agent_type: str):
        self.agent_id = agent_id
        self.agent_type = agent_type
        self.memory = {}
        self.message_queue = asyncio.Queue()
        self.tools = {}
        self.logger = None  # Will be set up by the agent system
    
    async def start(self):
        """Start the agent's message processing loop."""
        while True:
            message = await self.message_queue.get()
            try:
                response = await self.process_message(message)
                if response:
                    await self.send_message(response)
            except Exception as e:
                error_msg = f"Error processing message {message.message_id}: {str(e)}"
                self.log(error_msg, level="ERROR")
                # Create error response
                error_response = Message(
                    message_type="error",
                    sender_id=self.agent_id,
                    recipient_id=message.sender_id,
                    content={"error": error_msg},
                    parent_id=message.message_id
                )
                await self.send_message(error_response)
            finally:
                self.message_queue.task_done()
    
    async def receive_message(self, message: Message):
        """Add a message to the agent's queue."""
        await self.message_queue.put(message)
    
    async def send_message(self, message: Message):
        """Send a message to another agent."""
        # This will be implemented by the agent system
        pass
    
    @abstractmethod
    async def process_message(self, message: Message) -> Optional[Message]:
        """
        Process an incoming message and optionally return a response.
        Must be implemented by subclasses.
        """
        pass
    
    def log(self, message: str, level: str = "INFO"):
        """Log a message."""
        if self.logger:
            if level == "ERROR":
                self.logger.error(f"[{self.agent_id}] {message}")
            elif level == "WARNING":
                self.logger.warning(f"[{self.agent_id}] {message}")
            else:
                self.logger.info(f"[{self.agent_id}] {message}")
    
    def register_tool(self, tool_name: str, tool_function):
        """Register a tool that the agent can use."""
        self.tools[tool_name] = tool_function
    
    async def use_tool(self, tool_name: str, **kwargs):
        """Use a registered tool."""
        if tool_name not in self.tools:
            raise ValueError(f"Tool {tool_name} not registered")
        
        tool = self.tools[tool_name]
        return await tool(**kwargs) if asyncio.iscoroutinefunction(tool) else tool(**kwargs)
    
    def update_memory(self, key: str, value: Any):
        """Update the agent's memory."""
        self.memory[key] = value
    
    def get_memory(self, key: str, default: Any = None) -> Any:
        """Get a value from the agent's memory."""
        return self.memory.get(key, default)
    
    def clear_memory(self):
        """Clear the agent's memory."""
        self.memory = {} 