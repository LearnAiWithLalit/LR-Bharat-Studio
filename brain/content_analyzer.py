#!/usr/bin/env python3
"""
brain/content_analyzer.py — Smart Content & Intent Analyzer
Given ANY free-form user request, infers:
  - content_type   (unlimited: kids_story, educational_abcd, tech_ai, poem, history, cooking, space…)
  - language       (Hindi / English / Both)
  - format         (youtube_long_form 16:9 / youtube_shorts 9:16)
  - target_duration_min
  - voice_cast     (auto-selected from voice_registry based on context)
  - music_genre    (auto-selected or dynamically synthesized)
  - image_style    (storybook / cartoon / tech / documentary / fantasy / dark / pastel)
  - sfx_profile    (forest / classroom / tech_ui / night / spooky)
"""
import json, re

# ── Inference Rules (expandable, never hardcoded) ──────────────────────
CONTENT_PROFILES = {
    "kids_story": {
        "keywords": ["story", "kahani", "fairy", "magic", "adventure", "forest", "animal",
                     "princess", "dragon", "monster", "bedtime", "jungle"],
        "voice_cast": ["narrator", "kid_young_1", "kid_young_2", "kid_elder_sister", "grandpa_1"],
        "music_genre": "mystical_forest",
        "image_style": "storybook_watercolor_fantasy",
        "sfx_profile": "forest",
    },
    "kids_educational": {
        "keywords": ["abcd", "alphabet", "ka kha ga", "number", "rhyme", "poem", "nursery",
                     "learn letters", "sikh", "padhna", "count", "color", "shape"],
        "voice_cast": ["female_narrator_1", "kid_young_1", "kid_young_2"],
        "music_genre": "playful_kids",
        "image_style": "bright_cartoon_2d_with_text",
        "sfx_profile": "classroom",
    },
    "tech_educational": {
        "keywords": ["ai", "artificial intelligence", "coding", "programming", "science",
                     "technology", "space", "robot", "machine learning", "computer"],
        "voice_cast": ["male_narrator_1", "female_narrator_1"],
        "music_genre": "heroic_adventure",
        "image_style": "modern_4k_tech_vector",
        "sfx_profile": "tech_ui",
    },
    "history_documentary": {
        "keywords": ["history", "itihaas", "ancient", "war", "king", "empire", "freedom",
                     "documentary", "civilization", "explorer", "discovery"],
        "voice_cast": ["male_narrator_1", "male_narrator_2"],
        "music_genre": "heroic_adventure",
        "image_style": "cinematic_documentary_painting",
        "sfx_profile": "neutral_ambient",
    },
    "bedtime_lullaby": {
        "keywords": ["bedtime", "lullaby", "sleep", "sona", "raat", "moon", "stars",
                     "calm", "rest", "goodnight", "shubh ratri"],
        "voice_cast": ["female_character_1", "kid_young_1"],
        "music_genre": "lullaby_bedtime",
        "image_style": "soft_moonlight_pastel",
        "sfx_profile": "night",
    },
    "poem_recitation": {
        "keywords": ["poem", "poetry", "kavita", "rhyme", "shayari", "song", "geet",
                     "ballad", "recitation", "verse"],
        "voice_cast": ["female_narrator_1", "kid_elder_sister"],
        "music_genre": "mystical_forest",
        "image_style": "illustrated_literary_art",
        "sfx_profile": "soft_ambient",
    },
    "spooky_mystery": {
        "keywords": ["horror", "scary", "spooky", "ghost", "bhoot", "mystery", "dark",
                     "haunted", "thriller", "detective", "fear"],
        "voice_cast": ["male_narrator_2", "kid_young_1", "kid_young_2"],
        "music_genre": "horror_scary",
        "image_style": "dark_atmospheric_low_key",
        "sfx_profile": "spooky",
    },
    "cooking_lifestyle": {
        "keywords": ["recipe", "cooking", "food", "khana", "bake", "chef", "kitchen",
                     "ingredient", "dish", "taste", "nutrition"],
        "voice_cast": ["female_narrator_1", "female_character_1"],
        "music_genre": "playful_kids",
        "image_style": "warm_lifestyle_photography",
        "sfx_profile": "kitchen",
    },
    "space_science": {
        "keywords": ["space", "planet", "galaxy", "star", "nasa", "cosmos", "universe",
                     "rocket", "astronaut", "moon", "solar system"],
        "voice_cast": ["male_narrator_1"],
        "music_genre": "space_scifi",
        "image_style": "cinematic_space_4k",
        "sfx_profile": "space_ambient",
    },
    "mythology_spiritual": {
        "keywords": ["mythology", "purana", "ramayan", "mahabharat", "krishna", "shiva",
                     "goddess", "temple", "spiritual", "god", "bhagwan", "mantra"],
        "voice_cast": ["male_narrator_1", "grandpa_1"],
        "music_genre": "mythology_epic",
        "image_style": "divine_epic_oil_painting",
        "sfx_profile": "temple_ambient",
    },
}

def analyze_content(user_request: str, language: str = "auto", fmt: str = "auto") -> dict:
    """
    Infers content profile from any free-form user request.
    Returns full config dict for Agent 3 / Agent 7 to use.
    """
    req_lower = user_request.lower()

    # Match content profile
    matched_type = "kids_story"  # safe default
    best_score = 0
    for ctype, profile in CONTENT_PROFILES.items():
        score = sum(1 for kw in profile["keywords"] if kw in req_lower)
        if score > best_score:
            best_score = score
            matched_type = ctype

    profile = CONTENT_PROFILES[matched_type]

    # Infer language
    if language == "auto":
        hindi_signals = ["hindi", "हिंदी", "kahani", "बच्चे", "sikh", "padhna", "ka kha ga",
                         "geet", "bhoot", "khana", "raat", "shubh", "kavita"]
        language = "Hindi" if any(s in req_lower for s in hindi_signals) else "English"

    # Infer format
    if fmt == "auto":
        shorts_signals = ["short", "reel", "tiktok", "60 sec", "1 min", "quick", "brief"]
        fmt = "youtube_shorts" if any(s in req_lower for s in shorts_signals) else "youtube_long_form"

    # Infer duration
    dur_match = re.search(r"(\d+)\s*(min|minute|sec|second)", req_lower)
    if dur_match:
        val = int(dur_match.group(1))
        unit = dur_match.group(2)
        duration = val / 60 if "sec" in unit else float(val)
    else:
        duration = 1.0 if fmt == "youtube_shorts" else 5.0

    return {
        "content_type":      matched_type,
        "user_request":      user_request,
        "language":          language,
        "format":            fmt,
        "aspect_ratio":      "9:16" if fmt == "youtube_shorts" else "16:9",
        "target_duration_min": duration,
        "voice_cast":        profile["voice_cast"],
        "music_genre":       profile["music_genre"],
        "image_style":       profile["image_style"],
        "sfx_profile":       profile["sfx_profile"],
    }

if __name__ == "__main__":
    tests = [
        "Create a Hindi kids story about a magical forest with talking animals",
        "Make a 60 second educational reel teaching ABCD to toddlers",
        "Educational video about Artificial Intelligence for YouTube",
        "A spooky ghost story for Halloween in English",
        "Space exploration documentary about Mars mission",
        "Bedtime lullaby story for baby - calm and soothing",
        "Ramayana story for kids in Hindi",
        "Cooking recipe video for healthy breakfast",
    ]
    for t in tests:
        r = analyze_content(t)
        print(f"\n📌 Input: {t[:60]}")
        print(f"   Type: {r['content_type']:25s} | Lang: {r['language']:8s} | Music: {r['music_genre']}")
        print(f"   Cast: {r['voice_cast']}")
