#!/usr/bin/env python3
"""
brain/llm_router.py — Smart LLM & Combo Router with Primary + Fallback Combos & Model Inspection
Priority chain:
  1. OmniRoute Primary (e.g. auto/claude/opus or custom project combo)
  2. OmniRoute Fallback (e.g. auto/claude or antigravity/gemini-3.5-flash-low)
  3. FreeBuff CLI       (100% free fallback, MiniMax M3 + DeepSeek V4)

Agents call call_llm() and get exact model resolution feedback.
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
        content = data["choices"][0]["message"]["content"].strip()
        resolved_model = data.get("model", model)
        return content, resolved_model

def _call_freebuff(prompt, system_prompt="", timeout=60):
    combined = f"{system_prompt}\n\n{prompt}".strip() if system_prompt else prompt
    try:
        result = subprocess.run(
            ["npx", "freebuff", "--json", "--prompt", combined],
            capture_output=True, text=True, timeout=timeout
        )
        if result.returncode == 0 and result.stdout.strip():
            try:
                out = json.loads(result.stdout)
                res_text = out.get("response", result.stdout).strip()
                res_model = out.get("model", "FreeBuff: MiniMax-M3 / DeepSeek-V4")
                return res_text, res_model
            except json.JSONDecodeError:
                return result.stdout.strip(), "FreeBuff: MiniMax-M3"
    except (FileNotFoundError, subprocess.TimeoutExpired):
        pass

    node_bin = FREEBUFF_NODE if os.path.exists(FREEBUFF_NODE) else "node"
    with tempfile.NamedTemporaryFile(mode="w", suffix=".js", delete=False) as f:
        f.write(f"""
const {{ execSync }} = require('child_process');
process.stdout.write(JSON.stringify({{error: "freebuff_not_installed"}}));
""")
        tmp = f.name
    try:
        result = subprocess.run([node_bin, tmp], capture_output=True, text=True, timeout=10)
        return result.stdout.strip(), "FreeBuff Fallback"
    finally:
        os.unlink(tmp)

def call_llm(prompt, system_prompt="You are a helpful AI assistant.", mode="fast",
             fallback_mode=None, temperature=0.3, max_tokens=4096, return_meta=False):
    """
    Public API for all agents.
    If return_meta=True, returns tuple: (response_text, resolved_model_name, backend_name)
    Otherwise returns response_text string.
    """
    messages = [
        {"role": "system", "content": system_prompt},
        {"role": "user",   "content": prompt},
    ]

    # Resolve target primary model
    if mode == "fast":
        primary_model = OMNIROUTE_MODEL_FAST
    elif mode == "pro":
        primary_model = OMNIROUTE_MODEL_PRO
    else:
        primary_model = mode

    # 1. Try OmniRoute Primary Combo / Model
    if mode != "free":
        try:
            content, resolved_model = _call_omniroute(messages, primary_model, temperature, max_tokens)
            print(f"[LLM Router] ✅ OmniRoute Primary [{primary_model}] → Resolved to exact model: [{resolved_model}]")
            if return_meta:
                return content, resolved_model, f"OmniRoute ({primary_model})"
            return content
        except Exception as e:
            print(f"[LLM Router] ⚠️  OmniRoute Primary [{primary_model}] failed ({e}).")

    # 2. Try OmniRoute Secondary Fallback Combo / Model if specified
    if fallback_mode and fallback_mode not in (mode, "free"):
        fallback_target = OMNIROUTE_MODEL_FAST if fallback_mode == "fast" else \
                         OMNIROUTE_MODEL_PRO if fallback_mode == "pro" else fallback_mode
        try:
            content, resolved_model = _call_omniroute(messages, fallback_target, temperature, max_tokens)
            print(f"[LLM Router] ✅ OmniRoute Fallback [{fallback_target}] → Resolved to exact model: [{resolved_model}]")
            if return_meta:
                return content, resolved_model, f"OmniRoute Fallback ({fallback_target})"
            return content
        except Exception as e:
            print(f"[LLM Router] ⚠️  OmniRoute Fallback [{fallback_target}] also failed ({e}).")

    # 3. Fallback: FreeBuff (100% free, no API key)
    try:
        content, resolved_model = _call_freebuff(prompt, system_prompt)
        if content and "freebuff_not_installed" not in content:
            print(f"[LLM Router] ✅ FreeBuff (free fallback) → Resolved model: [{resolved_model}]")
            if return_meta:
                return content, resolved_model, "FreeBuff (Free Fallback)"
            return content
    except Exception as e:
        print(f"[LLM Router] ❌ FreeBuff also failed: {e}")

    raise RuntimeError(f"All LLM backends failed (Primary: {primary_model}, Fallback: {fallback_mode}). Check OmniRoute (localhost:20128) or install FreeBuff.")

if __name__ == "__main__":
    print("Testing LLM Router with Model Meta return...")
    text, res_model, backend = call_llm('Respond with JSON: {"status": "ok"}', mode="auto/claude/opus", return_meta=True)
    print(f"Response: {text}\nResolved Model: {res_model}\nBackend: {backend}")
