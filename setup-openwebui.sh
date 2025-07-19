#!/bin/bash

echo "🚀 Setting up Langflow + Open WebUI environment..."

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Check if Docker is running
if ! docker info > /dev/null 2>&1; then
    echo -e "${RED}❌ Docker is not running. Please start Docker first.${NC}"
    exit 1
fi

# Stop existing containers if running
echo -e "${YELLOW}📦 Stopping existing containers...${NC}"
docker-compose -f docker-compose.yml down 2>/dev/null || true
docker-compose -f docker-compose.openwebui.yml down 2>/dev/null || true

# Clean up old volumes if requested
if [[ "$1" == "--clean" ]]; then
    echo -e "${YELLOW}🧹 Cleaning up old data volumes...${NC}"
    docker volume rm langflow-ui_postgres_data 2>/dev/null || true
    docker volume rm langflow-ui_redis_data 2>/dev/null || true
    docker volume rm langflow-ui_langflow_data 2>/dev/null || true
    docker volume rm langflow-ui_open_webui_data 2>/dev/null || true
fi

# Create .env.openwebui if it doesn't exist
if [ ! -f .env.openwebui ]; then
    echo -e "${BLUE}📝 Creating .env.openwebui file...${NC}"
    cat > .env.openwebui << EOF
# Database Configuration
POSTGRES_DB=langflow_db
POSTGRES_USER=langflow_user
POSTGRES_PASSWORD=langflow_pass_$(date +%s)

# Langflow Configuration
LANGFLOW_SUPERUSER=admin
LANGFLOW_SUPERUSER_PASSWORD=admin123
LANGFLOW_SECRET_KEY=super-secret-key-$(openssl rand -hex 32)

# Open WebUI Configuration
WEBUI_SECRET_KEY=webui-secret-$(openssl rand -hex 32)
OPENAI_API_KEY=sk-langflow-integration-key

# Security (change in production)
WEBUI_AUTH=true
LANGFLOW_AUTO_LOGIN=false
EOF
    echo -e "${GREEN}✅ Created .env.openwebui with secure defaults${NC}"
fi

# Pull latest images
echo -e "${BLUE}📥 Pulling latest Docker images...${NC}"
docker-compose -f docker-compose.openwebui.yml pull

# Start services
echo -e "${BLUE}🏗️ Starting Langflow + Open WebUI services...${NC}"
docker-compose -f docker-compose.openwebui.yml up -d

# Wait for services to be healthy
echo -e "${YELLOW}⏳ Waiting for services to be ready...${NC}"
sleep 10

# Check service health
check_service() {
    # local service=$1  # Service name (unused but kept for clarity)
    local url=$2
    local name=$3
    
    for i in {1..30}; do
        if curl -f -s "$url" > /dev/null 2>&1; then
            echo -e "${GREEN}✅ $name is ready!${NC}"
            return 0
        fi
        echo -e "${YELLOW}⏳ Waiting for $name... (attempt $i/30)${NC}"
        sleep 5
    done
    echo -e "${RED}❌ $name failed to start${NC}"
    return 1
}

# Health checks
check_service "postgres" "postgres://langflow_user:langflow_pass@localhost:5432/langflow_db" "PostgreSQL"
check_service "redis" "redis://localhost:6379" "Redis"
check_service "langflow" "http://localhost:7860/health" "Langflow"
check_service "pipelines" "http://localhost:9099/health" "Pipelines"
check_service "open-webui" "http://localhost:3000/health" "Open WebUI"

# Show status
echo ""
echo -e "${GREEN}🎉 Langflow + Open WebUI + Pipelines is ready!${NC}"
echo ""
echo -e "${BLUE}📊 Service URLs:${NC}"
echo -e "  🌐 Open WebUI (Main Interface): ${GREEN}http://localhost:3000${NC}"
echo -e "  🔧 Langflow (Flow Builder):     ${GREEN}http://localhost:7860${NC}"
echo -e "  � Pipelines (Integration):     ${GREEN}http://localhost:9099${NC}"
echo -e "  �🗄️  Database (PostgreSQL):      ${GREEN}localhost:5432${NC}"
echo -e "  📦 Cache (Redis):               ${GREEN}localhost:6379${NC}"
echo ""
echo -e "${BLUE}🔐 Default Credentials:${NC}"
echo -e "  Langflow Admin: ${GREEN}admin / admin123${NC}"
echo ""
echo -e "${BLUE}📚 Next Steps:${NC}"
echo -e "  1. Open ${GREEN}http://localhost:3000${NC} for the modern chat interface"
echo -e "  2. Open ${GREEN}http://localhost:7860${NC} to create Langflow workflows"
echo -e "  3. Import example workflows from ${YELLOW}examples/langflow-workflows/${NC}"
echo -e "  4. Copy flow ID and use in chat: ${YELLOW}@flow:your-flow-id your message${NC}"
echo ""
echo -e "${YELLOW}💡 Pipeline Integration:${NC}"
echo -e "  • Messages are processed through Pipelines → Langflow"
echo -e "  • Use ${YELLOW}@flow:flow-id${NC} to specify which flow to use"
echo -e "  • Pipeline handles authentication and routing"
echo -e "  • Check logs: ${YELLOW}docker-compose -f docker-compose.openwebui.yml logs pipelines${NC}"
echo ""
echo -e "${BLUE}🤖 AI Workflow Examples:${NC}"
echo -e "  • Gemini 2.5 Flash: ${YELLOW}examples/langflow-workflows/basic-gemini-chat.json${NC}"
echo -e "  • GPT-4o:           ${YELLOW}examples/langflow-workflows/basic-gpt4o-chat.json${NC}"
echo -e "  • Claude 3.5:       ${YELLOW}examples/langflow-workflows/basic-claude-chat.json${NC}"
echo -e "  📖 See ${YELLOW}examples/README.md${NC} for usage instructions"
echo ""
echo -e "${YELLOW}💡 Pro Tips:${NC}"
echo -e "  • Open WebUI has built-in RAG, document upload, and web search"
echo -e "  • Configure Langflow flows and expose them via API"
echo -e "  • Use Open WebUI's pipelines feature for custom integrations"
echo ""
echo -e "${BLUE}🛠️ Management Commands:${NC}"
echo -e "  Stop:    ${YELLOW}docker-compose -f docker-compose.openwebui.yml down${NC}"
echo -e "  Logs:    ${YELLOW}docker-compose -f docker-compose.openwebui.yml logs -f${NC}"
echo -e "  Clean:   ${YELLOW}./setup-openwebui.sh --clean${NC}"
echo ""
