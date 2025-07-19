#!/usr/bin/env python3
"""
LangFlow Workflow Generator

Simple script to generate basic LangFlow AI integration workflows.
Creates minimal "Chat Input → AI Model → Chat Output" flows for different providers.

Usage:
    python generate_workflows.py [provider]
    
Providers: gemini, openai, anthropic, all
"""

import json
import os
from typing import Dict, Any

def create_base_workflow_template() -> Dict[str, Any]:
    """Create the base workflow structure"""
    return {
        "data": {
            "nodes": [],
            "edges": []
        },
        "description": "",
        "name": "",
        "last_tested_version": "1.0.0"
    }

def create_chat_input_node() -> Dict[str, Any]:
    """Create a chat input node"""
    return {
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
    }

def create_chat_output_node() -> Dict[str, Any]:
    """Create a chat output node"""
    return {
        "id": "ChatOutput-1",
        "type": "ChatOutput",
        "position": {"x": 700, "y": 200},
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

def create_ai_model_node(provider: str) -> Dict[str, Any]:
    """Create an AI model node for the specified provider"""
    
    if provider == "gemini":
        return {
            "id": "GoogleAI-1",
            "type": "GoogleAI",
            "position": {"x": 400, "y": 200},
            "data": {
                "type": "GoogleAI",
                "node": {
                    "template": {
                        "google_api_key": {
                            "required": True,
                            "placeholder": "",
                            "show": True,
                            "multiline": False,
                            "value": "",
                            "password": True,
                            "name": "google_api_key",
                            "display_name": "Google API Key",
                            "type": "str",
                            "info": "Enter your Google AI API key here",
                            "list": False
                        },
                        "model": {
                            "required": True,
                            "placeholder": "",
                            "show": True,
                            "multiline": False,
                            "value": "gemini-2.5-flash",
                            "password": False,
                            "name": "model",
                            "display_name": "Model",
                            "type": "str",
                            "info": "Google AI model to use",
                            "list": False,
                            "options": ["gemini-2.5-flash", "gemini-pro", "gemini-pro-vision"]
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
                        }
                    },
                    "description": "Google AI LLM component using Gemini models.",
                    "base_classes": ["BaseLanguageModel", "LanguageModel"],
                    "display_name": "Google AI",
                    "documentation": "",
                    "custom_fields": {},
                    "output_types": ["Message"]
                }
            }
        }
    
    elif provider == "openai":
        return {
            "id": "OpenAI-1",
            "type": "OpenAI",
            "position": {"x": 400, "y": 200},
            "data": {
                "type": "OpenAI",
                "node": {
                    "template": {
                        "openai_api_key": {
                            "required": True,
                            "placeholder": "",
                            "show": True,
                            "multiline": False,
                            "value": "",
                            "password": True,
                            "name": "openai_api_key",
                            "display_name": "OpenAI API Key",
                            "type": "str",
                            "info": "Enter your OpenAI API key here",
                            "list": False
                        },
                        "model": {
                            "required": True,
                            "placeholder": "",
                            "show": True,
                            "multiline": False,
                            "value": "gpt-4o",
                            "password": False,
                            "name": "model",
                            "display_name": "Model",
                            "type": "str",
                            "info": "OpenAI model to use",
                            "list": False,
                            "options": ["gpt-4o", "gpt-4o-mini", "gpt-4-turbo", "gpt-3.5-turbo"]
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
                        "max_tokens": {
                            "required": False,
                            "placeholder": "",
                            "show": True,
                            "multiline": False,
                            "value": 1000,
                            "password": False,
                            "name": "max_tokens",
                            "display_name": "Max Tokens",
                            "type": "int",
                            "info": "Maximum number of tokens to generate",
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
                        }
                    },
                    "description": "OpenAI LLM component using GPT models.",
                    "base_classes": ["BaseLanguageModel", "LanguageModel"],
                    "display_name": "OpenAI",
                    "documentation": "",
                    "custom_fields": {},
                    "output_types": ["Message"]
                }
            }
        }
    
    elif provider == "anthropic":
        return {
            "id": "Anthropic-1",
            "type": "Anthropic",
            "position": {"x": 400, "y": 200},
            "data": {
                "type": "Anthropic",
                "node": {
                    "template": {
                        "anthropic_api_key": {
                            "required": True,
                            "placeholder": "",
                            "show": True,
                            "multiline": False,
                            "value": "",
                            "password": True,
                            "name": "anthropic_api_key",
                            "display_name": "Anthropic API Key",
                            "type": "str",
                            "info": "Enter your Anthropic API key here",
                            "list": False
                        },
                        "model": {
                            "required": True,
                            "placeholder": "",
                            "show": True,
                            "multiline": False,
                            "value": "claude-3-5-sonnet-20241022",
                            "password": False,
                            "name": "model",
                            "display_name": "Model",
                            "type": "str",
                            "info": "Anthropic model to use",
                            "list": False,
                            "options": ["claude-3-5-sonnet-20241022", "claude-3-5-haiku-20241022", "claude-3-opus-20240229", "claude-3-haiku-20240307"]
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
                        "max_tokens": {
                            "required": False,
                            "placeholder": "",
                            "show": True,
                            "multiline": False,
                            "value": 1000,
                            "password": False,
                            "name": "max_tokens",
                            "display_name": "Max Tokens",
                            "type": "int",
                            "info": "Maximum number of tokens to generate",
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
                        }
                    },
                    "description": "Anthropic LLM component using Claude models.",
                    "base_classes": ["BaseLanguageModel", "LanguageModel"],
                    "display_name": "Anthropic",
                    "documentation": "",
                    "custom_fields": {},
                    "output_types": ["Message"]
                }
            }
        }

def create_edges(ai_node_id: str) -> list:
    """Create edges connecting the nodes"""
    return [
        {
            "source": "ChatInput-1",
            "sourceHandle": "{œid∶ChatInput-1,outputName∶input_value,type∶str}",
            "target": ai_node_id,
            "targetHandle": f"{{œid∶{ai_node_id},inputName∶input_value,type∶str}}",
            "data": {
                "targetHandle": {
                    "id": ai_node_id,
                    "inputName": "input_value",
                    "type": "str"
                },
                "sourceHandle": {
                    "id": "ChatInput-1",
                    "outputName": "input_value",
                    "type": "str"
                }
            },
            "id": f"reactflow__edge-ChatInput-1{{œid∶ChatInput-1,outputName∶input_value,type∶str}}-{ai_node_id}{{œid∶{ai_node_id},inputName∶input_value,type∶str}}"
        },
        {
            "source": ai_node_id,
            "sourceHandle": f"{{œid∶{ai_node_id},outputName∶text,type∶Message}}",
            "target": "ChatOutput-1",
            "targetHandle": "{œid∶ChatOutput-1,inputName∶input_value,type∶str}",
            "data": {
                "targetHandle": {
                    "id": "ChatOutput-1",
                    "inputName": "input_value",
                    "type": "str"
                },
                "sourceHandle": {
                    "id": ai_node_id,
                    "outputName": "text",
                    "type": "Message"
                }
            },
            "id": f"reactflow__edge-{ai_node_id}{{œid∶{ai_node_id},outputName∶text,type∶Message}}-ChatOutput-1{{œid∶ChatOutput-1,inputName∶input_value,type∶str}}"
        }
    ]

def generate_workflow(provider: str) -> Dict[str, Any]:
    """Generate a complete workflow for the specified provider"""
    
    # Provider configurations
    config = {
        "gemini": {
            "name": "Basic Gemini Chat",
            "description": "Basic chat with Gemini 2.5 Flash - Simple chat flow using Google's latest Gemini model. Add your API key to get started.",
            "ai_node_id": "GoogleAI-1"
        },
        "openai": {
            "name": "Basic GPT-4o Chat", 
            "description": "Basic chat with GPT-4o - Simple chat flow using OpenAI's latest GPT-4o model. Add your API key to get started.",
            "ai_node_id": "OpenAI-1"
        },
        "anthropic": {
            "name": "Basic Claude Chat",
            "description": "Basic chat with Claude 3.5 Sonnet - Simple chat flow using Anthropic's latest Claude model. Add your API key to get started.",
            "ai_node_id": "Anthropic-1"
        }
    }
    
    if provider not in config:
        raise ValueError(f"Unknown provider: {provider}")
    
    # Create workflow
    workflow = create_base_workflow_template()
    workflow["name"] = config[provider]["name"]
    workflow["description"] = config[provider]["description"]
    
    # Add nodes
    workflow["data"]["nodes"] = [
        create_chat_input_node(),
        create_ai_model_node(provider),
        create_chat_output_node()
    ]
    
    # Add edges
    workflow["data"]["edges"] = create_edges(config[provider]["ai_node_id"])
    
    return workflow

def save_workflow(provider: str, output_dir: str = "examples/langflow-workflows"):
    """Generate and save a workflow to file"""
    
    # File mapping
    filenames = {
        "gemini": "basic-gemini-chat.json",
        "openai": "basic-gpt4o-chat.json", 
        "anthropic": "basic-claude-chat.json"
    }
    
    if provider not in filenames:
        raise ValueError(f"Unknown provider: {provider}")
    
    # Create output directory
    os.makedirs(output_dir, exist_ok=True)
    
    # Generate workflow
    workflow = generate_workflow(provider)
    
    # Save to file
    filepath = os.path.join(output_dir, filenames[provider])
    with open(filepath, 'w', encoding='utf-8') as f:
        json.dump(workflow, f, indent=2, ensure_ascii=False)
    
    print(f"Generated {provider} workflow: {filepath}")

def main():
    """Main function"""
    import sys
    
    providers = ["gemini", "openai", "anthropic"]
    
    if len(sys.argv) < 2:
        print("Usage: python generate_workflows.py [provider]")
        print(f"Providers: {', '.join(providers)}, all")
        sys.exit(1)
    
    provider = sys.argv[1].lower()
    
    if provider == "all":
        for p in providers:
            save_workflow(p)
        print(f"Generated all {len(providers)} workflows!")
    elif provider in providers:
        save_workflow(provider)
    else:
        print(f"Unknown provider: {provider}")
        print(f"Available providers: {', '.join(providers)}, all")
        sys.exit(1)

if __name__ == "__main__":
    main()