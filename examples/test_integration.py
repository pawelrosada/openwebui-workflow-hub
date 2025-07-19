#!/usr/bin/env python3
"""
Integration test for the LangFlow pipeline and examples.

Tests that the pipeline can load and validate the example workflows.
"""

import json
import sys
import os
from pathlib import Path

# Add pipelines directory to path so we can import the pipeline
sys.path.insert(0, str(Path(__file__).parent.parent / "pipelines"))

def test_pipeline_import():
    """Test that the pipeline module can be imported"""
    try:
        from langflow_pipeline import Pipeline
        print("✅ Pipeline module imported successfully")
        return True
    except ImportError as e:
        print(f"❌ Failed to import pipeline: {e}")
        return False

def test_pipeline_initialization():
    """Test that the pipeline can be initialized"""
    try:
        from langflow_pipeline import Pipeline
        pipeline = Pipeline()
        print(f"✅ Pipeline initialized: {pipeline.name}")
        print(f"   Base URL: {pipeline.valves.LANGFLOW_BASE_URL}")
        print(f"   Workflow ID: {pipeline.valves.WORKFLOW_ID}")
        print(f"   Rate limit: {pipeline.valves.RATE_LIMIT}")
        return True
    except Exception as e:
        print(f"❌ Failed to initialize pipeline: {e}")
        return False

def test_workflow_examples():
    """Test that workflow examples exist and are valid"""
    examples_dir = Path("examples/langflow-workflows")
    
    if not examples_dir.exists():
        print(f"❌ Examples directory not found: {examples_dir}")
        return False
    
    json_files = list(examples_dir.glob("*.json"))
    
    if len(json_files) < 3:
        print(f"❌ Expected at least 3 workflow files, found {len(json_files)}")
        return False
    
    print(f"✅ Found {len(json_files)} workflow examples:")
    for json_file in json_files:
        try:
            with open(json_file, 'r') as f:
                data = json.load(f)
            name = data.get('name', 'Unknown')
            print(f"   • {json_file.name}: {name}")
        except Exception as e:
            print(f"   ❌ {json_file.name}: ERROR - {e}")
            return False
    
    return True

def main():
    """Run all integration tests"""
    
    print("🔧 LangFlow Integration Tests")
    print("=" * 40)
    
    # Change to repository root
    os.chdir(Path(__file__).parent.parent)
    
    tests = [
        ("Pipeline Import", test_pipeline_import),
        ("Pipeline Initialization", test_pipeline_initialization), 
        ("Workflow Examples", test_workflow_examples)
    ]
    
    passed = 0
    total = len(tests)
    
    for test_name, test_func in tests:
        print(f"\n🧪 Testing {test_name}...")
        try:
            if test_func():
                passed += 1
            else:
                print(f"❌ {test_name} failed")
        except Exception as e:
            print(f"❌ {test_name} crashed: {e}")
    
    print(f"\n📊 Results: {passed}/{total} tests passed")
    
    if passed == total:
        print("🎉 All integration tests PASSED!")
        return 0
    else:
        print("💥 Some integration tests FAILED!")
        return 1

if __name__ == "__main__":
    exit(main())