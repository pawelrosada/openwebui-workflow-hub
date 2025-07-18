"""
Simple Langflow Integration Pipeline for Open WebUI
Direct HTTP integration without complex dependencies
"""

import requests
import json


def pipe(user_message: str, model_id: str, messages: list, body: dict) -> str:
    """
    Pipeline function that forwards messages to Langflow
    """
    
    # Configuration
    LANGFLOW_BASE_URL = "http://langflow:7860"
    DEFAULT_FLOW_ID = "basic-chat"  # You'll need to set this to an actual flow ID
    
    try:
        # Parse flow ID if specified in message
        flow_id = DEFAULT_FLOW_ID
        message = user_message
        
        if user_message.startswith("@flow:"):
            parts = user_message.split(" ", 1)
            if len(parts) >= 1:
                flow_id = parts[0][6:]  # Remove "@flow:" prefix
                message = parts[1] if len(parts) > 1 else ""
        
        # Prepare request to Langflow
        url = f"{LANGFLOW_BASE_URL}/api/v1/run/{flow_id}"
        
        payload = {
            "input_value": message,
            "input_type": "chat",
            "output_type": "chat"
        }
        
        headers = {
            "Content-Type": "application/json"
        }
        
        # Make request to Langflow
        response = requests.post(url, json=payload, headers=headers, timeout=30)
        
        if response.status_code == 200:
            result = response.json()
            
            # Extract response from Langflow
            if "outputs" in result and result["outputs"]:
                output = result["outputs"][0]
                if "outputs" in output and output["outputs"]:
                    response_text = output["outputs"][0].get("message", {}).get("text", "")
                    if response_text:
                        return f"🤖 **Langflow** (Flow: {flow_id}):\n\n{response_text}"
            
            return f"🤖 **Langflow** (Flow: {flow_id}):\n\n{json.dumps(result, indent=2)}"
            
        else:
            return f"🚨 **Langflow Error**: HTTP {response.status_code} - {response.text}"
            
    except requests.exceptions.Timeout:
        return "🚨 **Langflow Error**: Request timed out"
        
    except requests.exceptions.ConnectionError:
        return "🚨 **Langflow Error**: Cannot connect to Langflow service"
        
    except Exception as e:
        return f"🚨 **Langflow Error**: {str(e)}"
