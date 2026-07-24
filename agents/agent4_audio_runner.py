#!/usr/bin/env python3
# agent4_audio_runner.py — Agent 4: Audio Generation Runner & Mixer
# Runs Chatterbox v3 TTS, procedural music, 60s organic wind, and multi-track SFX mixing.
# Saves: output/audio_master.wav

import os, sys, re, time
import numpy as np

os.environ["HSA_OVERRIDE_GFX_VERSION"] = "11.0.0"
os.environ["HSA_ENABLE_SDMA"] = "0"
os.environ["PYTORCH_ATTENTION_BACKEND"] = "eager"
os.environ["ROCR_VISIBLE_DEVICES"] = "0"

import torch, soundfile as sf
import json

# Add chatterbox_v3 scripts to sys.path
CHATTERBOX_SCRIPTS = "/media/lalit/HIKVISION1/LRNarrator/chatterbox_v3/scripts"
sys.path.append(CHATTERBOX_SCRIPTS)

from music_generator import generate_procedural_music

R = "/media/lalit/HIKVISION1/LRNarrator/chatterbox_v3/reference_voices"
SR = 24000

def clean_hindi_text(text):
    text = re.sub(r"\([^)]*\)", "", text)
    text = re.sub(r"[A-Za-z]+", "", text)
    text = re.sub(r"[\U0001F300-\U0001FFFF]", "", text)
    text = text.replace(":-","।").replace(":","।").replace("\u2014",", ")
    text = re.sub(r"[।]{2,}", "।", text)
    return re.sub(r"\s+", " ", text).strip().strip("।").strip()

def strict_vad_clean(wav, sr=24000, thresh=0.008, fade_ms=40):
    fl = int(sr * 0.01)
    out = []
    for i in range(0, len(wav), fl):
        f = wav[i:i+fl]
        rms = np.sqrt(np.mean(f.astype(np.float64)**2))
        if rms < thresh:
            out.append(np.zeros_like(f))
        else:
            out.append(f)
    r = np.concatenate(out)
    
    mask = np.abs(r) > thresh
    if np.any(mask):
        start = np.argmax(mask)
        end = len(r) - np.argmax(mask[::-1])
        r = r[start:end]
        
    fade_len = int(sr * fade_ms / 1000)
    if len(r) > fade_len:
        r[-fade_len:] *= np.linspace(1.0, 0.0, fade_len).astype(np.float32)
    return r

def build_smooth_wind_bed(total_len, wind_clip, sr=24000):
    clip_len = len(wind_clip)
    overlap = int(sr * 5.0)
    step = clip_len - overlap
    
    num_clips = int(np.ceil((total_len + overlap) / step))
    wind_bed = np.zeros(num_clips * step + clip_len, dtype=np.float32)
    
    shaped_clip = wind_clip.copy().astype(np.float32)
    for i in range(num_clips):
        start = i * step
        end = start + clip_len
        wind_bed[start:end] += shaped_clip
        
    return wind_bed[:total_len]

def run_audio_generation():
    print(f"\n=================================================================")
    print(f"🤖 AGENT 4: Audio Generation Runner (Chatterbox v3)")
    print(f"=================================================================")
    
    config_path = "/media/lalit/HIKVISION1/LR-Bharat-Studio/output/story_config.json"
    script_path = "/media/lalit/HIKVISION1/LR-Bharat-Studio/output/story_script.json"
    out_master_path = "/media/lalit/HIKVISION1/LR-Bharat-Studio/output/audio_master.wav"
    
    with open(config_path, "r", encoding="utf-8") as f:
        config = json.load(f)
    with open(script_path, "r", encoding="utf-8") as f:
        script = json.load(f)
        
    # 1. Load Chatterbox Multilingual TTS Model
    device = "cuda" if torch.cuda.is_available() else "cpu"
    print(f"Device: {device}\nLoading Chatterbox model...")
    from chatterbox.mtl_tts import ChatterboxMultilingualTTS
    model = ChatterboxMultilingualTTS.from_pretrained(device=device)
    
    # Voice Map & TTS Parameters per Character
    REF = config["character_voice_map"]
    PARAMS = {
        "narrator": dict(language_id="hi", exaggeration=0.35, temperature=0.50, cfg_weight=0.52),
        "chintu":   dict(language_id="hi", exaggeration=0.45, temperature=0.65, cfg_weight=0.48),
        "meena":    dict(language_id="hi", exaggeration=0.45, temperature=0.60, cfg_weight=0.50),
        "grandpa":  dict(language_id="hi", exaggeration=0.32, temperature=0.50, cfg_weight=0.52),
        "spirit":   dict(language_id="hi", exaggeration=0.38, temperature=0.48, cfg_weight=0.54),
    }
    
    # 2. Synthesize Speech Track
    all_speech_parts = []
    speech_segments = []
    current_pos = 0
    prev_char = None
    
    for idx, item in enumerate(script, 1):
        char = item.get("character", "narrator")
        raw_text = item.get("text", "")
        pause_sec = item.get("pause_sec", 0.5)
        sfx_type = item.get("sfx")
        
        text = clean_hindi_text(raw_text)
        if not text: continue
        
        if char != prev_char and prev_char is not None:
            p_len = int(SR * 0.20)
            all_speech_parts.append(np.zeros(p_len, dtype=np.float32))
            current_pos += p_len
            
        print(f"[{idx:02d}/{len(script)}][{char:10s}] {text}")
        try:
            ref_path = REF.get(char, REF["narrator"])
            params = {**PARAMS.get(char, PARAMS["narrator"]), "audio_prompt_path": ref_path}
            wav = model.generate(text, **params)
            wav_np = wav.squeeze().detach().cpu().numpy().astype(np.float32) if isinstance(wav, torch.Tensor) else np.squeeze(np.array(wav)).astype(np.float32)
            wav_np = strict_vad_clean(wav_np, SR)
            
            start_idx = current_pos
            all_speech_parts.append(wav_np)
            current_pos += len(wav_np)
            end_idx = current_pos
            
            speech_segments.append((start_idx, end_idx, sfx_type))
            
            pause_samples = int(SR * pause_sec)
            all_speech_parts.append(np.zeros(pause_samples, dtype=np.float32))
            current_pos += pause_samples
            
            prev_char = char
        except Exception as e:
            print(f"   ERROR generating line {idx}: {e}")
            
    speech_track = np.concatenate(all_speech_parts)
    total_len = len(speech_track)
    
    # 3. Load / Generate Procedural Music & SFX
    genre = config.get("genre", "mystical_forest")
    music_file = generate_procedural_music(genre=genre, duration_sec=float(total_len/SR) + 10.0, seed=42)
    music_sfx, _ = sf.read(music_file)
    
    wind_sfx, _      = sf.read(f"{R}/forest_wind_rich_sfx.wav")
    water_sfx, _     = sf.read(f"{R}/water_stream_sfx.wav")
    birds_sfx, _     = sf.read(f"{R}/birds_chirping_sfx.wav")
    footsteps_sfx, _ = sf.read(f"{R}/footsteps_sfx.wav")
    
    # 4. Mix Audio Layers
    # Wind Bed (vol=0.16)
    wind_bed = build_smooth_wind_bed(total_len, wind_sfx, SR)
    sfx_track = wind_bed * config["audio_config"]["wind_volume"]
    
    # Music Bed (vol=0.05)
    num_music_tiles = int(np.ceil(total_len / len(music_sfx)))
    music_bed = np.tile(music_sfx, num_music_tiles)[:total_len].astype(np.float32)
    sfx_track += (music_bed * config["audio_config"]["music_volume"])
    
    # Contextual Dynamic SFX Swells
    for start_idx, end_idx, sfx_type in speech_segments:
        seg_len = end_idx - start_idx
        if sfx_type == "wind":
            gust_boost = 0.30
            swell = np.sin(np.linspace(0, np.pi, seg_len)).astype(np.float32) ** 0.8
            sfx_track[start_idx:end_idx] += wind_bed[start_idx:end_idx] * (gust_boost * swell)
        elif sfx_type == "water":
            num_tiles = int(np.ceil(seg_len / len(water_sfx)))
            w_seg = np.tile(water_sfx, num_tiles)[:seg_len].astype(np.float32)
            sfx_track[start_idx:end_idx] += w_seg * 0.35
        elif sfx_type == "birds":
            num_tiles = int(np.ceil(seg_len / len(birds_sfx)))
            b_seg = np.tile(birds_sfx, num_tiles)[:seg_len].astype(np.float32)
            sfx_track[start_idx:end_idx] += b_seg * 0.38
        elif sfx_type == "footsteps":
            num_tiles = int(np.ceil(seg_len / len(footsteps_sfx)))
            f_seg = np.tile(footsteps_sfx, num_tiles)[:seg_len].astype(np.float32)
            sfx_track[start_idx:end_idx] += f_seg * 0.30

    # 5. Master Output Peak Normalization
    final = speech_track + sfx_track
    peak = np.max(np.abs(final))
    if peak > 0.01:
        final = (final / peak) * 0.92
        
    os.makedirs(os.path.dirname(out_master_path), exist_ok=True)
    sf.write(out_master_path, final, SR)
    print(f"\n✅ Agent 4 Completed: Master Audio track saved to {out_master_path}")
    print(f"   Duration: {len(final)/SR:.2f}s ({len(final)/SR/60:.2f} min)")
    return out_master_path

if __name__ == "__main__":
    run_audio_generation()
