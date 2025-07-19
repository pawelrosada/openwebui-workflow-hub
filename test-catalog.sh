#!/bin/bash

# Test script for Langflow AI Catalog Examples
# This script validates the catalog structure and examples

echo "🧪 Testing Langflow AI Catalog..."

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Test counters
TESTS=0
PASSED=0

run_test() {
    local test_name="$1"
    local command="$2"
    TESTS=$((TESTS + 1))
    
    echo -e "${BLUE}[TEST $TESTS]${NC} $test_name"
    
    if eval "$command"; then
        echo -e "${GREEN}✅ PASSED${NC}: $test_name"
        PASSED=$((PASSED + 1))
    else
        echo -e "${RED}❌ FAILED${NC}: $test_name"
    fi
    echo
}

# Test 1: Check catalog structure
run_test "Catalog directory structure exists" "
    [ -d 'catalog' ] && 
    [ -d 'catalog/flows' ] && 
    [ -d 'catalog/pipelines' ] &&
    [ -f 'catalog/README.md' ] &&
    [ -f 'catalog/QUICKSTART.md' ]
"

# Test 2: Check Langflow JSON files
run_test "All Langflow JSON files exist and are valid" "
    [ -f 'catalog/flows/gemini-chat-basic.json' ] &&
    [ -f 'catalog/flows/gpt4-chat-basic.json' ] &&
    [ -f 'catalog/flows/claude3-chat-basic.json' ] &&
    python3 -c '
import json
files = [\"catalog/flows/gemini-chat-basic.json\", \"catalog/flows/gpt4-chat-basic.json\", \"catalog/flows/claude3-chat-basic.json\"]
for f in files:
    with open(f, \"r\") as file:
        data = json.load(file)
        assert \"data\" in data, f\"Missing data in {f}\"
        assert \"nodes\" in data[\"data\"], f\"Missing nodes in {f}\"
        assert \"edges\" in data[\"data\"], f\"Missing edges in {f}\"
        assert len(data[\"data\"][\"nodes\"]) >= 3, f\"Need at least 3 nodes in {f}\"
        assert \"name\" in data, f\"Missing name in {f}\"
        assert \"description\" in data, f\"Missing description in {f}\"
'
"

# Test 3: Check pipeline Python files
run_test "All pipeline Python files exist and compile" "
    [ -f 'catalog/pipelines/gemini_chat_pipeline.py' ] &&
    [ -f 'catalog/pipelines/gpt4_chat_pipeline.py' ] &&
    [ -f 'catalog/pipelines/claude_chat_pipeline.py' ] &&
    python3 -m py_compile catalog/pipelines/gemini_chat_pipeline.py &&
    python3 -m py_compile catalog/pipelines/gpt4_chat_pipeline.py &&
    python3 -m py_compile catalog/pipelines/claude_chat_pipeline.py
"

# Test 4: Check pipeline structure
run_test "Pipeline files have required structure" "
    python3 -c '
import sys
sys.path.append(\"catalog/pipelines\")

files = [\"gemini_chat_pipeline\", \"gpt4_chat_pipeline\", \"claude_chat_pipeline\"]
for module_name in files:
    module = __import__(module_name)
    assert hasattr(module, \"Pipeline\"), f\"Missing Pipeline class in {module_name}\"
    pipeline_class = getattr(module, \"Pipeline\")
    
    # Check if Pipeline class has required attributes
    pipeline = pipeline_class()
    assert hasattr(pipeline, \"name\"), f\"Missing name attribute in {module_name}\"
    assert hasattr(pipeline, \"valves\"), f\"Missing valves attribute in {module_name}\"
    assert hasattr(pipeline, \"pipe\"), f\"Missing pipe method in {module_name}\"
    
    # Check valves structure
    assert hasattr(pipeline.valves, \"LANGFLOW_BASE_URL\"), f\"Missing LANGFLOW_BASE_URL in {module_name}\"
    assert hasattr(pipeline.valves, \"WORKFLOW_ID\"), f\"Missing WORKFLOW_ID in {module_name}\"
'
"

# Test 5: Check Docker configuration
run_test "Docker Compose configuration is valid" "
    docker compose config --quiet
"

# Test 6: Check if existing pipelines still work
run_test "Existing pipeline files are not broken" "
    [ -f 'pipelines/langflow_pipeline.py' ] &&
    python3 -m py_compile pipelines/langflow_pipeline.py
"

# Test 7: Check documentation completeness
run_test "Documentation files are complete" "
    grep -q 'Gemini' catalog/README.md &&
    grep -q 'GPT-4' catalog/README.md &&
    grep -q 'Claude' catalog/README.md &&
    grep -q 'Szybkie Wdrożenie' catalog/QUICKSTART.md &&
    grep -q 'catalog' README.md
"

# Summary
echo "🏁 Test Summary"
echo "==============="
echo -e "Total Tests: ${BLUE}$TESTS${NC}"
echo -e "Passed:      ${GREEN}$PASSED${NC}"
echo -e "Failed:      ${RED}$((TESTS - PASSED))${NC}"

if [ $PASSED -eq $TESTS ]; then
    echo -e "${GREEN}🎉 All tests passed! Catalog is ready to use.${NC}"
    exit 0
else
    echo -e "${RED}❌ Some tests failed. Please check the output above.${NC}"
    exit 1
fi