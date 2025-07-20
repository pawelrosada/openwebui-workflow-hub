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

#### Option 1: Using Helm Repository (Recommended)

```bash
# Add the Helm repository
helm repo add langflow-ui https://pawelrosada.github.io/langflow-ui
helm repo update

# Install from repository
helm install my-langflow langflow-ui/langflow-app

# Install with custom values
helm install my-langflow langflow-ui/langflow-app \
  --set mcpServers.filesystem-mcp.enabled=true \
  --set mcpServers.brave-search-mcp.enabled=true
```

#### Option 2: Using Local Chart

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

### GKE and GCP Load Balancer Setup

For production deployment on Google Kubernetes Engine:

```bash
# Deploy with external load balancer
helm install my-langflow ./helm \
  --set service.type=NodePort \
  --set ingress.enabled=true \
  --set ingress.annotations."kubernetes\.io/ingress\.class"=gce

# With custom annotations for GCP
helm install my-langflow ./helm \
  --set service.annotations."cloud\.google\.com/neg"='{"ingress": true}'
```

### Security & Secrets Management

The Helm chart follows Kubernetes security best practices for handling sensitive data:

#### Development (built-in secrets)
```bash
# Quick development setup with built-in secrets
helm install my-langflow ./helm
```

#### Production (external secrets)
```bash
# 1. Create secrets manually first
kubectl create secret generic my-langflow-secrets \
  --from-literal=langflow-superuser-password=YOUR_SECURE_PASSWORD \
  --from-literal=postgresql-password=YOUR_DB_PASSWORD

# 2. Create MCP server secrets
kubectl create secret generic my-langflow-mcp-github-mcp-secrets \
  --from-literal=GITHUB_PERSONAL_ACCESS_TOKEN=YOUR_GITHUB_TOKEN

# 3. Deploy without built-in secrets
helm install my-langflow ./helm \
  --set secrets.create=false \
  --values values-production-example.yaml
```

#### MCP Server Security
Add API keys securely to MCP servers:

```yaml
mcpServers:
  your-custom-server:
    enabled: true
    image:
      repository: your-mcp-server
    # Non-sensitive config
    env:
      - name: SERVER_CONFIG
        value: "public-value"
    # Sensitive data in Kubernetes secrets
    secrets:
      API_KEY: "your-secret-key"
      TOKEN: "your-token"
```

### OpenWebUI with PostgreSQL (Production Ready)

By default, OpenWebUI uses SQLite which is not suitable for production. Enable PostgreSQL for persistent, production-ready storage:

```bash
# Enable OpenWebUI with PostgreSQL (recommended for production)
helm install my-langflow ./helm \
  --set openwebui.enabled=true \
  --set openwebui.database.usePostgreSQL=true

# OpenWebUI with SQLite (development only - data lost on restart)
helm install my-langflow ./helm \
  --set openwebui.enabled=true \
  --set openwebui.database.usePostgreSQL=false
```

OpenWebUI PostgreSQL configuration:
- **Database**: `openwebui_db` (automatically created)
- **Shared PostgreSQL**: Uses same instance as LangFlow
- **Persistent storage**: Data survives pod restarts
- **Production ready**: Suitable for production environments

### Production Best Practices

✅ **No CPU limits** - Follows Kubernetes best practices for better performance
✅ **Memory limits only** - Prevents OOM while allowing CPU bursting  
✅ **GKE optimized** - Compatible with Google Kubernetes Engine
✅ **Official chart pattern** - Uses community standards for PostgreSQL
✅ **Secure secrets** - Kubernetes Secret objects for sensitive data
✅ **External secret support** - Compatible with secret management systems

### Docker Compose (Alternative)

For local development, use the provided Docker Compose setup:

```bash
./setup-openwebui.sh
```

## Helm Chart Development

### Automatic Releases

The Helm chart is automatically released when changes are made to the `helm/` directory:

- **Validation**: Charts are automatically linted and tested on every PR
- **Release**: Charts are packaged and published to GitHub Pages when changes are merged to `main`
- **Repository**: Available at https://pawelrosada.github.io/langflow-ui

### Manual Release

You can also trigger a chart release manually using GitHub Actions:

1. Go to the **Actions** tab in the repository
2. Select **Helm Chart Release** workflow
3. Click **Run workflow** and select the `main` branch
4. Click **Run workflow** button

### Chart Versioning

Chart versions are managed through the `helm/Chart.yaml` file. Update the `version` field to release a new version:

```yaml
apiVersion: v2
name: langflow-app
version: 0.3.0  # Increment this for new releases
```

### Local Testing

Before submitting changes, test your chart locally:

```bash
# Lint the chart
helm lint ./helm

# Test template rendering
helm template test-release ./helm --dry-run

# Validate with values
helm template test-release ./helm -f ./helm/values.yaml
```

## Contributing
Fork and submit PRs for improvements, but keep it clean – no adding extra files/scripts.