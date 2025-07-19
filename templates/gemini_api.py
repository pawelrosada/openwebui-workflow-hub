#!/usr/bin/env python3
"""
Google Gemini 2.5 Flash API - Individual Model Server
Dedicated FastAPI server for Google Gemini 2.5 Flash model.

Features:
- Dedicated server for gemini model on port 8001
- Flow ID routing for different workflows
- Direct LangFlow integration
- Docker-compatible setup

Usage:
    GEMINI_API_KEY="your-key-here" python gemini_api.py
    
    # Test endpoint:
    POST /invoke/{flow_id}
"""

import fastapi
import httpx
import os
from typing import Dict, Any, Optional
from pydantic import BaseModel
import logging

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = fastapi.FastAPI(
    title="Google Gemini 2.5 Flash LangFlow API",
    description="Dedicated API for Google Gemini 2.5 Flash through LangFlow",
    version="1.0.0"
)

# Model configuration
MODEL_CONFIG = {
    "model": "gemini-2.5-flash",
    "api_key": os.getenv("GEMINI_API_KEY", "<YOUR_GEMINI_API_KEY>"),
    "display_name": "Google Gemini 2.5 Flash"
}

# LangFlow configuration
LANGFLOW_BASE_URL = os.getenv("LANGFLOW_BASE_URL", "http://localhost:7860")

class ChatRequest(BaseModel):
    message: str
    context: Optional[Dict[str, Any]] = None
    temperature: Optional[float] = 0.7
    max_tokens: Optional[int] = 1000

class ChatResponse(BaseModel):
    response: str
    model: str = "Google Gemini 2.5 Flash"
    flow_id: str
    status: str = "success"

@app.get("/")
async def root():
    """API information endpoint"""
    return {
        "name": "Google Gemini 2.5 Flash LangFlow API",
        "version": "1.0.0",
        "model": MODEL_CONFIG["model"],
        "port": 8001,
        "configured": MODEL_CONFIG["api_key"] != "<YOUR_GEMINI_API_KEY>"
    }

@app.get("/health")
async def health():
    """Health check endpoint"""
    return {
        "status": "healthy", 
        "model": MODEL_CONFIG["model"],
        "langflow_url": LANGFLOW_BASE_URL,
        "configured": MODEL_CONFIG["api_key"] != "<YOUR_GEMINI_API_KEY>"
    }

@app.post("/invoke/{flow_id}", response_model=ChatResponse)
async def invoke_flow(flow_id: str, request: ChatRequest):
    """
    Invoke a LangFlow workflow with Google Gemini 2.5 Flash
    
    Args:
        flow_id: LangFlow workflow ID
        request: Chat request with message and parameters
    """
    
    # Check if API key is configured
    if MODEL_CONFIG["api_key"] == "<YOUR_GEMINI_API_KEY>":
        raise fastapi.HTTPException(
            status_code=400,
            detail="API key not configured. Set GEMINI_API_KEY environment variable."
        )
    
    try:
        # Call LangFlow API
        url = f"{LANGFLOW_BASE_URL}/api/v1/run/{flow_id}"
        
        payload = {
            "input_value": request.message,
            "output_type": "chat",
            "input_type": "chat",
            "tweaks": {
                # Model-specific configuration
                "gemini_api_key": MODEL_CONFIG["api_key"],
                "model": MODEL_CONFIG["model"],
                "temperature": request.temperature,
                "max_tokens": request.max_tokens
            }
        }
        
        logger.info(f"Invoking flow {flow_id} with gemini")
        
        async with httpx.AsyncClient(timeout=30.0) as client:
            response = await client.post(url, json=payload)
            response.raise_for_status()
            data = response.json()
            
            # Extract response text from LangFlow output structure
            text = (
                data.get("outputs", [{}])[0]
                .get("outputs", [{}])[0]
                .get("results", {})
                .get("message", {})
                .get("text", "No response from LangFlow workflow.")
            )
            
            return ChatResponse(
                response=text,
                flow_id=flow_id,
                status="success"
            )
            
    except httpx.TimeoutException:
        logger.error(f"Timeout calling LangFlow: {url}")
        raise fastapi.HTTPException(
            status_code=408,
            detail="Request timeout. LangFlow took too long to respond."
        )
        
    except httpx.HTTPStatusError as e:
        logger.error(f"HTTP error {e.response.status_code} calling LangFlow: {e}")
        raise fastapi.HTTPException(
            status_code=e.response.status_code,
            detail=f"LangFlow API error: {e.response.text}"
        )
        
    except httpx.ConnectError:
        logger.error(f"Connection error calling LangFlow: {url}")
        raise fastapi.HTTPException(
            status_code=503,
            detail="Cannot connect to LangFlow service. Check if service is running."
        )
        
    except Exception as e:
        logger.error(f"Unexpected error: {e}")
        raise fastapi.HTTPException(
            status_code=500,
            detail=f"Unexpected error: {str(e)}"
        )

if __name__ == "__main__":
    import uvicorn
    
    print(f"🚀 Starting Google Gemini 2.5 Flash API on port 8001")
    print(f"🤖 Model: {MODEL_CONFIG['model']}")
    print(f"🔗 LangFlow URL: {LANGFLOW_BASE_URL}")
    print(f"📖 API docs: http://localhost:8001/docs")
    print(f"🔑 API key configured: {MODEL_CONFIG['api_key'] != '<YOUR_GEMINI_API_KEY>'}")
    
    uvicorn.run(app, host="0.0.0.0", port=8001)
