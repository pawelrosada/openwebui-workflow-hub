"""
Claude-3.5 Chat Pipeline for Open WebUI
Integracja z Anthropic Claude-3.5 Sonnet przez Langflow
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
        LANGFLOW_BASE_URL: str = Field(
            default="http://langflow:7860",
            description="URL bazowy do Langflow API"
        )
        WORKFLOW_ID: str = Field(
            default="claude3-chat-basic",
            description="ID przepływu Claude-3.5 w Langflow (endpoint_name)"
        )
        RATE_LIMIT: int = Field(
            default=5,
            description="Limit żądań na sekundę"
        )
        TIMEOUT: int = Field(
            default=30,
            description="Timeout w sekundach dla żądań do Langflow"
        )

    def __init__(self):
        self.name = "Claude-3.5 Sonnet Chat Pipeline"
        self.valves = self.Valves(
            **{k: os.getenv(k, v.default) for k, v in self.Valves.model_fields.items()}
        )

    async def on_startup(self):
        logger.info(f"🚀 Uruchomiono pipeline: {self.name}")
        logger.info(f"🔗 Langflow URL: {self.valves.LANGFLOW_BASE_URL}")
        logger.info(f"🔄 Workflow ID: {self.valves.WORKFLOW_ID}")
    
    async def on_shutdown(self): 
        logger.info(f"🛑 Zamknięto pipeline: {self.name}")

    def rate_check(self, dt_start: datetime):
        """Sprawdza i wymusza rate limiting"""
        diff = (datetime.now() - dt_start).total_seconds()
        buffer = 1 / self.valves.RATE_LIMIT
        if diff < buffer: 
            time.sleep(buffer - diff)

    def pipe(self, user_message: str, model_id: str, messages: List[dict], body: dict) -> Union[str, Generator, Iterator]:
        """
        Główna funkcja pipeline - przekazuje wiadomość do Langflow z Claude-3.5
        """
        logger.debug(f"📨 Przetwarzanie wiadomości przez {self.name}")
        logger.debug(f"📋 Wiadomość: {user_message[:100]}...")
        
        dt_start = datetime.now()
        
        try:
            result = "".join([chunk for chunk in self.call_langflow(user_message, dt_start)])
            logger.info(f"✅ Odpowiedź wygenerowana przez Claude-3.5 (długość: {len(result)})")
            return result
        except Exception as e:
            logger.error(f"❌ Błąd w pipeline Claude-3.5: {e}")
            return f"🚨 **Błąd Claude-3.5 Pipeline**: {str(e)}"

    def call_langflow(self, prompt: str, dt_start: datetime) -> Generator:
        """
        Wywołuje Langflow API z przepływem Claude-3.5
        """
        self.rate_check(dt_start)
        
        # URL do konkretnego przepływu Claude-3.5
        url = f"{self.valves.LANGFLOW_BASE_URL}/api/v1/run/{self.valves.WORKFLOW_ID}?stream=false"
        
        payload = {
            "input_value": prompt,
            "output_type": "chat",
            "input_type": "chat"
        }
        
        headers = {
            "Content-Type": "application/json"
        }
        
        logger.debug(f"🔗 Wywołuję Langflow: {url}")
        logger.debug(f"📦 Payload: {payload}")
        
        try:
            with httpx.Client(timeout=self.valves.TIMEOUT) as client:
                response = client.post(url, json=payload, headers=headers)
                response.raise_for_status()
                
                data = response.json()
                logger.debug(f"📥 Odpowiedź Langflow: {data}")
                
                # Wyciągnij tekst odpowiedzi z struktury Langflow
                text = (
                    data.get("outputs", [{}])[0]
                        .get("outputs", [{}])[0]
                        .get("results", {})
                        .get("message", {})
                        .get("text", "Brak odpowiedzi z Claude-3.5")
                )
                
                if text:
                    yield f"🤖 **Claude-3.5 Sonnet**: {text}"
                else:
                    yield "🚨 **Claude-3.5 Error**: Nie otrzymano odpowiedzi z modelu"
                    
        except httpx.TimeoutException:
            logger.error(f"⏰ Timeout podczas łączenia z Langflow")
            yield "🚨 **Claude-3.5 Error**: Przekroczono limit czasu odpowiedzi"
            
        except httpx.HTTPStatusError as e:
            logger.error(f"🚫 Błąd HTTP z Langflow: {e.response.status_code}")
            yield f"🚨 **Claude-3.5 Error**: Błąd serwera ({e.response.status_code})"
            
        except Exception as e:
            logger.error(f"❌ Nieoczekiwany błąd Langflow: {e}")
            yield f"🚨 **Claude-3.5 Error**: {str(e)}"