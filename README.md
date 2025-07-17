# Langflow Chat UI

Modern ChatGPT-like interface for Langflow workflows built with Node.js, TypeScript, React, and Tailwind CSS.

## 🚀 Features

- **Modern Chat Interface** - ChatGPT/Perplexity-inspired design
- **Real-time Communication** - WebSocket support for live updates
- **Langflow Integration** - Seamless connection to Langflow workflows
- **Session Management** - Persistent chat sessions
- **Responsive Design** - Works on desktop and mobile
- **Dark/Light Theme** - Toggle between themes
- **Message Formatting** - Markdown and code syntax highlighting
- **Docker Ready** - Complete containerized deployment

## 🛠 Tech Stack

### Backend
- **Node.js 22+** with TypeScript
- **Fastify** - Fast web framework
- **Zod** - Runtime type validation
- **WebSocket** - Real-time communication
- **Redis** - Caching and session storage

### Frontend
- **React 18** with TypeScript
- **Vite** - Fast build tool
- **Tailwind CSS** - Utility-first styling
- **Lucide Icons** - Beautiful icons
- **Framer Motion** - Smooth animations

### DevOps
- **Docker** - Containerization
- **Nginx** - Reverse proxy
- **PostgreSQL** - Database for Langflow
- **Docker Compose** - Multi-container orchestration

## 🏃‍♂️ Quick Start

### Prerequisites
- Docker and Docker Compose
- Node.js 22+ (for local development)
- pnpm 8.15+ (package manager)

### Production Deployment

1. **Clone and setup**:
   ```bash
   git clone <repository>
   cd langflow-ui
   chmod +x scripts/*.sh
   ```

2. **Deploy with Docker**:
   ```bash
   ./scripts/prod.sh
   ```

3. **Access the application**:
   - Chat UI: http://localhost
   - Langflow: http://localhost/langflow
   - API Health: http://localhost:3000/api/health

### Development Setup

1. **Start development environment**:
   ```bash
   ./scripts/dev.sh
   ```

2. **Access development servers**:
   - Frontend: http://localhost:3001
   - Backend API: http://localhost:3000
   - Langflow: http://localhost:7860

## 📁 Project Structure

```
langflow-ui/
├── src/
│   ├── backend/           # Node.js/Fastify backend
│   │   ├── routes/        # API routes
│   │   ├── services/      # Business logic
│   │   └── websocket/     # WebSocket handlers
│   ├── frontend/          # React frontend
│   │   ├── src/
│   │   │   ├── components/  # React components
│   │   │   ├── hooks/       # Custom hooks
│   │   │   └── utils/       # Utilities
│   └── shared/            # Shared types and utilities
│       └── types/         # TypeScript types
├── scripts/               # Deployment scripts
├── docker-compose.yml     # Container orchestration
├── Dockerfile            # Multi-stage build
├── nginx.conf            # Reverse proxy config
└── package.json          # Dependencies and scripts
```

## 🔧 Configuration

### Environment Variables

Create `.env` file (see `.env.example`):

```bash
NODE_ENV=development
PORT=3000
LANGFLOW_API_URL=http://localhost:7860
LOG_LEVEL=debug
REDIS_URL=redis://localhost:6379
```

### Docker Services

- **langflow-chat-ui**: Main Node.js application
- **langflow**: Original Langflow backend
- **postgres**: Database for Langflow
- **redis**: Caching and sessions
- **nginx**: Reverse proxy and load balancer

## 🔌 API Endpoints

### Chat API
- `POST /api/chat/send` - Send message to Langflow
- `GET /api/chat/messages/:sessionId` - Get chat history
- `WS /api/chat/stream/:sessionId` - WebSocket streaming

### Session Management
- `GET /api/sessions` - List all sessions
- `POST /api/sessions` - Create new session
- `DELETE /api/sessions/:id` - Delete session

### Flows
- `GET /api/flows` - List available Langflow workflows
- `GET /api/flows/:id` - Get specific workflow

## 🎨 UI Components

### Layout
- **ChatLayout** - Main application layout
- **Sidebar** - Session list and navigation
- **ChatArea** - Message display and input

### Messaging
- **MessageList** - Scrollable message container
- **MessageBubble** - Individual message display
- **TypingIndicator** - Shows when AI is responding

### Features
- **Theme Toggle** - Dark/light mode switching
- **Message Formatting** - Markdown and code highlighting
- **Copy to Clipboard** - Easy message copying
- **Responsive Design** - Mobile-friendly interface

## 🚦 Development

### Available Scripts

```bash
# Development
pnpm dev              # Start both backend and frontend
pnpm dev:backend      # Backend only
pnpm dev:frontend     # Frontend only

# Building
pnpm build           # Build for production
pnpm build:backend   # Build backend only
pnpm build:frontend  # Build frontend only

# Testing
pnpm test            # Run tests
pnpm test:coverage   # Coverage report

# Docker
./scripts/dev.sh     # Development environment
./scripts/prod.sh    # Production deployment
```

### Code Standards

- **TypeScript Strict Mode** - Full type safety
- **ESLint + Prettier** - Code formatting
- **Zod Validation** - Runtime type checking
- **Error Handling** - Comprehensive error management
- **Testing** - Vitest for unit tests

## 🔒 Security Features

- **Rate Limiting** - API and chat endpoint protection
- **CORS** - Cross-origin request handling
- **Helmet** - Security headers
- **Input Validation** - Zod schema validation
- **Content Security Policy** - XSS protection

## 📊 Monitoring

- **Health Checks** - Built-in health endpoints
- **Structured Logging** - JSON formatted logs
- **Error Tracking** - Comprehensive error handling
- **Performance Metrics** - Response time tracking

## 🌐 Nginx Configuration

The included Nginx configuration provides:
- **Reverse Proxy** - Routes to appropriate services
- **Rate Limiting** - Protection against abuse
- **Static File Caching** - Performance optimization
- **WebSocket Support** - Real-time communication
- **Security Headers** - Protection against common attacks

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests if applicable
5. Submit a pull request

## 📝 License

This project is licensed under the MIT License.

## 🆘 Troubleshooting

### Common Issues

1. **Docker not starting**:
   ```bash
   # Check Docker status
   docker info
   # Restart Docker service
   sudo systemctl restart docker
   ```

2. **Port conflicts**:
   ```bash
   # Check what's using the port
   lsof -i :3000
   # Kill the process
   kill -9 <PID>
   ```

3. **Langflow not responding**:
   ```bash
   # Check Langflow logs
   docker-compose logs langflow
   # Restart Langflow
   docker-compose restart langflow
   ```

4. **Frontend build issues**:
   ```bash
   # Clear node_modules and reinstall
   rm -rf node_modules package-lock.json
   pnpm install
   ```

### Logs and Debugging

```bash
# View all service logs
docker-compose logs -f

# View specific service logs
docker-compose logs -f langflow-chat-ui
docker-compose logs -f langflow
docker-compose logs -f nginx

# Enter container for debugging
docker-compose exec langflow-chat-ui sh
```

---

**Built with ❤️ for the Langflow community**
