#!/usr/bin/env python3
"""
agent3_story_configurator.py — Agent 3: Story Configurator
Maps character cast from voice_registry.py, procedural music genre, SFX settings, and resolution targets.
Saves: output/story_config.json
"""
import json
import os
import sys

# Import voice registry from chatterbox_v3
sys.path.append("/media/lalit/HIKVISION1/LRNarrator/chatterbox_v3/scripts")
from voice_registry import VOICE_REGISTRY

def configure_story():
    print(f"\n=================================================================")
    print(f"🤖 AGENT 3: Story Configurator (Voice Cast & Music Mapping)")
    print(f"=================================================================")
    
    topic_path = "/media/lalit/HIKVISION1/LR-Bharat-Studio/output/plan_topic.json"
    script_path = "/media/lalit/HIKVISION1/LR-Bharat-Studio/output/story_script.json"
    
    with open(topic_path, "r", encoding="utf-8") as f:
        topic = json.load(f)
    with open(script_path, "r", encoding="utf-8") as f:
        script = json.load(f)
        
    genre = topic.get("genre", "mystical_forest")
    format_type = topic.get("format", "youtube_long_form")
    
    # 1. Map Characters to Voice Registry
    char_map = {
        "narrator": VOICE_REGISTRY["male_narrator_1"],
        "chintu":   VOICE_REGISTRY["kid_boy_3"],      # Boy kid 3
        "meena":    VOICE_REGISTRY["kid_girl_1"],     # Girl kid 1
        "grandpa":  VOICE_REGISTRY["grandpa_1"],     # Grandpa 1
        "spirit":   VOICE_REGISTRY["male_character_2"]# Spirit male 6
    }
    
    # 2. Configure Format & Resolution
    if format_type == "youtube_shorts":
        format_config = {
            "format_name": "YouTube Shorts (9:16)",
            "aspect_ratio": "9:16",
            "base_w": 1080, "base_h": 1920,
            "final_w": 2160, "final_h": 3840,
            "upscale_factor": 2.0
        }
    else:
        format_config = {
            "format_name": "YouTube Long-Form (16:9)",
            "aspect_ratio": "16:9",
            "base_w": 1920, "base_h": 1080,
            "final_w": 3840, "final_h": 2160,
            "upscale_factor": 2.0
        }
        
    # 3. Configure Audio & SFX settings
    audio_config = {
        "genre": genre,
        "wind_volume": 0.16,          # 2.2x balanced wind level
        "wind_flow_cycle_sec": 60.0,   # 60s organic wave cycle
        "music_volume": 0.05,         # Soft background bed
        "allow_blanket_chimes": False # Strictly forbidden per project rules
    }
    
    config = {
        "story_title": topic.get("title"),
        "genre": genre,
        "format": format_config,
        "character_voice_map": char_map,
        "audio_config": audio_config,
        "total_lines": len(script)
    }
    
    out_path = "/media/lalit/HIKVISION1/LR-Bharat-Studio/output/story_config.json"
    os.makedirs(os.path.dirname(out_path), exist_ok=True)
    with open(out_path, "w", encoding="utf-8") as f:
        json.dump(config, f, indent=2, ensure_ascii=False)
        
    print(f"✅ Agent 3 Completed: Story Config saved to {out_path}")
    print(f"   Mapped Characters: {list(char_map.keys())}")
    print(f"   Format: {format_config['format_name']} ({format_config['final_w']}x{format_config['final_h']})")
    return config

if __name__ == "__main__":
    configure_story()
