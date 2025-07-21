#!/bin/bash

# stop.sh - Cleanup script for the development environment
# Stops port forwarding and optionally destroys the cluster

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

echo -e "${BLUE}🛑 Stopping development environment...${NC}"

# Function to stop port forwarding
stop_port_forwarding() {
    echo -e "${BLUE}🔌 Stopping port forwarding processes...${NC}"
    
    local port_forward_pids
    port_forward_pids=$(pgrep -f "kubectl port-forward" 2>/dev/null || true)
    
    if [[ -n "$port_forward_pids" ]]; then
        echo -e "${YELLOW}⏹️  Killing port-forward processes: $port_forward_pids${NC}"
        pkill -f "kubectl port-forward" || true
        echo -e "${GREEN}✅ Port forwarding stopped${NC}"
    else
        echo -e "${GREEN}✅ No port forwarding processes running${NC}"
    fi
}

# Function to uninstall Helm release
uninstall_application() {
    if [[ "$1" == "--uninstall-app" ]]; then
        echo -e "${BLUE}📦 Uninstalling Helm release...${NC}"
        
        if helm list -n "$NAMESPACE" | grep -q "$RELEASE_NAME"; then
            helm uninstall "$RELEASE_NAME" -n "$NAMESPACE" --timeout 300s
            echo -e "${GREEN}✅ Application uninstalled${NC}"
        else
            echo -e "${YELLOW}⚠️  No Helm release found to uninstall${NC}"
        fi
        
        # Clean up any remaining resources
        echo -e "${BLUE}🧹 Cleaning up remaining resources...${NC}"
        kubectl delete pvc --all -n "$NAMESPACE" --timeout=60s 2>/dev/null || true
        echo -e "${GREEN}✅ Resources cleaned up${NC}"
    fi
}

# Function to destroy Kind cluster
destroy_cluster() {
    if [[ "$1" == "--destroy-cluster" ]]; then
        echo -e "${BLUE}💥 Destroying Kind cluster...${NC}"
        
        if kind get clusters | grep -q "^${CLUSTER_NAME}$"; then
            kind delete cluster --name "$CLUSTER_NAME"
            echo -e "${GREEN}✅ Cluster destroyed${NC}"
        else
            echo -e "${YELLOW}⚠️  No cluster found to destroy${NC}"
        fi
    fi
}

# Function to show cleanup status
show_cleanup_status() {
    echo -e "${GREEN}🎉 Cleanup completed!${NC}"
    echo ""
    
    # Show what's still running
    echo -e "${BLUE}📋 Current Status:${NC}"
    
    # Check for clusters
    local clusters
    clusters=$(kind get clusters 2>/dev/null || true)
    if [[ -n "$clusters" ]]; then
        echo -e "${BLUE}🏗️  Remaining Kind clusters:${NC}"
        echo "$clusters" | sed 's/^/  • /'
    else
        echo -e "${GREEN}✅ No Kind clusters running${NC}"
    fi
    
    # Check for port forwarding
    if pgrep -f "kubectl port-forward" >/dev/null 2>&1; then
        echo -e "${YELLOW}⚠️  Some port forwarding processes may still be running${NC}"
    else
        echo -e "${GREEN}✅ No port forwarding processes running${NC}"
    fi
    
    echo ""
    echo -e "${BLUE}🚀 To restart the environment:${NC}"
    echo -e "  ${YELLOW}task start${NC}"
    echo -e "  ${YELLOW}task deploy${NC}"
}

# Function to show usage
show_usage() {
    echo -e "${BLUE}Usage:${NC}"
    echo -e "  $0                    # Stop port forwarding only"
    echo -e "  $0 --uninstall-app    # Also uninstall the Helm application"
    echo -e "  $0 --destroy-cluster  # Also destroy the Kind cluster"
    echo -e "  $0 --full-cleanup     # Uninstall app AND destroy cluster"
    echo ""
    echo -e "${BLUE}Examples:${NC}"
    echo -e "  # Quick stop (keep cluster and app running):"
    echo -e "  ${YELLOW}$0${NC}"
    echo ""
    echo -e "  # Stop and uninstall app (keep cluster):"
    echo -e "  ${YELLOW}$0 --uninstall-app${NC}"
    echo ""
    echo -e "  # Complete cleanup (destroy everything):"
    echo -e "  ${YELLOW}$0 --destroy-cluster${NC}"
}

# Function to handle full cleanup
full_cleanup() {
    uninstall_application "--uninstall-app"
    destroy_cluster "--destroy-cluster"
}

# Main execution
main() {
    case "${1:-}" in
        "--help"|"-h")
            show_usage
            exit 0
            ;;
        "--full-cleanup")
            stop_port_forwarding
            full_cleanup
            ;;
        "--uninstall-app")
            stop_port_forwarding
            uninstall_application "--uninstall-app"
            ;;
        "--destroy-cluster")
            stop_port_forwarding
            uninstall_application "--uninstall-app"
            destroy_cluster "--destroy-cluster"
            ;;
        "")
            stop_port_forwarding
            ;;
        *)
            echo -e "${RED}❌ Unknown option: $1${NC}"
            show_usage
            exit 1
            ;;
    esac
    
    show_cleanup_status
}

# Run main function
main "$@"