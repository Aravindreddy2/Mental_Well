# app/llama_api.py
import requests
from app.utils.config import LLAMA_API_URL, LLAMA_API_KEY

def llama_generate(prompt: str) -> str:
    """Generate empathetic mental health responses using Groq’s LLaMA API."""
    headers = {
        "Authorization": f"Bearer {LLAMA_API_KEY}",
        "Content-Type": "application/json"
    }

    payload = {
        "model": "llama-3.1-8b-instant",  # ✅ Groq model name
        "messages": [
            {"role": "system", "content": "You are a kind and empathetic mental health support assistant for youth."},
            {"role": "user", "content": prompt}
        ],
        "temperature": 0.7,
        "max_tokens": 512
    }

    try:
        response = requests.post(LLAMA_API_URL, headers=headers, json=payload, timeout=30)
        response.raise_for_status()  # raise if 4xx/5xx error
        data = response.json()

        # ✅ Groq uses OpenAI-style response
        if "choices" in data and len(data["choices"]) > 0:
            return data["choices"][0]["message"]["content"].strip()

        # Handle edge cases (bad responses)
        return f"[Unexpected response: {data}]"

    except requests.exceptions.HTTPError as e:
        return f"[HTTP error: {e.response.status_code} - {e.response.text}]"
    except Exception as e:
        return f"[Error calling LLaMA API: {e}]"
