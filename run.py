#!/usr/bin/env python3
"""
run.py — LR-Bharat-Studio Master Entry Point
Usage:
  python3 run.py                                          # Interactive CLI mode
  python3 run.py --ui                                     # Launch Local Web Studio UI (http://localhost:8080)
  python3 run.py --prompt "Hindi kids story about stars" # Direct prompt
  python3 run.py --prompt "..." --lang Hindi --fmt shorts # With options
"""
import argparse
import json
import sys
import os
import subprocess

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

def launch_web_ui(port=8080):
    print(BANNER)
    print(f"🚀 Launching Local Web Studio UI on http://localhost:{port} ...")
    print("   Close terminal or press Ctrl+C to stop.\n")
    cmd = [sys.executable, os.path.join(STUDIO_DIR, "web_studio.py")]
    subprocess.run(cmd)

def interactive_prompt():
    print(BANNER)
    print("  What would you like to create today?")
    print("  Options:")
    print("    [1] Enter prompt in CLI")
    print("    [2] Open Local Web Studio UI (browser interface)")
    print()
    choice = input("  Select [1/2] (default 1): ").strip()
    if choice == "2":
        launch_web_ui()
        sys.exit(0)

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
    print(BANNER)
    print("🧠 Analyzing request...")
    config = analyze_content(prompt, language=lang, fmt=fmt)
    print(f"   ✅ Detected: [{config['content_type']}] | {config['language']} | "
          f"{config['format']} | {config['target_duration_min']:.1f} min")
    print(f"   🎤 Voice cast : {config['voice_cast']}")
    print(f"   🎵 Music genre: {config['music_genre']}")
    print(f"   🖼  Image style: {config['image_style']}")
    print()

    print("📋 Agent 1 → Planning topic & structure...")
    try:
        from agents.agent1_topic_planner import run as agent1_run
        plan = agent1_run(config)
    except ImportError:
        plan = call_llm(
            f"Create a detailed {config['content_type']} video plan for: {prompt}\n"
            f"Language: {config['language']}, Duration: {config['target_duration_min']} min\n"
            "Return JSON with: title, hook, sections (list of scene titles), moral/takeaway",
            system_prompt="You are a professional YouTube content strategist.",
            mode="fast"
        )
        plan = {"raw": plan}
    print(f"   ✅ Plan ready")

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
            system_prompt="You are an expert children's content scriptwriter.",
            mode="pro"
        )
        script = {"raw": script}
    print(f"   ✅ Script ready")

    print("⚙️  Agent 3 → Building story config...")
    try:
        from agents.agent3_story_configurator import run as agent3_run
        story_config = agent3_run(config, script)
    except ImportError:
        story_config = config
    print(f"   ✅ Config ready")

    print("🎙️  Agent 4 → Generating audio with Chatterbox TTS...")
    try:
        from agents.agent4_audio_runner import run as agent4_run
        audio_result = agent4_run(story_config, script)
        print(f"   ✅ Audio ready: {audio_result.get('output_path', 'see output/audio/')}")
    except ImportError:
        audio_result = {"output_path": "./output/audio/"}

    print("🔍 Agent 5 → Running audio quality check...")
    try:
        from agents.agent5_audio_qa import run as agent5_run
        qa_result = agent5_run(audio_result)
        print(f"   ✅ QA passed: {qa_result.get('score', 'N/A')}")
    except ImportError:
        qa_result = {}

    print("🖼️  Agent 6 → Generating 4K scene images...")
    try:
        from agents.agent6_image_generator import run as agent6_run
        images = agent6_run(story_config, script)
        print(f"   ✅ Images ready: {len(images.get('scenes', []))} scenes")
    except ImportError:
        images = {"scenes": []}

    print("🎬 Agent 7 → Assembling final video...")
    try:
        from agents.agent7_master_orchestrator import run as agent7_run
        final = agent7_run(story_config, audio_result, images, qa_result)
        print(f"\n✨ VIDEO READY: {final.get('video_path', 'see output/video/')}")
    except ImportError:
        final = {"video_path": "./output/video/"}

    print("\n" + "=" * 65)
    print("  📁 Outputs saved in output/ directory")
    print("=" * 65)
    return final

def main():
    parser = argparse.ArgumentParser(description="LR-Bharat-Studio Master Entry Point")
    parser.add_argument("--ui", action="store_true", help="Launch Local Web Studio UI (http://localhost:8080)")
    parser.add_argument("--prompt", type=str, default=None, help="Content request prompt")
    parser.add_argument("--lang", type=str, default="auto", choices=["Hindi", "English", "Both", "auto"])
    parser.add_argument("--fmt", type=str, default="long", choices=["long", "shorts"])
    parser.add_argument("--analyze-only", action="store_true", help="Only run content analysis")
    args = parser.parse_args()

    if args.ui:
        launch_web_ui()
        return

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
