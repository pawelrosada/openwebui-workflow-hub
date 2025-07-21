#!/bin/bash

# Script to create/update pipelines ConfigMap from local files
# This maintains clean project structure without copying files to helm/

set -e

NAMESPACE=${NAMESPACE:-default}
CONFIGMAP_NAME="langflow-app-pipelines-config"

echo "🔧 Creating ConfigMap from pipelines directory..."

# Check if pipelines directory exists
if [ ! -d "pipelines" ]; then
    echo "❌ Error: pipelines directory not found!"
    echo "Run this script from the project root directory."
    exit 1
fi

# Create ConfigMap from all .py files in pipelines directory
kubectl create configmap "$CONFIGMAP_NAME" \
    --from-file=pipelines/ \
    --namespace="$NAMESPACE" \
    --dry-run=client -o yaml | \
kubectl apply -f -

echo "✅ ConfigMap '$CONFIGMAP_NAME' created/updated successfully"

# Count files
FILE_COUNT=$(find pipelines -name "*.py" | wc -l | tr -d ' ')
echo "📊 Loaded $FILE_COUNT Python pipeline files"

echo ""
echo "🚀 Now you can deploy with:"
echo "   helm upgrade langflow-app ./helm -f values-dev.yaml"
echo "   kubectl rollout restart deployment langflow-app-pipelines"
