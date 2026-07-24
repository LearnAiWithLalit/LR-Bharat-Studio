# 🎬 LR-Bharat-Studio

> **AI-powered Hindi/English Video Generation Pipeline**
> Kids Stories · Education · Documentary · Poetry · YouTube Shorts & Long-Form

[![Python](https://img.shields.io/badge/Python-3.10+-blue.svg)](https://python.org)
[![License](https://img.shields.io/badge/License-MIT-green.svg)](LICENSE)
[![Platform](https://img.shields.io/badge/Platform-Linux%20%7C%20AMD%20ROCm%20%7C%20NVIDIA-orange.svg)](https://github.com)
[![LLM](https://img.shields.io/badge/LLM-OmniRoute%20%2B%20FreeBuff%20%28Free%29-purple.svg)](https://freebuff.com)

---

## 📖 What Is This?

LR-Bharat-Studio is a **fully automated, 7-agent AI video pipeline** that turns a single text prompt into a complete YouTube-ready video with:

- 🎙️ **Voice cloned narration** (Chatterbox TTS — local, no API)
- 🎵 **Procedural background music** (auto-generated per genre)
- 🌬️ **Organic SFX beds** (wind, forest, classroom, space, etc.)
- 🖼️ **4K AI images** (FLUX.1 hero reference → DreamShaperXL Lightning + IP-Adapter)
- 🎬 **Final assembled video** (MP4, 16:9 or 9:16)

Everything runs **locally on your GPU** — no cloud rendering costs.

---

## 🧠 Smart Multi-Format Agent

Just tell it what you want. It figures out the rest:

| Your Prompt | Auto-Detected |
|---|---|
| *"Hindi kids story about magical forest"* | `kids_story` · Hindi · Storybook art · Forest SFX |
| *"60 second reel teaching ABCD"* | `kids_educational` · Shorts · Bright cartoon · Classroom |
| *"AI documentary for YouTube"* | `tech_educational` · English · Tech vector · UI SFX |
| *"Spooky Halloween ghost story"* | `spooky_mystery` · Dark atmospheric · Horror music |
| *"Ramayana episode for kids"* | `mythology_spiritual` · Hindi · Epic painting · Temple |
| *"Bedtime lullaby for baby"* | `bedtime_lullaby` · Soft pastel · Lullaby music |

Supported content types (extensible — adds new ones automatically):
`kids_story` · `kids_educational` · `tech_educational` · `history_documentary`
`bedtime_lullaby` · `poem_recitation` · `spooky_mystery` · `cooking_lifestyle`
`space_science` · `mythology_spiritual` · *(any new type you describe)*

---

## 🔧 Architecture

```
run.py  (entry point)
  │
  ├── brain/
  │   ├── content_analyzer.py   ← Smart intent detection (no LLM needed)
  │   └── llm_router.py         ← OmniRoute (primary) → FreeBuff (free fallback)
  │
  ├── agents/
  │   ├── agent1_topic_planner.py       ← Title, hook, scene structure
  │   ├── agent2_script_writer.py       ← Full narration script (character lines)
  │   ├── agent3_story_configurator.py  ← Voice cast, SFX, music selection
  │   ├── agent4_audio_runner.py        ← Chatterbox TTS + music + SFX mix
  │   ├── agent5_audio_qa.py            ← RMS check, clipping, VAD QA
  │   ├── agent6_image_generator.py     ← FLUX hero + SDXL Lightning + 4K upscale
  │   └── agent7_master_orchestrator.py ← Assemble final MP4
  │
  ├── core/
  │   ├── voice_registry/    ← Reference WAV clips + voice_registry.py
  │   ├── music_library/     ← Procedural music generator (self-learning)
  │   └── sfx_library/       ← SFX generator (wind, forest, classroom…)
  │
  ├── tools/
  │   ├── omniroute/         ← Self-hosted LLM proxy (your API keys)
  │   └── freebuff/          ← Free LLM fallback (no API key needed)
  │
  ├── config/
  │   └── config.yaml        ← All settings in one place
  │
  └── output/
      ├── audio/             ← Generated WAV files
      ├── images/            ← 4K scene images
      ├── video/             ← Final MP4
      └── qa_reports/        ← Audio QA logs
```

---

## 🚀 Quick Start

### 1. Clone & Setup

```bash
git clone https://github.com/yourusername/LR-Bharat-Studio.git
cd LR-Bharat-Studio
bash setup.sh
```

### 2. Add Your Voice Clips

Place reference WAV files (3–10 sec, clean audio) in `core/voice_registry/`:

```
core/voice_registry/
  kid_young_1.wav       ← Chintu (young boy, ~5yr)
  kid_young_2.wav       ← Pappu (boy, ~7yr)
  Kids_girl1.wav        ← Meena (elder sister voice)
  male_narrator_1.wav   ← Main narrator (add your own)
```

See `core/voice_registry/README.md` for full voice guide.

### 3. Configure LLM (Optional)

The pipeline works out of the box with **FreeBuff** (100% free, no signup).
For higher quality, add your API keys to OmniRoute:

```bash
# Start OmniRoute LLM proxy
bash tools/omniroute/start.sh
# Then open http://localhost:3000 to add your API keys
```

### 4. Generate Your First Video

```bash
# Interactive mode (asks you what to create)
python3 run.py

# Direct prompt
python3 run.py --prompt "Hindi kids story about a magical forest with talking animals"

# YouTube Shorts (9:16)
python3 run.py --prompt "Teach ABCD to toddlers" --fmt shorts --lang Hindi

# Just see what the AI detects (no generation)
python3 run.py --prompt "Spooky Halloween ghost story" --analyze-only
```

---

## 🧩 LLM Backend — Zero Cost Architecture

The pipeline uses a **two-tier free LLM strategy**:

| Tier | Backend | Cost | API Key? | Quality |
|------|---------|------|----------|---------|
| 1st  | **OmniRoute** | Your own keys | Yes (yours) | Best |
| 2nd  | **FreeBuff** | 100% Free | ❌ None | Good |

FreeBuff uses: MiniMax M3, DeepSeek V4 Pro, Kimi K2.7, MiMo 2.5 — all free.

---

## 🎤 Voice System

```
Character        →  Voice File         →  Use Case
─────────────────────────────────────────────────────
kid_young_1      →  kid_young_1.wav    →  Young boy (Chintu, ~5yr)
kid_young_2      →  kid_young_2.wav    →  Slightly older boy (Pappu, ~7yr)
kid_elder_sister →  Kids_girl1.wav     →  Meena — older sister feel
narrator         →  male_narrator_1    →  Story narration (male)
female_narrator  →  female_narrator_1  →  Story narration (female)
grandpa_1        →  grandpa_1.wav      →  Grandfather character
```

Stories are cast **dynamically** — sometimes 2 kids, sometimes all 4, sometimes just narrator + 1 kid. It never feels repetitive.

---

## 🖼️ Image Pipeline — Option C (Best Quality + Speed)

```
Step A: FLUX.1 Schnell      → Hero reference image per character (1–2s)
Step B: DreamShaperXL Light → Scene batch via IP-Adapter (character locked)
Step C: Real-ESRGAN 4K      → Upscale to 3840×2160 (long) or 2160×3840 (shorts)
```

IP-Adapter weight `0.62` = optimal balance of style freedom + character consistency.

---

## 📺 Output Formats

| Format | Resolution | Use Case |
|--------|-----------|---------|
| YouTube Long-Form | **3840×2160 (4K 16:9)** | Main channel videos |
| YouTube Shorts | **2160×3840 (4K 9:16)** | Shorts / Reels |

---

## 🔊 Music Engine (Self-Learning)

The music generator learns from every run:

- Starts with 10 built-in genre profiles
- When a new genre/mood is requested → **synthesizes it procedurally**
- Saves the new track to `core/music_library/generated/`
- Indexes it for re-use in future videos
- Gets better over time without any manual work

---

## 📁 Project Structure

| Folder | What Goes Here |
|--------|---------------|
| `agents/` | The 7 AI agents (topic → script → audio → image → video) |
| `brain/` | LLM router + smart content analyzer |
| `core/voice_registry/` | Voice WAV clips + registry (add your own) |
| `core/music_library/` | Procedural music engine + generated tracks |
| `core/sfx_library/` | SFX generator (wind, forest, classroom…) |
| `tools/omniroute/` | Self-hosted LLM proxy (Docker) |
| `tools/freebuff/` | Free LLM fallback (Node.js) |
| `config/` | All settings (config.yaml) |
| `output/` | Generated audio / images / video |
| `docs/` | Pipeline design docs + rules |

---

## 🛠️ Requirements

| Component | Requirement |
|-----------|------------|
| OS | Ubuntu 22.04+ |
| GPU | AMD RX 7900 XTX (ROCm 6.2) or NVIDIA RTX (CUDA 12+) |
| RAM | 16 GB+ system RAM |
| VRAM | 16 GB+ recommended |
| Python | 3.10+ |
| Docker | For OmniRoute LLM proxy |
| Node.js | For FreeBuff (or use bundled binary) |

---

## 🤝 Contributing

1. Fork the repo
2. Add a new content profile in `brain/content_analyzer.py`
3. Add voice clips to `core/voice_registry/`
4. Test with `python3 run.py --analyze-only --prompt "your test"`
5. Open a PR!

---

## 📄 License

MIT License — free to use, modify, and distribute.

---

## 🙏 Credits

- **Chatterbox TTS** — Local voice cloning
- **FLUX.1 Schnell** — Character reference images (Black Forest Labs)
- **DreamShaperXL Lightning** — Fast scene generation (Lykon)
- **OmniRoute** — Self-hosted LLM proxy
- **FreeBuff** — Free AI coding & LLM agent
- **Real-ESRGAN** — 4K upscaling

---

*Made with ❤️ for Indian kids content creators. Publish once, run forever.*
