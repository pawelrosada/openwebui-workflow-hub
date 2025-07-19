# Multi-Model API Templates

This directory contains templates and generators for creating universal LangFlow pipelines with multi-model API support. These templates are designed to enhance Copilot's ability to generate code for handling multiple AI models dynamically.

## 📁 Files Overview

### Core API Templates
- **`multi_model_api_single.py`** - Single FastAPI script handling all models with dynamic routing
- **`generate_multi_scripts.py`** - Generator for creating separate API scripts per model (scalable approach)

### Workflow Generators  
- **`generate_universal_workflows.py`** - Creates LangFlow JSON workflows for multi-model scenarios

## 🚀 Quick Start

### Option 1: Single-Script Multi-Model API

Use when you want all models in one application:

```bash
# Install dependencies
pip install fastapi uvicorn httpx pydantic

# Set API keys
export GEMINI_API_KEY="your-gemini-key"
export OPENAI_API_KEY="your-openai-key"  
export ANTHROPIC_API_KEY="your-anthropic-key"

# Run single API server
python multi_model_api_single.py
```

**Endpoints:**
- `POST /invoke/{flow_id}/gemini` - Route to Gemini
- `POST /invoke/{flow_id}/gpt` - Route to GPT-4o
- `POST /invoke/{flow_id}/claude` - Route to Claude
- `POST /invoke/agent/{flow_id}` - Smart routing based on input

### Option 2: Multi-Script Scalable Approach

Use when you want separate isolated APIs per model:

```bash
# Generate individual API scripts
python generate_multi_scripts.py

# This creates:
# - gemini_api.py (port 8001)
# - gpt_api.py (port 8002) 
# - claude_api.py (port 8003)
# - orchestrator.py (manages all)

# Run all with orchestrator
python orchestrator.py start
```

### Option 3: Generate Universal LangFlow Workflows

Create workflow templates that support multiple models:

```bash
# Generate workflow JSON files
python generate_universal_workflows.py

# This creates:
# - universal-multi-model-chat.json
# - agentic-multi-model-router.json
```

## 🤖 AI Model Support

All templates support these models out-of-the-box:

| Model | API Key | Default Version |
|-------|---------|----------------|
| **Gemini** | `GEMINI_API_KEY` | gemini-2.5-flash |
| **GPT** | `OPENAI_API_KEY` | gpt-4o |
| **Claude** | `ANTHROPIC_API_KEY` | claude-3-5-sonnet-20241022 |

## 🏗 Architecture Patterns

### Single-Script Pattern
```
┌─────────────────────────────────────────┐
│           FastAPI Application           │
│  ┌─────────────────────────────────────┐ │
│  │     /invoke/{flow_id}/{model}       │ │
│  │                                     │ │
│  │  ┌─────────┐ ┌─────────┐ ┌────────┐ │ │
│  │  │ Gemini  │ │   GPT   │ │ Claude │ │ │
│  │  └─────────┘ └─────────┘ └────────┘ │ │
│  └─────────────────────────────────────┘ │
│                Port 8000                 │
└─────────────────────────────────────────┘
```

### Multi-Script Pattern
```
┌──────────────┐ ┌──────────────┐ ┌──────────────┐
│ Gemini API   │ │   GPT API    │ │ Claude API   │
│ Port 8001    │ │ Port 8002    │ │ Port 8003    │
└──────────────┘ └──────────────┘ └──────────────┘
        │                │               │
        └────────────────┼───────────────┘
                         │
         ┌──────────────────────────┐
         │    Orchestrator         │
         │  (Load Balancing &      │
         │   Health Monitoring)    │
         └──────────────────────────┘
```

## 🔗 Integration with LangFlow

### Universal Workflows

The generated JSON workflows can be imported into LangFlow:

1. **Universal Multi-Model Chat** - Manual model selection via dropdown
2. **Agentic Multi-Model Router** - Automatic model selection based on input

### Workflow Features
- **Dynamic Model Switching** - Change models without rebuilding workflows
- **Conditional Routing** - Smart model selection based on query type
- **UI-Friendly** - Visual editing in LangFlow interface
- **Exportable** - JSON format for version control and sharing

## 📊 Usage Examples

### Basic Multi-Model Request

```python
import httpx

# Single-script API
response = httpx.post("http://localhost:8000/invoke/my-flow-id/gemini", 
    json={
        "message": "Explain quantum computing",
        "temperature": 0.7,
        "max_tokens": 1000
    }
)

# Multi-script API (Gemini instance)
response = httpx.post("http://localhost:8001/invoke/my-flow-id",
    json={"message": "Explain quantum computing"}
)
```

### Agentic Routing

```python
# Smart routing based on input content
requests = [
    {"message": "Write a Python function to sort a list"},  # → Claude (coding)
    {"message": "Write a creative story about space"},      # → GPT (creative)
    {"message": "What's the latest news about AI?"}        # → Gemini (search)
]

for req in requests:
    response = httpx.post("http://localhost:8000/invoke/agent/my-flow-id", json=req)
```

## 🛠 Development

### Extending Model Support

To add new models, update the `models` dictionary in the templates:

```python
models = {
    "gemini": {...},
    "gpt": {...}, 
    "claude": {...},
    "new_model": {
        "model": "new-model-version",
        "api_key": os.getenv("NEW_MODEL_API_KEY", "<YOUR_NEW_MODEL_API_KEY>"),
        "display_name": "New Model Name"
    }
}
```

### Custom Routing Logic

Modify the agentic routing in `invoke_agent` endpoint:

```python
# Custom routing logic
if "database" in message_lower:
    selected_model = "claude"  # Best for SQL/DB queries
elif "translation" in message_lower:
    selected_model = "gpt"     # Good for translations
elif "summarize" in message_lower:
    selected_model = "gemini"  # Fast summarization
```

## 🔍 Testing

Test the APIs using the built-in FastAPI docs:

- Single API: http://localhost:8000/docs
- Gemini API: http://localhost:8001/docs  
- GPT API: http://localhost:8002/docs
- Claude API: http://localhost:8003/docs

## 🚀 Production Deployment

### Docker Deployment

Create a `Dockerfile` for the single-script approach:

```dockerfile
FROM python:3.11-slim

WORKDIR /app
COPY requirements.txt .
RUN pip install -r requirements.txt

COPY multi_model_api_single.py .

EXPOSE 8000
CMD ["python", "multi_model_api_single.py"]
```

### Environment Configuration

Set these environment variables in production:

```bash
# Model API Keys
GEMINI_API_KEY=your-production-gemini-key
OPENAI_API_KEY=your-production-openai-key  
ANTHROPIC_API_KEY=your-production-anthropic-key

# LangFlow Configuration
LANGFLOW_BASE_URL=https://your-langflow-instance.com
UNIVERSAL_FLOW_ID=your-default-universal-flow-id

# Server Configuration  
HOST=0.0.0.0
PORT=8000
```

## 🤝 Contributing

These templates are designed to be enhanced by GitHub Copilot. When working with this code:

1. **Keep it Simple** - Maintain basic structure for easy Copilot understanding
2. **Use Comments** - Brief English comments for key functionality
3. **Follow Patterns** - Consistent API patterns across all templates
4. **Test Integration** - Ensure compatibility with OpenWebUI Pipelines

## 📚 Related Documentation

- [LangFlow Documentation](https://docs.langflow.org/)
- [OpenWebUI Pipelines](https://docs.openwebui.com/pipelines/)
- [FastAPI Documentation](https://fastapi.tiangolo.com/)

---

**Built to enhance Copilot's ability to generate universal LangFlow pipelines with multi-model support!**