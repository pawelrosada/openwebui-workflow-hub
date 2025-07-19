#!/usr/bin/env python3
"""
Universal Multi-Model Workflow Generator
Creates LangFlow workflows that can dynamically handle multiple AI models.

Generates JSON workflows for:
1. Universal Multi-Model Chat - Single workflow that can switch between models
2. Agentic Multi-Model Flow - Workflow that routes based on input type  
3. RAG Multi-Model Pipeline - Retrieval-Augmented Generation with model selection

These workflows are UI-friendly and can be imported into LangFlow for visual editing.
"""

import json
import os
from typing import Dict, Any, List

def create_base_universal_workflow() -> Dict[str, Any]:
    """Create base structure for universal workflows"""
    return {
        "data": {
            "nodes": [],
            "edges": []
        },
        "description": "",
        "name": "",
        "last_tested_version": "1.0.0"
    }

def create_model_selector_node() -> Dict[str, Any]:
    """Create a model selector component node"""
    return {
        "id": "ModelSelector-1",
        "type": "DropdownInput", 
        "position": {"x": 200, "y": 100},
        "data": {
            "type": "DropdownInput",
            "node": {
                "template": {
                    "value": {
                        "required": True,
                        "placeholder": "",
                        "show": True,
                        "multiline": False,
                        "value": "gpt",
                        "password": False,
                        "name": "value",
                        "display_name": "Select Model",
                        "type": "str",
                        "info": "Choose AI model for this conversation",
                        "list": False,
                        "options": ["gemini", "gpt", "claude"]
                    }
                },
                "description": "Dropdown to select AI model dynamically.",
                "base_classes": ["str"],
                "display_name": "Model Selector",
                "documentation": "",
                "custom_fields": {},
                "output_types": ["str"]
            }
        }
    }

def create_conditional_router_node() -> Dict[str, Any]:
    """Create a conditional router that selects model based on input"""
    return {
        "id": "ConditionalRouter-1",
        "type": "ConditionalRouter",
        "position": {"x": 400, "y": 200},
        "data": {
            "type": "ConditionalRouter", 
            "node": {
                "template": {
                    "input_text": {
                        "dynamic": True,
                        "required": True,
                        "placeholder": "",
                        "show": True,
                        "multiline": True,
                        "value": "",
                        "password": False,
                        "name": "input_text",
                        "display_name": "Input Text",
                        "type": "str",
                        "info": "Text to analyze for model routing",
                        "list": False
                    },
                    "routing_logic": {
                        "required": True,
                        "placeholder": "",
                        "show": True,
                        "multiline": True,
                        "value": """# Simple model routing logic
if any(word in input_text.lower() for word in ['code', 'programming', 'python', 'javascript']):
    return 'claude'  # Claude for coding
elif any(word in input_text.lower() for word in ['creative', 'story', 'poem', 'writing']):
    return 'gpt'  # GPT for creative tasks  
elif any(word in input_text.lower() for word in ['search', 'current', 'recent', 'google']):
    return 'gemini'  # Gemini for search-like queries
else:
    return 'gpt'  # Default to GPT""",
                        "password": False,
                        "name": "routing_logic",
                        "display_name": "Routing Logic",
                        "type": "code",
                        "info": "Python code to determine model selection",
                        "list": False
                    }
                },
                "description": "Routes input to appropriate model based on content analysis.",
                "base_classes": ["str"],
                "display_name": "Conditional Router",
                "documentation": "",
                "custom_fields": {},
                "output_types": ["str"]
            }
        }
    }

def create_multi_model_node(model_name: str, position: Dict[str, int]) -> Dict[str, Any]:
    """Create a conditional model node that activates based on selection"""
    
    model_configs = {
        "gemini": {
            "type": "GoogleAI",
            "model": "gemini-2.5-flash",
            "api_key_field": "google_api_key",
            "display_name": "Google Gemini"
        },
        "gpt": {
            "type": "OpenAI",
            "model": "gpt-4o",
            "api_key_field": "openai_api_key", 
            "display_name": "OpenAI GPT"
        },
        "claude": {
            "type": "Anthropic",
            "model": "claude-3-5-sonnet-20241022",
            "api_key_field": "anthropic_api_key",
            "display_name": "Anthropic Claude"
        }
    }
    
    config = model_configs[model_name]
    node_id = f"{config['type']}-Multi-{model_name.capitalize()}-1"
    
    return {
        "id": node_id,
        "type": config["type"],
        "position": position,
        "data": {
            "type": config["type"],
            "node": {
                "template": {
                    config["api_key_field"]: {
                        "required": True,
                        "placeholder": "",
                        "show": True,
                        "multiline": False,
                        "value": "",
                        "password": True,
                        "name": config["api_key_field"],
                        "display_name": f"{config['display_name']} API Key",
                        "type": "str",
                        "info": f"Enter your {config['display_name']} API key",
                        "list": False
                    },
                    "model": {
                        "required": True,
                        "placeholder": "",
                        "show": True,
                        "multiline": False,
                        "value": config["model"],
                        "password": False,
                        "name": "model",
                        "display_name": "Model",
                        "type": "str",
                        "info": f"{config['display_name']} model to use",
                        "list": False
                    },
                    "temperature": {
                        "required": False,
                        "placeholder": "",
                        "show": True,
                        "multiline": False,
                        "value": 0.7,
                        "password": False,
                        "name": "temperature",
                        "display_name": "Temperature",
                        "type": "float",
                        "info": "Controls randomness in responses",
                        "list": False
                    },
                    "input_value": {
                        "dynamic": True,
                        "required": True,
                        "placeholder": "",
                        "show": True,
                        "multiline": True,
                        "value": "",
                        "password": False,
                        "name": "input_value",
                        "display_name": "Input",
                        "type": "str",
                        "info": "",
                        "list": False
                    },
                    "active_condition": {
                        "required": False,
                        "placeholder": "",
                        "show": True,
                        "multiline": False,
                        "value": f"model_selection == '{model_name}'",
                        "password": False,
                        "name": "active_condition",
                        "display_name": "Activation Condition",
                        "type": "str",
                        "info": f"Condition to activate {config['display_name']}",
                        "list": False
                    }
                },
                "description": f"{config['display_name']} node with conditional activation.",
                "base_classes": ["BaseLanguageModel", "LanguageModel"],
                "display_name": f"{config['display_name']} (Multi)",
                "documentation": "",
                "custom_fields": {},
                "output_types": ["Message"]
            }
        }
    }

def create_output_merger_node() -> Dict[str, Any]:
    """Create node that merges outputs from multiple models"""
    return {
        "id": "OutputMerger-1",
        "type": "OutputMerger",
        "position": {"x": 900, "y": 200},
        "data": {
            "type": "OutputMerger",
            "node": {
                "template": {
                    "gemini_output": {
                        "dynamic": True,
                        "required": False,
                        "placeholder": "",
                        "show": True,
                        "multiline": True,
                        "value": "",
                        "password": False,
                        "name": "gemini_output",
                        "display_name": "Gemini Output",
                        "type": "str",
                        "info": "Output from Gemini model",
                        "list": False
                    },
                    "gpt_output": {
                        "dynamic": True,
                        "required": False,
                        "placeholder": "",
                        "show": True,
                        "multiline": True,
                        "value": "",
                        "password": False,
                        "name": "gpt_output",
                        "display_name": "GPT Output", 
                        "type": "str",
                        "info": "Output from GPT model",
                        "list": False
                    },
                    "claude_output": {
                        "dynamic": True,
                        "required": False,
                        "placeholder": "",
                        "show": True,
                        "multiline": True,
                        "value": "",
                        "password": False,
                        "name": "claude_output",
                        "display_name": "Claude Output",
                        "type": "str",
                        "info": "Output from Claude model",
                        "list": False
                    }
                },
                "description": "Merges outputs from multiple models into single response.",
                "base_classes": ["Message"],
                "display_name": "Output Merger",
                "documentation": "",
                "custom_fields": {},
                "output_types": ["Message"]
            }
        }
    }

def generate_universal_multi_model_workflow() -> Dict[str, Any]:
    """Generate universal workflow that can handle multiple models"""
    
    workflow = create_base_universal_workflow()
    workflow["name"] = "Universal Multi-Model Chat"
    workflow["description"] = "Universal chat workflow with dynamic model selection. Choose between Gemini, GPT-4o, and Claude in a single flow. Perfect for testing different models with the same input."
    
    # Add nodes
    workflow["data"]["nodes"] = [
        {
            "id": "ChatInput-1",
            "type": "ChatInput",
            "position": {"x": 100, "y": 200},
            "data": {
                "type": "ChatInput",
                "node": {
                    "template": {
                        "input_value": {
                            "dynamic": True,
                            "required": True,
                            "placeholder": "",
                            "show": True,
                            "multiline": True,
                            "value": "",
                            "password": False,
                            "name": "input_value",
                            "display_name": "Chat Input",
                            "type": "str",
                            "info": "",
                            "list": False
                        }
                    },
                    "description": "A chat input component for user messages.",
                    "base_classes": ["Message"],
                    "display_name": "Chat Input",
                    "documentation": "",
                    "custom_fields": {},
                    "output_types": ["Message"]
                }
            }
        },
        create_model_selector_node(),
        create_multi_model_node("gemini", {"x": 500, "y": 100}),
        create_multi_model_node("gpt", {"x": 500, "y": 200}),
        create_multi_model_node("claude", {"x": 500, "y": 300}),
        create_output_merger_node(),
        {
            "id": "ChatOutput-1",
            "type": "ChatOutput",
            "position": {"x": 1100, "y": 200},
            "data": {
                "type": "ChatOutput",
                "node": {
                    "template": {
                        "input_value": {
                            "dynamic": True,
                            "required": True,
                            "placeholder": "",
                            "show": True,
                            "multiline": True,
                            "value": "",
                            "password": False,
                            "name": "input_value",
                            "display_name": "Text",
                            "type": "str",
                            "info": "",
                            "list": False
                        }
                    },
                    "description": "A chat output component for AI responses.",
                    "base_classes": ["Message"],
                    "display_name": "Chat Output",
                    "documentation": "",
                    "custom_fields": {},
                    "output_types": ["Message"]
                }
            }
        }
    ]
    
    # Create edges - simplified for demo
    workflow["data"]["edges"] = [
        {
            "source": "ChatInput-1",
            "target": "GoogleAI-Multi-Gemini-1",
            "data": {"connection": "input_to_gemini"},
            "id": "edge-input-gemini"
        },
        {
            "source": "ChatInput-1", 
            "target": "OpenAI-Multi-Gpt-1",
            "data": {"connection": "input_to_gpt"},
            "id": "edge-input-gpt"
        },
        {
            "source": "ChatInput-1",
            "target": "Anthropic-Multi-Claude-1",
            "data": {"connection": "input_to_claude"},
            "id": "edge-input-claude"
        },
        {
            "source": "OutputMerger-1",
            "target": "ChatOutput-1",
            "data": {"connection": "merger_to_output"},
            "id": "edge-merger-output"
        }
    ]
    
    return workflow

def generate_agentic_workflow() -> Dict[str, Any]:
    """Generate agentic workflow with automatic model routing"""
    
    workflow = create_base_universal_workflow()
    workflow["name"] = "Agentic Multi-Model Router"
    workflow["description"] = "Smart agentic workflow that automatically routes queries to the most suitable AI model based on content analysis. Coding questions → Claude, Creative tasks → GPT-4o, Search queries → Gemini."
    
    workflow["data"]["nodes"] = [
        {
            "id": "ChatInput-1",
            "type": "ChatInput", 
            "position": {"x": 100, "y": 200},
            "data": {
                "type": "ChatInput",
                "node": {
                    "template": {
                        "input_value": {
                            "dynamic": True,
                            "required": True,
                            "placeholder": "Ask anything - I'll route to the best AI model automatically!",
                            "show": True,
                            "multiline": True,
                            "value": "",
                            "password": False,
                            "name": "input_value",
                            "display_name": "Chat Input",
                            "type": "str",
                            "info": "Type your question - will be automatically routed to best model",
                            "list": False
                        }
                    },
                    "description": "Smart chat input with automatic model routing.",
                    "base_classes": ["Message"],
                    "display_name": "Smart Chat Input",
                    "documentation": "",
                    "custom_fields": {},
                    "output_types": ["Message"]
                }
            }
        },
        create_conditional_router_node(),
        create_multi_model_node("gemini", {"x": 600, "y": 100}),
        create_multi_model_node("gpt", {"x": 600, "y": 200}),
        create_multi_model_node("claude", {"x": 600, "y": 300}),
        create_output_merger_node(),
        {
            "id": "ChatOutput-1",
            "type": "ChatOutput",
            "position": {"x": 1100, "y": 200},
            "data": {
                "type": "ChatOutput",
                "node": {
                    "template": {
                        "input_value": {
                            "dynamic": True,
                            "required": True,
                            "placeholder": "",
                            "show": True,
                            "multiline": True,
                            "value": "",
                            "password": False,
                            "name": "input_value",
                            "display_name": "Smart Response",
                            "type": "str",
                            "info": "Response from automatically selected model",
                            "list": False
                        }
                    },
                    "description": "Output showing which model was selected and the response.",
                    "base_classes": ["Message"],
                    "display_name": "Smart Chat Output",
                    "documentation": "",
                    "custom_fields": {},
                    "output_types": ["Message"]
                }
            }
        }
    ]
    
    workflow["data"]["edges"] = [
        {
            "source": "ChatInput-1",
            "target": "ConditionalRouter-1", 
            "data": {"connection": "input_to_router"},
            "id": "edge-input-router"
        },
        {
            "source": "ConditionalRouter-1",
            "target": "OutputMerger-1",
            "data": {"connection": "router_to_merger"},
            "id": "edge-router-merger"
        },
        {
            "source": "OutputMerger-1",
            "target": "ChatOutput-1",
            "data": {"connection": "merger_to_output"},
            "id": "edge-merger-output"
        }
    ]
    
    return workflow

def save_workflow(workflow: Dict[str, Any], filename: str, output_dir: str = "examples/langflow-workflows"):
    """Save workflow to file"""
    
    os.makedirs(output_dir, exist_ok=True)
    filepath = os.path.join(output_dir, filename)
    
    with open(filepath, 'w', encoding='utf-8') as f:
        json.dump(workflow, f, indent=2, ensure_ascii=False)
    
    print(f"Generated universal workflow: {filepath}")

def main():
    """Generate all universal workflow templates"""
    
    print("🔧 Generating universal multi-model LangFlow workflows...")
    
    # Generate workflows
    workflows = [
        (generate_universal_multi_model_workflow(), "universal-multi-model-chat.json"),
        (generate_agentic_workflow(), "agentic-multi-model-router.json")
    ]
    
    for workflow, filename in workflows:
        save_workflow(workflow, filename)
    
    print(f"\\n✅ Generated {len(workflows)} universal workflow templates")
    print("\\n📁 Files created:")
    print("   • universal-multi-model-chat.json - Manual model selection")  
    print("   • agentic-multi-model-router.json - Automatic model routing")
    print("\\n🚀 Import these into LangFlow for visual editing!")
    print("📖 Each workflow supports dynamic model switching in a single flow")

if __name__ == "__main__":
    main()