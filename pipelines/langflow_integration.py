"""
Langflow Integration Pipeline for Open WebUI
Connects Open WebUI chat interface with Langflow workflows
"""

import asyncio
import aiohttp
import json
import logging
from typing import List, Dict, Any, Optional, AsyncGenerator
from pydantic import BaseModel, Field

from pipelines.base import Pipeline


class LangflowPipeline(Pipeline):
    """
    Pipeline that integrates Open WebUI with Langflow workflows
    """
    
    class Valves(BaseModel):
        """Configuration valves for the Langflow integration"""
        LANGFLOW_BASE_URL: str = Field(
            default="http://langflow:7860",
            description="Base URL for Langflow API"
        )
        LANGFLOW_API_KEY: str = Field(
            default="",
            description="API key for Langflow authentication"
        )
        DEFAULT_FLOW_ID: str = Field(
            default="",
            description="Default flow ID to use if none specified"
        )
        ENABLE_STREAMING: bool = Field(
            default=True,
            description="Enable streaming responses from Langflow"
        )
        TIMEOUT_SECONDS: int = Field(
            default=30,
            description="Request timeout in seconds"
        )
        DEBUG_MODE: bool = Field(
            default=False,
            description="Enable debug logging"
        )

    def __init__(self):
        super().__init__()
        self.valves = self.Valves()
        self.name = "Langflow Integration"
        self.id = "langflow_pipeline"
        self.description = "Integrates Open WebUI with Langflow workflows"
        
        # Setup logging
        self.logger = logging.getLogger(self.__class__.__name__)
        if self.valves.DEBUG_MODE:
            self.logger.setLevel(logging.DEBUG)

    async def on_startup(self):
        """Initialize the pipeline on startup"""
        self.logger.info(f"🚀 Starting Langflow Pipeline")
        self.logger.info(f"📡 Langflow URL: {self.valves.LANGFLOW_BASE_URL}")
        
        # Test connection to Langflow
        try:
            await self._test_langflow_connection()
            self.logger.info("✅ Langflow connection successful")
        except Exception as e:
            self.logger.error(f"❌ Langflow connection failed: {e}")

    async def on_shutdown(self):
        """Cleanup on shutdown"""
        self.logger.info("🛑 Shutting down Langflow Pipeline")

    async def _test_langflow_connection(self) -> bool:
        """Test connection to Langflow API"""
        url = f"{self.valves.LANGFLOW_BASE_URL}/api/v1/health"
        
        async with aiohttp.ClientSession() as session:
            async with session.get(
                url,
                timeout=aiohttp.ClientTimeout(total=5)
            ) as response:
                if response.status == 200:
                    return True
                else:
                    raise Exception(f"Health check failed with status {response.status}")

    async def _get_available_flows(self) -> List[Dict[str, Any]]:
        """Get list of available flows from Langflow"""
        url = f"{self.valves.LANGFLOW_BASE_URL}/api/v1/flows"
        headers = {}
        
        if self.valves.LANGFLOW_API_KEY:
            headers["Authorization"] = f"Bearer {self.valves.LANGFLOW_API_KEY}"

        async with aiohttp.ClientSession() as session:
            async with session.get(url, headers=headers) as response:
                if response.status == 200:
                    data = await response.json()
                    return data.get("flows", [])
                else:
                    self.logger.error(f"Failed to get flows: {response.status}")
                    return []

    async def _run_langflow(
        self, 
        flow_id: str, 
        message: str, 
        user_id: str = "user",
        session_id: str = "default",
        input_type: str = "chat",
        **kwargs
    ) -> Dict[str, Any]:
        """Execute a Langflow workflow"""
        
        url = f"{self.valves.LANGFLOW_BASE_URL}/api/v1/run/{flow_id}"
        
        # Prepare the payload for Langflow
        payload = {
            "input_value": message,
            "input_type": input_type,
            "output_type": "chat",
            "tweaks": kwargs.get("tweaks", {}),
            "session_id": session_id,
        }
        
        headers = {
            "Content-Type": "application/json",
            "User-Agent": "OpenWebUI-Langflow-Pipeline/1.0"
        }
        
        if self.valves.LANGFLOW_API_KEY:
            headers["Authorization"] = f"Bearer {self.valves.LANGFLOW_API_KEY}"

        if self.valves.DEBUG_MODE:
            self.logger.debug(f"🔄 Running flow {flow_id} with payload: {payload}")

        async with aiohttp.ClientSession() as session:
            async with session.post(
                url,
                json=payload,
                headers=headers,
                timeout=aiohttp.ClientTimeout(total=self.valves.TIMEOUT_SECONDS)
            ) as response:
                
                if response.status == 200:
                    result = await response.json()
                    if self.valves.DEBUG_MODE:
                        self.logger.debug(f"✅ Langflow response: {result}")
                    return result
                else:
                    error_text = await response.text()
                    raise Exception(f"Langflow request failed: {response.status} - {error_text}")

    def _extract_flow_id_from_message(self, message: str) -> tuple[str, str]:
        """Extract flow ID from message if specified, otherwise use default"""
        
        # Check for flow ID in message like: @flow:flow-id rest of message
        if message.startswith("@flow:"):
            parts = message.split(" ", 1)
            if len(parts) >= 1:
                flow_id = parts[0][6:]  # Remove "@flow:" prefix
                cleaned_message = parts[1] if len(parts) > 1 else ""
                return flow_id, cleaned_message
        
        # Use default flow
        return self.valves.DEFAULT_FLOW_ID, message

    async def inlet(self, body: Dict[str, Any], user: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
        """Process incoming request before sending to model"""
        
        # Extract user information
        user_id = user.get("id", "anonymous") if user else "anonymous"
        
        # Get the last message
        messages = body.get("messages", [])
        if not messages:
            return body

        last_message = messages[-1]
        message_content = last_message.get("content", "")
        
        # Extract flow ID and clean message
        flow_id, cleaned_message = self._extract_flow_id_from_message(message_content)
        
        if not flow_id:
            # No flow specified and no default - pass through to normal model
            return body
        
        # Store flow context for outlet processing
        body["__langflow_context"] = {
            "flow_id": flow_id,
            "original_message": message_content,
            "cleaned_message": cleaned_message,
            "user_id": user_id
        }
        
        # Update the message content
        last_message["content"] = cleaned_message
        
        return body

    async def outlet(self, body: Dict[str, Any], user: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
        """Process response after model generation"""
        
        langflow_context = body.get("__langflow_context")
        if not langflow_context:
            # No Langflow context - return as is
            return body
        
        try:
            # Run the Langflow workflow
            result = await self._run_langflow(
                flow_id=langflow_context["flow_id"],
                message=langflow_context["cleaned_message"],
                user_id=langflow_context["user_id"],
                session_id=body.get("session_id", "default")
            )
            
            # Extract the response from Langflow result
            if "outputs" in result and result["outputs"]:
                # Get the first output
                output = result["outputs"][0]
                if "outputs" in output and output["outputs"]:
                    response_text = output["outputs"][0].get("message", {}).get("text", "")
                    
                    # Update the response
                    if "choices" in body and body["choices"]:
                        body["choices"][0]["message"]["content"] = response_text
                    
                    # Add metadata
                    body["__langflow_metadata"] = {
                        "flow_id": langflow_context["flow_id"],
                        "execution_time": result.get("execution_time"),
                        "session_id": result.get("session_id")
                    }
        
        except Exception as e:
            self.logger.error(f"❌ Langflow execution failed: {e}")
            
            # Return error message
            error_message = f"🚨 Langflow Error: {str(e)}"
            if "choices" in body and body["choices"]:
                body["choices"][0]["message"]["content"] = error_message
        
        # Clean up context
        if "__langflow_context" in body:
            del body["__langflow_context"]
        
        return body

    async def pipe(
        self, 
        user_message: str, 
        model_id: str, 
        messages: List[Dict[str, Any]], 
        body: Dict[str, Any]
    ) -> AsyncGenerator[str, None]:
        """
        Streaming pipe method for real-time responses
        """
        
        if not self.valves.ENABLE_STREAMING:
            # Fall back to non-streaming
            yield user_message
            return
        
        # Extract flow ID
        flow_id, cleaned_message = self._extract_flow_id_from_message(user_message)
        
        if not flow_id:
            yield user_message
            return
        
        try:
            # For streaming, we'll need to implement Langflow streaming API
            # For now, we'll simulate streaming by chunking the response
            result = await self._run_langflow(
                flow_id=flow_id,
                message=cleaned_message,
                session_id=body.get("session_id", "default")
            )
            
            if "outputs" in result and result["outputs"]:
                output = result["outputs"][0]
                if "outputs" in output and output["outputs"]:
                    response_text = output["outputs"][0].get("message", {}).get("text", "")
                    
                    # Simulate streaming by yielding chunks
                    words = response_text.split()
                    for i, word in enumerate(words):
                        if i == 0:
                            yield word
                        else:
                            yield f" {word}"
                        await asyncio.sleep(0.05)  # Small delay for streaming effect
            
        except Exception as e:
            yield f"🚨 Langflow Error: {str(e)}"


# Pipeline registration
pipeline = LangflowPipeline()
