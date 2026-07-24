# Voice Registry — Reference Clips

Place your reference voice WAV files here. These are used by Chatterbox TTS
to clone character voices. Keep them short (3–10 seconds, clean, no background noise).

## Required Voice Files

| Filename          | Character         | Notes                                  |
|-------------------|-------------------|----------------------------------------|
| kid_young_1.wav   | Chintu (boy ~5yr) | Trimmed from Kids11.wav (first 3.5s)   |
| kid_young_2.wav   | Pappu (boy ~7yr)  | Trimmed from Kids12.wav (first 7.0s)   |
| Kids_girl1.wav    | Meena (elder sis) | Older girl voice, feels mature than kids|

## Optional Voice Files (add as needed)

| Filename              | Character             |
|-----------------------|-----------------------|
| male_narrator_1.wav   | Main narrator (male)  |
| female_narrator_1.wav | Main narrator (female)|
| male_narrator_2.wav   | Narrator #2 (deep)    |
| female_character_1.wav| Female supporting role|
| grandpa_1.wav         | Grandfather character |

## Best Practices

- 16-bit PCM WAV, 24000 Hz (or 44100 Hz — resampled automatically)
- No music, no SFX, no room echo in reference clips
- The first few seconds are most important for voice capture
- Run through VAD (strict_vad_clean threshold=0.008) if clips have noise

## Adding New Voices

1. Record or extract 3–10 seconds of clean voice audio
2. Save as WAV in this folder
3. Register in `core/voice_registry/voice_registry.py` under `VOICE_REGISTRY`
4. The content_analyzer will auto-select voices based on content type
