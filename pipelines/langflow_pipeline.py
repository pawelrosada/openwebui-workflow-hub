import os
import time
from datetime import datetime
from logging import getLogger
from typing import Generator, Iterator, List, Union

import httpx
from pydantic import BaseModel, Field

logger = getLogger(__name__)
logger.setLevel("DEBUG")

class Pipeline:
    class Valves(BaseModel):
        LANGFLOW_BASE_URL: str = Field(default="http://host.docker.internal:7860")
        WORKFLOW_ID: str = Field(default="3ec49b62-4a8e-4cb9-9913-a51086ca7471")
        RATE_LIMIT: int = Field(default=5)

    def __init__(self):
        self.name = "Langflow Pipeline"
        self.valves = self.Valves(**{k: os.getenv(k, v.default) for k, v in self.Valves.model_fields.items()})

    async def on_startup(self): 
        logger.debug(f"on_startup:{self.name}")
    
    async def on_shutdown(self): 
        logger.debug(f"on_shutdown:{self.name}")

    def rate_check(self, dt_start: datetime):
        diff = (datetime.now() - dt_start).total_seconds()
        buffer = 1 / self.valves.RATE_LIMIT
        if diff < buffer: 
            time.sleep(buffer - diff)

    def pipe(self, user_message: str, model_id: str, messages: List[dict], body: dict) -> Union[str, Generator, Iterator]:
        logger.debug(f"pipe:{self.name}")
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
                        .get("text", "No text found.")
                )
                yield text
        except Exception as e:
            logger.error(f"Langflow error: {e}")
            yield f"Error: {e}"
