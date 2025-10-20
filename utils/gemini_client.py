
"""
Simple wrapper for Gemini 2.0 Flash LLM usage.
Reads GEMINI_API_KEY from .env. Uses a minimal HTTP interface via requests.
This wrapper provides a single function `call_gemini(prompt, max_tokens=...)`.
"""
import os
import json
import requests
from dotenv import load_dotenv

load_dotenv()

GEMINI_KEY = os.getenv("GEMINI_API_KEY")

if not GEMINI_KEY:
    # we keep behavior explicit but do not stop execution — caller can decide.
    # For the assignment, ensure user sets GEMINI_API_KEY in .env
    pass

GEMINI_BASE = "https://gemini.googleapis.com/v1"  # placeholder base; wrapper is general

def call_gemini(prompt: str, max_tokens: int = 256, model: str = "gemini-2.0-flash") -> str:
    """
    Call Gemini 2.0 Flash model with simple prompt -> text response.
    NOTE: Depending on the actual API, endpoint and headers may vary; adapt as needed.
    """
    if not GEMINI_KEY:
        raise RuntimeError("GEMINI_API_KEY not set in environment (.env).")

    # Example request structure — adapt to the real Gemini HTTP API / SDK when available.
    url = f"{GEMINI_BASE}/models/{model}:predict"
    headers = {
        "Authorization": f"Bearer {GEMINI_KEY}",
        "Content-Type": "application/json",
    }
    payload = {
        "prompt": prompt,
        "maxTokens": max_tokens,
    }

    resp = requests.post(url, headers=headers, data=json.dumps(payload), timeout=15)
    resp.raise_for_status()
    data = resp.json()
    # Try to extract common fields safely
    text = None
    # common patterns: data['predictions'][0]['content'] or data['output'][0] etc.
    if isinstance(data, dict):
        if "predictions" in data and data["predictions"]:
            text = data["predictions"][0].get("content") or data["predictions"][0].get("output")
        elif "output" in data and isinstance(data["output"], list):
            text = " ".join([str(item) for item in data["output"]])
        else:
            # fallback to full JSON string
            text = json.dumps(data)
    else:
        text = str(data)

    return text or ""
