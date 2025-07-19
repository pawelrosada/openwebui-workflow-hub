#!/bin/bash
# setup-pre-commit.sh - Setup script for pre-commit hooks with Trivy and validation

echo "🔧 Setting up pre-commit hooks with Trivy and validation..."

# Install pre-commit if not already installed
if ! command -v pre-commit &> /dev/null; then
    echo "Installing pre-commit..."
    pip install pre-commit
fi

# Install Trivy if not available
if ! command -v trivy &> /dev/null; then
    echo "Installing Trivy..."
    curl -sfL https://raw.githubusercontent.com/aquasecurity/trivy/main/contrib/install.sh | sh -s -- -b /usr/local/bin latest
fi

# Install pre-commit hooks
echo "Installing pre-commit hooks..."
pre-commit install

# Run initial validation
echo "Running initial validation..."
pre-commit run --all-files

echo "✅ Pre-commit setup complete!"
echo "All commits will now be automatically validated with:"
echo "  - Python formatting (black)"
echo "  - Python linting (flake8)" 
echo "  - JSON formatting (prettier)"
echo "  - Shell script validation (shellcheck)"
echo "  - Security scanning (Trivy)"