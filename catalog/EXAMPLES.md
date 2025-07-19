# 📖 AI Catalog Usage Examples

Examples of practical use of the AI catalog in the Langflow + Open WebUI environment.

## 🚀 Example 1: Import and Configure Gemini

### Step 1: Import workflow
```bash
# Start environment
./setup-openwebui.sh

# Open Langflow
# http://localhost:7860
```

### Step 2: Load Gemini workflow
1. In Langflow click **"+ New Flow"**
2. Select **"Import from JSON"**
3. Load `catalog/flows/gemini-chat-basic.json`
4. The workflow will appear with three components:
   - **Chat Input** (message from user)
   - **Google Generative AI** (Gemini Pro)
   - **Chat Output** (response to user)

### Step 3: API Key configuration
```json
{
  "google_api_key": "AIza-your-google-api-key-here",
  "model": "gemini-1.5-pro-latest",
  "temperature": 0.1,
  "system_message": "You are a helpful AI assistant. Respond in English."
}
```

### Step 4: Test in Playground
```
Message: "Tell me about artificial intelligence"
Expected response: Detailed response in English about AI
```

## 🚀 Example 2: Using Multiple Models

### Scenario: Different AI for different tasks

**GPT-4o for writing:**
```bash
@flow:gpt4o-chat-basic Write an article about the future of remote work
```

**Gemini for analysis:**
```bash
@flow:gemini-chat-basic Analyze trends in the technology industry
```

**Claude for creativity:**
```bash
@flow:claude3-chat-basic Create an innovative idea for a mobile app
```

## 🚀 Example 3: Custom Pipeline Integration

### Creating custom pipeline

```python
# custom_ai_pipeline.py
from catalog.pipelines.gemini_chat_pipeline import Pipeline as GeminiPipeline

class CustomMultiModelPipeline:
    def __init__(self):
        self.gemini = GeminiPipeline()
        self.name = "Multi-Model Pipeline"
    
    def pipe(self, user_message: str, model_id: str, messages: list, body: dict):
        # Logic for model selection based on query type
        if "code" in user_message.lower() or "program" in user_message.lower():
            return self.gemini.pipe(user_message, model_id, messages, body)
        # ... other models
```

## 🚀 Example 4: Production Setup

### Docker Compose with production configuration

```yaml
# docker-compose.prod.yml
services:
  langflow:
    image: langflowai/langflow:latest
    environment:
      - LANGFLOW_DATABASE_URL=postgresql://user:pass@db:5432/langflow
      - LANGFLOW_SECRET_KEY=${LANGFLOW_SECRET_KEY}
    volumes:
      - ./catalog/flows:/app/flows:ro  # Read-only examples
    
  pipelines:
    build: ./catalog/pipelines
    environment:
      - LANGFLOW_BASE_URL=http://langflow:7860
      - GEMINI_API_KEY=${GEMINI_API_KEY}
      - OPENAI_API_KEY=${OPENAI_API_KEY}
      - ANTHROPIC_API_KEY=${ANTHROPIC_API_KEY}
```

### Environment Variables
```bash
# .env.production
GEMINI_API_KEY=AIza-your-gemini-key
OPENAI_API_KEY=sk-your-openai-key
ANTHROPIC_API_KEY=sk-ant-your-anthropic-key
LANGFLOW_SECRET_KEY=your-secret-key
```

## 🚀 Example 5: Monitoring and Logging

### Checking pipeline logs
```bash
# All services logs
docker-compose logs -f

# Specific pipeline logs
docker-compose logs -f pipelines | grep "Gemini"

# Performance metrics
docker-compose exec pipelines python3 -c "
from catalog.pipelines.gemini_chat_pipeline import Pipeline
p = Pipeline()
print(f'Pipeline: {p.name}')
print(f'Config: {p.valves}')
"
```

### Health Check Endpoints
```bash
# Check Langflow status
curl http://localhost:7860/health

# Check available workflows
curl http://localhost:7860/api/v1/flows

# Test pipeline directly
curl -X POST http://localhost:9099/v1/chat/completions \
  -H "Content-Type: application/json" \
  -d '{
    "model": "gemini-pipeline",
    "messages": [{"role": "user", "content": "Test message"}]
  }'
```

## 🚀 Example 6: Scaling and Load Balancing

### Multiple Pipeline Instances
```yaml
services:
  pipelines-gemini:
    build: ./catalog/pipelines
    environment:
      - PIPELINE_TYPE=gemini
      - WORKFLOW_ID=gemini-chat-basic
      
  pipelines-gpt4:
    build: ./catalog/pipelines
    environment:
      - PIPELINE_TYPE=gpt4
      - WORKFLOW_ID=gpt4o-chat-basic
      
  nginx-lb:
    image: nginx:alpine
    volumes:
      - ./nginx-lb.conf:/etc/nginx/nginx.conf
```

### Load Balancer Configuration
```nginx
# nginx-lb.conf
upstream ai_backends {
    server pipelines-gemini:9099 weight=3;
    server pipelines-gpt4:9099 weight=2;
    server pipelines-claude:9099 weight=1;
}

server {
    listen 80;
    location /ai/ {
        proxy_pass http://ai_backends;
    }
}
```

## 🚀 Example 7: Custom Flow Modifications

### Extending basic workflow
```json
{
  "name": "Enhanced Gemini with Memory",
  "description": "Gemini with conversation memory",
  "nodes": [
    {"type": "ChatInput"},
    {"type": "ConversationMemory", "config": {"max_turns": 10}},
    {"type": "GoogleGenerativeAI", "config": {"model": "gemini-1.5-pro-latest"}},
    {"type": "ChatOutput"}
  ]
}
```

## 📊 Metrics and Benchmarking

### Model comparison
| Model | Avg Response Time | Cost per 1K tokens | Quality Score |
|-------|-------------------|-------------------|---------------|
| Gemini 1.5 Pro | 2.3s | $0.001 | 8.5/10 |
| GPT-4o | 1.8s | $0.005 | 9.2/10 |
| Claude-3.5 | 2.1s | $0.003 | 9.0/10 |

### Monitoring Dashboard
```python
# monitoring.py - simple dashboard
import streamlit as st
from catalog.pipelines import *

st.title("AI Pipeline Monitoring")
st.metric("Gemini Requests", "1,234", "↑12%")
st.metric("GPT-4o Requests", "856", "↑5%")
st.metric("Claude Requests", "645", "↑8%")
```

## 🔧 Troubleshooting Common Issues

### Problem: API Key not working
```bash
# Check if key is properly set
docker-compose exec pipelines python3 -c "
import os
print('GEMINI_API_KEY:', 'SET' if os.getenv('GEMINI_API_KEY') else 'NOT SET')
"

# Test key directly
python3 -c "
import httpx
response = httpx.get('https://generativelanguage.googleapis.com/v1/models', 
                    params={'key': 'YOUR_API_KEY'})
print(response.status_code)
"
```

### Problem: Workflow not responding
```bash
# Check Langflow logs
docker-compose logs langflow | tail -50

# Restart specific service
docker-compose restart langflow

# Test endpoint directly
curl -X POST http://localhost:7860/api/v1/run/gemini-chat-basic \
  -H "Content-Type: application/json" \
  -d '{"input_value": "test", "input_type": "chat"}'
```

---

## 💡 Best Practices

1. **Always test in Langflow Playground first**
2. **Use environment variables for API keys**
3. **Monitor API usage and costs**
4. **Implement proper error handling**
5. **Keep backups of working flows**
6. **Use descriptive endpoint names**
7. **Document custom modifications**
8. **Test with real user scenarios**

## 🔗 Helpful Links

- [Langflow Documentation](https://docs.langflow.org/)
- [Open WebUI Pipelines Guide](https://docs.openwebui.com/pipelines/)
- [Google AI Studio](https://aistudio.google.com/)
- [OpenAI API Docs](https://platform.openai.com/docs)
- [Anthropic API Docs](https://docs.anthropic.com/)

---

*Need more examples? See [catalog/README.md](README.md) or [QUICKSTART.md](QUICKSTART.md)*