# Langflow + Open WebUI Integration

[![pre-commit](https://img.shields.io/badge/pre--commit-enabled-brightgreen)](https://github.com/pre-commit/pre-commit) [![Trivy](https://img.shields.io/badge/Trivy-Enabled-blue)](https://aquasecurity.github.io/trivy/) [![GitHub Actions](https://github.com/pawelrosada/langflow-ui/workflows/Pre-Commit%20CI/badge.svg)](https://github.com/pawelrosada/langflow-ui/actions) [![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black) [![security: bandit](https://img.shields.io/badge/security-bandit-yellow.svg)](https://github.com/PyCQA/bandit)

Simple integration setup that connects Open WebUI with Langflow for AI workflow management with dynamic workflow selection capabilities.

## 🚀 Features

- **Dynamic Workflow Selection** - Switch between different Langflow workflows directly from chat
- **Open WebUI** - Modern chat interface with multi-model support
- **Langflow Integration** - Enhanced pipeline with dynamic workflow switching
- **Session Memory** - Remembers selected workflows per user session
- **Automatic Discovery** - Auto-discovers available workflows from Langflow
- **Multi-Model AI** - Support for Gemini, GPT-4o, and Claude with intelligent routing
- **Universal Pipelines** - Single workflows that handle multiple AI models
- **Agentic Routing** - Automatic model selection based on query content
- **Docker Ready** - Complete containerized deployment
- **API Templates** - Ready-to-use templates for multi-model API development

## 🎯 New: Dynamic Workflow Selection

Now you can select and switch between different Langflow workflows directly from the chat interface:

### Chat Commands
- `@workflows` - List all available workflows
- `@workflow:name Your message` - Use specific workflow by name
- `@flow:id Your message` - Use specific workflow by ID
- `@set-workflow:name` - Set default workflow for current session

### Usage Examples
```
User: @workflows
Bot: 📋 Dostępne przepływy pracy:
     • Customer Support Bot
     • Document QA System
     • Code Helper
     💡 Użycie: @workflow:nazwa Twoja wiadomość

User: @workflow:document-qa What is machine learning?
Bot: 🔧 Document QA System: Machine learning is a subset of artificial intelligence...

User: @set-workflow:code-helper
Bot: ✅ Ustawiono domyślny przepływ: Code Helper dla tej sesji.

User: How do I implement binary search?
Bot: 🔧 Code Helper: Here's a binary search implementation...
```

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

4. **Try the workflow selector**:
   ```bash
   # Chat with dynamic workflow selection
   # Open http://localhost:3000 and try:
   # @workflows                    - List available workflows  
   # @workflow:name Your message   - Use specific workflow
   # @set-workflow:name           - Set session default
   ```

## 📋 Pipeline Options

Choose the pipeline that fits your needs:

### Option 1: Dynamic Workflow Selector (Recommended)
Perfect for users who want to switch between different workflows:

```bash
# Use the workflow selector pipeline
cp pipelines/workflow_selector_pipeline.py pipelines/langflow_pipeline.py
```

**Features:**
- ✅ Dynamic workflow discovery
- ✅ Chat-based workflow selection 
- ✅ Session memory
- ✅ Auto-discovery from Langflow API

### Option 2: Enhanced Multi-Model Pipeline
For users who want multi-model AI routing:

```bash
# Use the enhanced multi-model pipeline  
cp pipelines/enhanced_langflow_pipeline.py pipelines/langflow_pipeline.py
```

**Features:**
- ✅ Multi-model support (Gemini, GPT, Claude)
- ✅ Intelligent routing with @agent
- ✅ Model-specific workflows
- ✅ Backward compatibility

### Option 3: Simple Single-Workflow Pipeline
For basic single-workflow setups:

```bash
# Use the original simple pipeline
# No changes needed - uses langflow_pipeline.py as-is
```

**Features:**  
- ✅ Simple and reliable
- ✅ Single workflow configuration
- ✅ Minimal setup required

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

### Quick Start with Workflow Selection

1. **Open Langflow** at http://localhost:7860
2. **Create multiple workflows** (e.g., "Customer Support", "Document QA", "Code Helper")
3. **Open Chat Interface** at http://localhost:3000
4. **List workflows**: Type `@workflows` to see all available options
5. **Select workflow**: Use `@workflow:customer-support How can I help you?`
6. **Set session default**: Use `@set-workflow:code-helper` for coding tasks

### Multi-Model Usage (Enhanced Pipeline)

With the enhanced pipeline, users can:

```bash
# Explicit model selection
@model:gemini What's the latest in AI research?
@model:gpt Write a creative short story about robots
@model:claude Help me debug this Python function

# Automatic intelligent routing
@agent How do I implement a binary search tree?  # → Routes to Claude
@agent What's happening in tech news today?      # → Routes to Gemini  
@agent Write a poem about the ocean             # → Routes to GPT
```

## 📁 Project Structure

```
langflow-ui/
├── docs/                           # Documentation
│   ├── MULTI_MODEL_GUIDE.md       # Multi-model enhancement guide
│   └── WORKFLOW_SELECTOR_GUIDE.md # Dynamic workflow selector guide
├── examples/                       # AI workflow examples and templates
│   ├── langflow-workflows/         # Ready-to-use LangFlow JSON workflows
│   ├── generate_workflows.py       # Script to generate workflow templates  
│   └── README.md                   # Examples documentation
├── pipelines/                      # Python pipelines for Langflow integration
│   ├── langflow_pipeline.py        # Original pipeline implementation
│   ├── enhanced_langflow_pipeline.py # Multi-model enhanced pipeline
│   ├── workflow_selector_pipeline.py # Dynamic workflow selector pipeline
│   └── requirements.txt            # Python dependencies
├── templates/                      # Multi-model API and workflow templates
│   ├── multi_model_api_single.py          # Single-script multi-model API
│   ├── generate_multi_scripts.py          # Multi-script API generator  
│   ├── generate_universal_workflows.py    # Universal workflow generator
│   └── README.md                   # Templates documentation
├── tests/                          # Test suite
│   ├── test_multi_model_enhancements.py   # Multi-model functionality tests
│   └── test_workflow_selector.py          # Workflow selector tests
├── docker-compose.yml              # Container orchestration
├── setup-openwebui.sh              # Setup script
└── README.md                       # This file
```

## 🔧 Configuration

The setup script automatically creates a `.env.openwebui` file with secure defaults. You can customize:

- **LANGFLOW_BASE_URL**: Langflow API endpoint
- **WORKFLOW_ID**: Default Langflow workflow ID
- **POSTGRES_***: Database configuration
- **WEBUI_***: Open WebUI settings

## 🛡️ Code Quality & Security

This project uses automated code quality and security tools:

### Pre-commit Hooks
```bash
# Install pre-commit hooks
./setup-pre-commit.sh

# Or manually:
pip install pre-commit
pre-commit install
pre-commit run --all-files
```

**Tools included:**
- **Black** - Python code formatting (auto-fix)
- **Flake8** - Python linting per PEP 8
- **Trivy** - Security vulnerability scanning
- **Shellcheck** - Shell script validation
- **JSON/YAML validators** - Format validation

### GitHub Actions
Every pull request automatically runs:
- Pre-commit validation
- Security scanning with Trivy  
- Code formatting checks
- Auto-fixing where possible

### Security Features
- 🔒 **Trivy scanning** for vulnerabilities and secrets
- 🎯 **Automated validation** on every commit and PR
- ✨ **Auto-fixing** for formatting issues
- 📊 **Status badges** showing code quality

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
