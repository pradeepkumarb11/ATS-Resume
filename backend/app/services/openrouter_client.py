import requests
import time
from fastapi import HTTPException
from app.config import settings

def call_openrouter(messages: list, model: str | None = None) -> str:
    """
    Calls OpenRouter API with retries and graceful error handling. 
    Returns the content of the response message.
    """
    if not settings.OPENROUTER_API_KEY:
        # Demo mode / Mock response
        return "This is a mock response from OpenRouter (API Key missing)."

    target_model = model or settings.OPENROUTER_MODEL
    url = "https://openrouter.ai/api/v1/chat/completions"
    
    headers = {
        "Authorization": f"Bearer {settings.OPENROUTER_API_KEY}",
        "Content-Type": "application/json",
        "HTTP-Referer": settings.APP_URL,
        "X-Title": "AI Resume Checker & Optimizer",
    }
    
    payload = {
        "model": target_model,
        "messages": messages
    }

    retries = 2
    for attempt in range(retries + 1):
        try:
            response = requests.post(
                url, 
                json=payload, 
                headers=headers, 
                timeout=settings.REQUEST_TIMEOUT
            )
            response.raise_for_status()
            data = response.json()
            return data["choices"][0]["message"]["content"]
            
        except requests.exceptions.RequestException as e:
            if attempt < retries:
                time.sleep(1 * (attempt + 1))  # Exponential-ish backoff
                continue
            
            # If it was the last attempt, raise HTTPException
            error_msg = f"OpenRouter API call failed: {str(e)}"
            if 'response' in locals() and hasattr(response, 'text') and response.text:
                 error_msg += f" | Response: {response.text}"
            
            # Log error internally here if logger available
            raise HTTPException(status_code=502, detail=error_msg)
            
    raise HTTPException(status_code=500, detail="Unknown error in calling OpenRouter API")
