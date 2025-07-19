#!/usr/bin/env python3
"""
Enhanced Multi-Model Langflow Pipeline for Open WebUI
Extends the original pipeline with multi-model support and dynamic routing.

Features:
- Multiple AI model support (Gemini, GPT-4o, Claude)
- Dynamic model selection via user input
- Agentic routing based on query content
- Backward compatibility with existing single-model setups
- Enhanced error handling and logging

Usage in Open WebUI:
- @model:gemini Your question here
- @model:gpt Your question here  
- @model:claude Your question here
- @agent Your question here (automatic model selection)
- Regular messages use default model
"""

import os
import re
import time
from datetime import datetime
from logging import getLogger
from typing import Generator, Iterator, List, Union, Dict, Any

import httpx
from pydantic import BaseModel, Field

logger = getLogger(__name__)
logger.setLevel("DEBUG")

class Pipeline:
    class Valves(BaseModel):
        # LangFlow Configuration
        LANGFLOW_BASE_URL: str = Field(default="http://host.docker.internal:7860")
        WORKFLOW_ID: str = Field(default="3ec49b62-4a8e-4cb9-9913-a51086ca7471")
        
        # Multi-Model Configuration
        ENABLE_MULTI_MODEL: bool = Field(default=True, description="Enable multi-model support")
        DEFAULT_MODEL: str = Field(default="gpt", description="Default model (gemini, gpt, claude)")
        
        # Model-specific workflow IDs (optional - uses WORKFLOW_ID if not set)
        GEMINI_WORKFLOW_ID: str = Field(default="", description="Specific workflow for Gemini")
        GPT_WORKFLOW_ID: str = Field(default="", description="Specific workflow for GPT")
        CLAUDE_WORKFLOW_ID: str = Field(default="", description="Specific workflow for Claude")
        
        # Universal workflow support
        UNIVERSAL_WORKFLOW_ID: str = Field(default="", description="Universal workflow that handles all models")
        
        # API Keys (for tweaks)
        GEMINI_API_KEY: str = Field(default="", description="Gemini API key for tweaks")
        OPENAI_API_KEY: str = Field(default="", description="OpenAI API key for tweaks")
        ANTHROPIC_API_KEY: str = Field(default="", description="Anthropic API key for tweaks")
        
        # Rate limiting and performance
        RATE_LIMIT: int = Field(default=5, description="Requests per second limit")
        ENABLE_AGENTIC_ROUTING: bool = Field(default=True, description="Enable smart model routing")

    def __init__(self):
        self.name = "Enhanced Multi-Model Langflow Pipeline"
        self.valves = self.Valves(**{k: os.getenv(k, v.default) for k, v in self.Valves.model_fields.items()})
        
        # Model configurations
        self.models = {
            "gemini": {
                "model": "gemini-2.5-flash",
                "display_name": "Google Gemini 2.5 Flash",
                "keywords": ["search", "current", "recent", "google", "web"]
            },
            "gpt": {
                "model": "gpt-4o",
                "display_name": "OpenAI GPT-4o",
                "keywords": ["creative", "story", "poem", "writing", "chat", "conversation"]
            },
            "claude": {
                "model": "claude-3-5-sonnet-20241022", 
                "display_name": "Anthropic Claude 3.5 Sonnet",
                "keywords": ["code", "programming", "python", "javascript", "technical", "analysis"]
            }
        }

    async def on_startup(self): 
        logger.debug(f"on_startup: {self.name}")
        logger.info(f"Multi-model support: {self.valves.ENABLE_MULTI_MODEL}")
        logger.info(f"Default model: {self.valves.DEFAULT_MODEL}")
        logger.info(f"Agentic routing: {self.valves.ENABLE_AGENTIC_ROUTING}")
    
    async def on_shutdown(self): 
        logger.debug(f"on_shutdown: {self.name}")

    def rate_check(self, dt_start: datetime):
        """Rate limiting check"""
        diff = (datetime.now() - dt_start).total_seconds()
        buffer = 1 / self.valves.RATE_LIMIT
        if diff < buffer: 
            time.sleep(buffer - diff)

    def parse_model_directive(self, user_message: str) -> tuple[str, str]:
        """
        Parse model directive from user message
        
        Supports formats:
        - @model:gemini Your question
        - @model:gpt Your question
        - @model:claude Your question  
        - @agent Your question (automatic routing)
        
        Returns: (selected_model, cleaned_message)
        """
        
        # Check for explicit model directive
        model_match = re.match(r'@model:(\w+)\s+(.*)', user_message, re.IGNORECASE)
        if model_match:
            requested_model = model_match.group(1).lower()
            cleaned_message = model_match.group(2).strip()
            
            if requested_model in self.models:
                logger.info(f"Explicit model requested: {requested_model}")
                return requested_model, cleaned_message
            else:
                logger.warning(f"Unknown model requested: {requested_model}, using default")
                return self.valves.DEFAULT_MODEL, cleaned_message
        
        # Check for agent directive
        agent_match = re.match(r'@agent\s+(.*)', user_message, re.IGNORECASE)
        if agent_match and self.valves.ENABLE_AGENTIC_ROUTING:
            cleaned_message = agent_match.group(1).strip()
            selected_model = self.select_model_by_content(cleaned_message)
            logger.info(f"Agent routing: '{cleaned_message[:50]}...' -> {selected_model}")
            return selected_model, cleaned_message
            
        # No directive found, use default
        return self.valves.DEFAULT_MODEL, user_message

    def select_model_by_content(self, message: str) -> str:
        """
        Intelligent model selection based on message content
        """
        message_lower = message.lower()
        
        # Score each model based on keyword matches
        model_scores = {}
        for model_name, config in self.models.items():
            score = sum(1 for keyword in config["keywords"] if keyword in message_lower)
            model_scores[model_name] = score
        
        # Select model with highest score
        selected_model = max(model_scores, key=model_scores.get)
        
        # If no keywords matched, use some heuristics
        if model_scores[selected_model] == 0:
            if len(message) > 500:  # Long messages
                selected_model = "claude"  # Good for detailed analysis
            elif any(char in message for char in "?!"):  # Questions/exclamations
                selected_model = "gpt"  # Good for conversation
            else:
                selected_model = self.valves.DEFAULT_MODEL
        
        return selected_model

    def get_workflow_id(self, model: str) -> str:
        """Get appropriate workflow ID for the model"""
        
        # Use universal workflow if available
        if self.valves.UNIVERSAL_WORKFLOW_ID:
            return self.valves.UNIVERSAL_WORKFLOW_ID
            
        # Use model-specific workflow IDs
        model_workflow_map = {
            "gemini": self.valves.GEMINI_WORKFLOW_ID,
            "gpt": self.valves.GPT_WORKFLOW_ID,
            "claude": self.valves.CLAUDE_WORKFLOW_ID
        }
        
        specific_workflow = model_workflow_map.get(model, "")
        if specific_workflow:
            return specific_workflow
            
        # Fall back to default workflow
        return self.valves.WORKFLOW_ID

    def get_model_tweaks(self, model: str, temperature: float = 0.7) -> Dict[str, Any]:
        """Get model-specific tweaks for LangFlow API"""
        
        base_tweaks = {
            "temperature": temperature,
            "model": self.models[model]["model"]
        }
        
        # Add API keys if available
        api_key_map = {
            "gemini": ("google_api_key", self.valves.GEMINI_API_KEY),
            "gpt": ("openai_api_key", self.valves.OPENAI_API_KEY), 
            "claude": ("anthropic_api_key", self.valves.ANTHROPIC_API_KEY)
        }
        
        if model in api_key_map:
            key_name, api_key = api_key_map[model]
            if api_key:
                base_tweaks[key_name] = api_key
        
        return base_tweaks

    def pipe(self, user_message: str, model_id: str, messages: List[dict], body: dict) -> Union[str, Generator, Iterator]:
        logger.debug(f"pipe: {self.name}")
        dt_start = datetime.now()
        
        # Parse model selection if multi-model is enabled
        if self.valves.ENABLE_MULTI_MODEL:
            selected_model, cleaned_message = self.parse_model_directive(user_message)
        else:
            selected_model, cleaned_message = self.valves.DEFAULT_MODEL, user_message
            
        return "".join([chunk for chunk in self.call_langflow(cleaned_message, selected_model, dt_start)])

    def call_langflow(self, prompt: str, model: str, dt_start: datetime) -> Generator:
        """Call Langflow API with specified model"""
        self.rate_check(dt_start)
        
        workflow_id = self.get_workflow_id(model)
        url = f"{self.valves.LANGFLOW_BASE_URL}/api/v1/run/{workflow_id}?stream=false"
        
        # Prepare payload with model-specific tweaks
        payload = {
            "input_value": prompt,
            "output_type": "chat",
            "input_type": "chat"
        }
        
        # Add tweaks for model configuration
        tweaks = self.get_model_tweaks(model)
        if tweaks:
            payload["tweaks"] = tweaks
        
        logger.info(f"Calling LangFlow with {model} model: {workflow_id}")
        
        try:
            with httpx.Client(timeout=30.0) as client:
                response = client.post(url, json=payload)
                response.raise_for_status()
                data = response.json()
                
                # Extract response text from Langflow output structure
                text = (
                    data.get("outputs", [{}])[0]
                        .get("outputs", [{}])[0]
                        .get("results", {})
                        .get("message", {})
                        .get("text", "Brak odpowiedzi z przepływu Langflow.")
                )
                
                # Add model info to response
                model_display = self.models[model]["display_name"]
                prefix = f"🤖 **{model_display}**: " if self.valves.ENABLE_MULTI_MODEL else ""
                yield f"{prefix}{text}"
                
        except httpx.TimeoutException:
            logger.error(f"Timeout calling Langflow: {url}")
            yield f"🚨 **Błąd**: Przekroczono limit czasu oczekiwania na odpowiedź z Langflow ({model})."
            
        except httpx.HTTPStatusError as e:
            logger.error(f"HTTP error {e.response.status_code} calling Langflow: {e}")
            yield f"🚨 **Błąd HTTP {e.response.status_code}**: Nie udało się połączyć z przepływem Langflow ({model})."
            
        except httpx.ConnectError:
            logger.error(f"Connection error calling Langflow: {url}")
            yield "🚨 **Błąd połączenia**: Nie można połączyć się z usługą Langflow. Sprawdź czy usługa działa."
            
        except Exception as e:
            logger.error(f"Unexpected error calling Langflow with {model}: {e}")
            yield f"🚨 **Nieoczekiwany błąd ({model})**: {str(e)}"