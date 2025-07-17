"""
Simple Langflow Pipeline for Open WebUI
Basic integration that forwards chat messages to Langflow
"""

import requests
import json
import logging
from typing import Dict, Any, List, Optional


def pipe(
    user_message: str, 
    model_id: str, 
    messages: List[Dict[str, Any]], 
    body: Dict[str, Any]
) -> str:
    """
    Main pipe function that processes user messages through Langflow
    """
    
    # Configuration - można też wyciągnąć do zmiennych środowiskowych
    LANGFLOW_BASE_URL = "http://langflow:7860"
    DEFAULT_FLOW_ID = "your-flow-id"  # Trzeba będzie wstawić prawdziwy ID
    
    # Logging
    logging.basicConfig(level=logging.INFO)
    logger = logging.getLogger(__name__)
    
    try:
        # Check if user specified a specific flow
        flow_id = DEFAULT_FLOW_ID
        message = user_message
        
        # Parse flow ID from message if specified: @flow:flow-id message
        if user_message.startswith("@flow:"):
            parts = user_message.split(" ", 1)
            if len(parts) >= 1:
                flow_id = parts[0][6:]  # Remove "@flow:" prefix
                message = parts[1] if len(parts) > 1 else ""
        
        logger.info(f"🔄 Sending to Langflow - Flow ID: {flow_id}, Message: {message}")
        
        # Prepare request to Langflow
        url = f"{LANGFLOW_BASE_URL}/api/v1/run/{flow_id}"
        
        payload = {
            "input_value": message,
            "input_type": "chat",
            "output_type": "chat",
            "tweaks": {}
        }
        
        headers = {
            "Content-Type": "application/json",
            "User-Agent": "OpenWebUI-Langflow-Pipeline/1.0"
        }
        
        # Make request to Langflow
        response = requests.post(
            url,
            json=payload,
            headers=headers,
            timeout=30
        )
        
        if response.status_code == 200:
            result = response.json()
            logger.info(f"✅ Langflow response received")
            
            # Extract response text from Langflow result
            if "outputs" in result and result["outputs"]:
                output = result["outputs"][0]
                if "outputs" in output and output["outputs"]:
                    response_text = output["outputs"][0].get("message", {}).get("text", "")
                    if response_text:
                        return f"🤖 **Langflow Response** (Flow: {flow_id}):\n\n{response_text}"
            
            # Fallback if no proper response found
            return f"🤖 **Langflow Response** (Flow: {flow_id}):\n\n{json.dumps(result, indent=2)}"
            
        else:
            error_msg = f"Langflow API error: {response.status_code} - {response.text}"
            logger.error(error_msg)
            return f"🚨 **Langflow Error**: {error_msg}"
            
    except requests.exceptions.Timeout:
        error_msg = "Langflow request timed out"
        logger.error(error_msg)
        return f"🚨 **Langflow Error**: {error_msg}"
        
    except requests.exceptions.ConnectionError:
        error_msg = "Cannot connect to Langflow - check if service is running"
        logger.error(error_msg)
        return f"🚨 **Langflow Error**: {error_msg}"
        
    except Exception as e:
        error_msg = f"Unexpected error: {str(e)}"
        logger.error(error_msg)
        return f"🚨 **Langflow Error**: {error_msg}"


# Pipeline metadata
PIPELINE_INFO = {
    "name": "Langflow Integration",
    "description": "Forwards chat messages to Langflow workflows",
    "version": "1.0.0",
    "author": "Langflow UI Team"
}
