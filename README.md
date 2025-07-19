# Langflow + Open WebUI Integration

Simple integration setup that connects Open WebUI with Langflow for AI workflow management.

## 🚀 Features

- **Open WebUI** - Modern chat interface
- **Langflow Integration** - Custom pipeline for workflow execution
- **Docker Ready** - Complete containerized deployment
- **Pipeline Support** - Custom Python pipeline for Langflow communication
- **AI Examples** - Ready-to-use workflow templates for Gemini, GPT-4o, and Claude

## 🛠 Tech Stack

- **Open WebUI** - Modern chat interface
- **Langflow** - AI workflow builder
- **PostgreSQL** - Database for Langflow
- **Docker Compose** - Multi-container orchestration
- **Python Pipelines** - Custom integration layer

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
- **Gemini 2.5 Flash** - Latest Google AI model
- **GPT-4o** - Newest OpenAI model with multimodal capabilities
- **Claude 3.5 Sonnet** - Advanced Anthropic reasoning model

### Quick Start with Examples

1. Open Langflow at http://localhost:7860
2. Import any workflow from `examples/langflow-workflows/`
3. Add your API key to the AI model component
4. Copy the flow ID and use with Open WebUI

## 📁 Project Structure

```
langflow-ui/
├── examples/                # AI workflow examples and templates
│   ├── langflow-workflows/  # Ready-to-use LangFlow JSON workflows
│   ├── generate_workflows.py # Script to generate workflow templates  
│   └── README.md            # Examples documentation
├── pipelines/               # Python pipelines for Langflow integration
│   ├── langflow_pipeline.py # Main pipeline implementation
│   └── requirements.txt     # Python dependencies
├── docker-compose.yml       # Container orchestration
├── setup-openwebui.sh       # Setup script
└── README.md                # This file
```

## 🔧 Configuration

The setup script automatically creates a `.env.openwebui` file with secure defaults. You can customize:

- **LANGFLOW_BASE_URL**: Langflow API endpoint
- **WORKFLOW_ID**: Default Langflow workflow ID
- **POSTGRES_***: Database configuration
- **WEBUI_***: Open WebUI settings

## 🔌 Pipeline Integration

The `pipelines/langflow_pipeline.py` file provides integration between Open WebUI and Langflow:

- Handles rate limiting and error management
- Supports custom workflow IDs via configuration
- Provides robust HTTP client with timeout handling
- Formats responses for Open WebUI chat interface

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
