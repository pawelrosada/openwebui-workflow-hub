# Architecture Documentation

## System Overview

The OpenWebUI-LangFlow-MCP Integration Framework is a containerized solution that provides a seamless bridge between conversational AI interfaces and visual workflow management systems. This document provides comprehensive technical details about the system architecture, component interactions, and data flow patterns.

## High-Level Architecture

```mermaid
graph TB
    subgraph ExtLayer ["External Layer"]
        User["User Browser"]
        AIProviders["AI Model Providers: OpenAI, Google, Anthropic"]
        MCPServers["MCP Servers: External Tools & APIs"]
    end

    subgraph DockerEnv ["Docker Compose Environment"]
        subgraph FrontLayer ["Frontend Layer"]
            OpenWebUI["OpenWebUI - Port 3000 - Image: ghcr.io/open-webui/open-webui:main"]
        end

        subgraph IntLayer ["Integration Layer"]
            Pipelines["Pipelines - Port 9099 - Image: ghcr.io/open-webui/pipelines:main"]
        end

        subgraph WorkLayer ["Workflow Layer"]
            LangFlow["LangFlow - Port 7860 - Image: langflowai/langflow:latest"]
        end

        subgraph DataLayer ["Data Layer"]
            PostgreSQL["PostgreSQL - Port 5432 - Image: postgres:16"]
        end

        subgraph StorageLayer ["Storage Layer"]
            OpenWebUIVol["open-webui volume"]
            PipelinesVol["pipelines volume"]
            LangFlowVol["langflow-data volume"]
            PostgreSQLVol["langflow-postgres volume"]
        end
    end

    User --> |"HTTPS/HTTP"| OpenWebUI
    OpenWebUI --> |"OpenAI API Format - HTTP REST"| Pipelines
    Pipelines --> |"Custom HTTP API - JSON Payload"| LangFlow
    LangFlow --> |"SQL Queries - PostgreSQL Protocol"| PostgreSQL
    LangFlow --> |"HTTP/HTTPS - API Calls"| AIProviders
    LangFlow --> |"HTTP/WebSocket - MCP Protocol"| MCPServers

    OpenWebUI -.-> OpenWebUIVol
    Pipelines -.-> PipelinesVol
    LangFlow -.-> LangFlowVol
    PostgreSQL -.-> PostgreSQLVol

    classDef external fill:#ffebee
    classDef frontend fill:#e1f5fe
    classDef integration fill:#f3e5f5
    classDef workflow fill:#e8f5e8
    classDef database fill:#fff3e0
    classDef storage fill:#f9f9f9

    class User,AIProviders,MCPServers external
    class OpenWebUI frontend
    class Pipelines integration
    class LangFlow workflow
    class PostgreSQL database
    class OpenWebUIVol,PipelinesVol,LangFlowVol,PostgreSQLVol storage
```

## Component Details

### 🌐 OpenWebUI (Frontend Layer)

**Purpose**: Modern chat interface providing user interaction capabilities

**Technical Specifications**:
- **Image**: `ghcr.io/open-webui/open-webui:main`
- **Port**: `3000` (external) → `8080` (internal)
- **Protocol**: HTTP/HTTPS
- **API Compatibility**: OpenAI Chat Completions API

**Key Features**:
- Multi-user authentication and session management
- Real-time streaming responses with WebSocket support
- File upload and document processing capabilities
- Plugin system for extended functionality
- Responsive web interface (desktop/mobile)

**Configuration**:
```yaml
environment:
  - OPENAI_API_BASE_URL=http://pipelines:9099/v1
  - OPENAI_API_KEY=0p3n-w3bu
  - ENABLE_SIGNUP=true
```

### 🔧 Pipelines (Integration Layer)

**Purpose**: Custom Python middleware handling API translation and workflow routing

**Technical Specifications**:
- **Image**: `ghcr.io/open-webui/pipelines:main`
- **Port**: `9099` (exposed)
- **Protocol**: HTTP REST API (OpenAI compatible)
- **Runtime**: Python with FastAPI framework

**Core Capabilities**:
- **Rate Limiting**: Configurable request throttling
- **Model Routing**: Dynamic selection between AI providers
- **Response Processing**: Format conversion and streaming
- **Error Handling**: Comprehensive exception management
- **Logging**: Structured logging for debugging

**Pipeline Types Available**:
1. **Basic Pipeline** (`langflow_pipeline.py`)
   - Simple OpenWebUI ↔ LangFlow bridge
   - Single workflow routing

2. **Enhanced Pipeline** (`enhanced_langflow_pipeline.py`)
   - Multi-model support with dynamic routing
   - User commands (`@model:gemini`, `@model:gpt`)

3. **Workflow Selector** (`workflow_selector_pipeline.py`)
   - Dynamic workflow selection based on input
   - Context-aware routing

### ⚡ LangFlow (Workflow Layer)

**Purpose**: Visual AI workflow builder and execution engine

**Technical Specifications**:
- **Image**: `langflowai/langflow:latest`
- **Port**: `7860` (exposed)
- **Protocol**: HTTP API with WebSocket for real-time updates
- **Framework**: FastAPI with React frontend

**Architecture Components**:
- **Flow Builder**: Drag-and-drop visual interface
- **Component Library**: Pre-built nodes for AI operations
- **Execution Engine**: Workflow processing and state management
- **Version Control**: Workflow versioning and rollback
- **API Gateway**: RESTful API for external integrations

**Integration Points**:
- **Input**: HTTP POST requests from Pipelines
- **Processing**: Node-based workflow execution
- **Output**: JSON responses with structured data
- **Storage**: PostgreSQL for workflow persistence

### 🗄️ PostgreSQL (Data Layer)

**Purpose**: Persistent storage for workflows, configurations, and chat history

**Technical Specifications**:
- **Image**: `postgres:16`
- **Port**: `5432` (exposed)
- **Protocol**: PostgreSQL wire protocol
- **Authentication**: Username/password

**Data Schema**:
- **Workflows**: Flow definitions and configurations
- **Components**: Custom component metadata
- **Sessions**: Chat conversation history
- **Users**: Authentication and preference data

## Data Flow Patterns

### Request-Response Flow

```mermaid
sequenceDiagram
    participant User as 👤 User
    participant OW as 🌐 OpenWebUI
    participant P as 🔧 Pipelines
    participant LF as ⚡ LangFlow
    participant DB as 🗄️ PostgreSQL
    participant AI as 🤖 AI Provider
    participant MCP as 🔌 MCP Server

    Note over User,MCP: Complete Request-Response Cycle

    User->>+OW: Send Chat Message
    OW->>+P: "POST /v1/chat/completions<br/>{model, messages, stream: true}"

    Note over P: Rate Limiting & Validation
    P->>P: Check Rate Limits
    P->>P: Validate Request Format

    P->>+LF: "POST /api/v1/run/{workflow_id}<br/>{input_value: message, stream: true}"

    Note over LF: Workflow Execution
    LF->>+DB: SELECT workflow_config
    DB-->>-LF: Workflow Definition

    LF->>LF: Initialize Flow Context
    LF->>LF: Process Input Nodes

    alt AI Model Node
        LF->>+AI: "API Request (GPT/Gemini/Claude)"
        AI-->>-LF: AI Response
    else MCP Tool Node
        LF->>+MCP: MCP Protocol Request
        MCP-->>-LF: Tool Response
    else Custom Component
        LF->>LF: Execute Custom Logic
    end

    LF->>DB: INSERT conversation_log
    LF->>LF: Process Output Nodes

    LF-->>-P: "Stream Response<br/>{data, session_id, message_id}"

    Note over P: Response Processing
    P->>P: Format OpenAI Compatible Response
    P->>P: Apply Response Filters

    P-->>-OW: "Stream SSE Response<br/>data: {choices: [{delta: {content: ...}}]}"

    OW-->>-User: Display Streaming Response

    Note over User,MCP: Error Handling Path
    alt Error Occurs
        LF->>DB: INSERT error_log
        LF-->>P: "Error Response<br/>{error: description, type: error_type}"
        P-->>OW: "HTTP 500 + Error Details"
        OW-->>User: User-Friendly Error Message
    end
```

## API Specifications

### OpenWebUI ↔ Pipelines API

**Endpoint**: `POST /v1/chat/completions`
**Protocol**: HTTP REST (OpenAI Compatible)

```json
{
  "model": "langflow",
  "messages": [
    {"role": "user", "content": "Hello, how are you?"}
  ],
  "stream": true,
  "temperature": 0.7,
  "max_tokens": 1000
}
```

### Pipelines ↔ LangFlow API

**Endpoint**: `POST /api/v1/run/{workflow_id}`
**Protocol**: HTTP REST with JSON payload

```json
{
  "input_value": "User message content",
  "stream": true,
  "session_id": "optional-session-id",
  "tweaks": {
    "parameter_name": "parameter_value"
  }
}
```

### LangFlow ↔ PostgreSQL

**Protocol**: PostgreSQL wire protocol
**Connection**: `postgresql://langflow:langflow@postgres:5432/langflow`

## Security Considerations

### Authentication & Authorization
- OpenWebUI handles user authentication
- Pipelines uses API key authentication (`PIPELINES_API_KEY`)
- PostgreSQL uses username/password authentication
- LangFlow inherits session context from pipelines

### Network Security
- All services run within isolated Docker network
- Only necessary ports exposed to host machine
- Internal service communication via DNS names
- No direct external access to PostgreSQL (configurable)

### Data Privacy
- Chat history stored locally in PostgreSQL
- No data transmitted outside Docker environment (except AI API calls)
- API keys stored as environment variables
- Volume mounts for persistent data

## Monitoring & Observability

### Logging Strategy
```mermaid
graph LR
    OpenWebUI[OpenWebUI Logs] --> Docker[Docker Logs]
    Pipelines[Pipeline Logs] --> Docker
    LangFlow[LangFlow Logs] --> Docker
    PostgreSQL[PostgreSQL Logs] --> Docker

    Docker --> |"docker-compose logs"| Console[Console Output]
    Docker --> |"Volume Mount"| LogFiles[Log Files]

    classDef service fill:#e3f2fd
    classDef output fill:#f3e5f5

    class OpenWebUI,Pipelines,LangFlow,PostgreSQL service
    class Docker,Console,LogFiles output
```

### Health Check Endpoints
- **OpenWebUI**: `http://localhost:3000/health`
- **Pipelines**: `http://localhost:9099/health`
- **LangFlow**: `http://localhost:7860/health`
- **PostgreSQL**: Connection test via psql

## Deployment Patterns

### Development Environment
- Single machine Docker Compose setup
- All services on same host with port mapping
- Volume mounts for development file changes
- Direct database access for debugging

### Production Environment
- Kubernetes deployment with Helm charts
- Horizontal pod autoscaling
- External PostgreSQL with high availability
- Ingress controllers for load balancing
- Secret management for API keys

## Extensibility Points

### Custom Pipeline Development
- Add new Python files to `/pipelines` directory
- Implement Pipeline class with required methods
- Configure model routing and response handling
- Test integration with OpenWebUI interface

### LangFlow Workflow Creation
- Use visual flow builder at `http://localhost:7860`
- Import/export workflow JSON configurations
- Create custom components for specific use cases
- Version control workflow definitions

### MCP Server Integration
- Configure MCP servers in LangFlow components
- Implement custom MCP protocol handlers
- Connect to external tools and APIs
- Manage authentication and rate limiting

---

*Last Updated: January 2025*
