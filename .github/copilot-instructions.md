# Copilot Instructions for Langflow-UI Integration

## 🎯 General Guidelines

This repository provides a simple integration between Open WebUI and Langflow using Docker Compose and Python pipelines.

### Basic Principles
- **Use Docker Compose** for all services
- **Keep it simple** - avoid unnecessary complexity 
- **Document changes** in Polish for better user experience
- **Test with provided setup script**

## 🛠 Technology Stack

### Core Components
| Component | Technology | Purpose |
|-----------|-------------|---------|
| **Frontend** | Open WebUI | Chat interface |
| **AI Workflows** | Langflow | Workflow builder |
| **Database** | PostgreSQL | Langflow data |
| **Integration** | Python Pipelines | Connect Open WebUI to Langflow |
| **Orchestration** | Docker Compose | Container management |

## 🏗 Repository Structure

```
langflow-ui/
├── pipelines/              # Python integration pipelines
│   ├── langflow_pipeline.py # Main pipeline implementation
│   └── requirements.txt    # Python dependencies
├── docker-compose.yml      # Service orchestration
├── setup-openwebui.sh      # Setup and deployment script
└── README.md               # Documentation
```

## 🔧 Development Rules

### ✅ When making changes:

1. **Test with setup script** - Always run `./setup-openwebui.sh` after changes
2. **Update pipeline code** - Modify `pipelines/langflow_pipeline.py` for integration logic
3. **Update docker-compose.yml** - For service configuration changes
4. **Keep documentation current** - Update README.md to match changes
5. **Use Polish messages** - For user-facing error messages and logs

### 📝 Code Standards

- **Simple Python** - Keep pipeline code straightforward
- **Error handling** - Provide clear error messages in Polish
- **Docker first** - All changes should work in containerized environment
- **Rate limiting** - Respect API limits in pipeline implementations

## 🚀 Testing

Always test changes with the complete stack:

```bash
# Clean start
./setup-openwebui.sh --clean

# Regular start  
./setup-openwebui.sh

# Check services
docker-compose logs -f
```

## 🎯 End Goal

Keep this repository focused on providing a simple, working integration between Open WebUI and Langflow that can be deployed with a single script.

---

*Ostatnia aktualizacja: Styczeń 2025*