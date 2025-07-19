"""
Langflow Integration Pipeline for Open WebUI

This pipeline provides integration between Open WebUI chat interface and Langflow workflows.
It handles rate limiting, error management, and response formatting for optimal user experience.

Features:
- Configurable Langflow base URL and workflow ID
- Rate limiting to prevent API overload
- Comprehensive error handling with user-friendly messages
- Robust HTTP client with timeout management
- Structured logging for debugging

Usage:
- Configure valves in Open WebUI admin panel
- Messages are automatically forwarded to specified Langflow workflow
- Responses are formatted and returned to the chat interface
"""

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
        self.valves = self.Valves(
            **{k: os.getenv(k, v.default) for k, v in self.Valves.model_fields.items()}
        )

    async def on_startup(self):
        logger.debug(f"on_startup:{self.name}")

    async def on_shutdown(self):
        logger.debug(f"on_shutdown:{self.name}")

    def rate_check(self, dt_start: datetime):
        diff = (datetime.now() - dt_start).total_seconds()
        buffer = 1 / self.valves.RATE_LIMIT
        if diff < buffer:
            time.sleep(buffer - diff)

    def pipe(
        self, user_message: str, model_id: str, messages: List[dict], body: dict
    ) -> Union[str, Generator, Iterator]:
        logger.debug(f"pipe:{self.name}")
        dt_start = datetime.now()
        return "".join([chunk for chunk in self.call_langflow(user_message, dt_start)])

    def call_langflow(self, prompt: str, dt_start: datetime) -> Generator:
        """Call Langflow API with rate limiting and error handling"""
        self.rate_check(dt_start)
        url = f"{self.valves.LANGFLOW_BASE_URL}/api/v1/run/{self.valves.WORKFLOW_ID}?stream=false"
        payload = {"input_value": prompt, "output_type": "chat", "input_type": "chat"}

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
                yield text

        except httpx.TimeoutException:
            logger.error(f"Timeout calling Langflow: {url}")
            yield "🚨 **Błąd**: Przekroczono limit czasu oczekiwania na odpowiedź z Langflow."

        except httpx.HTTPStatusError as e:
            logger.error(f"HTTP error {e.response.status_code} calling Langflow: {e}")
            yield f"🚨 **Błąd HTTP {e.response.status_code}**: Nie udało się połączyć z przepływem Langflow."

        except httpx.ConnectError:
            logger.error(f"Connection error calling Langflow: {url}")
            yield "🚨 **Błąd połączenia**: Nie można połączyć się z usługą Langflow. Sprawdź czy usługa działa."

        except Exception as e:
            logger.error(f"Unexpected error calling Langflow: {e}")
            yield f"🚨 **Nieoczekiwany błąd**: {str(e)}"
