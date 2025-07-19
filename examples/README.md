# LangFlow AI Integration Examples

Basic LangFlow workflow templates for quick AI integration setup.

## Available Examples

### 🤖 Basic AI Chat Workflows

| Model | File | Description |
|-------|------|-------------|
| **Gemini 2.5 Flash** | [`basic-gemini-chat.json`](langflow-workflows/basic-gemini-chat.json) | Chat with Google's latest Gemini model |
| **GPT-4o** | [`basic-gpt4o-chat.json`](langflow-workflows/basic-gpt4o-chat.json) | Chat with OpenAI's newest GPT model |
| **Claude 3.5 Sonnet** | [`basic-claude-chat.json`](langflow-workflows/basic-claude-chat.json) | Chat with Anthropic's latest Claude model |

## 🚀 How to Use

1. **Open LangFlow** at http://localhost:7860
2. **Import workflow**: Click "Import" and select one of the JSON files
3. **Add API key**: Configure your API key in the model component
4. **Test the flow**: Run a test message to verify it works
5. **Get flow ID**: Copy the flow ID for use with Open WebUI

## 📋 Workflow Pattern

All examples follow the same simple pattern:

```
Chat Input → AI Model → Chat Output
```

- **Chat Input**: Receives user messages
- **AI Model**: Processes with your chosen AI service
- **Chat Output**: Returns AI response

## 🔑 API Key Setup

Each workflow requires an API key:

- **Gemini**: Get from [Google AI Studio](https://makersuite.google.com/app/apikey)
- **OpenAI**: Get from [OpenAI Platform](https://platform.openai.com/api-keys)
- **Anthropic**: Get from [Anthropic Console](https://console.anthropic.com/)

## 💡 Integration with Open WebUI

After importing and configuring a workflow:

1. Copy the workflow/flow ID from LangFlow
2. Use in Open WebUI chat with: `@flow:your-flow-id your message`
3. The pipeline will route messages through LangFlow

## 🛠 Customization

These are minimal starting templates. You can extend them by:

- Adding system prompts
- Including memory components
- Adding document processing
- Creating multi-step workflows
- Implementing RAG (Retrieval-Augmented Generation)

## 📚 Model Information

- **Gemini 2.5 Flash**: Latest Google model with fast responses
- **GPT-4o**: OpenAI's newest model with multimodal capabilities  
- **Claude 3.5 Sonnet**: Anthropic's advanced reasoning model

*Keep it simple, keep it working!*