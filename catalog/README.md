# 📚 Langflow Examples Catalog

This catalog contains ready-to-use Langflow workflow examples that can be imported and used directly in the Langflow + Open WebUI environment.

## 🤖 Available AI Examples

### 1. **Gemini Pro Chat** (`gemini-chat-basic.json`)
- **Model**: Google Gemini Pro (latest version)
- **Architecture**: Chat Input → Gemini → Chat Output
- **Usage**: Basic chat with Google Gemini
- **Pipeline**: `gemini_chat_pipeline.py`

### 2. **GPT-4 Chat** (`gpt4-chat-basic.json`)
- **Model**: OpenAI GPT-4 (latest version)
- **Architecture**: Chat Input → OpenAI GPT → Chat Output
- **Usage**: Basic chat with GPT-4
- **Pipeline**: `gpt4_chat_pipeline.py`

### 3. **Claude-3 Chat** (`claude3-chat-basic.json`)
- **Model**: Anthropic Claude-3 (latest version)
- **Architecture**: Chat Input → Claude → Chat Output
- **Usage**: Basic chat with Claude-3
- **Pipeline**: `claude_chat_pipeline.py`

## 🚀 How to Use Examples

### Import to Langflow
1. Start the environment: `./setup-openwebui.sh`
2. Open Langflow: http://localhost:7860
3. Click "Import" or "Load Flow"
4. Select JSON file from `flows/` directory
5. Configure API keys for your chosen model
6. Save and run the workflow

### Usage in Open WebUI
1. Copy the flow ID from Langflow
2. In Open WebUI write: `@flow:your-flow-id Your message`
3. Pipeline automatically routes to the appropriate AI model

### Pipeline Configuration
1. Copy the appropriate pipeline file from `pipelines/`
2. Update `WORKFLOW_ID` in the pipeline file
3. Restart pipelines service: `docker-compose restart pipelines`

## 🔧 Catalog Structure

```
catalog/
├── README.md                          # This file
├── flows/                            # JSON files for import
│   ├── gemini-chat-basic.json       # Gemini example
│   ├── gpt4-chat-basic.json         # GPT-4 example
│   └── claude3-chat-basic.json      # Claude-3 example
└── pipelines/                       # Integration scripts
    ├── gemini_chat_pipeline.py      # Pipeline for Gemini
    ├── gpt4_chat_pipeline.py        # Pipeline for GPT-4
    └── claude_chat_pipeline.py      # Pipeline for Claude
```

## 🔑 Required API Keys

To use the examples, you need API keys:

- **Gemini**: Google AI Studio API Key
- **GPT-4**: OpenAI API Key
- **Claude-3**: Anthropic API Key

Configure them in environment variables or directly in Langflow.

## 💡 Tips

- **Each example** is a complete, functional workflow
- **Single AI usage** - one model per workflow
- **Latest models** - we use the newest versions of each AI
- **Simple integrations** - focus on basic chat flow

## 🛠️ Extending

You can easily extend these examples:
- Add text preprocessing
- Integrate with databases
- Add memory/conversation history
- Connect to external APIs

---

*More documentation: [Main README](../README.md)*