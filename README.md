# Langflow + Open WebUI Integration

Simple integration setup that connects Open WebUI with Langflow for AI workflow management.

## 🚀 Features

- **Open WebUI** - Modern chat interface
- **Langflow Integration** - Custom pipeline for workflow execution
- **Docker Ready** - Complete containerized deployment
- **Pipeline Support** - Custom Python pipeline for Langflow communication

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

## 📁 Project Structure

```
langflow-ui/
├── pipelines/              # Python pipelines for Langflow integration
│   ├── langflow_pipeline.py # Main pipeline implementation
│   └── requirements.txt    # Python dependencies
├── docker-compose.yml      # Container orchestration
├── setup-openwebui.sh      # Setup script
└── README.md               # This file
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
