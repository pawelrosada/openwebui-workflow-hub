#!/usr/bin/env python3
"""
Multi-Model API Generator - Multi-Script Version
Generates separate API scripts for each model, running on different ports for scalability.

Creates individual FastAPI applications for each AI model (Gemini on 8001, GPT on 8002, Claude on 8003).
This approach provides better isolation and scalability for production deployments.

Usage:
    python generate_multi_scripts.py
    
    # This will generate:
    # - gemini_api.py (runs on port 8001)
    # - gpt_api.py (runs on port 8002) 
    # - claude_api.py (runs on port 8003)
    
    # Then run each script:
    # python gemini_api.py &
    # python gpt_api.py &
    # python claude_api.py &
"""

import os
from typing import Dict

def generate_model_api_script(model_name: str, model_config: Dict, port: int) -> str:
    """Generate individual API script for a specific model"""
    
    api_key_env = f"{model_name.upper()}_API_KEY"
    api_key_placeholder = f"<YOUR_{model_name.upper()}_API_KEY>"
    
    return f'''#!/usr/bin/env python3
"""
{model_config["display_name"]} API - Individual Model Server
Dedicated FastAPI server for {model_config["display_name"]} model.

Features:
- Dedicated server for {model_name} model on port {port}
- Flow ID routing for different workflows
- Direct LangFlow integration
- Docker-compatible setup

Usage:
    {api_key_env}="your-key-here" python {model_name}_api.py
    
    # Test endpoint:
    POST /invoke/{{flow_id}}
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
    title="{model_config["display_name"]} LangFlow API",
    description="Dedicated API for {model_config["display_name"]} through LangFlow",
    version="1.0.0"
)

# Model configuration
MODEL_CONFIG = {{
    "model": "{model_config["model"]}",
    "api_key": os.getenv("{api_key_env}", "{api_key_placeholder}"),
    "display_name": "{model_config["display_name"]}"
}}

# LangFlow configuration
LANGFLOW_BASE_URL = os.getenv("LANGFLOW_BASE_URL", "http://localhost:7860")

class ChatRequest(BaseModel):
    message: str
    context: Optional[Dict[str, Any]] = None
    temperature: Optional[float] = 0.7
    max_tokens: Optional[int] = 1000

class ChatResponse(BaseModel):
    response: str
    model: str = "{model_config["display_name"]}"
    flow_id: str
    status: str = "success"

@app.get("/")
async def root():
    """API information endpoint"""
    return {{
        "name": "{model_config["display_name"]} LangFlow API",
        "version": "1.0.0",
        "model": MODEL_CONFIG["model"],
        "port": {port},
        "configured": MODEL_CONFIG["api_key"] != "{api_key_placeholder}"
    }}

@app.get("/health")
async def health():
    """Health check endpoint"""
    return {{
        "status": "healthy", 
        "model": MODEL_CONFIG["model"],
        "langflow_url": LANGFLOW_BASE_URL,
        "configured": MODEL_CONFIG["api_key"] != "{api_key_placeholder}"
    }}

@app.post("/invoke/{{flow_id}}", response_model=ChatResponse)
async def invoke_flow(flow_id: str, request: ChatRequest):
    """
    Invoke a LangFlow workflow with {model_config["display_name"]}
    
    Args:
        flow_id: LangFlow workflow ID
        request: Chat request with message and parameters
    """
    
    # Check if API key is configured
    if MODEL_CONFIG["api_key"] == "{api_key_placeholder}":
        raise fastapi.HTTPException(
            status_code=400,
            detail="API key not configured. Set {api_key_env} environment variable."
        )
    
    try:
        # Call LangFlow API
        url = f"{{LANGFLOW_BASE_URL}}/api/v1/run/{{flow_id}}"
        
        payload = {{
            "input_value": request.message,
            "output_type": "chat",
            "input_type": "chat",
            "tweaks": {{
                # Model-specific configuration
                "{model_name}_api_key": MODEL_CONFIG["api_key"],
                "model": MODEL_CONFIG["model"],
                "temperature": request.temperature,
                "max_tokens": request.max_tokens
            }}
        }}
        
        logger.info(f"Invoking flow {{flow_id}} with {model_name}")
        
        async with httpx.AsyncClient(timeout=30.0) as client:
            response = await client.post(url, json=payload)
            response.raise_for_status()
            data = response.json()
            
            # Extract response text from LangFlow output structure
            text = (
                data.get("outputs", [{{}}])[0]
                .get("outputs", [{{}}])[0]
                .get("results", {{}})
                .get("message", {{}})
                .get("text", "No response from LangFlow workflow.")
            )
            
            return ChatResponse(
                response=text,
                flow_id=flow_id,
                status="success"
            )
            
    except httpx.TimeoutException:
        logger.error(f"Timeout calling LangFlow: {{url}}")
        raise fastapi.HTTPException(
            status_code=408,
            detail="Request timeout. LangFlow took too long to respond."
        )
        
    except httpx.HTTPStatusError as e:
        logger.error(f"HTTP error {{e.response.status_code}} calling LangFlow: {{e}}")
        raise fastapi.HTTPException(
            status_code=e.response.status_code,
            detail=f"LangFlow API error: {{e.response.text}}"
        )
        
    except httpx.ConnectError:
        logger.error(f"Connection error calling LangFlow: {{url}}")
        raise fastapi.HTTPException(
            status_code=503,
            detail="Cannot connect to LangFlow service. Check if service is running."
        )
        
    except Exception as e:
        logger.error(f"Unexpected error: {{e}}")
        raise fastapi.HTTPException(
            status_code=500,
            detail=f"Unexpected error: {{str(e)}}"
        )

if __name__ == "__main__":
    import uvicorn
    
    print(f"🚀 Starting {model_config["display_name"]} API on port {port}")
    print(f"🤖 Model: {{MODEL_CONFIG['model']}}")
    print(f"🔗 LangFlow URL: {{LANGFLOW_BASE_URL}}")
    print(f"📖 API docs: http://localhost:{port}/docs")
    print(f"🔑 API key configured: {{MODEL_CONFIG['api_key'] != '{api_key_placeholder}'}}")
    
    uvicorn.run(app, host="0.0.0.0", port={port})
'''

def generate_orchestrator_script() -> str:
    """Generate orchestrator script to manage all model APIs"""
    
    return '''#!/usr/bin/env python3
"""
Multi-Model API Orchestrator
Manages multiple model API servers and provides a unified interface.

Features:
- Starts all model APIs on different ports
- Health check aggregation
- Load balancing capabilities
- Unified logging

Usage:
    python orchestrator.py [start|stop|status]
"""

import subprocess
import time
import requests
import sys
import signal
import os
from typing import Dict, List

# Model API configurations
MODELS = {
    "gemini": {"port": 8001, "script": "gemini_api.py"},
    "gpt": {"port": 8002, "script": "gpt_api.py"},
    "claude": {"port": 8003, "script": "claude_api.py"}
}

class MultiModelOrchestrator:
    def __init__(self):
        self.processes: Dict[str, subprocess.Popen] = {}
    
    def start_all(self):
        """Start all model API servers"""
        print("🚀 Starting Multi-Model API Orchestrator...")
        
        for model_name, config in MODELS.items():
            if os.path.exists(config["script"]):
                print(f"   Starting {model_name} API on port {config['port']}...")
                process = subprocess.Popen([
                    sys.executable, config["script"]
                ], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
                self.processes[model_name] = process
                time.sleep(2)  # Give time to start
            else:
                print(f"   ⚠️  Script {config['script']} not found, skipping {model_name}")
        
        print(f"✅ Started {len(self.processes)} model APIs")
        self.check_health()
    
    def stop_all(self):
        """Stop all model API servers"""
        print("🛑 Stopping all model APIs...")
        
        for model_name, process in self.processes.items():
            print(f"   Stopping {model_name} API...")
            process.terminate()
            try:
                process.wait(timeout=5)
            except subprocess.TimeoutExpired:
                process.kill()
        
        self.processes.clear()
        print("✅ All APIs stopped")
    
    def check_health(self):
        """Check health of all APIs"""
        print("\\n🏥 Health Check:")
        
        for model_name, config in MODELS.items():
            try:
                response = requests.get(f"http://localhost:{config['port']}/health", timeout=3)
                if response.status_code == 200:
                    data = response.json()
                    status = "✅" if data.get("configured") else "⚠️ "
                    print(f"   {status} {model_name} API (port {config['port']}) - {data.get('status', 'unknown')}")
                else:
                    print(f"   ❌ {model_name} API (port {config['port']}) - HTTP {response.status_code}")
            except requests.RequestException:
                print(f"   ❌ {model_name} API (port {config['port']}) - Not responding")
    
    def get_status(self):
        """Get status of all APIs"""
        running = []
        for model_name, process in self.processes.items():
            if process.poll() is None:  # Still running
                running.append(model_name)
        
        print(f"📊 Status: {len(running)}/{len(MODELS)} APIs running")
        if running:
            print(f"   Running: {', '.join(running)}")
        
        return running

def signal_handler(sig, frame):
    """Handle Ctrl+C gracefully"""
    print("\\n🛑 Received interrupt signal, shutting down...")
    orchestrator.stop_all()
    sys.exit(0)

def main():
    global orchestrator
    orchestrator = MultiModelOrchestrator()
    
    # Handle Ctrl+C
    signal.signal(signal.SIGINT, signal_handler)
    
    command = sys.argv[1] if len(sys.argv) > 1 else "start"
    
    if command == "start":
        orchestrator.start_all()
        print("\\n🔄 Press Ctrl+C to stop all services")
        try:
            # Keep running
            while True:
                time.sleep(30)
                orchestrator.check_health()
        except KeyboardInterrupt:
            pass
        finally:
            orchestrator.stop_all()
            
    elif command == "stop":
        orchestrator.stop_all()
        
    elif command == "status":
        orchestrator.get_status()
        orchestrator.check_health()
        
    else:
        print("Usage: python orchestrator.py [start|stop|status]")

if __name__ == "__main__":
    main()
'''

def main():
    """Generate all multi-script files"""
    
    # Model configurations
    models = {
        "gemini": {
            "model": "gemini-2.5-flash",
            "display_name": "Google Gemini 2.5 Flash",
            "port": 8001
        },
        "gpt": {
            "model": "gpt-4o",
            "display_name": "OpenAI GPT-4o", 
            "port": 8002
        },
        "claude": {
            "model": "claude-3-5-sonnet-20241022",
            "display_name": "Anthropic Claude 3.5 Sonnet",
            "port": 8003
        }
    }
    
    print("🔧 Generating multi-script API files...")
    
    # Generate individual model scripts
    for model_name, config in models.items():
        script_content = generate_model_api_script(model_name, config, config["port"])
        filename = f"{model_name}_api.py"
        
        with open(filename, 'w', encoding='utf-8') as f:
            f.write(script_content)
        
        # Make executable
        os.chmod(filename, 0o755)
        print(f"   ✅ Generated {filename}")
    
    # Generate orchestrator script
    orchestrator_content = generate_orchestrator_script()
    with open("orchestrator.py", 'w', encoding='utf-8') as f:
        f.write(orchestrator_content)
    
    os.chmod("orchestrator.py", 0o755)
    print(f"   ✅ Generated orchestrator.py")
    
    print(f"\\n🚀 Generated {len(models)} individual API scripts + orchestrator")
    print("\\nUsage:")
    print("   # Option 1: Use orchestrator (recommended)")
    print("   python orchestrator.py start")
    print("   ")
    print("   # Option 2: Run individual scripts")
    for model_name, config in models.items():
        print(f"   {model_name.upper()}_API_KEY='your-key' python {model_name}_api.py &")
    print("\\n📚 Each API provides OpenAPI docs at http://localhost:[port]/docs")

if __name__ == "__main__":
    main()