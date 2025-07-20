"""
Pipeline Generator - automatically starts and generates files for each workflow
"""

import os
import asyncio
import json
import re
import time
from pathlib import Path
from typing import List, Dict, Optional
from logging import getLogger

logger = getLogger(__name__)


class Pipeline:
    def __init__(self):
        self.name = "🔧 Pipeline Generator"
        self.id = "pipeline_generator"
        self.generated = False

    async def on_startup(self):
        """Automatically generate pipeline on startup"""
        if not self.generated:
            logger.info("🚀 Starting pipeline generation...")
            await self.generate_workflow_pipelines()
            self.generated = True

    def pipe(self, user_message: str, model_id: str, messages: List[dict], body: dict):
        return f"🔧 Pipeline Generator\n\n✅ Automatically generating pipeline files for each workflow from Langflow.\n\nCheck other available models in OpenWebUI - each workflow should be available as a separate model!"

    async def generate_workflow_pipelines(self):
        """Main function for generating pipelines"""
        try:
            langflow_url = os.getenv("LANGFLOW_BASE_URL", "http://langflow:7860")
            pipelines_dir = Path("/app/pipelines")

            # Wait for Langflow
            await self.wait_for_langflow(langflow_url)

            # Get workflows
            workflows = await self.discover_workflows(langflow_url)

            if not workflows:
                logger.warning("❌ No workflows found")
                return

            # Generate files
            template = self.get_template()
            generated_count = 0

            for workflow in workflows:
                try:
                    pipeline_code = self.generate_pipeline_code(workflow, template)
                    filename = f"langflow_{self.sanitize_name(workflow['name'])}.py"
                    filepath = pipelines_dir / filename

                    with open(filepath, "w", encoding="utf-8") as f:
                        f.write(pipeline_code)

                    logger.info(f"✅ Generated: {filename} -> {workflow['name']}")
                    generated_count += 1

                except Exception as e:
                    logger.error(f"❌ Failed to generate {workflow['name']}: {e}")

            logger.info(f"🎉 Generated {generated_count} pipeline files!")

        except Exception as e:
            logger.error(f"❌ Generation failed: {e}")

    async def wait_for_langflow(self, langflow_url: str, max_attempts: int = 30):
        """Wait until Langflow becomes available"""
        import httpx

        for attempt in range(1, max_attempts + 1):
            try:
                async with httpx.AsyncClient(timeout=5.0) as client:
                    response = await client.get(f"{langflow_url}/api/v1/flows/")
                    if response.status_code == 200:
                        logger.info("✅ Langflow is ready!")
                        return
            except:
                pass

            logger.info(f"⏳ Waiting for Langflow... ({attempt}/{max_attempts})")
            await asyncio.sleep(10)

        logger.warning("⚠️  Langflow not ready, proceeding anyway...")

    async def discover_workflows(self, langflow_url: str) -> List[Dict]:
        """Discover available workflows"""
        import httpx

        excluded = json.loads(
            os.getenv(
                "EXCLUDED_WORKFLOWS",
                '["Document Q&A", "Simple Agent", "Memory Chatbot", "SaaS Pricing", "Basic Prompting", "Sequential Tasks Agents", "Travel Planning Agents", "Chat with PDF"]'
            )
        )

        try:
            async with httpx.AsyncClient(timeout=10.0) as client:
                response = await client.get(f"{langflow_url}/api/v1/flows/")

                if response.status_code != 200:
                    return []

                # Parse response
                try:
                    import gzip

                    content = gzip.decompress(response.content)
                except:
                    content = response.content

                data = json.loads(content.decode("utf-8"))

                workflows = []
                for workflow in data:
                    name = workflow.get("name", "Unknown")
                    if name not in excluded:
                        workflows.append(
                            {
                                "name": name,
                                "id": workflow.get("id", ""),
                                "description": workflow.get("description", ""),
                            }
                        )
                        logger.info(f"✅ Found: {name}")

                return workflows

        except Exception as e:
            logger.error(f"❌ Discovery error: {e}")
            return []

    def sanitize_name(self, name: str) -> str:
        """Convert name to valid Python identifier"""
        sanitized = re.sub(r"[^a-zA-Z0-9_]", "_", name)
        sanitized = re.sub(r"_+", "_", sanitized)
        sanitized = sanitized.strip("_")
        if sanitized and sanitized[0].isdigit():
            sanitized = f"workflow_{sanitized}"
        return sanitized.lower()

    def get_template(self) -> str:
        """Template for generated pipelines"""
        return '''"""
Langflow Workflow: {{WORKFLOW_NAME}}
Auto-generated pipeline
"""

import os
import time
from datetime import datetime
from logging import getLogger
from typing import Generator, Iterator, List, Union

import httpx
from pydantic import BaseModel, Field

logger = getLogger(__name__)

class Pipeline:
    class Valves(BaseModel):
        LANGFLOW_BASE_URL: str = Field(default="http://host.docker.internal:7860")
        WORKFLOW_ID: str = Field(default="{{WORKFLOW_ID}}")
        WORKFLOW_NAME: str = Field(default="{{WORKFLOW_NAME}}")
        RATE_LIMIT: int = Field(default=5)

    def __init__(self):
        self.name = "{{PIPELINE_NAME}}"
        self.id = "{{PIPELINE_ID}}"
        self.valves = self.Valves()

    async def on_startup(self):
        logger.info(f"Workflow pipeline started: {self.name}")

    def rate_check(self, dt_start: datetime):
        diff = (datetime.now() - dt_start).total_seconds()
        buffer = 1 / self.valves.RATE_LIMIT
        if diff < buffer:
            time.sleep(buffer - diff)

    def pipe(self, user_message: str, model_id: str, messages: List[dict], body: dict) -> Union[str, Generator, Iterator]:
        logger.info(f"Processing request for workflow: {self.valves.WORKFLOW_NAME}")

        dt_start = datetime.now()
        return "".join([chunk for chunk in self.call_langflow(user_message, dt_start)])

    def call_langflow(self, prompt: str, dt_start: datetime) -> Generator:
        self.rate_check(dt_start)

        url = f"{self.valves.LANGFLOW_BASE_URL}/api/v1/run/{self.valves.WORKFLOW_ID}?stream=false"
        payload = {"input_value": prompt, "output_type": "chat", "input_type": "chat"}

        try:
            with httpx.Client(timeout=30.0) as client:
                response = client.post(url, json=payload)
                response.raise_for_status()
                data = response.json()

                text = (
                    data.get("outputs", [{}])[0]
                    .get("outputs", [{}])[0]
                    .get("results", {})
                    .get("message", {})
                    .get("text", f"No response from workflow '{self.valves.WORKFLOW_NAME}'.")
                )

                yield text

        except Exception as e:
            logger.error(f"Error calling workflow: {e}")
            yield f"🚨 **Error**: {str(e)}"
'''

    def generate_pipeline_code(self, workflow: Dict, template: str) -> str:
        """Generate pipeline code from template"""
        workflow_name = workflow["name"]
        workflow_id = workflow["id"]

        pipeline_id = self.sanitize_name(workflow_name)
        pipeline_name = f"Langflow: {workflow_name}"

        code = template.replace("{{WORKFLOW_ID}}", workflow_id)
        code = code.replace("{{WORKFLOW_NAME}}", workflow_name)
        code = code.replace("{{PIPELINE_NAME}}", pipeline_name)
        code = code.replace("{{PIPELINE_ID}}", pipeline_id)

        return code
