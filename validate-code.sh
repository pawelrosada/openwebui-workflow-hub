#!/bin/bash
# validate-code.sh - Basic code validation that works without network dependencies

set -e

echo "Running basic code validation..."

# Check Python syntax
echo "Checking Python syntax..."
find . -name "*.py" -not -path "./.*" -not -path "./build/*" -not -path "./dist/*" | while read -r file; do
    echo "Checking: $file"
    python -m py_compile "$file" || { echo "Syntax error in $file"; exit 1; }
done

# Check JSON syntax
echo "Checking JSON syntax..."
find . -name "*.json" -not -path "./.*" -not -path "./build/*" -not -path "./dist/*" | while read -r file; do
    echo "Checking: $file"
    python -m json.tool "$file" > /dev/null || { echo "JSON syntax error in $file"; exit 1; }
done

# Check YAML syntax (if PyYAML is available)
echo "Checking YAML syntax..."
find . -name "*.yml" -o -name "*.yaml" | while read -r file; do
    if [[ "$file" != ./.*/* ]]; then
        echo "Checking: $file"
        python -c "import yaml; yaml.safe_load(open('$file'))" 2>/dev/null || { echo "YAML syntax error in $file"; exit 1; }
    fi
done

# Check shell scripts with shellcheck if available
if command -v shellcheck >/dev/null 2>&1; then
    echo "Checking shell scripts..."
    find . -name "*.sh" -not -path "./.*" | while read -r file; do
        echo "Checking: $file"
        shellcheck -e SC2034 "$file" || { echo "Shellcheck issues in $file"; }
    done
else
    echo "Shellcheck not available, skipping shell script validation"
fi

echo "Basic validation completed successfully"