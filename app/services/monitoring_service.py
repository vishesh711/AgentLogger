import logging
import time
from typing import Dict, Any, Optional
from datetime import datetime

import httpx

from app.core.config import settings

logger = logging.getLogger(__name__)


class MonitoringService:
    """
    Service for monitoring and analytics
    
    This service provides methods for tracking usage, performance metrics,
    and other analytics data.
    """
    
    def __init__(self):
        self.enabled = settings.ENABLE_ANALYTICS
        self.provider = settings.ANALYTICS_PROVIDER
        self.api_key = settings.ANALYTICS_API_KEY
        
        if self.enabled and not self.api_key:
            logger.warning("Analytics enabled but no API key provided")
            self.enabled = False
    
    async def track_api_call(
        self, 
        endpoint: str, 
        user_id: str, 
        duration_ms: float,
        status_code: int,
        metadata: Optional[Dict[str, Any]] = None
    ) -> None:
        """
        Track an API call
        
        Args:
            endpoint: The API endpoint called
            user_id: The ID of the user making the call
            duration_ms: The duration of the call in milliseconds
            status_code: The HTTP status code of the response
            metadata: Additional metadata about the call
        """
        if not self.enabled:
            return
            
        try:
            event_data = {
                "event": "api_call",
                "timestamp": datetime.utcnow().isoformat(),
                "properties": {
                    "endpoint": endpoint,
                    "user_id": user_id,
                    "duration_ms": duration_ms,
                    "status_code": status_code,
                }
            }
            
            if metadata:
                event_data["properties"].update(metadata)
                
            await self._send_analytics_event(event_data)
        except Exception as e:
            logger.error(f"Error tracking API call: {str(e)}")
    
    async def track_feature_usage(
        self,
        feature: str,
        user_id: str,
        success: bool,
        metadata: Optional[Dict[str, Any]] = None
    ) -> None:
        """
        Track feature usage
        
        Args:
            feature: The feature being used
            user_id: The ID of the user using the feature
            success: Whether the feature usage was successful
            metadata: Additional metadata about the feature usage
        """
        if not self.enabled:
            return
            
        try:
            event_data = {
                "event": "feature_usage",
                "timestamp": datetime.utcnow().isoformat(),
                "properties": {
                    "feature": feature,
                    "user_id": user_id,
                    "success": success,
                }
            }
            
            if metadata:
                event_data["properties"].update(metadata)
                
            await self._send_analytics_event(event_data)
        except Exception as e:
            logger.error(f"Error tracking feature usage: {str(e)}")
    
    async def _send_analytics_event(self, event_data: Dict[str, Any]) -> None:
        """
        Send an analytics event to the configured provider
        
        Args:
            event_data: The event data to send
        """
        if not self.enabled or not self.provider:
            return
            
        try:
            # Different implementations based on the provider
            if self.provider.lower() == "segment":
                await self._send_to_segment(event_data)
            elif self.provider.lower() == "mixpanel":
                await self._send_to_mixpanel(event_data)
            elif self.provider.lower() == "posthog":
                await self._send_to_posthog(event_data)
            else:
                logger.warning(f"Unknown analytics provider: {self.provider}")
        except Exception as e:
            logger.error(f"Error sending analytics event: {str(e)}")
    
    async def _send_to_segment(self, event_data: Dict[str, Any]) -> None:
        """Send event to Segment"""
        async with httpx.AsyncClient() as client:
            headers = {
                "Content-Type": "application/json",
                "Authorization": f"Bearer {self.api_key}"
            }
            
            payload = {
                "userId": event_data["properties"].get("user_id", "anonymous"),
                "event": event_data["event"],
                "properties": event_data["properties"],
                "timestamp": event_data["timestamp"]
            }
            
            await client.post(
                "https://api.segment.io/v1/track",
                headers=headers,
                json=payload,
                timeout=5.0
            )
    
    async def _send_to_mixpanel(self, event_data: Dict[str, Any]) -> None:
        """Send event to Mixpanel"""
        async with httpx.AsyncClient() as client:
            headers = {
                "Content-Type": "application/json",
                "Accept": "text/plain"
            }
            
            payload = {
                "event": event_data["event"],
                "properties": {
                    "token": self.api_key,
                    "distinct_id": event_data["properties"].get("user_id", "anonymous"),
                    "time": int(time.time()),
                    **event_data["properties"]
                }
            }
            
            await client.post(
                "https://api.mixpanel.com/track",
                headers=headers,
                json=payload,
                timeout=5.0
            )
    
    async def _send_to_posthog(self, event_data: Dict[str, Any]) -> None:
        """Send event to PostHog"""
        async with httpx.AsyncClient() as client:
            headers = {
                "Content-Type": "application/json",
                "Authorization": f"Bearer {self.api_key}"
            }
            
            payload = {
                "api_key": self.api_key,
                "event": event_data["event"],
                "properties": event_data["properties"],
                "distinct_id": event_data["properties"].get("user_id", "anonymous"),
                "timestamp": event_data["timestamp"]
            }
            
            await client.post(
                "https://app.posthog.com/capture/",
                headers=headers,
                json=payload,
                timeout=5.0
            )


# Create a global instance of the monitoring service
monitoring_service = MonitoringService() 