#!/usr/bin/env python3
"""
run.py — LR-Bharat-Studio Master Entry Point
Usage:
  python3 run.py                                          # Interactive mode
  python3 run.py --prompt "Hindi kids story about stars" # Direct prompt
  python3 run.py --prompt "..." --lang Hindi --fmt shorts # With options
  python3 run.py --prompt "..." --lang English --fmt long # YouTube long form
"""
import argparse
import json
import sys
import os

# ── Path bootstrap ──────────────────────────────────────────
STUDIO_DIR = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, STUDIO_DIR)

from brain.content_analyzer import analyze_content
from brain.llm_router import call_llm


BANNER = """
╔══════════════════════════════════════════════════════════════════╗
║          LR-Bharat-Studio  🎬  AI Video Pipeline               ║
║   Kids Stories · Education · Documentary · Poetry · More        ║
╚══════════════════════════════════════════════════════════════════╝
"""

def interactive_prompt():
    print(BANNER)
    print("  What would you like to create today?")
    print("  Examples:")
    print("    • Hindi kids story about a magical forest with talking animals")
    print("    • 60 second reel teaching ABCD to toddlers")
    print("    • YouTube video about Artificial Intelligence")
    print("    • Bedtime lullaby story — calm and soothing")
    print("    • Spooky Halloween ghost story in English")
    print("    • Ramayana episode for kids in Hindi")
    print()
    prompt = input("  Your request: ").strip()
    if not prompt:
        print("❌  Empty prompt. Exiting.")
        sys.exit(1)

    print()
    lang = input("  Language? [Hindi / English / Both] (default: auto): ").strip() or "auto"
    fmt  = input("  Format?   [shorts / long] (default: long): ").strip() or "auto"
    fmt  = "youtube_shorts" if fmt.lower() in ("shorts", "short", "reel") else \
           "youtube_long_form" if fmt.lower() in ("long", "youtube", "longform") else "auto"
    return prompt, lang, fmt


def run_pipeline(prompt: str, lang: str = "auto", fmt: str = "auto"):
    """
    Full 7-Agent pipeline:
      Agent 1 → Topic / title plan
      Agent 2 → Full narration script
      Agent 3 → Story config (cast, music, SFX)
      Agent 4 → Audio generation (Chatterbox TTS)
      Agent 5 → Audio QA
      Agent 6 → Image generation (FLUX + SDXL Lightning + 4K upscale)
      Agent 7 → Master orchestrator (assembles final video)
    """
    print(BANNER)

    # ── Step 0: Smart content analysis ──────────────────────
    print("🧠 Analyzing request...")
    config = analyze_content(prompt, language=lang, fmt=fmt)
    print(f"   ✅ Detected: [{config['content_type']}] | {config['language']} | "
          f"{config['format']} | {config['target_duration_min']:.1f} min")
    print(f"   🎤 Voice cast : {config['voice_cast']}")
    print(f"   🎵 Music genre: {config['music_genre']}")
    print(f"   🖼  Image style: {config['image_style']}")
    print()

    # ── Step 1: Topic Planner ───────────────────────────────
    print("📋 Agent 1 → Planning topic & structure...")
    try:
        from agents.agent1_topic_planner import run as agent1_run
        plan = agent1_run(config)
    except ImportError:
        plan = call_llm(
            f"Create a detailed {config['content_type']} video plan for: {prompt}\n"
            f"Language: {config['language']}, Duration: {config['target_duration_min']} min\n"
            "Return JSON with: title, hook, sections (list of scene titles), moral/takeaway",
            system_prompt="You are a professional YouTube content strategist for Indian kids content.",
            mode="fast"
        )
        plan = {"raw": plan}
    print(f"   ✅ Plan ready")

    # ── Step 2: Script Writer ───────────────────────────────
    print("✍️  Agent 2 → Writing narration script...")
    try:
        from agents.agent2_script_writer import run as agent2_run
        script = agent2_run(config, plan)
    except ImportError:
        script = call_llm(
            f"Write a full narration script for: {prompt}\n"
            f"Content type: {config['content_type']}\n"
            f"Language: {config['language']}, Duration: {config['target_duration_min']} min\n"
            f"Voice cast: {config['voice_cast']}\n"
            "Return JSON array: [{character, line, emotion, sfx_hint}]",
            system_prompt="You are an expert children's content scriptwriter. Write engaging, age-appropriate scripts.",
            mode="pro"
        )
        script = {"raw": script}
    print(f"   ✅ Script ready")

    # ── Step 3: Story Configurator ──────────────────────────
    print("⚙️  Agent 3 → Building story config...")
    try:
        from agents.agent3_story_configurator import run as agent3_run
        story_config = agent3_run(config, script)
    except ImportError:
        story_config = config
    print(f"   ✅ Config ready")

    # ── Step 4: Audio Generation ────────────────────────────
    print("🎙️  Agent 4 → Generating audio with Chatterbox TTS...")
    try:
        from agents.agent4_audio_runner import run as agent4_run
        audio_result = agent4_run(story_config, script)
        print(f"   ✅ Audio ready: {audio_result.get('output_path', 'see output/audio/')}")
    except ImportError:
        print("   ⚠️  Agent 4 not loaded (run directly from chatterbox_v3)")
        audio_result = {"output_path": "./output/audio/"}

    # ── Step 5: Audio QA ────────────────────────────────────
    print("🔍 Agent 5 → Running audio quality check...")
    try:
        from agents.agent5_audio_qa import run as agent5_run
        qa_result = agent5_run(audio_result)
        print(f"   ✅ QA passed: {qa_result.get('score', 'N/A')}")
    except ImportError:
        print("   ⚠️  Agent 5 not loaded — skipping audio QA")
        qa_result = {}

    # ── Step 6: Image Generation ─────────────────────────────
    print("🖼️  Agent 6 → Generating 4K scene images...")
    try:
        from agents.agent6_image_generator import run as agent6_run
        images = agent6_run(story_config, script)
        print(f"   ✅ Images ready: {len(images.get('scenes', []))} scenes")
    except ImportError:
        print("   ⚠️  Agent 6 not loaded — skipping image generation")
        images = {"scenes": []}

    # ── Step 7: Master Orchestrator ─────────────────────────
    print("🎬 Agent 7 → Assembling final video...")
    try:
        from agents.agent7_master_orchestrator import run as agent7_run
        final = agent7_run(story_config, audio_result, images, qa_result)
        print(f"\n✨ VIDEO READY: {final.get('video_path', 'see output/video/')}")
        print(f"   Resolution : {final.get('resolution', config.get('aspect_ratio', '16:9'))}")
        print(f"   Duration   : {final.get('duration_sec', '?')}s")
    except ImportError:
        print("   ⚠️  Agent 7 not loaded — all parts are in output/ folder")
        final = {"video_path": "./output/video/"}

    print()
    print("=" * 65)
    print("  📁 Outputs saved in:")
    print(f"     Audio  → {os.path.join(STUDIO_DIR, 'output/audio')}")
    print(f"     Images → {os.path.join(STUDIO_DIR, 'output/images')}")
    print(f"     Video  → {os.path.join(STUDIO_DIR, 'output/video')}")
    print(f"     QA     → {os.path.join(STUDIO_DIR, 'output/qa_reports')}")
    print("=" * 65)
    return final


def main():
    parser = argparse.ArgumentParser(
        description="LR-Bharat-Studio — AI Video Generation Pipeline"
    )
    parser.add_argument("--prompt", type=str, default=None,
                        help="Content request (what video to create)")
    parser.add_argument("--lang",   type=str, default="auto",
                        choices=["Hindi", "English", "Both", "auto"],
                        help="Language (default: auto-detect)")
    parser.add_argument("--fmt",    type=str, default="long",
                        choices=["long", "shorts"],
                        help="Format: long (16:9 YouTube) or shorts (9:16 Shorts)")
    parser.add_argument("--analyze-only", action="store_true",
                        help="Only run content analysis, don't generate")
    args = parser.parse_args()

    fmt = "youtube_shorts" if args.fmt == "shorts" else "youtube_long_form"

    if args.prompt:
        prompt, lang, fmt_out = args.prompt, args.lang, fmt
    else:
        prompt, lang, fmt_out = interactive_prompt()

    if args.analyze_only:
        config = analyze_content(prompt, language=lang, fmt=fmt_out)
        print(json.dumps(config, indent=2, ensure_ascii=False))
        return

    run_pipeline(prompt, lang=lang, fmt=fmt_out)


if __name__ == "__main__":
    main()
