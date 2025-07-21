#!/bin/bash

# start.sh - Daily startup script for the development environment
# Ensures cluster is running and basic services are deployed

set -e

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Configuration
CLUSTER_NAME="langflow-dev"
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_ROOT="$(dirname "$SCRIPT_DIR")"

echo -e "${BLUE}🚀 Starting development environment...${NC}"

# Function to check if cluster exists and is running
check_cluster() {
    echo -e "${BLUE}🎯 Checking Kind cluster...${NC}"
    
    if ! kind get clusters | grep -q "^${CLUSTER_NAME}$"; then
        echo -e "${YELLOW}⚠️  Cluster '$CLUSTER_NAME' does not exist. Running setup...${NC}"
        "$SCRIPT_DIR/setup.sh"
        return
    fi
    
    # Check if cluster is accessible
    if ! kubectl cluster-info --context "kind-${CLUSTER_NAME}" > /dev/null 2>&1; then
        echo -e "${YELLOW}⚠️  Cluster exists but is not accessible. Recreating...${NC}"
        kind delete cluster --name "$CLUSTER_NAME"
        "$SCRIPT_DIR/setup.sh"
        return
    fi
    
    echo -e "${GREEN}✅ Cluster is running${NC}"
    
    # Set kubectl context
    kubectl config use-context "kind-${CLUSTER_NAME}"
}

# Function to check if ingress controller is running
check_ingress() {
    echo -e "${BLUE}🌐 Checking ingress controller...${NC}"
    
    if ! kubectl get pods -n ingress-nginx -l app.kubernetes.io/component=controller --no-headers 2>/dev/null | grep -q Running; then
        echo -e "${YELLOW}⚠️  Ingress controller not running. Installing...${NC}"
        
        # Install ingress-nginx if not present
        helm upgrade --install ingress-nginx ingress-nginx/ingress-nginx \
            --namespace ingress-nginx \
            --create-namespace \
            --set controller.service.type=NodePort \
            --set controller.watchIngressWithoutClass=true \
            --set controller.nodeSelector."ingress-ready"=true \
            --set controller.tolerations[0].key=node-role.kubernetes.io/control-plane \
            --set controller.tolerations[0].operator=Equal \
            --set controller.tolerations[0].effect=NoSchedule
        
        # Wait for ingress controller
        kubectl wait --namespace ingress-nginx \
            --for=condition=ready pod \
            --selector=app.kubernetes.io/component=controller \
            --timeout=90s
    fi
    
    echo -e "${GREEN}✅ Ingress controller is running${NC}"
}

# Function to setup basic port forwarding
setup_port_forwarding() {
    echo -e "${BLUE}🔗 Setting up basic port forwarding...${NC}"
    
    # Kill any existing port-forward processes
    pkill -f "kubectl port-forward" 2>/dev/null || true
    
    # Start port forwarding in background (will be managed by tasks later)
    echo -e "${GREEN}✅ Port forwarding ready (use 'task expose:port-forward' to start)${NC}"
}

# Function to display environment info
show_environment_info() {
    echo -e "${GREEN}🎉 Development environment is ready!${NC}"
    echo ""
    echo -e "${BLUE}📋 Environment Information:${NC}"
    echo -e "  Cluster: ${YELLOW}${CLUSTER_NAME}${NC}"
    echo -e "  Context: ${YELLOW}kind-${CLUSTER_NAME}${NC}"
    echo ""
    
    echo -e "${BLUE}🔗 Available Ports (via Kind):${NC}"
    echo -e "  • OpenWebUI: ${YELLOW}http://localhost:3000${NC} (after deployment)"
    echo -e "  • Langflow: ${YELLOW}http://localhost:7860${NC} (after deployment)"
    echo -e "  • Pipelines: ${YELLOW}http://localhost:9099${NC} (after deployment)"
    echo -e "  • PostgreSQL: ${YELLOW}localhost:5432${NC} (after deployment)"
    echo -e "  • Ingress HTTP: ${YELLOW}http://localhost:8080${NC}"
    echo -e "  • Ingress HTTPS: ${YELLOW}https://localhost:8443${NC}"
    echo ""
    
    echo -e "${BLUE}🎯 Next Commands:${NC}"
    echo -e "  • Deploy application: ${YELLOW}task deploy${NC}"
    echo -e "  • Check status: ${YELLOW}task status${NC}"
    echo -e "  • View logs: ${YELLOW}task logs${NC}"
    echo -e "  • Expose services: ${YELLOW}task expose:expose-all${NC}"
    echo -e "  • List all tasks: ${YELLOW}task --list${NC}"
    echo ""
    
    # Show current cluster info
    echo -e "${BLUE}🏗️  Cluster Status:${NC}"
    kubectl get nodes
    echo ""
    kubectl get namespaces
}

# Main execution
main() {
    cd "$PROJECT_ROOT"
    
    check_cluster
    check_ingress
    setup_port_forwarding
    show_environment_info
}

# Run main function
main "$@"