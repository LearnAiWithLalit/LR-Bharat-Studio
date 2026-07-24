# FreeBuff — Free LLM Fallback

FreeBuff is the **100% free AI coding agent** used as a fallback brain
when OmniRoute is not running or API keys are exhausted.

## What is FreeBuff?

- **Website**: https://freebuff.com
- **Free models**: MiniMax M3, DeepSeek V4 Pro, Kimi K2.7, MiMo 2.5
- **No API key** · **No subscription** · **No credit card**
- Works in India (limited mode: 6 sessions/hour)

## Install

```bash
npm install -g freebuff
```

## How It's Used in This Pipeline

`brain/llm_router.py` automatically falls back to FreeBuff when OmniRoute fails:

```
OmniRoute (your keys) → FreeBuff (free) → Error
```

You never need to configure anything — it just works.

## Note on the Bundled Node Binary

The `node` binary in this folder is the Node.js runtime bundled with FreeBuff.
It is NOT committed to git (see `.gitignore`).

After cloning, install FreeBuff via:
```bash
npm install -g freebuff
```
or use the system Node.js (`node --version`).
