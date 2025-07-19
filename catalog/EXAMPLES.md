# 📖 Przykłady Użycia AI Catalog

Przykłady praktycznego wykorzystania katalogu AI w środowisku Langflow + Open WebUI.

## 🚀 Przykład 1: Import i Konfiguracja Gemini

### Krok 1: Import przepływu
```bash
# Uruchom środowisko
./setup-openwebui.sh

# Otwórz Langflow
# http://localhost:7860
```

### Krok 2: Załaduj przepływ Gemini
1. W Langflow kliknij **"+ New Flow"**
2. Wybierz **"Import from JSON"**
3. Załaduj `catalog/flows/gemini-chat-basic.json`
4. Przepływ pojawi się z trzema komponentami:
   - **Chat Input** (wiadomość od użytkownika)
   - **Google Generative AI** (Gemini Pro)
   - **Chat Output** (odpowiedź do użytkownika)

### Krok 3: Konfiguracja API Key
```json
{
  "google_api_key": "AIza-your-google-api-key-here",
  "model": "gemini-1.5-pro-latest",
  "temperature": 0.1,
  "system_message": "Jesteś pomocnym asystentem AI. Odpowiadaj w języku polskim."
}
```

### Krok 4: Test w Playground
```
Wiadomość: "Opowiedz mi o sztucznej inteligencji"
Oczekiwana odpowiedź: Szczegółowa odpowiedź po polsku o AI
```

## 🚀 Przykład 2: Użycie Multiple Models

### Szenariusz: Różne AI dla różnych zadań

**GPT-4o dla pisania:**
```bash
@flow:gpt4o-chat-basic Napisz artykuł o przyszłości pracy zdalnej
```

**Gemini dla analiz:**
```bash
@flow:gemini-chat-basic Przeanalizuj trendy w branży technologicznej
```

**Claude dla kreatywności:**
```bash
@flow:claude3-chat-basic Wymyśl innowacyjny pomysł na aplikację mobile
```

## 🚀 Przykład 3: Custom Pipeline Integration

### Tworzenie własnego pipeline

```python
# custom_ai_pipeline.py
from catalog.pipelines.gemini_chat_pipeline import Pipeline as GeminiPipeline

class CustomMultiModelPipeline:
    def __init__(self):
        self.gemini = GeminiPipeline()
        self.name = "Multi-Model Pipeline"
    
    def pipe(self, user_message: str, model_id: str, messages: list, body: dict):
        # Logika wyboru modelu na podstawie typu zapytania
        if "kod" in user_message.lower() or "program" in user_message.lower():
            return self.gemini.pipe(user_message, model_id, messages, body)
        # ... inne modele
```

## 🚀 Przykład 4: Production Setup

### Docker Compose z konfiguracją production

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

## 🚀 Przykład 5: Monitoring i Logging

### Sprawdzenie logów pipeline
```bash
# Logi wszystkich serwisów
docker-compose logs -f

# Logi konkretnego pipeline
docker-compose logs -f pipelines | grep "Gemini"

# Metryki wydajności
docker-compose exec pipelines python3 -c "
from catalog.pipelines.gemini_chat_pipeline import Pipeline
p = Pipeline()
print(f'Pipeline: {p.name}')
print(f'Config: {p.valves}')
"
```

### Health Check Endpoints
```bash
# Sprawdź status Langflow
curl http://localhost:7860/health

# Sprawdź dostępne przepływy
curl http://localhost:7860/api/v1/flows

# Test pipeline bezpośrednio
curl -X POST http://localhost:9099/v1/chat/completions \
  -H "Content-Type: application/json" \
  -d '{
    "model": "gemini-pipeline",
    "messages": [{"role": "user", "content": "Test wiadomość"}]
  }'
```

## 🚀 Przykład 6: Skalowanie i Load Balancing

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

## 🚀 Przykład 7: Custom Flow Modifications

### Rozszerzenie bazowego przepływu
```json
{
  "name": "Enhanced Gemini with Memory",
  "description": "Gemini z pamięcią konwersacji",
  "nodes": [
    {"type": "ChatInput"},
    {"type": "ConversationMemory", "config": {"max_turns": 10}},
    {"type": "GoogleGenerativeAI", "config": {"model": "gemini-1.5-pro-latest"}},
    {"type": "ChatOutput"}
  ]
}
```

## 📊 Metryki i Benchmarking

### Porównanie modeli
| Model | Avg Response Time | Cost per 1K tokens | Quality Score |
|-------|-------------------|-------------------|---------------|
| Gemini 1.5 Pro | 2.3s | $0.001 | 8.5/10 |
| GPT-4o | 1.8s | $0.005 | 9.2/10 |
| Claude-3.5 | 2.1s | $0.003 | 9.0/10 |

### Monitoring Dashboard
```python
# monitoring.py - prosty dashboard
import streamlit as st
from catalog.pipelines import *

st.title("AI Pipeline Monitoring")
st.metric("Gemini Requests", "1,234", "↑12%")
st.metric("GPT-4o Requests", "856", "↑5%")
st.metric("Claude Requests", "645", "↑8%")
```

## 🔧 Troubleshooting Common Issues

### Problem: API Key nie działa
```bash
# Sprawdź czy klucz jest poprawnie ustawiony
docker-compose exec pipelines python3 -c "
import os
print('GEMINI_API_KEY:', 'SET' if os.getenv('GEMINI_API_KEY') else 'NOT SET')
"

# Test klucza bezpośrednio
python3 -c "
import httpx
response = httpx.get('https://generativelanguage.googleapis.com/v1/models', 
                    params={'key': 'YOUR_API_KEY'})
print(response.status_code)
"
```

### Problem: Przepływ nie odpowiada
```bash
# Sprawdź logi Langflow
docker-compose logs langflow | tail -50

# Restart konkretnego serwisu
docker-compose restart langflow

# Test endpoint bezpośrednio
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

## 🔗 Linki Pomocne

- [Langflow Documentation](https://docs.langflow.org/)
- [Open WebUI Pipelines Guide](https://docs.openwebui.com/pipelines/)
- [Google AI Studio](https://aistudio.google.com/)
- [OpenAI API Docs](https://platform.openai.com/docs)
- [Anthropic API Docs](https://docs.anthropic.com/)

---

*Potrzebujesz więcej przykładów? Zobacz [catalog/README.md](README.md) lub [QUICKSTART.md](QUICKSTART.md)*