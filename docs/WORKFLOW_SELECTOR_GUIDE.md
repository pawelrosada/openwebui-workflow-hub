# Dynamic Workflow Selector Guide

## Overview
The Dynamic Workflow Selector Pipeline enables users to dynamically select and switch between different Langflow workflows directly from the OpenWebUI chat interface, eliminating the need to manually configure workflow IDs.

## 🚀 Key Features

### Dynamic Workflow Selection
- **Auto-discovery**: Automatically discovers all available workflows from Langflow
- **Chat Commands**: Select workflows using simple chat commands  
- **Session Memory**: Remembers workflow selection per user session
- **Real-time Switching**: Switch between workflows during conversations

### Workflow Management Commands
- `@workflows` - List all available workflows
- `@workflow:name Your message` - Use specific workflow by name
- `@flow:id Your message` - Use specific workflow by ID
- `@set-workflow:name` - Set default workflow for current session

### Backward Compatibility
- Maintains compatibility with existing single-workflow setups
- Fallback to default workflow if discovery fails
- Preserves all existing pipeline features

## 📋 Setup Instructions

### 1. Replace Pipeline File
Replace your current pipeline with the workflow selector:

```bash
# Backup your current pipeline (optional)
cp pipelines/langflow_pipeline.py pipelines/langflow_pipeline.py.backup

# Copy the new workflow selector pipeline
cp pipelines/workflow_selector_pipeline.py pipelines/langflow_pipeline.py
```

### 2. Configure Pipeline Settings
In OpenWebUI Admin → Settings → Pipelines, configure:

```
LANGFLOW_BASE_URL=http://host.docker.internal:7860
DEFAULT_WORKFLOW_ID=your-fallback-workflow-id
ENABLE_WORKFLOW_DISCOVERY=true
ENABLE_SESSION_MEMORY=true
WORKFLOW_CACHE_TTL=300
```

### 3. Optional: Authentication
If your Langflow instance requires authentication:

```
LANGFLOW_API_KEY=your-api-key-here
```

## 💬 Usage Examples

### Listing Available Workflows
```
User: @workflows
Bot: 📋 Dostępne przepływy pracy:

• Basic Chat Bot
  - Klucz: basic-chat-bot
  - ID: 3ec49b62-4a8e-4cb9-9913-a51086ca7471...
  - Opis: Simple conversational AI

• Document QA
  - Klucz: document-qa  
  - ID: 7f8e9a2b-5c6d-4e5f-8912-3456789abcde...
  - Opis: Document question answering

💡 Użycie:
- @workflow:nazwa Twoja wiadomość - Użyj konkretnego przepływu
- @flow:id Twoja wiadomość - Użyj ID przepływu
- @set-workflow:nazwa - Ustaw domyślny dla sesji
```

### Using Specific Workflows
```
User: @workflow:document-qa What is the main topic of the uploaded document?
Bot: 🔧 Document QA: The main topic of the document is artificial intelligence...

User: @workflow:basic-chat-bot Hello, how are you today?
Bot: 🔧 Basic Chat Bot: Hello! I'm doing great, thank you for asking...
```

### Setting Default Workflow for Session
```
User: @set-workflow:document-qa
Bot: ✅ Ustawiono domyślny przepływ: Document QA dla tej sesji.

User: What is machine learning?
Bot: 🔧 Document QA: Machine learning is a subset of artificial intelligence...
```

### Using Workflow by ID
```
User: @flow:7f8e9a2b-5c6d-4e5f-8912-3456789abcde Tell me about quantum computing
Bot: 🔧 Document QA: Quantum computing is an emerging technology...
```

## 🔧 Advanced Configuration

### Workflow Discovery Settings
```python
# Cache duration for workflow list (seconds)
WORKFLOW_CACHE_TTL=300

# Enable/disable automatic workflow discovery
ENABLE_WORKFLOW_DISCOVERY=true

# HTTP timeout for Langflow API calls
CONNECTION_TIMEOUT=30
```

### Session Management
```python
# Remember workflow selection per user session
ENABLE_SESSION_MEMORY=true

# Rate limiting (requests per second)
RATE_LIMIT=5
```

## 🎯 Workflow Discovery Process

The pipeline automatically discovers workflows using multiple endpoints:
1. `/api/v1/flows` - Primary endpoint
2. `/api/v1/flows/` - Alternative endpoint  
3. `/api/flows` - Legacy endpoint

### Workflow Naming Convention
- Workflow names are automatically converted to lowercase keys
- Spaces are replaced with hyphens
- Example: "My Chat Bot" becomes "my-chat-bot"

## 🛠️ Troubleshooting

### Common Issues

**No workflows found:**
```
🚨 Błąd: Nie znaleziono dostępnych przepływów pracy.
```
- Check Langflow is running on correct URL
- Verify API authentication if enabled
- Check Langflow logs for errors

**Workflow not found:**
```
🚨 Błąd: Nie znaleziono przepływu 'my-workflow'. Dostępne: basic-chat, document-qa
```
- Use `@workflows` to see exact workflow names
- Check spelling and use lowercase with hyphens

**Connection errors:**
```
🚨 Błąd połączenia: Nie można połączyć się z usługą Langflow.
```
- Verify Langflow service is running
- Check LANGFLOW_BASE_URL configuration
- Test connectivity: `curl http://host.docker.internal:7860/health`

### Debug Mode
Enable debug logging to troubleshoot issues:
```python
logger.setLevel("DEBUG")
```

Check pipeline logs:
```bash
docker-compose logs -f pipelines
```

## 🔄 Migration from Existing Pipeline

### From Original Pipeline
1. Save your current `WORKFLOW_ID` value
2. Replace pipeline file
3. Set `DEFAULT_WORKFLOW_ID` to your saved value
4. Test with existing workflows

### From Enhanced Multi-Model Pipeline  
1. Save your model-specific workflow IDs
2. Replace pipeline file
3. Create workflows in Langflow with descriptive names
4. Use `@set-workflow:name` for each model workflow

## 📊 Session Management

### How Sessions Work
- Sessions are identified by user ID or chat ID
- Each session remembers the selected workflow
- Session data is stored in memory (resets on pipeline restart)

### Session Commands
```
@set-workflow:my-workflow    # Set default for this session
@workflows                   # List available workflows
Regular message              # Uses session default or system default
```

## 🎯 Integration with OpenWebUI Features

### Compatible Features
- ✅ Document upload and RAG
- ✅ Web search integration  
- ✅ User authentication and sessions
- ✅ Chat history and context
- ✅ Pipeline admin configuration

### Workflow Selection in Different Contexts
- **New Chat**: Uses system default workflow
- **Existing Chat**: Uses session-selected workflow
- **Different Users**: Each user has independent session
- **Admin Panel**: Configure system-wide defaults

## 🚀 Best Practices

### Workflow Organization
1. **Use Descriptive Names**: "Customer Support Bot" vs "Bot1"
2. **Consistent Naming**: Use clear naming conventions
3. **Categorize Workflows**: Group by purpose (chat, qa, analysis)

### Performance Optimization
1. **Cache Settings**: Adjust `WORKFLOW_CACHE_TTL` based on workflow update frequency
2. **Rate Limiting**: Configure appropriate `RATE_LIMIT` for your setup
3. **Connection Timeout**: Set reasonable `CONNECTION_TIMEOUT` values

### User Experience
1. **Default Workflow**: Set a good general-purpose workflow as default
2. **Clear Instructions**: Document available workflows for your users
3. **Error Handling**: Monitor logs for common user errors

---

**Note**: This pipeline is designed to work seamlessly with existing Langflow setups while providing powerful dynamic workflow selection capabilities. It maintains backward compatibility and provides extensive error handling for production use.