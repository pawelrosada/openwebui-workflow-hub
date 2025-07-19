#!/usr/bin/env python3
"""
multi-model-api.py - Basic Python API for universal LangFlow pipelines (English only; 
handles multiple models and flow IDs; run on port 8000; compatible with OpenWebUI Pipelines).

This implementation matches the example provided in the GitHub issue for enhanced Copilot
generation of universal LangFlow pipelines.
"""
import fastapi  # For API routing
import httpx
import uvicorn
from langflow import load_flow  # LangFlow utilities (placeholder)

app = fastapi.FastAPI()

models = {
    "gemini": {"model": "gemini-2.5-flash", "api_key": "<YOUR_GEMINI_API_KEY>"},
    "gpt": {"model": "gpt-4o", "api_key": "<YOUR_GPT_API_KEY>"},
    "claude": {"model": "claude-sonnet-4", "api_key": "<YOUR_CLAUDE_API_KEY>"},
}


@app.post("/invoke/{flow_id}/{model_name}")
async def invoke_flow(flow_id: str, model_name: str, input_data: dict):
    if model_name not in models:
        raise fastapi.HTTPException(status_code=400, detail="Invalid model")
    
    # For demonstration purposes - actual langflow integration would go here
    # flow = load_flow(flow_id)  # Load from LangFlow ID
    # Route input to selected model in pipeline (e.g., ChatInput -> Model -> ChatOutput)
    # result = flow.run(input_data, model_config=models[model_name])  # Multi-model handling
    
    # Mock result for now
    result = f"Response from {model_name} using flow {flow_id}: {input_data.get('message', 'No input')}"
    return {"result": result}


# For multi-script option: Duplicate and run on different ports (e.g., 8001 for Gemini).
if __name__ == "__main__":
    # Easy setup, Docker-compatible
    uvicorn.run(app, host="0.0.0.0", port=8000)