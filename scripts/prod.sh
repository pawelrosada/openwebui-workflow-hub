#!/bin/bash
# Production deployment script

set -e  # Exit on any error

echo "🚀 Deploying Langflow Chat UI to production..."

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

# Build production images
echo -e "${BLUE}🏗️  Building production images...${NC}"
docker-compose build --no-cache langflow-chat-ui

# Start all services
echo -e "${BLUE}🚀 Starting all services...${NC}"
docker-compose up -d

# Wait for services to be ready
echo -e "${YELLOW}⏳ Waiting for services to start...${NC}"
sleep 15

# Health checks
echo -e "${BLUE}🏥 Running health checks...${NC}"

# Check Chat UI
if curl -f http://localhost:3000/api/health > /dev/null 2>&1; then
    echo -e "${GREEN}✅ Chat UI API is healthy${NC}"
else
    echo -e "${RED}❌ Chat UI API health check failed${NC}"
    docker-compose logs langflow-chat-ui
    exit 1
fi

# Check Langflow
if curl -f http://localhost:7860/health > /dev/null 2>&1; then
    echo -e "${GREEN}✅ Langflow is healthy${NC}"
else
    echo -e "${RED}❌ Langflow health check failed${NC}"
    docker-compose logs langflow
    exit 1
fi

# Check Nginx
if curl -f http://localhost:80/health > /dev/null 2>&1; then
    echo -e "${GREEN}✅ Nginx proxy is healthy${NC}"
else
    echo -e "${YELLOW}⚠️  Nginx health check failed (may be expected)${NC}"
fi

# Display service URLs
echo -e "${GREEN}🎉 Production deployment successful!${NC}"
echo ""
echo -e "${BLUE}📍 Available services:${NC}"
echo -e "🌐 Main Application: ${GREEN}http://localhost${NC}"
echo -e "🔧 Langflow Direct: ${GREEN}http://localhost/langflow${NC}"
echo -e "📊 API Health: ${GREEN}http://localhost:3000/api/health${NC}"
echo -e "📱 Chat UI API: ${GREEN}http://localhost:3000${NC}"
echo -e "🗄️  Database: ${GREEN}localhost:5432${NC}"
echo -e "🔴 Redis: ${GREEN}localhost:6379${NC}"
echo ""
echo -e "${YELLOW}💡 Tips:${NC}"
echo -e "• View logs: ${GREEN}docker-compose logs -f${NC}"
echo -e "• Stop services: ${GREEN}docker-compose down${NC}"
echo -e "• Restart: ${GREEN}docker-compose restart${NC}"
echo -e "• Scale UI: ${GREEN}docker-compose up -d --scale langflow-chat-ui=3${NC}"

# Show running containers
echo -e "\n${BLUE}🐳 Running containers:${NC}"
docker-compose ps
