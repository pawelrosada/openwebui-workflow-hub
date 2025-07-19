#!/usr/bin/env python3
"""
Multi-Model API - Single Script Version
Universal LangFlow pipeline API that handles multiple AI models dynamically.

Basic Python API for universal LangFlow pipelines (English only; handles multiple models and flow IDs;
run on port 8000; compatible with OpenWebUI Pipelines).

Features:
- Single FastAPI app with dynamic routing
- Support for multiple models (Gemini, GPT, Claude)
- Flow ID routing for different workflows
- Easy API key configuration
- Docker-compatible setup

Usage:
    python multi_model_api_single.py

    # Test endpoints:
    POST /invoke/{flow_id}/gemini
    POST /invoke/{flow_id}/gpt
    POST /invoke/{flow_id}/claude
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
    title="Multi-Model LangFlow API",
    description="Universal API for routing requests to different AI models through LangFlow",
    version="1.0.0",
)

# Model configurations - replace with your API keys
models = {
    "gemini": {
        "model": "gemini-2.5-flash",
        "api_key": os.getenv("GEMINI_API_KEY", "<YOUR_GEMINI_API_KEY>"),
        "display_name": "Google Gemini 2.5 Flash",
    },
    "gpt": {
        "model": "gpt-4o",
        "api_key": os.getenv("OPENAI_API_KEY", "<YOUR_GPT_API_KEY>"),
        "display_name": "OpenAI GPT-4o",
    },
    "claude": {
        "model": "claude-3-5-sonnet-20241022",
        "api_key": os.getenv("ANTHROPIC_API_KEY", "<YOUR_CLAUDE_API_KEY>"),
        "display_name": "Anthropic Claude 3.5 Sonnet",
    },
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
    model: str
    flow_id: str
    status: str = "success"


@app.get("/")
async def root():
    """API information endpoint"""
    return {
        "name": "Multi-Model LangFlow API",
        "version": "1.0.0",
        "available_models": list(models.keys()),
        "endpoints": {
            "invoke": "/invoke/{flow_id}/{model_name}",
            "health": "/health",
            "models": "/models",
        },
    }


@app.get("/health")
async def health():
    """Health check endpoint"""
    return {"status": "healthy", "langflow_url": LANGFLOW_BASE_URL}


@app.get("/models")
async def get_models():
    """Get available models"""
    return {
        model_name: {
            "model": config["model"],
            "display_name": config["display_name"],
            "configured": config["api_key"] != f"<YOUR_{model_name.upper()}_API_KEY>",
        }
        for model_name, config in models.items()
    }


@app.post("/invoke/{flow_id}/{model_name}", response_model=ChatResponse)
async def invoke_flow(flow_id: str, model_name: str, request: ChatRequest):
    """
    Invoke a LangFlow workflow with specified model

    Args:
        flow_id: LangFlow workflow ID
        model_name: Model to use (gemini, gpt, claude)
        request: Chat request with message and parameters
    """

    if model_name not in models:
        raise fastapi.HTTPException(
            status_code=400,
            detail=f"Invalid model. Available models: {list(models.keys())}",
        )

    model_config = models[model_name]

    # Check if API key is configured
    if model_config["api_key"].startswith("<YOUR_"):
        raise fastapi.HTTPException(
            status_code=400,
            detail=f"API key not configured for {model_name}. Set {model_name.upper()}_API_KEY environment variable.",
        )

    try:
        # Call LangFlow API with model-specific configuration
        url = f"{LANGFLOW_BASE_URL}/api/v1/run/{flow_id}"

        payload = {
            "input_value": request.message,
            "output_type": "chat",
            "input_type": "chat",
            "tweaks": {
                # Dynamic model configuration based on selected model
                f"{model_name}_api_key": model_config["api_key"],
                "model": model_config["model"],
                "temperature": request.temperature,
                "max_tokens": request.max_tokens,
            },
        }

        logger.info(f"Invoking flow {flow_id} with model {model_name}")

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
                model=model_config["display_name"],
                flow_id=flow_id,
                status="success",
            )

    except httpx.TimeoutException:
        logger.error(f"Timeout calling LangFlow: {url}")
        raise fastapi.HTTPException(
            status_code=408,
            detail="Request timeout. LangFlow took too long to respond.",
        )

    except httpx.HTTPStatusError as e:
        logger.error(f"HTTP error {e.response.status_code} calling LangFlow: {e}")
        raise fastapi.HTTPException(
            status_code=e.response.status_code,
            detail=f"LangFlow API error: {e.response.text}",
        )

    except httpx.ConnectError:
        logger.error(f"Connection error calling LangFlow: {url}")
        raise fastapi.HTTPException(
            status_code=503,
            detail="Cannot connect to LangFlow service. Check if service is running.",
        )

    except Exception as e:
        logger.error(f"Unexpected error: {e}")
        raise fastapi.HTTPException(
            status_code=500, detail=f"Unexpected error: {str(e)}"
        )


@app.post("/invoke/universal/{model_name}")
async def invoke_universal(model_name: str, request: ChatRequest):
    """
    Universal endpoint that routes to appropriate model workflow
    Uses a default universal flow ID that can handle multiple models
    """
    # Default universal flow ID - replace with your actual universal workflow
    universal_flow_id = os.getenv("UNIVERSAL_FLOW_ID", "universal-multi-model-workflow")
    return await invoke_flow(universal_flow_id, model_name, request)


# For multi-model agentic routing
@app.post("/invoke/agent/{flow_id}")
async def invoke_agent(flow_id: str, request: ChatRequest):
    """
    Agent endpoint that can dynamically choose models based on input
    Useful for agentic workflows that route queries to different models
    """

    # Simple model selection logic based on input content
    # This can be enhanced with more sophisticated routing
    message_lower = request.message.lower()

    if any(
        word in message_lower
        for word in ["code", "programming", "python", "javascript"]
    ):
        selected_model = "claude"  # Claude is good for coding
    elif any(
        word in message_lower for word in ["creative", "story", "poem", "writing"]
    ):
        selected_model = "gpt"  # GPT-4o for creative tasks
    elif any(
        word in message_lower for word in ["search", "current", "recent", "google"]
    ):
        selected_model = "gemini"  # Gemini for search-like queries
    else:
        selected_model = "gpt"  # Default to GPT-4o

    logger.info(f"Agent routing: '{request.message[:50]}...' -> {selected_model}")
    return await invoke_flow(flow_id, selected_model, request)


if __name__ == "__main__":
    import uvicorn

    # Easy setup, Docker-compatible
    port = int(os.getenv("PORT", "8000"))
    host = os.getenv("HOST", "0.0.0.0")

    print(f"🚀 Starting Multi-Model LangFlow API on {host}:{port}")
    print(f"📊 Available models: {list(models.keys())}")
    print(f"🔗 LangFlow URL: {LANGFLOW_BASE_URL}")
    print(f"📖 API docs: http://{host}:{port}/docs")

    uvicorn.run(app, host=host, port=port)
