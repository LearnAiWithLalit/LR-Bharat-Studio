#!/usr/bin/env python3
"""
omniroute_client.py — Universal OmniRoute API Client
Routes LLM requests for Agent 1 (Topic), Agent 2 (Script), Agent 3 (Config), and Agent 7 (Orchestrator)
through the local OmniRoute server (http://localhost:20128/v1/chat/completions) to save agent tokens.
"""
import json
import urllib.request
import urllib.error

OMNIROUTE_URL = "http://localhost:20128/v1/chat/completions"
OMNIROUTE_KEY = "sk-6667040940fc2fd7-8ba520-cd973981"  # Valid OmniRoute API Key

DEFAULT_MODEL_FAST = "antigravity/gemini-3.5-flash-low"
DEFAULT_MODEL_PRO  = "agy/gemini-3.1-pro-high"

def call_omniroute(prompt, system_prompt="You are a helpful AI assistant.", model=DEFAULT_MODEL_FAST, temperature=0.3, max_tokens=2048):
    """
    Calls OmniRoute LLM endpoint in non-streaming mode.
    Returns string content response.
    """
    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {OMNIROUTE_KEY}"
    }
    
    payload = {
        "model": model,
        "messages": [
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": prompt}
        ],
        "temperature": temperature,
        "max_tokens": max_tokens,
        "stream": False
    }
    
    try:
        req = urllib.request.Request(OMNIROUTE_URL, data=json.dumps(payload).encode("utf-8"), headers=headers)
        with urllib.request.urlopen(req, timeout=45) as resp:
            data = json.loads(resp.read().decode("utf-8"))
            return data["choices"][0]["message"]["content"].strip()
    except urllib.error.HTTPError as e:
        err_body = e.read().decode("utf-8") if e.fp else ""
        print(f"❌ OmniRoute HTTP Error {e.code}: {err_body}")
        raise RuntimeError(f"OmniRoute HTTP {e.code}")
    except Exception as e:
        print(f"❌ OmniRoute Request Error: {e}")
        raise

if __name__ == "__main__":
    print("Testing omniroute_client.py...")
    res = call_omniroute("Respond with JSON: {\"status\": \"ok\", \"omniroute_client\": \"ready\"}")
    print("Response:\n", res)
