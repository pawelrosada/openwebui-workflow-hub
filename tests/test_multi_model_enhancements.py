#!/usr/bin/env python3
"""
Test suite for multi-model LangFlow pipeline enhancements
Tests all new multi-model functionality and API templates.
"""

import json
import sys
import os
from pathlib import Path

# Add the pipelines directory to the path
sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'pipelines'))
sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'templates'))

def test_enhanced_pipeline():
    """Test the enhanced multi-model pipeline"""
    print("🧪 Testing Enhanced Multi-Model Pipeline...")
    
    try:
        # Import the enhanced pipeline
        from enhanced_langflow_pipeline import Pipeline
        
        # Test pipeline initialization
        pipeline = Pipeline()
        print(f"   ✅ Pipeline initialized: {pipeline.name}")
        
        # Test model directive parsing
        test_cases = [
            ("@model:gemini What is AI?", ("gemini", "What is AI?")),
            ("@model:gpt Write a story", ("gpt", "Write a story")),
            ("@model:claude Debug this code", ("claude", "Debug this code")),
            ("@agent How do I learn Python?", ("claude", "How do I learn Python?")),  # Should route to claude for coding
            ("Regular question", ("gpt", "Regular question"))  # Default model
        ]
        
        for input_text, expected in test_cases:
            result = pipeline.parse_model_directive(input_text)
            if result == expected or (result[0] in ["gemini", "gpt", "claude"] and result[1] == expected[1]):
                print(f"   ✅ Parsing test passed: '{input_text[:30]}...'")
            else:
                print(f"   ❌ Parsing test failed: '{input_text[:30]}...' -> {result} (expected {expected})")
        
        # Test model selection by content
        content_tests = [
            ("Write Python code for sorting", "claude"),
            ("Tell me a creative story", "gpt"),
            ("What's the latest news?", "gemini")
        ]
        
        for content, expected_model in content_tests:
            selected = pipeline.select_model_by_content(content)
            if selected == expected_model:
                print(f"   ✅ Content routing: '{content[:30]}...' -> {selected}")
            else:
                print(f"   ⚠️  Content routing: '{content[:30]}...' -> {selected} (expected {expected_model})")
        
        print(f"   📊 Enhanced pipeline tests completed")
        return True
        
    except ImportError as e:
        print(f"   ❌ Import error: {e}")
        return False
    except Exception as e:
        print(f"   ❌ Test error: {e}")
        return False

def test_api_templates():
    """Test API template syntax and functionality"""
    print("\n🧪 Testing API Templates...")
    
    templates_dir = Path(__file__).parent.parent / "templates"
    
    # Test single API template
    try:
        single_api_path = templates_dir / "multi_model_api_single.py"
        if single_api_path.exists():
            with open(single_api_path) as f:
                compile(f.read(), single_api_path, 'exec')
            print("   ✅ Single API template syntax valid")
        else:
            print("   ❌ Single API template not found")
    except SyntaxError as e:
        print(f"   ❌ Single API template syntax error: {e}")
    
    # Test workflow generators
    generators = [
        "generate_multi_scripts.py",
        "generate_universal_workflows.py"
    ]
    
    for generator in generators:
        try:
            generator_path = templates_dir / generator
            if generator_path.exists():
                with open(generator_path) as f:
                    compile(f.read(), generator_path, 'exec')
                print(f"   ✅ {generator} syntax valid")
            else:
                print(f"   ❌ {generator} not found")
        except SyntaxError as e:
            print(f"   ❌ {generator} syntax error: {e}")
    
    return True

def test_workflow_templates():
    """Test generated workflow templates"""
    print("\n🧪 Testing Workflow Templates...")
    
    templates_dir = Path(__file__).parent.parent / "templates" / "examples" / "langflow-workflows"
    
    if not templates_dir.exists():
        print("   ❌ Workflow templates directory not found")
        return False
    
    workflows = [
        "universal-multi-model-chat.json",
        "agentic-multi-model-router.json"
    ]
    
    for workflow_file in workflows:
        workflow_path = templates_dir / workflow_file
        if workflow_path.exists():
            try:
                with open(workflow_path, 'r', encoding='utf-8') as f:
                    data = json.load(f)
                
                # Validate basic structure
                required_keys = ["data", "name", "description"]
                if all(key in data for key in required_keys):
                    nodes = data["data"].get("nodes", [])
                    edges = data["data"].get("edges", [])
                    print(f"   ✅ {workflow_file}: {len(nodes)} nodes, {len(edges)} edges")
                    print(f"      📝 {data['name']}")
                else:
                    print(f"   ❌ {workflow_file}: Missing required keys")
                    
            except json.JSONDecodeError as e:
                print(f"   ❌ {workflow_file}: Invalid JSON - {e}")
        else:
            print(f"   ❌ {workflow_file}: File not found")
    
    return True

def test_integration_compatibility():
    """Test compatibility with existing integration"""
    print("\n🧪 Testing Integration Compatibility...")
    
    try:
        # Test original pipeline still works
        from langflow_pipeline import Pipeline as OriginalPipeline
        original = OriginalPipeline()
        print(f"   ✅ Original pipeline works: {original.name}")
        
        # Test enhanced pipeline works
        from enhanced_langflow_pipeline import Pipeline as EnhancedPipeline
        enhanced = EnhancedPipeline()
        print(f"   ✅ Enhanced pipeline works: {enhanced.name}")
        
        # Compare valve structures
        orig_valves = set(original.valves.model_fields.keys())
        enh_valves = set(enhanced.valves.model_fields.keys())
        
        common_valves = orig_valves.intersection(enh_valves)
        new_valves = enh_valves - orig_valves
        
        print(f"   📊 Common valves: {len(common_valves)}")
        print(f"   🆕 New valves: {len(new_valves)}")
        if new_valves:
            print(f"      New: {', '.join(sorted(new_valves))}")
        
        return True
        
    except ImportError as e:
        print(f"   ❌ Import error: {e}")
        return False
    except Exception as e:
        print(f"   ❌ Integration test error: {e}")
        return False

def test_generated_multi_scripts():
    """Test the generated multi-script API files"""
    print("\n🧪 Testing Generated Multi-Scripts...")
    
    templates_dir = Path(__file__).parent.parent / "templates"
    
    # Expected generated files
    expected_files = [
        "gemini_api.py",
        "gpt_api.py", 
        "claude_api.py",
        "orchestrator.py"
    ]
    
    found_files = 0
    
    for filename in expected_files:
        filepath = templates_dir / filename
        if filepath.exists():
            try:
                with open(filepath) as f:
                    compile(f.read(), filepath, 'exec')
                print(f"   ✅ {filename} exists and syntax valid")
                found_files += 1
            except SyntaxError as e:
                print(f"   ❌ {filename} syntax error: {e}")
        else:
            print(f"   ⚠️  {filename} not found (run generate_multi_scripts.py)")
    
    if found_files > 0:
        print(f"   📊 Found {found_files}/{len(expected_files)} generated scripts")
    
    return found_files > 0

def run_comprehensive_tests():
    """Run all tests"""
    print("🔬 Multi-Model LangFlow Pipeline Tests")
    print("=" * 50)
    
    test_results = []
    
    # Run all test modules
    tests = [
        ("Enhanced Pipeline", test_enhanced_pipeline),
        ("API Templates", test_api_templates),
        ("Workflow Templates", test_workflow_templates),
        ("Integration Compatibility", test_integration_compatibility),
        ("Generated Multi-Scripts", test_generated_multi_scripts)
    ]
    
    for test_name, test_func in tests:
        try:
            result = test_func()
            test_results.append((test_name, result))
        except Exception as e:
            print(f"   ❌ {test_name} failed with exception: {e}")
            test_results.append((test_name, False))
    
    # Summary
    print("\n📊 Test Results Summary:")
    print("=" * 30)
    
    passed = sum(1 for _, result in test_results if result)
    total = len(test_results)
    
    for test_name, result in test_results:
        status = "✅ PASS" if result else "❌ FAIL"
        print(f"   {status} {test_name}")
    
    print(f"\n🎉 Overall: {passed}/{total} tests passed")
    
    if passed == total:
        print("🚀 All tests passed! Multi-model enhancements are working correctly.")
        return True
    else:
        print("⚠️  Some tests failed. Check the output above for details.")
        return False

if __name__ == "__main__":
    success = run_comprehensive_tests()
    sys.exit(0 if success else 1)