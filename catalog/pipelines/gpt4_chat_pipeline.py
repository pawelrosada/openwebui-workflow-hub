"""
GPT-4 Chat Pipeline for Open WebUI
Integracja z OpenAI GPT-4o przez Langflow
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
            default="gpt4o-chat-basic",
            description="ID przepływu GPT-4o w Langflow (endpoint_name)"
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
        self.name = "GPT-4o Chat Pipeline"
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
        Główna funkcja pipeline - przekazuje wiadomość do Langflow z GPT-4o
        """
        logger.debug(f"📨 Przetwarzanie wiadomości przez {self.name}")
        logger.debug(f"📋 Wiadomość: {user_message[:100]}...")
        
        dt_start = datetime.now()
        
        try:
            result = "".join([chunk for chunk in self.call_langflow(user_message, dt_start)])
            logger.info(f"✅ Odpowiedź wygenerowana przez GPT-4o (długość: {len(result)})")
            return result
        except Exception as e:
            logger.error(f"❌ Błąd w pipeline GPT-4o: {e}")
            return f"🚨 **Błąd GPT-4o Pipeline**: {str(e)}"

    def call_langflow(self, prompt: str, dt_start: datetime) -> Generator:
        """
        Wywołuje Langflow API z przepływem GPT-4o
        """
        self.rate_check(dt_start)
        
        # URL do konkretnego przepływu GPT-4o
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
                        .get("text", "Brak odpowiedzi z GPT-4o")
                )
                
                if text:
                    yield f"🤖 **GPT-4o**: {text}"
                else:
                    yield "🚨 **GPT-4o Error**: Nie otrzymano odpowiedzi z modelu"
                    
        except httpx.TimeoutException:
            logger.error(f"⏰ Timeout podczas łączenia z Langflow")
            yield "🚨 **GPT-4o Error**: Przekroczono limit czasu odpowiedzi"
            
        except httpx.HTTPStatusError as e:
            logger.error(f"🚫 Błąd HTTP z Langflow: {e.response.status_code}")
            yield f"🚨 **GPT-4o Error**: Błąd serwera ({e.response.status_code})"
            
        except Exception as e:
            logger.error(f"❌ Nieoczekiwany błąd Langflow: {e}")
            yield f"🚨 **GPT-4o Error**: {str(e)}"