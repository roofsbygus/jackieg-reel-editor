# Caption test — round 1 (2026-11-23)

Clip: `VID20260811162406.mp4` (21.7 s). **The clip is English, not Spanish.** All 10 job-site clips are English.
Reference: `ref/VID20260811162406.txt`, a draft built from where the models agree. Gus must listen and correct it.
Score: `python3 -I scripts/wer.py ref/VID20260811162406.txt <outputs>`

| Engine | Model | Language | WER | Time (warm) |
|---|---|---|---|---|
| HyperFrames 0.9.86 (whisper.cpp 1.9.5) | small.en (upstream default) | — | 3.2% ("drip bed" ×3) | 1.2 s |
| HyperFrames | small | auto | 0% | 1.2 s |
| HyperFrames | medium | auto | 0% | 2.6 s |
| HyperFrames | large-v3 | auto | 0% | 4.3 s |
| HyperFrames | small | **forced es** | **95.7%** (invented Spanish: "rupturio") | ~1 s |
| mlx-whisper 0.4.3 | small | auto → en | 2.1% ("drip bed" ×2) | 1.4 s |
| mlx-whisper | medium | auto → en | 0% | 2.5 s |
| mlx-whisper | large-v3-turbo | auto → en | 0% | 2.4 s |

## Findings
- Every multilingual model detected English correctly.
- Forcing the wrong language produces confident nonsense. Never hard-code the language; detect it, show it, let the user override.
- Every model hears "Trusting Gus" / "Trust and Gus" for "Trust In Gus". Fix: pass the brand name as a vocabulary hint (prompt).
- Cutaway `VID20260811163518` (7 s) came back as "Hello again." The language check is unsure there (en 0.49 / 0.19), which suggests little or no speech, so the words are probably invented. The editor should skip captions on clips with no speech.
- Language check every 5 s (`scripts/langprob.py`): every talking clip is en 1.00 / es 0.00 the whole way through. No hidden Spanish. The other 7 Desktop videos have no audio track.
- Inside the Code tab, PATH has no `/opt/homebrew/bin`, so mlx-whisper couldn't find ffmpeg. Scripts must use full paths.
- On English, HyperFrames (whisper.cpp) matches mlx-whisper. Spanish/Spanglish: see Round 2 below.

## Installed for this test
- `brew install uv` (0.13.9) and `brew install whisper-cpp` (now `whisper.cpp` 1.9.5_2)
- `pruebas/whisper-env`: Python 3.12.16 + mlx-whisper 0.4.3 (versions in `whisper-env-versions.txt`)
- `pruebas/hf-cli`: `hyperframes@0.9.86` exact, with `package-lock.json`, `--ignore-scripts`
- Models: ~5.5 GB in `~/.cache/hyperframes`, ~3.4 GB in `~/.cache/huggingface`

# Round 2: Spanish/Spanglish (2026-11-23)

Clip: `test spanish.mp4` (64 s, QuickTime on the Mac mic, LERU Zoom-class style, Spanish with English roofing/sales words).
Language every 5 s: mostly es 0.66–1.00. English moments (around 55 s, "screen share") show up as en 0.97, which is real Spanglish.
Reference: `ref/test-spanish.txt` (153 words). Built from turbo's output; Gus confirmed all 6 disputed spots by ear. 1 word = 0.65% WER.

| Engine | Model | Lang | WER | Time (64 s clip) |
|---|---|---|---|---|
| HyperFrames | small.en (upstream) | — | **92.2%**: English nonsense, then stuck repeating one line | 1.9 s |
| HyperFrames | small | auto → es | 4.6% | 2.0 s |
| HyperFrames | medium | auto → es | 5.9% (glues words: "Ypues", "Yusando") | 4.6 s |
| HyperFrames | large-v3 | auto → es | 3.9% | 8.0 s |
| HyperFrames | large-v3 | forced es | 3.9% (same as auto) | 7.2 s |
| mlx-whisper | small | auto → es | 5.2% | 2.4 s |
| mlx-whisper | medium | auto → es | 7.8% | 4.8 s |
| mlx-whisper | large-v3-turbo | auto → es | 2.0% | 4.6 s |

- All multilingual models keep English words in English ("leads", "book of business", "checklist", "role plays", "screen share"). Spanglish works without extra effort.
- Upstream's Spanish bug is now proven on Gus's own voice.
- Spots to check by ear: 0:00 "hecho el tocapuertas", 0:08 "clientel", 0:33 "So hoy", 0:51 "¿ok?", 0:53–0:55 "en el zoom" (only small hears it), 1:00 "Oh, y saludos" / "Oye".
- Gus confirmed by ear: "tocapuertas", "clientel", "So hoy", "ok", "en el zoom", "Oh, y saludos".
- Part of every WER is the spelling "toca puertas" vs "tocapuertas" (counted as 2 wrong words). The real gaps are a few words: large-v3 hears "Oye" for "Oh, y"; medium glues words together.

## Decision rule (design doc §11): HyperFrames within ~2 WER points of the best → drop the separate Whisper engine
- Spanish: best mlx large-v3-turbo 2.0%, HyperFrames large-v3 3.9% → 1.9 points apart, **within the rule**.
- English: tied at 0%.
- **Pick: HyperFrames 0.9.86 + whisper.cpp, model large-v3, language auto-detect.** It's 8 s for 64 s of audio. Drop mlx-whisper (`pruebas/whisper-env` and ~3.4 GB in `~/.cache/huggingface` can be deleted once Gus agrees).
- Caveat: one clip per language, recorded on the Mac mic. Re-check on a phone + lav clip before release.

## Cleanup (2026-11-23, approved by Gus)
Deleted: `pruebas/whisper-env` (1.1 GB), the three mlx-community Whisper models (3.4 GB in `~/.cache/huggingface`), uv's Python 3.12.16.
Kept: `uv` (Homebrew), `whisper-env-versions.txt` (to reinstall mlx-whisper 0.4.3 exactly if ever needed), all results and scripts.
HyperFrames large-v3 re-run after cleanup: same result.
