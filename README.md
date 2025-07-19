# Langflow + Open WebUI Integration

Simple integration setup that connects Open WebUI with Langflow for AI workflow management.

## 🚀 Features

- **Open WebUI** - Modern chat interface with multi-model support
- **Langflow Integration** - Enhanced pipeline with dynamic model switching
- **Multi-Model AI** - Support for Gemini, GPT-4o, and Claude with intelligent routing
- **Universal Pipelines** - Single workflows that handle multiple AI models
- **Agentic Routing** - Automatic model selection based on query content
- **Docker Ready** - Complete containerized deployment
- **API Templates** - Ready-to-use templates for multi-model API development
- **AI Examples** - Workflow templates for single and multi-model scenarios

## 🛠 Tech Stack

- **Open WebUI** - Modern chat interface with multi-model support
- **Langflow** - AI workflow builder with universal pipeline templates
- **PostgreSQL** - Database for Langflow
- **Docker Compose** - Multi-container orchestration
- **Python Pipelines** - Enhanced integration layer with intelligent routing
- **Multi-Model APIs** - FastAPI templates for scalable AI model access

## 🏃‍♂️ Quick Start

### Prerequisites
- Docker and Docker Compose

### Production Deployment

1. **Clone and setup**:
   ```bash
   git clone <repository>
   cd langflow-ui
   chmod +x setup-openwebui.sh
   ```

2. **Deploy with Docker**:
   ```bash
   ./setup-openwebui.sh
   ```

3. **Access the application**:
   - Open WebUI: http://localhost:3000
   - Langflow: http://localhost:7860
   - Pipelines: http://localhost:9099

4. **Try the examples**:
   ```bash
   # Import ready-to-use AI workflows
   ls examples/langflow-workflows/
   # basic-gemini-chat.json   - Google Gemini 2.5 Flash
   # basic-gpt4o-chat.json    - OpenAI GPT-4o  
   # basic-claude-chat.json   - Anthropic Claude 3.5 Sonnet
   ```

## 🤖 AI Examples

The `/examples` directory contains ready-to-use LangFlow workflow templates:

- **[Basic AI Examples](examples/README.md)** - Simple "Chat Input → AI Model → Chat Output" flows
- **[Multi-Model Templates](templates/README.md)** - Universal workflows and API templates
- **Gemini 2.5 Flash** - Latest Google AI model
- **GPT-4o** - Newest OpenAI model with multimodal capabilities
- **Claude 3.5 Sonnet** - Advanced Anthropic reasoning model

### Multi-Model Usage

With the enhanced pipeline, users can:

```
# Explicit model selection
@model:gemini What's the latest in AI research?
@model:gpt Write a creative short story about robots
@model:claude Help me debug this Python function

# Automatic intelligent routing
@agent How do I implement a binary search tree?  # → Routes to Claude
@agent What's happening in tech news today?      # → Routes to Gemini  
@agent Write a poem about the ocean             # → Routes to GPT
```

### Quick Start with Examples

1. Open Langflow at http://localhost:7860
2. Import any workflow from `examples/langflow-workflows/`
3. Add your API key to the AI model component
4. Copy the flow ID and use with Open WebUI

## 📁 Project Structure

```
langflow-ui/
├── docs/                     # Documentation
│   └── MULTI_MODEL_GUIDE.md  # Multi-model enhancement guide
├── examples/                 # AI workflow examples and templates
│   ├── langflow-workflows/   # Ready-to-use LangFlow JSON workflows
│   ├── generate_workflows.py # Script to generate workflow templates  
│   └── README.md             # Examples documentation
├── pipelines/                # Python pipelines for Langflow integration
│   ├── langflow_pipeline.py  # Original pipeline implementation
│   ├── enhanced_langflow_pipeline.py # Multi-model enhanced pipeline
│   └── requirements.txt      # Python dependencies
├── templates/                # Multi-model API and workflow templates
│   ├── multi_model_api_single.py      # Single-script multi-model API
│   ├── generate_multi_scripts.py      # Multi-script API generator  
│   ├── generate_universal_workflows.py # Universal workflow generator
│   └── README.md             # Templates documentation
├── tests/                    # Test suite
│   └── test_multi_model_enhancements.py # Multi-model functionality tests
├── docker-compose.yml        # Container orchestration
├── setup-openwebui.sh        # Setup script
└── README.md                 # This file
```

## 🔧 Configuration

The setup script automatically creates a `.env.openwebui` file with secure defaults. You can customize:

- **LANGFLOW_BASE_URL**: Langflow API endpoint
- **WORKFLOW_ID**: Default Langflow workflow ID
- **POSTGRES_***: Database configuration
- **WEBUI_***: Open WebUI settings

## 🔌 Pipeline Integration

The enhanced pipeline system provides both backward compatibility and new multi-model capabilities:

### Original Pipeline (`pipelines/langflow_pipeline.py`)
- Single-model integration with rate limiting and error management
- Supports custom workflow IDs via configuration
- Robust HTTP client with timeout handling
- Formatted responses for Open WebUI chat interface

### Enhanced Multi-Model Pipeline (`pipelines/enhanced_langflow_pipeline.py`)  
- **Multi-model support** - Gemini, GPT-4o, Claude with dynamic switching
- **Intelligent routing** - Automatic model selection based on query content
- **User directives** - `@model:gemini`, `@agent` for explicit control
- **Universal workflows** - Single workflows handling multiple models
- **Backward compatibility** - Works with existing single-model setups

### API Templates (`templates/`)
- **Single-script API** - All models in one FastAPI application
- **Multi-script architecture** - Separate services for scalability  
- **Universal workflows** - LangFlow templates supporting multiple models
- **Production ready** - Docker deployment, health checks, orchestration

## 🚀 Multi-Model Quick Start

### Option 1: Enhanced Pipeline (Recommended)
```bash
# Use enhanced pipeline with multi-model support
cp pipelines/enhanced_langflow_pipeline.py pipelines/langflow_pipeline.py

# Configure in OpenWebUI admin:
# ENABLE_MULTI_MODEL=true
# DEFAULT_MODEL=gpt
# ENABLE_AGENTIC_ROUTING=true
```

### Option 2: Standalone Multi-Model API
```bash
# Setup API keys
export GEMINI_API_KEY="your-key"
export OPENAI_API_KEY="your-key" 
export ANTHROPIC_API_KEY="your-key"

# Run single-script API
python templates/multi_model_api_single.py

# Or generate multi-script architecture
cd templates
python generate_multi_scripts.py
python orchestrator.py start
```

### Option 3: Universal Workflows
```bash
# Generate universal workflow templates
cd templates  
python generate_universal_workflows.py

# Import generated JSON workflows into LangFlow
# Files: universal-multi-model-chat.json, agentic-multi-model-router.json
```

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Submit a pull request

## 📝 License

This project is licensed under the MIT License.

## 🆘 Troubleshooting

### Common Issues

1. **Docker not starting**:
   ```bash
   docker info
   sudo systemctl restart docker
   ```

2. **Services not responding**:
   ```bash
   # Check service logs
   docker-compose logs -f
   
   # Restart specific service
   docker-compose restart <service-name>
   ```

3. **Clean restart**:
   ```bash
   ./setup-openwebui.sh --clean
   ```

**Built with ❤️ for the Langflow community**
