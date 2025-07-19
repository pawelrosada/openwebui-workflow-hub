#!/usr/bin/env python3
"""
Dynamic Workflow Selector Pipeline for Open WebUI
Allows users to select and switch between different Langflow workflows dynamically from chat.

Features:
- Dynamic workflow selection via @workflow:name or @flow:id syntax
- List available workflows with @workflows command
- Set default workflow for session with @set-workflow:name
- Automatic workflow discovery from Langflow API
- Session-based workflow memory
- Backward compatibility with single workflow setups

Usage in Open WebUI:
- @workflows - List all available workflows
- @workflow:my-workflow-name Your message here
- @flow:3ec49b62-4a8e-4cb9-9913-a51086ca7471 Your message here  
- @set-workflow:my-workflow-name - Set default for session
- Regular messages use the current default workflow
"""

import os
import re
import time
from datetime import datetime
from logging import getLogger
from typing import Generator, Iterator, List, Union, Dict, Any
from urllib.parse import quote

import httpx
from pydantic import BaseModel, Field

logger = getLogger(__name__)
logger.setLevel("DEBUG")

class Pipeline:
    class Valves(BaseModel):
        # Langflow Configuration
        LANGFLOW_BASE_URL: str = Field(default="http://host.docker.internal:7860")
        DEFAULT_WORKFLOW_ID: str = Field(default="3ec49b62-4a8e-4cb9-9913-a51086ca7471", description="Fallback workflow ID")
        
        # Authentication (if needed)
        LANGFLOW_API_KEY: str = Field(default="", description="Langflow API key (if authentication enabled)")
        
        # Workflow Discovery  
        ENABLE_WORKFLOW_DISCOVERY: bool = Field(default=True, description="Enable automatic workflow discovery")
        WORKFLOW_CACHE_TTL: int = Field(default=300, description="Workflow cache TTL in seconds")
        
        # Session Management
        ENABLE_SESSION_MEMORY: bool = Field(default=True, description="Remember workflow selection per user session")
        
        # Performance
        RATE_LIMIT: int = Field(default=5, description="Requests per second limit")
        CONNECTION_TIMEOUT: int = Field(default=30, description="HTTP timeout in seconds")

    def __init__(self):
        self.name = "Dynamic Workflow Selector Pipeline"
        self.valves = self.Valves(**{k: os.getenv(k, v.default) for k, v in self.Valves.model_fields.items()})
        
        # Session storage for workflow selection
        self.session_workflows: Dict[str, str] = {}
        
        # Workflow cache
        self.workflow_cache: Dict[str, Any] = {}
        self.cache_timestamp = 0

    async def on_startup(self): 
        logger.debug(f"on_startup: {self.name}")
        logger.info(f"Workflow discovery: {self.valves.ENABLE_WORKFLOW_DISCOVERY}")
        logger.info(f"Session memory: {self.valves.ENABLE_SESSION_MEMORY}")
        
        # Initial workflow discovery
        if self.valves.ENABLE_WORKFLOW_DISCOVERY:
            await self.discover_workflows()
    
    async def on_shutdown(self): 
        logger.debug(f"on_shutdown: {self.name}")

    def get_session_id(self, body: dict) -> str:
        """Generate a session ID from request body"""
        # Try to get user info for session identification
        user_info = body.get("user", {})
        user_id = user_info.get("id", "")
        if user_id:
            return f"user_{user_id}"
        
        # Fallback to chat ID or create generic session
        chat_id = body.get("chat_id", body.get("conversation_id", "default"))
        return f"session_{chat_id}"

    def rate_check(self, dt_start: datetime):
        """Rate limiting check"""
        diff = (datetime.now() - dt_start).total_seconds()
        buffer = 1 / self.valves.RATE_LIMIT
        if diff < buffer: 
            time.sleep(buffer - diff)

    async def discover_workflows(self) -> Dict[str, Any]:
        """Discover available workflows from Langflow API"""
        try:
            # Check cache validity
            current_time = time.time()
            if (current_time - self.cache_timestamp) < self.valves.WORKFLOW_CACHE_TTL and self.workflow_cache:
                logger.debug("Using cached workflow list")
                return self.workflow_cache
            
            headers = {}
            if self.valves.LANGFLOW_API_KEY:
                headers["Authorization"] = f"Bearer {self.valves.LANGFLOW_API_KEY}"
            
            # Try different endpoints for workflow discovery
            endpoints_to_try = [
                "/api/v1/flows",
                "/api/v1/flows/",  
                "/api/flows",
            ]
            
            workflows = {}
            
            with httpx.Client(timeout=self.valves.CONNECTION_TIMEOUT) as client:
                for endpoint in endpoints_to_try:
                    try:
                        url = f"{self.valves.LANGFLOW_BASE_URL}{endpoint}"
                        response = client.get(url, headers=headers)
                        
                        if response.status_code == 200:
                            data = response.json()
                            logger.info(f"Successfully discovered workflows from {endpoint}")
                            
                            # Parse workflows based on response structure
                            if isinstance(data, list):
                                for workflow in data:
                                    if isinstance(workflow, dict):
                                        flow_id = workflow.get("id", workflow.get("flow_id", ""))
                                        name = workflow.get("name", workflow.get("title", f"Workflow {flow_id[:8]}"))
                                        if flow_id:
                                            workflows[name.lower().replace(" ", "-")] = {
                                                "id": flow_id,
                                                "name": name,
                                                "description": workflow.get("description", ""),
                                                "updated_at": workflow.get("updated_at", "")
                                            }
                            elif isinstance(data, dict) and "flows" in data:
                                for workflow in data["flows"]:
                                    flow_id = workflow.get("id", workflow.get("flow_id", ""))
                                    name = workflow.get("name", workflow.get("title", f"Workflow {flow_id[:8]}"))
                                    if flow_id:
                                        workflows[name.lower().replace(" ", "-")] = {
                                            "id": flow_id,
                                            "name": name,
                                            "description": workflow.get("description", ""),
                                            "updated_at": workflow.get("updated_at", "")
                                        }
                            break
                            
                    except Exception as e:
                        logger.debug(f"Failed to discover workflows from {endpoint}: {e}")
                        continue
            
            # Add default workflow if no workflows discovered
            if not workflows and self.valves.DEFAULT_WORKFLOW_ID:
                workflows["default"] = {
                    "id": self.valves.DEFAULT_WORKFLOW_ID,
                    "name": "Default Workflow",
                    "description": "Default configured workflow",
                    "updated_at": ""
                }
            
            # Update cache
            self.workflow_cache = workflows
            self.cache_timestamp = current_time
            
            logger.info(f"Discovered {len(workflows)} workflows")
            return workflows
            
        except Exception as e:
            logger.error(f"Error discovering workflows: {e}")
            # Return default workflow as fallback
            return {
                "default": {
                    "id": self.valves.DEFAULT_WORKFLOW_ID,
                    "name": "Default Workflow", 
                    "description": "Default configured workflow",
                    "updated_at": ""
                }
            }

    def parse_workflow_directive(self, user_message: str, session_id: str) -> tuple[str, str, str]:
        """
        Parse workflow directive from user message
        
        Supports formats:
        - @workflows - List all available workflows
        - @workflow:name Your message here
        - @flow:id Your message here
        - @set-workflow:name - Set default workflow for session
        
        Returns: (action, workflow_id, cleaned_message)
        """
        
        # Check for workflows list command
        if re.match(r'@workflows?\s*$', user_message.strip(), re.IGNORECASE):
            return "list_workflows", "", ""
        
        # Check for set-workflow command  
        set_match = re.match(r'@set-workflow:(\S+)\s*$', user_message.strip(), re.IGNORECASE)
        if set_match:
            workflow_name = set_match.group(1).lower()
            return "set_workflow", workflow_name, ""
            
        # Check for explicit workflow by name
        workflow_match = re.match(r'@workflow:(\S+)\s+(.*)', user_message, re.IGNORECASE)
        if workflow_match:
            workflow_name = workflow_match.group(1).lower()
            cleaned_message = workflow_match.group(2).strip()
            return "use_workflow_name", workflow_name, cleaned_message
        
        # Check for explicit workflow by ID
        flow_match = re.match(r'@flow:(\S+)\s+(.*)', user_message, re.IGNORECASE) 
        if flow_match:
            flow_id = flow_match.group(1).strip()
            cleaned_message = flow_match.group(2).strip()
            return "use_workflow_id", flow_id, cleaned_message
            
        # No directive found, use session default or system default
        current_workflow = self.get_current_workflow(session_id)
        return "use_current", current_workflow, user_message

    def get_current_workflow(self, session_id: str) -> str:
        """Get current workflow for session"""
        if self.valves.ENABLE_SESSION_MEMORY and session_id in self.session_workflows:
            return self.session_workflows[session_id]
        return self.valves.DEFAULT_WORKFLOW_ID

    def set_session_workflow(self, session_id: str, workflow_id: str):
        """Set workflow for session"""
        if self.valves.ENABLE_SESSION_MEMORY:
            self.session_workflows[session_id] = workflow_id
            logger.info(f"Set workflow {workflow_id} for session {session_id}")

    async def handle_list_workflows(self) -> str:
        """Handle workflow listing request"""
        workflows = await self.discover_workflows()
        
        if not workflows:
            return "🚨 **Błąd**: Nie znaleziono dostępnych przepływów pracy."
        
        response = "📋 **Dostępne przepływy pracy:**\n\n"
        for key, workflow in workflows.items():
            name = workflow["name"]
            flow_id = workflow["id"]
            description = workflow.get("description", "Brak opisu")
            
            response += f"• **{name}**\n"
            response += f"  - Klucz: `{key}`\n"
            response += f"  - ID: `{flow_id[:20]}...`\n"
            response += f"  - Opis: {description}\n\n"
        
        response += "💡 **Użycie:**\n"
        response += "- `@workflow:nazwa Twoja wiadomość` - Użyj konkretnego przepływu\n"
        response += "- `@flow:id Twoja wiadomość` - Użyj ID przepływu\n" 
        response += "- `@set-workflow:nazwa` - Ustaw domyślny dla sesji\n"
        
        return response

    async def handle_set_workflow(self, workflow_name: str, session_id: str) -> str:
        """Handle set workflow request"""
        workflows = await self.discover_workflows()
        
        if workflow_name in workflows:
            workflow_id = workflows[workflow_name]["id"]
            self.set_session_workflow(session_id, workflow_id)
            workflow_display_name = workflows[workflow_name]["name"]
            return f"✅ Ustawiono domyślny przepływ: **{workflow_display_name}** dla tej sesji."
        else:
            available_names = ", ".join(workflows.keys())
            return f"🚨 **Błąd**: Nie znaleziono przepływu '{workflow_name}'. Dostępne: {available_names}"

    def pipe(self, user_message: str, model_id: str, messages: List[dict], body: dict) -> Union[str, Generator, Iterator]:
        logger.debug(f"pipe: {self.name}")
        dt_start = datetime.now()
        
        session_id = self.get_session_id(body)
        action, workflow_identifier, cleaned_message = self.parse_workflow_directive(user_message, session_id)
        
        logger.info(f"Action: {action}, Session: {session_id}")
        
        # Handle special commands
        if action == "list_workflows":
            return self.handle_list_workflows_sync()
        elif action == "set_workflow":
            return self.handle_set_workflow_sync(workflow_identifier, session_id)
        
        # Handle workflow selection and message processing
        return "".join([chunk for chunk in self.call_langflow_with_workflow(
            action, workflow_identifier, cleaned_message, session_id, dt_start)])

    def handle_list_workflows_sync(self) -> str:
        """Synchronous wrapper for workflow listing"""
        import asyncio
        try:
            loop = asyncio.get_event_loop()
            if loop.is_running():
                # Create a new event loop for this thread if one is already running
                import concurrent.futures
                with concurrent.futures.ThreadPoolExecutor() as executor:
                    future = executor.submit(asyncio.run, self.discover_workflows())
                    workflows = future.result(timeout=10)
            else:
                workflows = loop.run_until_complete(self.discover_workflows())
        except:
            # Fallback to basic sync implementation
            workflows = {"default": {"id": self.valves.DEFAULT_WORKFLOW_ID, "name": "Default", "description": ""}}
        
        if not workflows:
            return "🚨 **Błąd**: Nie znaleziono dostępnych przepływów pracy."
        
        response = "📋 **Dostępne przepływy pracy:**\n\n"
        for key, workflow in workflows.items():
            name = workflow["name"]
            flow_id = workflow["id"]
            description = workflow.get("description", "Brak opisu")
            
            response += f"• **{name}**\n"
            response += f"  - Klucz: `{key}`\n"
            response += f"  - ID: `{flow_id[:20]}...`\n"
            response += f"  - Opis: {description}\n\n"
        
        response += "💡 **Użycie:**\n"
        response += "- `@workflow:nazwa Twoja wiadomość` - Użyj konkretnego przepływu\n"
        response += "- `@flow:id Twoja wiadomość` - Użyj ID przepływu\n" 
        response += "- `@set-workflow:nazwa` - Ustaw domyślny dla sesji\n"
        
        return response

    def handle_set_workflow_sync(self, workflow_name: str, session_id: str) -> str:
        """Synchronous wrapper for set workflow"""
        import asyncio
        try:
            loop = asyncio.get_event_loop()
            if loop.is_running():
                import concurrent.futures
                with concurrent.futures.ThreadPoolExecutor() as executor:
                    future = executor.submit(asyncio.run, self.discover_workflows())
                    workflows = future.result(timeout=10)
            else:
                workflows = loop.run_until_complete(self.discover_workflows())
        except:
            workflows = {"default": {"id": self.valves.DEFAULT_WORKFLOW_ID, "name": "Default", "description": ""}}
        
        if workflow_name in workflows:
            workflow_id = workflows[workflow_name]["id"]
            self.set_session_workflow(session_id, workflow_id)
            workflow_display_name = workflows[workflow_name]["name"]
            return f"✅ Ustawiono domyślny przepływ: **{workflow_display_name}** dla tej sesji."
        else:
            available_names = ", ".join(workflows.keys())
            return f"🚨 **Błąd**: Nie znaleziono przepływu '{workflow_name}'. Dostępne: {available_names}"

    def resolve_workflow_id(self, action: str, workflow_identifier: str) -> str:
        """Resolve workflow identifier to actual workflow ID"""
        if action == "use_workflow_id" or action == "use_current":
            return workflow_identifier
        elif action == "use_workflow_name":
            # Try to resolve name to ID from cache
            if workflow_identifier in self.workflow_cache:
                return self.workflow_cache[workflow_identifier]["id"]
            else:
                # Fallback to default if name not found
                logger.warning(f"Workflow name '{workflow_identifier}' not found, using default")
                return self.valves.DEFAULT_WORKFLOW_ID
        else:
            return self.valves.DEFAULT_WORKFLOW_ID

    def call_langflow_with_workflow(self, action: str, workflow_identifier: str, prompt: str, session_id: str, dt_start: datetime) -> Generator:
        """Call Langflow API with specified workflow"""
        self.rate_check(dt_start)
        
        workflow_id = self.resolve_workflow_id(action, workflow_identifier)
        url = f"{self.valves.LANGFLOW_BASE_URL}/api/v1/run/{workflow_id}?stream=false"
        
        # Prepare payload
        payload = {
            "input_value": prompt,
            "output_type": "chat",
            "input_type": "chat"
        }
        
        # Add headers if authentication is enabled
        headers = {"Content-Type": "application/json"}
        if self.valves.LANGFLOW_API_KEY:
            headers["Authorization"] = f"Bearer {self.valves.LANGFLOW_API_KEY}"
        
        # Get workflow name for display
        workflow_name = "Unknown"
        try:
            for key, workflow in self.workflow_cache.items():
                if workflow["id"] == workflow_id:
                    workflow_name = workflow["name"]
                    break
        except:
            pass
        
        logger.info(f"Calling workflow '{workflow_name}' (ID: {workflow_id[:8]}...) for session {session_id}")
        
        try:
            with httpx.Client(timeout=self.valves.CONNECTION_TIMEOUT) as client:
                response = client.post(url, json=payload, headers=headers)
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
                
                # Add workflow info to response
                prefix = f"🔧 **{workflow_name}**: "
                yield f"{prefix}{text}"
                
        except httpx.TimeoutException:
            logger.error(f"Timeout calling Langflow workflow {workflow_id}")
            yield f"🚨 **Błąd**: Przekroczono limit czasu oczekiwania na odpowiedź z przepływu ({workflow_name})."
            
        except httpx.HTTPStatusError as e:
            logger.error(f"HTTP error {e.response.status_code} calling Langflow workflow {workflow_id}: {e}")
            yield f"🚨 **Błąd HTTP {e.response.status_code}**: Nie udało się połączyć z przepływem Langflow ({workflow_name})."
            
        except httpx.ConnectError:
            logger.error(f"Connection error calling Langflow workflow {workflow_id}")
            yield "🚨 **Błąd połączenia**: Nie można połączyć się z usługą Langflow. Sprawdź czy usługa działa."
            
        except Exception as e:
            logger.error(f"Unexpected error calling Langflow workflow {workflow_id}: {e}")
            yield f"🚨 **Nieoczekiwany błąd ({workflow_name})**: {str(e)}"