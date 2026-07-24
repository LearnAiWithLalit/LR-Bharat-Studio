#!/usr/bin/env python3
"""
agent1_topic_planner.py — Agent 1: Story Topic & Concept Planner
Uses OmniRoute to generate story concept JSON based on user preferences.
Robust JSON extraction via regex.
Saves: output/plan_topic.json
"""
import json
import os
import re
import sys
from omniroute_client import call_omniroute, DEFAULT_MODEL_FAST

def generate_topic_plan(genre="mystical_forest", language="Hindi", format_type="youtube_long_form", target_duration_min=4.5):
    print(f"\n=================================================================")
    print(f"🤖 AGENT 1: Story Topic Planner [{genre} | {language} | {format_type}]")
    print(f"=================================================================")
    
    system_prompt = "You are an expert story topic planner for kids & family audio-video productions. Always output raw JSON only."
    user_prompt = f"""Generate a story concept JSON for a story generation pipeline.
Genre: {genre} (options: mystical_forest, horror_scary, lullaby_bedtime, heroic_adventure, playful_kids)
Language: {language} (Hindi or English)
Format: {format_type} (youtube_long_form or youtube_shorts)
Target Duration: {target_duration_min} minutes

Output format MUST be valid JSON:
{{
  "title": "चमकती तितली और जादुई पेड़",
  "genre": "{genre}",
  "language": "{language}",
  "format": "{format_type}",
  "aspect_ratio": "16:9",
  "target_duration_min": {target_duration_min},
  "character_roles": ["narrator", "chintu", "meena", "grandpa", "spirit"],
  "moral": "दयालुता और एकता ही सबसे बड़ा खजाना है",
  "setting_description": "प्राचीन जादुई जंगल और बहती चाँदी की नदी",
  "key_scenes": ["बच्चों का जंगल सीमा पर आना", "दादाजी की सीख", "नदी किनारे यात्रा", "वृक्ष देव का प्रकटीकरण", "जादुई फूल का खिलना"]
}}

Respond ONLY with valid JSON."""

    res_raw = call_omniroute(user_prompt, system_prompt=system_prompt, model=DEFAULT_MODEL_FAST, temperature=0.3, max_tokens=2048)
    
    match = re.search(r'\{.*\}', res_raw, re.DOTALL)
    if not match:
        print("Raw OmniRoute Response:\n", res_raw)
        raise ValueError("Could not locate JSON object in OmniRoute response")
        
    json_str = match.group(0)
    topic_data = json.loads(json_str)
    
    out_path = "/media/lalit/HIKVISION1/LR-Bharat-Studio/output/plan_topic.json"
    os.makedirs(os.path.dirname(out_path), exist_ok=True)
    with open(out_path, "w", encoding="utf-8") as f:
        json.dump(topic_data, f, indent=2, ensure_ascii=False)
        
    print(f"✅ Agent 1 Completed: Topic Plan saved to {out_path}")
    print(f"   Title: {topic_data.get('title')}")
    print(f"   Genre: {topic_data.get('genre')} | Format: {topic_data.get('format')}")
    return topic_data

if __name__ == "__main__":
    generate_topic_plan(genre="mystical_forest", language="Hindi", format_type="youtube_long_form", target_duration_min=4.5)
