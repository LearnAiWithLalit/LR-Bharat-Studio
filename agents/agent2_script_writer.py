#!/usr/bin/env python3
"""
agent2_script_writer.py — Agent 2: Story Writer
Uses OmniRoute to write full multi-character story script based on Topic Plan.
Clean JSON parsing with robust truncation recovery.
Saves: output/story_script.json
"""
import json
import os
import re
import sys
from omniroute_client import call_omniroute, DEFAULT_MODEL_FAST

def write_story_script():
    print(f"\n=================================================================")
    print(f"🤖 AGENT 2: Story Script Writer")
    print(f"=================================================================")
    
    topic_path = "/media/lalit/HIKVISION1/LR-Bharat-Studio/output/plan_topic.json"
    if not os.path.exists(topic_path):
        raise FileNotFoundError(f"Missing topic plan: {topic_path}")
        
    with open(topic_path, "r", encoding="utf-8") as f:
        topic = json.load(f)
        
    system_prompt = "You are a professional children's audiobook script writer. Output raw JSON only."
    user_prompt = f"""Write a multi-character story script in JSON array format:
Title: {topic.get('title')}
Genre: {topic.get('genre')}
Language: {topic.get('language')}

ROLES TO USE: "narrator", "chintu", "meena", "grandpa", "spirit"

RULES:
1. Output format MUST be a valid JSON array of objects:
[
  {{"chapter": "ch01", "character": "narrator", "text": "एक पुराने जंगल की कहानी...", "pause_sec": 0.5, "sfx": "wind"}},
  {{"chapter": "ch01", "character": "chintu", "text": "देखो मीना! वहाँ रोशनी है!", "pause_sec": 0.5, "sfx": null}},
  {{"chapter": "ch01", "character": "meena", "text": "हाँ भैया! चलो चलते हैं!", "pause_sec": 0.5, "sfx": "birds"}}
]
2. Write exactly 25 to 30 lines in {topic.get('language')}.
3. Use ONLY character names: "narrator", "chintu", "meena", "grandpa", "spirit".
4. sfx tags can ONLY be: "wind", "water", "birds", "footsteps", or null.

Respond ONLY with complete valid JSON array."""

    res_raw = call_omniroute(user_prompt, system_prompt=system_prompt, model=DEFAULT_MODEL_FAST, temperature=0.3, max_tokens=8192)
    
    # Clean output
    res_str = res_raw.strip()
    if res_str.startswith("```json"):
        res_str = res_str[7:]
    if res_str.startswith("```"):
        res_str = res_str[3:]
    if res_str.endswith("```"):
        res_str = res_str[:-3]
    res_str = res_str.strip()
    
    # Find last closing bracket
    if "[" in res_str and not res_str.rstrip().endswith("]"):
        last_obj = res_str.rfind("}")
        if last_obj != -1:
            res_str = res_str[:last_obj+1] + "\n]"
            
    script_data = json.loads(res_str)
    
    out_path = "/media/lalit/HIKVISION1/LR-Bharat-Studio/output/story_script.json"
    os.makedirs(os.path.dirname(out_path), exist_ok=True)
    with open(out_path, "w", encoding="utf-8") as f:
        json.dump(script_data, f, indent=2, ensure_ascii=False)
        
    print(f"✅ Agent 2 Completed: Story Script saved to {out_path} ({len(script_data)} dialogue lines)")
    return script_data

if __name__ == "__main__":
    write_story_script()
