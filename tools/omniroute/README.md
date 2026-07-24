# 🔌 OmniRoute Setup & Configuration Guide

OmniRoute is a self-hosted Docker container that acts as a unified OpenAI-compatible LLM proxy. It routes requests to multiple AI model providers (Gemini, OpenAI, Claude, Groq, DeepSeek, Ollama) using your own API keys.

---

## 🚀 Step 1: Start OmniRoute Container

From the project root directory, run:

```bash
bash tools/omniroute/start.sh
```

This starts the Docker container and exposes two local endpoints:
- 🌐 **Dashboard UI**: [http://localhost:3000](http://localhost:3000)
- 🔌 **OpenAI Proxy Endpoint**: [http://localhost:20128/v1](http://localhost:20128/v1)

---

## 🔑 Step 2: Configure Provider API Keys

1. Open **[http://localhost:3000](http://localhost:3000)** in your web browser.
2. Go to **Provider Nodes** / **API Keys**.
3. Add your preferred provider API keys:
   - **Google Gemini**: Add your Gemini API key (`antigravity/gemini-3.5-flash-low` or `agy/gemini-3.1-pro-high`)
   - **OpenAI**: Add your OpenAI key (`gpt-4o`, `gpt-4o-mini`)
   - **DeepSeek / Groq / Anthropic**: Add keys as needed.

---

## ⚙️ Step 3: Link OmniRoute with LR-Bharat-Studio

You can set your OmniRoute API key in any of the following 3 ways:

### Option A: Via Local Web Studio UI (Recommended)
Launch `python3 run.py --ui`, open [http://localhost:8080](http://localhost:8080), and select **OmniRoute** under LLM Engine.

### Option B: Via `config/config.yaml`
Edit `config/config.yaml`:
```yaml
llm:
  omniroute_url: "http://localhost:20128/v1/chat/completions"
  omniroute_key: "sk-YOUR_OMNIROUTE_KEY"
  model_fast: "antigravity/gemini-3.5-flash-low"
  model_pro: "agy/gemini-3.1-pro-high"
```

### Option C: Via Environment Variable
```bash
export OMNIROUTE_API_KEY="sk-YOUR_OMNIROUTE_KEY"
```

---

## 🆓 What if a User Has NO API Keys?

**No problem!** LR-Bharat-Studio includes an automatic fallback to **FreeBuff**:

- **Zero setup** · **No API keys required** · **No credit card**
- `brain/llm_router.py` automatically falls back to FreeBuff if OmniRoute is offline or keys run out.
- Install FreeBuff: `npm install -g freebuff`
