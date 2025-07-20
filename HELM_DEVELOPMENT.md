# 🚀 Chart Development & CI/CD Guide

## Quick Start for Contributors

This guide helps developers understand how to work with the Helm chart and CI/CD pipeline.

## 🛠 Chart Development Workflow

### 1. Making Changes
```bash
# Clone the repository
git clone https://github.com/pawelrosada/langflow-ui.git
cd langflow-ui

# Make your changes to helm/ directory
# Edit helm/Chart.yaml, helm/values.yaml, or helm/templates/
```

### 2. Local Testing
```bash
# Lint your changes
helm lint ./helm --strict

# Test template rendering with minimal config
helm template test-release ./helm -f helm/ci/test-values.yaml --dry-run

# Test template rendering with comprehensive config
helm template comprehensive-test ./helm -f helm/ci/comprehensive-values.yaml --dry-run

# Optional: Test installation in local cluster (requires kubectl/kind)
helm install test-release ./helm -f helm/ci/test-values.yaml --dry-run --debug
```

### 3. Submitting Changes
```bash
# Create a feature branch
git checkout -b feature/helm-improvements

# Commit your changes
git add helm/
git commit -m "feat: improve helm chart configuration"

# Push and create PR
git push origin feature/helm-improvements
```

## 🔄 CI/CD Pipeline Overview

### Automated Validation (on PR)
When you create a PR that touches `helm/` directory:

1. **Lint Check**: Validates chart syntax and structure
2. **Template Test**: Ensures templates render correctly
3. **Integration Test**: Installs chart in test Kubernetes cluster
4. **Multi-config Test**: Tests both minimal and comprehensive configurations

### Automated Release (on merge to main)
When PR is merged to main branch:

1. **Package Chart**: Creates .tgz package
2. **Create Release**: Tags and releases on GitHub
3. **Update Repository**: Updates Helm repository index
4. **Deploy to Pages**: Makes chart available at https://pawelrosada.github.io/langflow-ui

## 🧪 Testing Configurations

### Minimal Testing (`helm/ci/test-values.yaml`)
- Single replica
- Minimal resources
- PostgreSQL without persistence
- No MCP servers
- No OpenWebUI
- Used for basic functionality validation

### Comprehensive Testing (`helm/ci/comprehensive-values.yaml`)
- Multiple replicas
- Full resource allocation
- PostgreSQL with persistence
- Multiple MCP servers enabled
- OpenWebUI enabled
- Ingress configuration
- Used for complete feature validation

## 📋 Chart Version Management

### Version Bumping
Update version in `helm/Chart.yaml` to trigger new release:

```yaml
# helm/Chart.yaml
version: 0.3.0  # Increment for new release
```

### Version Strategy
- **Patch** (0.2.1): Bug fixes, small improvements
- **Minor** (0.3.0): New features, configuration options
- **Major** (1.0.0): Breaking changes, major restructure

## 🔧 Troubleshooting

### Common Issues

#### "No charts found" error
```bash
# Check chart structure
ls -la helm/
# Ensure Chart.yaml exists
cat helm/Chart.yaml
```

#### Template rendering fails
```bash
# Debug template rendering
helm template test helm/ --debug
# Check specific template
helm template test helm/ --show-only templates/deployment.yaml
```

#### Chart testing fails
```bash
# Run chart testing locally
ct lint --chart-dirs helm --target-branch main
ct install --chart-dirs helm --target-branch main
```

#### Release workflow fails
Check:
1. GitHub Pages is enabled in repository settings
2. Workflow has write permissions
3. Chart version has been incremented
4. No syntax errors in templates

### Debugging Commands
```bash
# Validate chart structure
helm show chart ./helm
helm show values ./helm

# Test with different value files
helm template test ./helm --values ./helm/values.yaml
helm template test ./helm --values ./helm/ci/test-values.yaml

# Package locally to test release process
helm package ./helm
```

## 📞 Getting Help

- **Helm Documentation**: https://helm.sh/docs/
- **Chart Best Practices**: https://helm.sh/docs/chart_best_practices/
- **Chart Testing**: https://github.com/helm/chart-testing
- **Issues**: Create issue in this repository

## 🚀 Advanced Topics

### Adding New MCP Servers
Edit `helm/values.yaml` and add configuration under `mcpServers`:

```yaml
mcpServers:
  your-new-server:
    enabled: false  # Disabled by default
    replicas: 1
    image:
      repository: your-org/your-mcp-server
      tag: "v1.0.0"
    # ... rest of configuration
```

### Custom Resource Configurations
Add your custom Kubernetes resources in `helm/templates/`:

```bash
# Create new template file
touch helm/templates/your-resource.yaml
# Follow existing template patterns
```

### Testing New Features
Always add test configurations:

```bash
# Update test values
vim helm/ci/test-values.yaml
vim helm/ci/comprehensive-values.yaml

# Test your changes
helm template test helm/ -f helm/ci/comprehensive-values.yaml
```

---

*For more detailed information, see [TODO.md](./TODO.md) for comprehensive implementation checklist.*
