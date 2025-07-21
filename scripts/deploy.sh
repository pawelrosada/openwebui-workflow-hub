#!/bin/bash

# deploy.sh - Deployment script for the application
# Deploys or upgrades the Helm chart with development values

set -e

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Configuration
CLUSTER_NAME="langflow-dev"
RELEASE_NAME="langflow-app"
NAMESPACE="default"
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_ROOT="$(dirname "$SCRIPT_DIR")"

echo -e "${BLUE}🚀 Deploying Langflow application...${NC}"

# Function to check if we're connected to the right cluster
check_cluster_context() {
    local current_context
    current_context=$(kubectl config current-context 2>/dev/null || echo "none")
    
    if [[ "$current_context" != "kind-${CLUSTER_NAME}" ]]; then
        echo -e "${YELLOW}⚠️  Not connected to the right cluster. Switching context...${NC}"
        if ! kubectl config use-context "kind-${CLUSTER_NAME}" 2>/dev/null; then
            echo -e "${RED}❌ Could not switch to cluster context. Is the cluster running?${NC}"
            echo -e "${YELLOW}💡 Try running: task start${NC}"
            exit 1
        fi
    fi
    
    echo -e "${GREEN}✅ Connected to cluster: ${current_context}${NC}"
}

# Function to update Helm repositories
update_helm_repos() {
    echo -e "${BLUE}📚 Updating Helm repositories...${NC}"
    helm repo update
    echo -e "${GREEN}✅ Helm repositories updated${NC}"
}

# Function to deploy or upgrade the application
deploy_application() {
    echo -e "${BLUE}🏗️  Deploying application with Helm...${NC}"
    
    # Check if release exists
    if helm list -n "$NAMESPACE" | grep -q "$RELEASE_NAME"; then
        echo -e "${BLUE}🔄 Upgrading existing release...${NC}"
        action="upgrade"
    else
        echo -e "${BLUE}📦 Installing new release...${NC}"
        action="install"
    fi
    
    # Deploy with development values
    helm "$action" "$RELEASE_NAME" "$PROJECT_ROOT/helm" \
        --namespace "$NAMESPACE" \
        --create-namespace \
        --values "$PROJECT_ROOT/values-dev.yaml" \
        --timeout 300s \
        --wait
    
    echo -e "${GREEN}✅ Application deployment completed${NC}"
}

# Function to wait for deployment to be ready
wait_for_deployment() {
    echo -e "${BLUE}⏳ Waiting for deployment to be ready...${NC}"
    
    # Wait for main langflow deployment
    if kubectl get deployment langflow-app -n "$NAMESPACE" >/dev/null 2>&1; then
        kubectl wait --for=condition=available --timeout=300s deployment/langflow-app -n "$NAMESPACE"
        echo -e "${GREEN}✅ Langflow deployment is ready${NC}"
    fi
    
    # Wait for PostgreSQL
    if kubectl get statefulset langflow-app-postgresql -n "$NAMESPACE" >/dev/null 2>&1; then
        kubectl wait --for=condition=ready --timeout=300s pod -l app.kubernetes.io/name=postgresql -n "$NAMESPACE"
        echo -e "${GREEN}✅ PostgreSQL is ready${NC}"
    fi
    
    # Wait for OpenWebUI if enabled
    if kubectl get deployment langflow-app-openwebui -n "$NAMESPACE" >/dev/null 2>&1; then
        kubectl wait --for=condition=available --timeout=300s deployment/langflow-app-openwebui -n "$NAMESPACE"
        echo -e "${GREEN}✅ OpenWebUI deployment is ready${NC}"
    fi
    
    echo -e "${GREEN}🎉 All deployments are ready!${NC}"
}

# Function to show deployment status and access information
show_deployment_info() {
    echo -e "${BLUE}📋 Deployment Information:${NC}"
    echo ""
    
    # Show pods status
    echo -e "${BLUE}🏃 Running Pods:${NC}"
    kubectl get pods -n "$NAMESPACE" -o wide
    echo ""
    
    # Show services
    echo -e "${BLUE}🔗 Services:${NC}"
    kubectl get services -n "$NAMESPACE"
    echo ""
    
    # Show ingress if any
    if kubectl get ingress -n "$NAMESPACE" --no-headers 2>/dev/null | grep -q .; then
        echo -e "${BLUE}🌐 Ingress:${NC}"
        kubectl get ingress -n "$NAMESPACE"
        echo ""
    fi
    
    # Show NodePort access information
    echo -e "${BLUE}🚀 Access Your Applications:${NC}"
    echo -e "  📱 OpenWebUI: ${YELLOW}http://localhost:3000${NC}"
    echo -e "  ⚡ Langflow: ${YELLOW}http://localhost:7860${NC}"
    echo -e "  🔧 Pipelines API: ${YELLOW}http://localhost:9099${NC}"
    echo -e "  🗄️ PostgreSQL: ${YELLOW}localhost:5432${NC}"
    echo ""
    
    # Show ingress access if enabled
    echo -e "${BLUE}🌐 Ingress Access (add to /etc/hosts):${NC}"
    echo -e "  ${YELLOW}127.0.0.1 langflow.local${NC}"
    echo -e "  Then visit: ${YELLOW}http://langflow.local:8080${NC}"
    echo ""
    
    # Show useful commands
    echo -e "${BLUE}🛠️  Useful Commands:${NC}"
    echo -e "  • View logs: ${YELLOW}task logs${NC}"
    echo -e "  • Port forward: ${YELLOW}task expose:port-forward${NC}"
    echo -e "  • Shell access: ${YELLOW}task shell${NC}"
    echo -e "  • Check status: ${YELLOW}task status${NC}"
    echo -e "  • Expose options: ${YELLOW}task expose:expose-all${NC}"
    
    # Show login information
    echo ""
    echo -e "${BLUE}🔑 Login Information:${NC}"
    echo -e "  Langflow Admin: ${YELLOW}admin / admin123${NC}"
    echo -e "  PostgreSQL: ${YELLOW}langflow_user / devpassword${NC}"
}

# Function to run post-deployment checks
run_health_checks() {
    echo -e "${BLUE}🏥 Running health checks...${NC}"
    
    # Check if all pods are running
    local failed_pods
    failed_pods=$(kubectl get pods -n "$NAMESPACE" --no-headers | grep -v Running | grep -v Completed || true)
    
    if [[ -n "$failed_pods" ]]; then
        echo -e "${YELLOW}⚠️  Some pods are not running:${NC}"
        echo "$failed_pods"
        echo -e "${YELLOW}💡 Check pod logs with: kubectl logs <pod-name> -n $NAMESPACE${NC}"
    else
        echo -e "${GREEN}✅ All pods are healthy${NC}"
    fi
    
    # Check services
    local services_count
    services_count=$(kubectl get services -n "$NAMESPACE" --no-headers | wc -l)
    echo -e "${GREEN}✅ $services_count services are running${NC}"
}

# Main execution
main() {
    cd "$PROJECT_ROOT"
    
    check_cluster_context
    update_helm_repos
    deploy_application
    wait_for_deployment
    run_health_checks
    show_deployment_info
}

# Run main function
main "$@"