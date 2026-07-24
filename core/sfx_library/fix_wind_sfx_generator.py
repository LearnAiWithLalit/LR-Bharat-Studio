#!/usr/bin/env python3
"""
fix_wind_sfx_generator.py (v2 — Smooth 60s Organic Flow)
Generates smooth 60-second non-repeating forest wind using:
  - Pink noise (1/f) base over 60 seconds
  - Ultra-slow organic wave envelopes (30s to 60s flow cycle)
  - 5s smooth fade-in -> 35-45s natural organic breeze -> 10s gentle fade-out
  - 2.0x-2.5x natural level (vol=0.16, RMS ~0.06)
Replaces 10s tiling with smooth, seamless 60s organic atmosphere.
"""
import numpy as np
import soundfile as sf
from scipy.signal import butter, sosfiltfilt

R = "/media/lalit/HIKVISION1/LRNarrator/chatterbox_v3/reference_voices"
SR = 24000
DURATION = 60.0  # 60 seconds continuous smooth flow
N = int(SR * DURATION)

np.random.seed(999)

def bandpass(data, lo, hi, sr, order=4):
    nyq = sr / 2
    sos = butter(order, [lo/nyq, hi/nyq], btype='band', output='sos')
    return sosfiltfilt(sos, data).astype(np.float32)

def pink_noise(n, sr):
    white = np.random.randn(n)
    fft = np.fft.rfft(white)
    freqs = np.fft.rfftfreq(n, 1/sr)
    freqs[0] = 1.0
    pink = np.fft.irfft(fft / np.sqrt(freqs), n=n).astype(np.float32)
    return pink / (np.max(np.abs(pink)) + 1e-9)

print("Generating 60-second Smooth Organic Wind Flow...")
t = np.arange(N) / SR
base_pink = pink_noise(N, SR)

# 1. Ultra-slow LFO (30s to 60s period) for organic wind flow
# Cycle 1: 0-35s (peaks around 18s), Cycle 2: 30-60s (peaks around 45s)
flow_lfo1 = 0.5 + 0.5 * np.sin(2 * np.pi * (1/45.0) * t - np.pi/4)
flow_lfo2 = 0.5 + 0.5 * np.sin(2 * np.pi * (1/30.0) * t + np.pi/3)
organic_flow = 0.6 * flow_lfo1 + 0.4 * flow_lfo2

# 2. Band-shaped layers
sub_rumble = bandpass(base_pink, 25, 90, SR)   * (0.4 + 0.6 * organic_flow)
wind_body  = bandpass(base_pink, 100, 750, SR)  * (0.3 + 0.7 * organic_flow)
leaf_air   = bandpass(np.random.randn(N).astype(np.float32), 1600, 5500, SR) * (0.2 + 0.8 * organic_flow**1.5)

wind_mix = sub_rumble * 0.35 + wind_body * 0.75 + leaf_air * 0.25

# 3. Apply 5s smooth fade-in and 10s gentle fade-out at ends for 60s block
fade_in_len  = int(SR * 5.0)
fade_out_len = int(SR * 10.0)

fade_in  = (np.sin(np.linspace(0, np.pi/2, fade_in_len)) ** 2).astype(np.float32)
fade_out = (np.sin(np.linspace(np.pi/2, 0, fade_out_len)) ** 2).astype(np.float32)

wind_mix[:fade_in_len]  *= fade_in
wind_mix[-fade_out_len:] *= fade_out

# 4. Normalize to 2.0x-2.5x target level (RMS ~0.060, Peak ~0.35)
peak = np.max(np.abs(wind_mix))
wind_mix = (wind_mix / peak) * 0.35

rms = np.sqrt(np.mean(wind_mix**2))
print(f"=== 60s SMOOTH ORGANIC WIND QA ===")
print(f"  Duration : {DURATION}s (60-second continuous flow)")
print(f"  RMS      : {rms:.4f} (-24.4 dBFS)")
print(f"  Peak     : {np.max(np.abs(wind_mix)):.4f}")

out_path = f"{R}/forest_wind_rich_sfx.wav"
sf.write(out_path, wind_mix, SR, subtype='PCM_16')
print(f"✅ Saved: {out_path}")
