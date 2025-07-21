# OpenWebUI-LangFlow-MCP Integration Framework

## Table of Contents
- [Overview](#overview)
- [Architecture](#architecture)
- [📋 Detailed Architecture Documentation](./ARCHITECTURE.md)
- [Components](#components)
- [Ready-to-Use Blocks](#ready-to-use-blocks)
- [Installation](#installation)
- [Usage](#usage)
- [Deployment Options](#deployment-options)
- [Configuration](#configuration)
- [Contributing](#contributing)

## Overview

A comprehensive integration framework that connects OpenWebUI's intuitive chat interface with LangFlow's powerful AI workflow engine through custom Python pipelines. This repository provides a complete, production-ready solution for building and deploying conversational AI applications with visual workflow management.

The framework bridges the gap between user-friendly chat interfaces and complex AI workflows, enabling developers to create sophisticated AI applications without sacrificing usability or flexibility. Whether you're building customer support bots, content generation tools, or interactive AI assistants, this integration provides all the necessary components in a containerized, scalable architecture.

## Architecture

> 📋 **For comprehensive technical documentation, component specifications, and advanced architecture patterns, see [ARCHITECTURE.md](./ARCHITECTURE.md)**

### System Overview

```mermaid
graph TB
    User([👤 User]) --> OpenWebUI["🌐 OpenWebUI<br/>Chat Interface<br/>Port 3000"]

    OpenWebUI --> |"OpenAI API<br/>HTTP REST"| Pipelines["🔧 Pipelines<br/>Integration Layer<br/>Port 9099"]

    Pipelines --> |"HTTP API<br/>JSON"| LangFlow["⚡ LangFlow<br/>Workflow Engine<br/>Port 7860"]

    LangFlow --> |SQL| PostgreSQL[("🗄️ PostgreSQL<br/>Database<br/>Port 5432")]

    LangFlow --> |"API Calls"| AIModels["🤖 AI Models<br/>GPT-4, Gemini, Claude"]

    AIModels --> LangFlow
    LangFlow --> Pipelines
    Pipelines --> OpenWebUI
    OpenWebUI --> User

    subgraph DockerNet ["Docker Network"]
        OpenWebUI
        Pipelines
        LangFlow
        PostgreSQL
    end

    classDef frontend fill:#e1f5fe
    classDef integration fill:#f3e5f5
    classDef workflow fill:#e8f5e8
    classDef database fill:#fff3e0
    classDef external fill:#fce4ec

    class OpenWebUI frontend
    class Pipelines integration
    class LangFlow workflow
    class PostgreSQL database
    class AIModels external
```

### Data Flow Architecture

```mermaid
sequenceDiagram
    participant U as 👤 User
    participant OW as 🌐 OpenWebUI
    participant P as 🔧 Pipelines
    participant LF as ⚡ LangFlow
    participant DB as 🗄️ PostgreSQL
    participant AI as 🤖 AI Models

    U->>OW: Send Message
    OW->>P: "POST /v1/chat/completions"
    P->>P: "Rate Limiting & Validation"
    P->>LF: "POST /api/v1/run/{workflow_id}"
    LF->>DB: Load Workflow Config
    DB-->>LF: Workflow Definition
    LF->>AI: "API Request (GPT/Gemini/Claude)"
    AI-->>LF: AI Response
    LF->>DB: Store Conversation
    LF-->>P: JSON Response
    P->>P: "Format & Process"
    P-->>OW: Streaming Response
    OW-->>U: Display Response
```

The architecture follows a clean separation of concerns:
- **Frontend Layer**: OpenWebUI provides the chat interface and user management
- **Integration Layer**: Custom Python pipelines handle routing and data transformation
- **Workflow Layer**: LangFlow manages AI workflows with visual flow builder
- **Data Layer**: PostgreSQL stores workflow configurations and chat history

> 📋 For detailed technical documentation, component specifications, and advanced architecture patterns, see [ARCHITECTURE.md](./ARCHITECTURE.md)

## Components

### 🖥️ **OpenWebUI**
Modern chat interface with support for:
- Multiple user management and authentication
- Real-time conversations with streaming responses
- File upload and document processing
- Custom model configurations
- Plugin system for extended functionality
- Responsive design for desktop and mobile

**Configuration**: Runs on port 3000, connects to pipelines via internal Docker network.

### 🔧 **Pipelines**
Custom Python integration layer featuring:
- **Rate Limiting**: Prevents API overload with configurable limits
- **Error Handling**: Comprehensive error management with user-friendly messages
- **Model Routing**: Dynamic routing between different AI models
- **Response Formatting**: Structured output processing for optimal UX
- **Logging System**: Detailed debugging and monitoring capabilities

**API Endpoint**: http://localhost:9099 - Compatible with OpenAI API format

### ⚡ **LangFlow**
Visual AI workflow builder with:
- **Drag-and-Drop Interface**: Build complex AI workflows visually
- **Component Library**: Pre-built nodes for common AI operations
- **Custom Components**: Create reusable workflow components
- **Version Control**: Track and manage workflow versions
- **Real-time Testing**: Test workflows directly in the interface

**Access**: http://localhost:7860 - Full workflow management interface

### 🗄️ **PostgreSQL Database**
Persistent storage for:
- LangFlow workflow configurations and metadata
- Open WebUI chat conversations and user data
- Component settings and cache
- **Shared PostgreSQL instance** with dedicated databases:
  - `langflow` database for LangFlow data
  - `openwebui` database for Open WebUI data

## Ready-to-Use Blocks

### 🔄 **LangFlow Workflows**

#### **GPT-4o Chat Workflow** ([gpt-4o-workflow.json](./examples/gpt-4o-workflow.json))
- OpenAI GPT-4o integration with optimized prompting
- Supports conversation context and memory
- Configured for general-purpose chat interactions
- Rate limiting and error handling built-in

#### **Gemini 2.5 Flash Workflow** ([gemini-2.5-flash-workflow.json](./examples/gemini-2.5-flash-workflow.json))
- Google Gemini integration for fast responses
- Optimized for quick queries and real-time interactions
- Multimodal capabilities for text and image processing
- Cost-effective for high-volume applications

#### **Claude Sonnet 4 Workflow** ([claude-sonnet-4-workflow.json](./examples/claude-sonnet-4-workflow.json))
- Anthropic Claude integration with safety features
- Excellent for complex reasoning and analysis tasks
- Built-in content moderation and safety filters
- Optimized prompt engineering for consistent outputs

### 🐍 **Integration Pipelines**

#### **Basic Pipeline** ([langflow_pipeline.py](./pipelines/langflow_pipeline.py))
- Simple OpenWebUI ↔ LangFlow bridge
- Single workflow routing
- Basic error handling and logging
- Perfect starting point for custom implementations

#### **Enhanced Pipeline** ([enhanced_langflow_pipeline.py](./pipelines/enhanced_langflow_pipeline.py))
- Multi-model support with dynamic routing
- Advanced user commands (`@model:gemini`, `@model:gpt`, `@model:claude`)
- Intelligent agent routing based on query analysis
- Backward compatibility with existing setups

#### **Workflow Selector** ([workflow_selector_pipeline.py](./pipelines/workflow_selector_pipeline.py))
- Dynamic workflow selection based on user input
- Support for multiple concurrent workflows
- Context-aware routing and load balancing
- Advanced session management

## Installation

### Prerequisites
- Docker and Docker Compose
- 4GB+ RAM recommended
- Internet connection for model API access
- **PostgreSQL Database**: Automatically configured via Docker Compose

### Option 1: Docker Compose (Quick Start)

#### Quick Start
```bash
# Clone the repository
git clone https://github.com/pawelrosada/langflow-ui.git
cd langflow-ui

# Start all services
./setup-openwebui.sh

# Access the applications
# OpenWebUI: http://localhost:3000
# LangFlow: http://localhost:7860
```

#### Clean Installation
```bash
# Start with fresh data (removes all volumes)
./setup-openwebui.sh --clean
```

### Option 2: Kubernetes Development Platform (Kind + Helm)

> 🚀 **Automated local Kubernetes development with advanced service exposure**

#### Prerequisites
- Docker (for Kind cluster)
- 8GB+ RAM recommended for Kubernetes
- Tools are auto-installed: Kind, Helm, kubectl, Task

#### Quick Setup
```bash
# Clone the repository
git clone https://github.com/pawelrosada/langflow-ui.git
cd langflow-ui

# One-time setup (installs tools + creates cluster)
task setup

# Start development environment
task start

# Deploy the application
task deploy
```

#### Daily Development Workflow
```bash
# Start your development session
task up            # Equivalent to: task start && task deploy

# Check application status
task status

# View application logs
task logs

# Access applications via multiple methods:
# 1. Direct NodePort access (via Kind port mapping):
#    - OpenWebUI: http://localhost:3000
#    - Langflow: http://localhost:7860
#    - Pipelines: http://localhost:9099
#    - PostgreSQL: localhost:5432

# 2. Port forwarding (custom ports):
task expose:port-forward SERVICE=langflow-app LOCAL_PORT=8080
task expose:port-forward-all  # Forward all services simultaneously

# 3. Ingress with custom domains:
task expose:ingress HOST=langflow.local
# Add to /etc/hosts: 127.0.0.1 langflow.local
# Access at: http://langflow.local:8080

# Stop environment
task down          # Stop port forwarding only
task stop --destroy-cluster  # Complete cleanup
```

#### Service Exposure Methods

The Kubernetes platform provides multiple ways to access your services:

**1. Direct Access (via Kind Port Mapping)**
```bash
# Already configured and ready to use:
curl http://localhost:7860/api/v1/flows  # Langflow API
curl http://localhost:3000               # OpenWebUI
curl http://localhost:9099/health        # Pipelines health
```

**2. Port Forwarding (Flexible)**
```bash
# Forward single service with custom ports
task expose:port-forward SERVICE=langflow-app LOCAL_PORT=8080 REMOTE_PORT=7860

# Forward all services simultaneously
task expose:port-forward-all

# Custom service forwarding
task expose:port-forward SERVICE=langflow-app-postgresql LOCAL_PORT=5433 REMOTE_PORT=5432
```

**3. NodePort Exposure**
```bash
# Expose with custom NodePort
task expose:nodeport NODE_PORT=30010 SERVICE=langflow-app

# Access via: http://localhost:30010
```

**4. Ingress (Domain-based Routing)**
```bash
# Create ingress for single service
task expose:ingress HOST=myapp.local SERVICE=langflow-app

# Create ingress for all services
task expose:ingress-all
# Adds: langflow.local, openwebui.local, api.local

# Add to /etc/hosts and access via: http://langflow.local:8080
```

**5. Debugging and Connectivity**
```bash
# Debug network connectivity
task expose:debug SERVICE=langflow-app

# Test all service connectivity
task expose:test-connectivity

# Show all current exposures and options
task expose:expose-all

# Reset all exposures to ClusterIP
task expose:cleanup
```

#### Available Tasks

```bash
# Environment Management
task setup         # Initial setup (one-time)
task start         # Start development environment
task deploy        # Deploy/upgrade application
task stop          # Stop environment
task clean         # Destroy cluster and all data
task restart       # Restart entire environment

# Application Management
task status        # Show cluster and deployment status
task logs          # Show application logs
task logs-all      # Show logs from all components
task shell         # Open shell in Langflow pod
task psql          # Connect to PostgreSQL database

# Development Tools
task validate      # Validate Helm chart and manifests
task update        # Update Helm chart and redeploy
task reset         # Reset application (keep cluster)
task info          # Show comprehensive environment info

# Service Exposure (see expose:* tasks above)
task expose:port-forward        # Port forwarding
task expose:nodeport           # NodePort exposure
task expose:ingress            # Ingress creation
task expose:expose-all         # Show all methods
task expose:cleanup            # Reset exposures
task expose:debug             # Debug connectivity

# Quick Aliases
task up            # start + deploy
task down          # stop
task ps            # status
task exec          # shell
```

#### Troubleshooting

**Cluster Issues:**
```bash
# Check cluster status
task info

# Recreate cluster
task clean && task setup

# View cluster logs
kubectl get events --sort-by='.lastTimestamp'
```

**Application Issues:**
```bash
# Check pod status
task status

# View specific pod logs
kubectl logs <pod-name> -n default

# Debug service connectivity
task expose:debug SERVICE=langflow-app

# Reset application
task reset
```

**Port Conflicts:**
```bash
# Check what's using ports
netstat -tlnp | grep :3000

# Use different local ports
task expose:port-forward LOCAL_PORT=3001 SERVICE=langflow-app-openwebui
```

## Usage

1. **Import Workflows**: Load example workflows into LangFlow via the web interface
2. **Configure Pipelines**: Modify pipeline configurations in the `pipelines/` directory
3. **Test Integration**: Send messages through OpenWebUI to test the complete pipeline
4. **Monitor Logs**: Use `docker-compose logs -f` to monitor all services

## Deployment Options

### Docker Compose (Development)
Default setup using `docker-compose.yml` with all services on single machine.

### Kubernetes with Helm (Production)
See [HELM_DEVELOPMENT.md](./HELM_DEVELOPMENT.md) for comprehensive production deployment including:
- Horizontal scaling configuration
- Production PostgreSQL with high availability
- Security hardening and secrets management
- Load balancing and ingress setup
- Monitoring and observability stack

## Configuration

### Database Configuration
Both environments (Docker Compose and Helm) use **PostgreSQL** for data persistence:

**Docker Compose:**
- PostgreSQL server: `postgres:5432`
- Langflow database: `postgresql://langflow:langflow@postgres:5432/langflow`
- Open WebUI database: `postgresql://langflow:langflow@postgres:5432/openwebui`

**Environment Variables:**
- `POSTGRES_DB=langflow` - Primary database name
- `POSTGRES_USER=langflow` - Database user
- `POSTGRES_PASSWORD=langflow` - Database password (change in production)
- `DATABASE_URL` - Open WebUI PostgreSQL connection string
- `LANGFLOW_DATABASE_URL` - Langflow PostgreSQL connection string

## Pipeline Management

### Overview
The framework includes **26 pre-built pipelines** that automatically connect OpenWebUI to Langflow workflows. These pipelines act as intelligent intermediaries, handling data transformation, rate limiting, and workflow orchestration.

### Available Pipelines
- **🔧 Pipeline Generator** - Automatically creates new pipelines from Langflow workflows
- **📝 Content Creation**: Blog Writer, Instagram Copywriter, Twitter Thread Generator
- **🔍 Research & Analysis**: Research Agent, Market Research, Financial Report Parser
- **💬 Communication**: Meeting Summary, News Aggregator, Invoice Summarizer
- **🤖 AI Integration**: OpenAI, Text/Image Sentiment Analysis, SEO Keyword Generator
- **📊 Data Processing**: Vector Store RAG, Hybrid Search RAG, Custom Component Generator
- **🎯 Specialized Agents**: Search Agent, Social Media Agent, Pokédex Agent, Price Deal Finder

### Pipeline Development Workflow

#### Using Kubernetes (Recommended for Development)

```bash
# 1. Modify pipeline files in pipelines/ directory
vim pipelines/langflow_custom_pipeline.py

# 2. Update pipelines in cluster
task update-pipelines

# 3. Check pipeline status
task pipelines-status

# 4. View real-time pipeline logs
task pipelines-logs
```

#### Manual Pipeline Update
```bash
# Create/update ConfigMap from local files
./scripts/update-pipelines.sh

# Restart pipelines deployment
kubectl rollout restart deployment langflow-app-pipelines

# Verify all pipelines loaded
kubectl exec deployment/langflow-app-pipelines --
  curl -s -H "Authorization: Bearer 0p3n-w3bu"
  http://localhost:9099/v1/models | jq '.data | length'
```

### Pipeline Generator Usage

The **Pipeline Generator** is a special pipeline that automatically creates new pipeline files from Langflow workflows:

1. **Access Pipeline Generator**: Available as "🔧 Pipeline Generator" model in OpenWebUI
2. **Automatic Discovery**: On startup, scans Langflow for available workflows
3. **Dynamic Generation**: Creates Python pipeline files for each workflow found
4. **Persistent Storage**: Generated pipelines survive pod restarts via PersistentVolume

#### Pipeline Generator Features
- **Auto-discovery** of Langflow workflows via API
- **Template-based generation** with consistent structure
- **Rate limiting** and error handling built-in
- **Persistent storage** for generated pipeline files
- **Automatic reload** when new workflows are added

### Pipeline Architecture

```mermaid
graph TB
    OpenWebUI["🌐 OpenWebUI"] --> |"HTTP Request"| Pipelines["🔧 Pipelines Service"]

    subgraph Pipelines ["🔧 Pipelines Container"]
        Generator["🔧 Pipeline Generator"]
        Pipeline1["📝 Blog Writer"]
        Pipeline2["🔍 Research Agent"]
        PipelineN["... 25+ Pipelines"]
    end

    Pipelines --> |"Workflow Execution"| Langflow["⚡ Langflow"]

    subgraph Storage ["💾 Persistent Storage"]
        PVC["PersistentVolumeClaim"]
        ConfigMap["Pipeline Files ConfigMap"]
    end

    ConfigMap --> |"Init Container"| Pipelines
    Pipelines --> |"Generated Files"| PVC
```

### Custom Pipeline Development

#### 1. Create New Pipeline
```python
# pipelines/my_custom_pipeline.py
"""
Custom Pipeline Example
"""
from typing import List, Dict, Union, Generator
import httpx
import os

class Pipeline:
    def __init__(self):
        self.name = "My Custom Pipeline"
        self.id = "my_custom_pipeline"

    async def on_startup(self):
        print(f"Pipeline started: {self.name}")

    def pipe(
        self, user_message: str, model_id: str,
        messages: List[dict], body: dict
    ) -> Union[str, Generator, Iterator]:
        # Your custom logic here
        langflow_url = os.getenv("LANGFLOW_BASE_URL", "http://langflow-app:7860")

        # Call Langflow workflow
        response = httpx.post(
            f"{langflow_url}/api/v1/run/your-workflow-id",
            json={"input_value": user_message}
        )

        return response.json()["outputs"][0]["outputs"][0]["results"]["message"]["text"]
```

#### 2. Deploy Custom Pipeline
```bash
# Update cluster with new pipeline
task update-pipelines

# Verify it's loaded
task pipelines-status
```

### Troubleshooting Pipelines

#### Common Issues
```bash
# Check pipeline pod status
kubectl get pods -l app.kubernetes.io/component=pipelines

# View pipeline logs
kubectl logs -l app.kubernetes.io/component=pipelines

# Test individual pipeline
kubectl exec deployment/langflow-app-pipelines --
  curl -s -H "Authorization: Bearer 0p3n-w3bu"
  "http://localhost:9099/v1/models" | jq '.data[] | select(.id=="my_pipeline")'

# Check persistent storage
kubectl exec deployment/langflow-app-pipelines -- ls -la /app/pipelines/
```

#### Pipeline Debugging
- **Rate Limiting**: Check if requests are being throttled
- **Langflow Connection**: Verify LANGFLOW_BASE_URL environment variable
- **API Authentication**: Ensure pipelines-api-key secret is correct
- **Persistent Storage**: Confirm PersistentVolumeClaim is bound and writable

## Contributing

### API Configuration
- `OPENAI_API_KEY`: API keys for model access
- `PIPELINES_API_KEY=0p3n-w3bu`: Pipeline authentication token
- `OPENAI_API_BASE_URL=http://pipelines:9099/v1`: Pipeline integration URL

### Development vs Production
- **Development**: Uses default credentials in `.env` file
- **Production**: Use secrets management (Kubernetes secrets, external vaults)

## Contributing

We welcome contributions! Please:
1. Fork the repository
2. Create feature branches for changes
3. Ensure all services start correctly with `./setup-openwebui.sh`
4. Submit focused pull requests with clear descriptions
5. Include tests for new pipeline features

Keep changes minimal and well-documented. Test thoroughly in both development and production environments.
