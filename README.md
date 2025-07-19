# LangFlow Examples Repo

Clean repository with basic LangFlow workflow examples for AI models.

## Table of Contents
- [Overview](#overview)
- [Examples](#examples)
- [Usage](#usage)
- [Deployment](#deployment)
- [Contributing](#contributing)

## Overview
This repo provides 3 simple, importable JSON workflows for LangFlow, each using a single AI model in a basic Chat Input -> Model -> Chat Output pipeline. No extras – clean and focused.

## Examples
- [GPT-4o Workflow](./examples/gpt-4o-workflow.json): For OpenAI's GPT-4o.
- [Gemini 2.5 Flash Workflow](./examples/gemini-2.5-flash-workflow.json): For Google's Gemini 2.5 Flash.
- [Claude Sonnet 4 Workflow](./examples/claude-sonnet-4-workflow.json): For Anthropic's Claude Sonnet 4.

## Usage
1. Import the JSON into LangFlow.
2. Add your API key.
3. Run the flow for basic chat testing.

## Deployment

### Kubernetes with Helm Chart

Deploy LangFlow to Kubernetes with dedicated PostgreSQL and flexible MCP servers:

```bash
# Basic deployment
helm install my-langflow ./helm

# Enable additional MCP servers
helm install my-langflow ./helm \
  --set mcpServers.filesystem-mcp.enabled=true \
  --set mcpServers.brave-search-mcp.enabled=true
```

### Adding Custom MCP Servers

Add your own MCP servers by editing `helm/values.yaml`:

```yaml
mcpServers:
  your-custom-server:
    enabled: true
    replicas: 1
    image:
      repository: your-company/your-mcp-server
      tag: "v1.0.0"
      pullPolicy: IfNotPresent
    service:
      type: ClusterIP
      port: 9102
    resources:
      requests:
        memory: 256Mi
        cpu: 250m
      limits:
        memory: 512Mi
        cpu: 500m
    env:
      - name: YOUR_API_KEY
        value: "your-secret-key"
```

### Scaling MCP Servers

```bash
# Scale specific MCP server
helm upgrade my-langflow ./helm --set mcpServers.github-mcp.replicas=3

# Enable/disable servers
helm upgrade my-langflow ./helm --set mcpServers.filesystem-mcp.enabled=false
```

### Docker Compose (Alternative)

For local development, use the provided Docker Compose setup:

```bash
./setup-openwebui.sh
```

## Contributing
Fork and submit PRs for improvements, but keep it clean – no adding extra files/scripts.