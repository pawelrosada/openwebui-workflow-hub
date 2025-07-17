#!/bin/bash
# Development startup script

set -e  # Exit on any error

echo "🚀 Starting Langflow Chat UI development environment..."

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

# Check if pnpm is installed
if ! command -v pnpm &> /dev/null; then
    echo -e "${YELLOW}📦 pnpm not found. Installing...${NC}"
    npm install -g pnpm
fi

# Create .env if it doesn't exist
if [ ! -f .env ]; then
    echo -e "${BLUE}📝 Creating .env file from template...${NC}"
    cp .env.example .env
fi

# Install dependencies if needed
if [ ! -d "node_modules" ]; then
    echo -e "${BLUE}📦 Installing dependencies...${NC}"
    pnpm install
fi

# Build and start services using dev compose
echo -e "${BLUE}🏗️  Building and starting development services...${NC}"
docker-compose -f docker-compose.dev.yml down
docker-compose -f docker-compose.dev.yml up --build -d

# Wait for services to be ready
echo -e "${YELLOW}⏳ Waiting for services to be ready...${NC}"

# Wait for PostgreSQL
echo -e "${YELLOW}🐘 Waiting for PostgreSQL...${NC}"
until docker-compose -f docker-compose.dev.yml exec postgres pg_isready -U langflow -d langflow > /dev/null 2>&1; do
    sleep 2
    echo -n "."
done
echo -e "${GREEN}✅ PostgreSQL is ready${NC}"

# Wait for Redis
echo -e "${YELLOW}🔴 Waiting for Redis...${NC}"
until docker-compose -f docker-compose.dev.yml exec redis redis-cli ping > /dev/null 2>&1; do
    sleep 2
    echo -n "."
done
echo -e "${GREEN}✅ Redis is ready${NC}"

# Wait for Langflow
echo -e "${YELLOW}🔧 Waiting for Langflow...${NC}"
until curl -f http://localhost:7860/health > /dev/null 2>&1; do
    sleep 5
    echo -n "."
done
echo -e "${GREEN}✅ Langflow is ready${NC}"

echo -e "${GREEN}🎉 All services are ready!${NC}"

echo -e "${BLUE}📍 Available services:${NC}"
echo -e "🌐 Frontend (Vite): ${GREEN}http://localhost:3001${NC}"
echo -e "🔧 Backend API: ${GREEN}http://localhost:3000${NC}"
echo -e "🧠 Langflow UI: ${GREEN}http://localhost:7860${NC}"
echo -e "🗄️  PostgreSQL: ${GREEN}localhost:5432${NC}"
echo -e "🔴 Redis: ${GREEN}localhost:6379${NC}"
echo -e "📊 API Health: ${GREEN}http://localhost:3000/api/health${NC}"

echo ""
echo -e "${BLUE}📋 Useful commands:${NC}"
echo -e "View logs: ${YELLOW}docker-compose -f docker-compose.dev.yml logs -f [service]${NC}"
echo -e "Shell access: ${YELLOW}docker-compose -f docker-compose.dev.yml exec [service] sh${NC}"
echo -e "Stop services: ${YELLOW}docker-compose -f docker-compose.dev.yml down${NC}"
