# OpenWebUI-LangFlow-MCP Integration Framework

Complete pipeline connecting OpenWebUI through custom pipelines to LangFlow workflows and MCP servers.

## Components
- **OpenWebUI** - Chat interface frontend
- **Pipelines** - Custom Python integration layer  
- **LangFlow** - AI workflow engine with PostgreSQL
- **MCP** - Model Context Protocol servers (GitHub, filesystem, search)

## Quick Start
```bash
./setup-openwebui.sh
```
Access: OpenWebUI (http://localhost:3000) | LangFlow (http://localhost:7860)

## Ready-to-Use Blocks

### LangFlow Workflows  
- [GPT-4o Chat](./examples/gpt-4o-workflow.json)
- [Gemini 2.5 Flash](./examples/gemini-2.5-flash-workflow.json)  
- [Claude Sonnet 4](./examples/claude-sonnet-4-workflow.json)

### Integration Pipelines
- [langflow_pipeline.py](./pipelines/langflow_pipeline.py) - OpenWebUI ↔ LangFlow bridge
- [enhanced_langflow_pipeline.py](./pipelines/enhanced_langflow_pipeline.py) - Advanced features
- [workflow_selector_pipeline.py](./pipelines/workflow_selector_pipeline.py) - Multi-workflow support

## Deployment

### Docker Compose (Recommended)
```bash
./setup-openwebui.sh          # Start all services
./setup-openwebui.sh --clean  # Clean start with fresh data
```

### Kubernetes with Helm
See [HELM_DEVELOPMENT.md](./HELM_DEVELOPMENT.md) for complete Kubernetes deployment guide including:
- MCP server scaling and configuration
- Production PostgreSQL setup
- Security and secrets management
- GKE and cloud provider setup

## Contributing
Fork and submit PRs for improvements. Keep changes focused and well-tested.