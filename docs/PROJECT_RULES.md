# 📜 LRNarrator Project Rules — GLOBAL & MANDATORY

> **Target Workspace**: `/media/lalit/HIKVISION1/LR-Bharat-Studio/` & `/media/lalit/HIKVISION1/LRNarrator/chatterbox_v3/`
> **Applies to**: ALL stories, educational videos, science lessons, documentaries, poems, bedtime stories, and future pipeline runs.

---

## 📌 Rule 1 — Infinite Dynamic Content & Format Expansion
1. **Never restrict topics to a fixed set of categories.**
2. The pipeline agent dynamically infers content type, tone, genre, audience, and atmosphere from ANY user request (e.g. Kids stories, AI/Coding lessons, Space exploration, Historical documentaries, Bedtime stories, Spooky mysteries, Cooking lessons, Poetry recitations).

---

## 📌 Rule 2 — Self-Learning Procedural Music & Asset Engine
1. **If a requested topic requires a music style or SFX not currently in our library, `music_generator.py` MUST dynamically compose a new custom procedural track on-the-fly.**
2. The new procedural music track is saved to `reference_voices/`, indexed into the Voice & Audio Registry, and remembered for future learning.
3. Our asset library grows continuously with every production.

---

## 📌 Rule 3 — Voice Cast & Character Classifications
1. **Younger Toddlers**:
   - `kid_young_1`: 3.5s clip from `Kids11.wav` (Younger toddler voice)
   - `kid_young_2`: 7.0s clip from `Kids12.wav` (Younger toddler voice)
2. **Elder Sister / Older Kid**:
   - `kid_elder_sister`: `Kids_girl1.wav` (Meena — older/mature kid tone for elder sister roles)
3. **Dynamic Voice Pool Rotation**:
   - **Never repeat the exact same character cast for every story.**
   - Vary cast setup dynamically: 1–4 kids (younger kids + elder sister) + grandparents/parents/spirits/teachers/expert narrators depending on content context.

---

## 📌 Rule 4 — Contextual Sound Effects (NO Blanket Bell Rings)
1. **Do NOT add blanket bell rings or magic chimes everywhere.**
2. Bell rings / chimes are strictly forbidden unless the script explicitly calls for a magic transformation spell.
3. Use 60s continuous organic wind flow (2.0x-2.5x volume, 30s-60s wave cycle) for forest scenes.

---

## 📌 Rule 5 — Option C Image Engine & YouTube Dual Resolutions
1. **Option C Pipeline**: FLUX.1 Hero Character Reference → DreamShaperXL Lightning + IP-Adapter batch scene renders (~0.8s/img) → 4K Real-ESRGAN / Tile Upscale.
2. **Dual Formats**:
   - **YouTube Long-Form (16:9)**: Base 1920x1080 → 4K UHD (`3840x2160`)
   - **YouTube Shorts (9:16)**: Base 1080x1920 → 4K Vertical (`2160x3840`)
