#!/usr/bin/env python3
"""
brain/llm_router.py — Smart LLM & Combo Router
Priority chain:
  1. OmniRoute (localhost:20128) — routes to user-configured Combos (e.g. auto/claude, auto/claude/opus) or provider models
  2. FreeBuff CLI   — 100% free, no API key needed (fallback brain)

Agents call call_llm() with mode="fast", mode="pro", or a custom Combo model name (e.g. "auto/claude").
"""
import json
import os
import subprocess
import tempfile
import urllib.request
import urllib.error

# ── OmniRoute (primary) ────────────────────────────────────────────────
OMNIROUTE_URL   = "http://localhost:20128/v1/chat/completions"
OMNIROUTE_KEY   = os.environ.get("OMNIROUTE_API_KEY", "sk-6667040940fc2fd7-8ba520-cd973981")
OMNIROUTE_MODEL_FAST = os.environ.get("OMNIROUTE_MODEL_FAST", "antigravity/gemini-3.5-flash-low")
OMNIROUTE_MODEL_PRO  = os.environ.get("OMNIROUTE_MODEL_PRO",  "agy/gemini-3.1-pro-high")

# ── FreeBuff (free fallback) ───────────────────────────────────────────
FREEBUFF_NODE   = os.path.join(os.path.dirname(__file__), "../tools/freebuff/node")
FREEBUFF_NPKG   = "freebuff"   # npm package name

def _call_omniroute(messages, model, temperature=0.3, max_tokens=4096, timeout=45):
    headers = {
        "Content-Type":  "application/json",
        "Authorization": f"Bearer {OMNIROUTE_KEY}",
    }
    payload = {
        "model": model,
        "messages": messages,
        "temperature": temperature,
        "max_tokens": max_tokens,
        "stream": False,
    }
    req = urllib.request.Request(
        OMNIROUTE_URL,
        data=json.dumps(payload).encode(),
        headers=headers,
    )
    with urllib.request.urlopen(req, timeout=timeout) as resp:
        data = json.loads(resp.read().decode())
        return data["choices"][0]["message"]["content"].strip()

def _call_freebuff(prompt, system_prompt="", timeout=60):
    """
    Calls FreeBuff CLI in headless mode to run a single prompt.
    FreeBuff uses free open-source models (MiniMax M3, DeepSeek, Kimi).
    No API key or account required.
    """
    combined = f"{system_prompt}\n\n{prompt}".strip() if system_prompt else prompt
    try:
        result = subprocess.run(
            ["npx", "freebuff", "--json", "--prompt", combined],
            capture_output=True, text=True, timeout=timeout
        )
        if result.returncode == 0 and result.stdout.strip():
            try:
                out = json.loads(result.stdout)
                return out.get("response", result.stdout).strip()
            except json.JSONDecodeError:
                return result.stdout.strip()
    except (FileNotFoundError, subprocess.TimeoutExpired):
        pass

    # Try via node binary directly if npx not found
    node_bin = FREEBUFF_NODE if os.path.exists(FREEBUFF_NODE) else "node"
    with tempfile.NamedTemporaryFile(mode="w", suffix=".js", delete=False) as f:
        f.write(f"""
const {{ execSync }} = require('child_process');
process.stdout.write(JSON.stringify({{error: "freebuff_not_installed"}}));
""")
        tmp = f.name
    try:
        result = subprocess.run([node_bin, tmp], capture_output=True, text=True, timeout=10)
        return result.stdout.strip()
    finally:
        os.unlink(tmp)

def call_llm(prompt, system_prompt="You are a helpful AI assistant.", mode="fast",
             temperature=0.3, max_tokens=4096):
    """
    Public API for all agents.
    mode can be:
      - "fast" : uses OMNIROUTE_MODEL_FAST (antigravity/gemini-3.5-flash-low)
      - "pro"  : uses OMNIROUTE_MODEL_PRO (agy/gemini-3.1-pro-high)
      - "free" : forces FreeBuff fallback (100% Free, no API key)
      - Any custom Combo or Model ID string (e.g., "auto/claude", "auto/claude/opus", "Image_Model")
    """
    messages = [
        {"role": "system", "content": system_prompt},
        {"role": "user",   "content": prompt},
    ]

    # Resolve target model
    if mode == "fast":
        target_model = OMNIROUTE_MODEL_FAST
    elif mode == "pro":
        target_model = OMNIROUTE_MODEL_PRO
    else:
        target_model = mode

    # Try OmniRoute first if not explicitly forced to 'free'
    if mode != "free":
        try:
            response = _call_omniroute(messages, target_model, temperature, max_tokens)
            print(f"[LLM Router] ✅ OmniRoute [{target_model}] responded.")
            return response
        except Exception as e:
            print(f"[LLM Router] ⚠️  OmniRoute [{target_model}] failed ({e}). Falling back to FreeBuff...")

    # Fallback: FreeBuff (100% free, no API key)
    try:
        response = _call_freebuff(prompt, system_prompt)
        if response and "freebuff_not_installed" not in response:
            print("[LLM Router] ✅ FreeBuff (free fallback) responded.")
            return response
    except Exception as e:
        print(f"[LLM Router] ❌ FreeBuff also failed: {e}")

    raise RuntimeError("All LLM backends failed. Check OmniRoute (localhost:20128) or install FreeBuff: npm install -g freebuff")

if __name__ == "__main__":
    print("Testing LLM Router with custom Combo model string...")
    resp = call_llm('Respond with JSON: {"status": "ok", "router": "working"}', mode="auto/claude")
    print("Response:", resp)
