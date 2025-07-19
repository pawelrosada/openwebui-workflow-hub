#!/usr/bin/env python3
"""
Test script for LangFlow workflow examples.

Validates the JSON structure and required components of the workflow files.
"""

import json
import os
from pathlib import Path

def validate_workflow(workflow_data, filename):
    """Validate a workflow JSON structure"""
    errors = []
    
    # Check required top-level keys
    required_keys = ["data", "description", "name", "last_tested_version"]
    for key in required_keys:
        if key not in workflow_data:
            errors.append(f"Missing required key: {key}")
    
    # Check data structure
    if "data" in workflow_data:
        data = workflow_data["data"]
        if "nodes" not in data:
            errors.append("Missing 'nodes' in data")
        if "edges" not in data:
            errors.append("Missing 'edges' in data")
        
        # Validate nodes
        if "nodes" in data:
            nodes = data["nodes"]
            if len(nodes) != 3:
                errors.append(f"Expected 3 nodes, found {len(nodes)}")
            
            # Check for required node types
            node_types = [node.get("type") for node in nodes]
            if "ChatInput" not in node_types:
                errors.append("Missing ChatInput node")
            if "ChatOutput" not in node_types:
                errors.append("Missing ChatOutput node")
            
            # Check for AI model node
            ai_types = ["GoogleAI", "OpenAI", "Anthropic"]
            has_ai_model = any(ai_type in node_types for ai_type in ai_types)
            if not has_ai_model:
                errors.append("Missing AI model node (GoogleAI, OpenAI, or Anthropic)")
        
        # Validate edges
        if "edges" in data:
            edges = data["edges"]
            if len(edges) != 2:
                errors.append(f"Expected 2 edges, found {len(edges)}")
    
    return errors

def test_all_workflows():
    """Test all workflow files in the langflow-workflows directory"""
    
    workflows_dir = Path("examples/langflow-workflows")
    
    if not workflows_dir.exists():
        print(f"❌ Directory not found: {workflows_dir}")
        return False
    
    workflow_files = list(workflows_dir.glob("*.json"))
    
    if not workflow_files:
        print(f"❌ No JSON files found in {workflows_dir}")
        return False
    
    print(f"🔍 Testing {len(workflow_files)} workflow files...\n")
    
    all_passed = True
    
    for workflow_file in workflow_files:
        print(f"📄 Testing {workflow_file.name}...")
        
        try:
            with open(workflow_file, 'r', encoding='utf-8') as f:
                workflow_data = json.load(f)
            
            errors = validate_workflow(workflow_data, workflow_file.name)
            
            if errors:
                print(f"❌ {workflow_file.name} - FAILED")
                for error in errors:
                    print(f"   • {error}")
                all_passed = False
            else:
                print(f"✅ {workflow_file.name} - PASSED")
                
                # Print basic info
                name = workflow_data.get("name", "Unknown")
                description = workflow_data.get("description", "No description")
                node_count = len(workflow_data.get("data", {}).get("nodes", []))
                print(f"   📝 Name: {name}")
                print(f"   📋 Description: {description[:80]}{'...' if len(description) > 80 else ''}")
                print(f"   🔗 Nodes: {node_count}")
        
        except json.JSONDecodeError as e:
            print(f"❌ {workflow_file.name} - JSON ERROR: {e}")
            all_passed = False
        except Exception as e:
            print(f"❌ {workflow_file.name} - ERROR: {e}")
            all_passed = False
        
        print()
    
    return all_passed

def main():
    """Main test function"""
    
    print("🧪 LangFlow Workflow Examples - Validation Test")
    print("=" * 50)
    
    # Change to repository root
    os.chdir(Path(__file__).parent.parent)
    
    success = test_all_workflows()
    
    if success:
        print("🎉 All tests PASSED! Workflows are ready to use.")
        return 0
    else:
        print("💥 Some tests FAILED! Please check the issues above.")
        return 1

if __name__ == "__main__":
    exit(main())