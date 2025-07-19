# 🚀 Quick Start Guide for AI Examples

Step-by-step guide to get Gemini, GPT-4, and Claude-3 examples running in the Langflow + Open WebUI environment.

## 📋 Requirements

- Docker and Docker Compose
- API keys for chosen models:
  - **Gemini**: Google AI Studio API Key
  - **GPT-4o**: OpenAI API Key  
  - **Claude-3.5**: Anthropic API Key

## 🎯 Installation and Setup

### 1. Start Environment

```bash
# Clone repository (if you don't have it yet)
git clone <repo-url>
cd langflow-ui

# Start all services
./setup-openwebui.sh
```

Wait until all services are ready. Check availability:
- 🌐 Open WebUI: http://localhost:3000
- 🔧 Langflow: http://localhost:7860

### 2. Import Example to Langflow

**Option A: Import from JSON file**
1. Open http://localhost:7860
2. Click **"New Flow"** → **"Upload"**
3. Select file from `catalog/flows/` directory:
   - `gemini-chat-basic.json` - for Gemini
   - `gpt4-chat-basic.json` - for GPT-4o
   - `claude3-chat-basic.json` - for Claude-3.5

**Option B: Copy pipeline**
1. Copy appropriate pipeline from `catalog/pipelines/` to main `pipelines/` directory
2. Restart pipelines service: `docker-compose restart pipelines`

### 3. Configure API Keys

After importing the workflow in Langflow:

1. Click on AI component (Gemini/GPT/Claude)
2. In the right panel find **"API Key"** field
3. Enter your API key
4. Click **"Save"** or **Ctrl+S**

### 4. Test the Workflow

**In Langflow:**
1. Click **"Playground"** in the bottom right corner
2. Write a test message, e.g. "Hello, how are you?"
3. Click **"Run"** and check if you receive a response

**In Open WebUI:**
1. Open http://localhost:3000
2. Write: `@flow:your-endpoint-name Your message`
   - Example: `@flow:gemini-chat-basic Tell me about AI`

## 🔧 Customization

### Changing AI Model

**Gemini:**
- `gemini-pro` - basic model
- `gemini-1.5-pro-latest` - newest (default)
- `gemini-1.5-flash-latest` - faster model

**GPT-4o:**
- `gpt-4o` - newest (default)
- `gpt-4-turbo` - alternative
- `gpt-4o-mini` - cheaper version

**Claude-3.5:**
- `claude-3-5-sonnet-20240620` - newest (default)
- `claude-3-opus-20240229` - most intelligent
- `claude-3-haiku-20240307` - fastest

### Customizing System Message

In each workflow you can change the system message:
1. Click on AI component
2. Find **"System Message"** field
3. Change to your instruction, e.g.:
   ```
   You are a programming expert. 
   Answer specifically with code examples.
   ```

### Changing Parameters

**Temperature (0.0-1.0):**
- `0.1` - very conservative responses
- `0.7` - more creative (default)
- `1.0` - very creative

**Max Tokens:**
- `512` - short responses
- `1024` - medium responses (default)
- `2048` - long responses

## 🐛 Troubleshooting

### Error: "API Key not found"
1. Check if you entered the correct API key
2. Check if the key has proper permissions
3. Make sure you saved the workflow after entering the key

### Error: "Connection Error"
1. Check if all services are running: `docker-compose ps`
2. Check logs: `docker-compose logs langflow`
3. Restart services: `docker-compose restart`

### No response from model
1. Check Langflow logs: `docker-compose logs -f langflow`
2. Test directly in Langflow Playground
3. Check if model is available in your region

### Pipeline not working in Open WebUI
1. Check if pipeline is in `pipelines/` directory
2. Restart pipelines: `docker-compose restart pipelines`
3. Check logs: `docker-compose logs -f pipelines`

## 💡 Pro Tips

1. **Copy flow ID** from Langflow URL after saving
2. **Use different endpoint_name** for different versions
3. **Always test in Playground** before using in Open WebUI
4. **Monitor logs** during first run
5. **Use Docker volumes** to preserve data

## 🔄 Updates

To update Docker images:
```bash
docker-compose pull
docker-compose up -d
```

## 📞 Help

- **Service logs**: `docker-compose logs -f [service-name]`
- **Service status**: `docker-compose ps`
- **Restart all**: `docker-compose restart`
- **Reset data**: `./setup-openwebui.sh --clean`

---

**Need help?** Check the main [README.md](../../README.md) or service logs.