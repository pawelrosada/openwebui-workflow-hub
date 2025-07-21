#!/bin/bash

# setup.sh - One-time setup script for Kind + Helm development environment
# This script checks for required tools and sets up the initial environment

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

echo -e "${BLUE}🚀 Setting up Kind + Helm development environment...${NC}"

# Function to check if a command exists
check_command() {
    if ! command -v "$1" &> /dev/null; then
        echo -e "${RED}❌ $1 is not installed.${NC}"
        return 1
    else
        echo -e "${GREEN}✅ $1 is available${NC}"
        return 0
    fi
}

# Function to install missing tools
install_missing_tools() {
    local missing_tools=()
    
    # Check required tools
    echo -e "${BLUE}📦 Checking required tools...${NC}"
    
    check_command "docker" || missing_tools+=("docker")
    check_command "kind" || missing_tools+=("kind")
    check_command "helm" || missing_tools+=("helm")
    check_command "kubectl" || missing_tools+=("kubectl")
    check_command "task" || missing_tools+=("task")
    
    if [[ ${#missing_tools[@]} -gt 0 ]]; then
        echo -e "${YELLOW}⚠️  Missing tools detected: ${missing_tools[*]}${NC}"
        echo -e "${BLUE}🔧 Attempting to install missing tools...${NC}"
        
        # Install based on OS
        if [[ "$OSTYPE" == "linux-gnu"* ]]; then
            for tool in "${missing_tools[@]}"; do
                case $tool in
                    "kind")
                        echo -e "${BLUE}Installing Kind...${NC}"
                        [ $(uname -m) = x86_64 ] && curl -Lo ./kind https://kind.sigs.k8s.io/dl/v0.29.0/kind-linux-amd64
                        chmod +x ./kind
                        sudo mv ./kind /usr/local/bin/kind
                        ;;
                    "helm")
                        echo -e "${BLUE}Installing Helm...${NC}"
                        curl https://raw.githubusercontent.com/helm/helm/main/scripts/get-helm-3 | bash
                        ;;
                    "kubectl")
                        echo -e "${BLUE}Installing kubectl...${NC}"
                        curl -LO "https://dl.k8s.io/release/$(curl -L -s https://dl.k8s.io/release/stable.txt)/bin/linux/amd64/kubectl"
                        chmod +x kubectl
                        sudo mv kubectl /usr/local/bin/kubectl
                        ;;
                    "task")
                        echo -e "${BLUE}Installing Task...${NC}"
                        sh -c "$(curl --location https://taskfile.dev/install.sh)" -- -d -b /usr/local/bin
                        ;;
                    "docker")
                        echo -e "${RED}❌ Docker installation requires manual setup. Please install Docker first.${NC}"
                        echo -e "${YELLOW}Visit: https://docs.docker.com/get-docker/${NC}"
                        exit 1
                        ;;
                esac
            done
        else
            echo -e "${YELLOW}⚠️  Automated installation not supported on your OS.${NC}"
            echo -e "${YELLOW}Please install the missing tools manually:${NC}"
            for tool in "${missing_tools[@]}"; do
                echo -e "  - $tool"
            done
            exit 1
        fi
    fi
}

# Function to check Docker is running
check_docker() {
    echo -e "${BLUE}🐳 Checking Docker status...${NC}"
    if ! docker info > /dev/null 2>&1; then
        echo -e "${RED}❌ Docker is not running. Please start Docker first.${NC}"
        exit 1
    fi
    echo -e "${GREEN}✅ Docker is running${NC}"
}

# Function to create Kind cluster
create_cluster() {
    echo -e "${BLUE}🎯 Setting up Kind cluster...${NC}"
    
    # Check if cluster already exists
    if kind get clusters | grep -q "^${CLUSTER_NAME}$"; then
        echo -e "${YELLOW}⚠️  Cluster '$CLUSTER_NAME' already exists${NC}"
        read -p "Do you want to recreate it? (y/N): " -n 1 -r
        echo
        if [[ $REPLY =~ ^[Yy]$ ]]; then
            echo -e "${BLUE}🗑️  Deleting existing cluster...${NC}"
            kind delete cluster --name "$CLUSTER_NAME"
        else
            echo -e "${GREEN}✅ Using existing cluster${NC}"
            return 0
        fi
    fi
    
    # Create cluster
    echo -e "${BLUE}🏗️  Creating Kind cluster with name '$CLUSTER_NAME'...${NC}"
    kind create cluster --config="$PROJECT_ROOT/kind-config.yaml" --name="$CLUSTER_NAME"
    
    # Wait for cluster to be ready
    echo -e "${BLUE}⏳ Waiting for cluster to be ready...${NC}"
    kubectl wait --for=condition=Ready nodes --all --timeout=300s
    
    echo -e "${GREEN}✅ Kind cluster created successfully${NC}"
}

# Function to setup Helm repositories
setup_helm() {
    echo -e "${BLUE}📚 Setting up Helm repositories...${NC}"
    
    # Add Bitnami repository for PostgreSQL
    helm repo add bitnami https://charts.bitnami.com/bitnami
    
    # Add ingress-nginx for ingress controller
    helm repo add ingress-nginx https://kubernetes.github.io/ingress-nginx
    
    # Update repositories
    helm repo update
    
    echo -e "${GREEN}✅ Helm repositories configured${NC}"
}

# Function to install ingress controller
setup_ingress() {
    echo -e "${BLUE}🌐 Installing ingress controller...${NC}"
    
    # Install ingress-nginx for Kind
    helm upgrade --install ingress-nginx ingress-nginx/ingress-nginx \
        --namespace ingress-nginx \
        --create-namespace \
        --set controller.service.type=NodePort \
        --set controller.watchIngressWithoutClass=true \
        --set controller.nodeSelector."ingress-ready"=true \
        --set controller.tolerations[0].key=node-role.kubernetes.io/control-plane \
        --set controller.tolerations[0].operator=Equal \
        --set controller.tolerations[0].effect=NoSchedule \
        --set controller.tolerations[0].tolerations[1].key=node-role.kubernetes.io/master \
        --set controller.tolerations[0].tolerations[1].operator=Equal \
        --set controller.tolerations[0].tolerations[1].effect=NoSchedule
    
    # Wait for ingress controller to be ready
    kubectl wait --namespace ingress-nginx \
        --for=condition=ready pod \
        --selector=app.kubernetes.io/component=controller \
        --timeout=90s
    
    echo -e "${GREEN}✅ Ingress controller installed${NC}"
}

# Function to display next steps
show_next_steps() {
    echo -e "${GREEN}🎉 Setup completed successfully!${NC}"
    echo -e "${BLUE}📋 Next steps:${NC}"
    echo -e "  1. Start the development environment: ${YELLOW}task start${NC}"
    echo -e "  2. Deploy the application: ${YELLOW}task deploy${NC}"
    echo -e "  3. Check status: ${YELLOW}task status${NC}"
    echo -e "  4. View available tasks: ${YELLOW}task --list${NC}"
    echo ""
    echo -e "${BLUE}🔗 Service exposure examples:${NC}"
    echo -e "  • Port forward: ${YELLOW}task expose:port-forward${NC}"
    echo -e "  • NodePort: ${YELLOW}task expose:nodeport${NC}"
    echo -e "  • Ingress: ${YELLOW}task expose:ingress${NC}"
    echo -e "  • Show all options: ${YELLOW}task expose:expose-all${NC}"
    echo ""
    echo -e "${BLUE}🐳 Cluster info:${NC}"
    kubectl cluster-info --context "kind-${CLUSTER_NAME}"
}

# Main execution
main() {
    cd "$PROJECT_ROOT"
    
    install_missing_tools
    check_docker
    create_cluster
    setup_helm
    setup_ingress
    show_next_steps
}

# Run main function
main "$@"