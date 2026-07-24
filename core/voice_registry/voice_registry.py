#!/usr/bin/env python3
"""
voice_registry.py — Dynamic Reference Voice Registry for Chatterbox v3
Updated with:
  - kid_young_1: 3.5s from Kids11.wav (Younger kid)
  - kid_young_2: 7.0s from Kids12.wav (Younger kid)
  - kid_elder_sister: Kids_girl1.wav (Elder sister / bigger kid)
  - Full pool of 20+ reference voices for dynamic rotation across stories & educational videos.
"""
import os
import soundfile as sf
import numpy as np

R = "/media/lalit/HIKVISION1/LRNarrator/chatterbox_v3/reference_voices"

VOICE_REGISTRY = {
    # Younger Kids (Boy / Girl)
    "kid_young_1": f"{R}/kid_young_1.wav",       # 3.5s clip from Kids11.wav
    "kid_young_2": f"{R}/kid_young_2.wav",       # 7.0s clip from Kids12.wav
    "kid_boy_1":    f"{R}/kids1 boy.wav",
    "kid_boy_2":    f"{R}/kids 2 boy.wav",
    "kid_boy_3":    f"{R}/kids 3 boy.wav",       # Chintu

    # Elder Sister / Older Girl Kid
    "kid_elder_sister": f"{R}/Kids_girl1.wav",   # Meena (Elder sister tone)
    "fairy_female":     f"{R}/fariy female.wav",

    # Male Narrators & Characters
    "male_narrator_1": f"{R}/male_Narrator_01.wav",
    "male_narrator_2": f"{R}/male_3.wav",
    "male_character_1": f"{R}/male_5.wav",
    "male_character_2": f"{R}/male_6.wav",
    "male_character_3": f"{R}/male_7.wav",

    # Female Narrators, Teachers & Characters
    "female_narrator_1": f"{R}/female_Narrator_01.wav",
    "female_character_1": f"{R}/female_3.wav",
    "female_character_2": f"{R}/female_3_1.wav",
    "female_character_3": f"{R}/female_4_1.wav",
    "female_character_4": f"{R}/female_5_1.wav",
    "female_character_5": f"{R}/female_6_1.wav",
    "female_character_6": f"{R}/female_08.wav",
    "female_character_7": f"{R}/female_8.wav",

    # Grandparents / Elders
    "grandpa_1": f"{R}/Grandpa1.wav",
    "grandpa_2": f"{R}/Grandpa2.wav",
    "grandpa_3": f"{R}/Grandpa05.wav",
    "grandpa_4": f"{R}/Grandpa06.wav",
    "grandpa_5": f"{R}/Grandpa_00.wav",
    "grandma_1": f"{R}/GrandMaa01.wav",
}

def get_voice_info(key):
    path = VOICE_REGISTRY.get(key)
    if not path or not os.path.exists(path):
        return None
    data, sr = sf.read(path)
    dur = len(data) / sr
    return {"key": key, "path": path, "duration_sec": round(dur, 2), "sample_rate": sr}

def list_all_voices():
    print("=== DYNAMIC VOICE REGISTRY ===")
    for category, keys in [
        ("Younger Kids", ["kid_young_1", "kid_young_2", "kid_boy_1", "kid_boy_2", "kid_boy_3"]),
        ("Elder Sister / Older Kids", ["kid_elder_sister", "fairy_female"]),
        ("Male Narrators & Experts", ["male_narrator_1", "male_narrator_2", "male_character_1", "male_character_2", "male_character_3"]),
        ("Female Narrators & Teachers", ["female_narrator_1", "female_character_1", "female_character_2", "female_character_3", "female_character_4", "female_character_5", "female_character_6", "female_character_7"]),
        ("Grandparents / Elders", ["grandpa_1", "grandpa_2", "grandpa_3", "grandpa_4", "grandpa_5", "grandma_1"]),
    ]:
        print(f"\n📁 {category}:")
        for k in keys:
            info = get_voice_info(k)
            if info:
                print(f"   • {k:20s} -> {info['duration_sec']:5.2f}s clip | {info['path']}")

if __name__ == "__main__":
    list_all_voices()
