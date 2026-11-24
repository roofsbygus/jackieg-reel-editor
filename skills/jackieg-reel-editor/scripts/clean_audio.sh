#!/usr/bin/env bash
# Clean a talking-head voice track for job-site footage (wind on the lav, traffic, generators, saws):
#   1. rumble cut below ~90 Hz (wind and handling noise live there, a voice doesn't)
#   2. DeepFilterNet voice isolation: "strong" (default: full strength + post-filter) or "light" (30 dB cap)
#   3. gentle EQ, de-essing and 2.5:1 compression, then two-pass loudness to -14 LUFS (Instagram/TikTok level)
# Picked by ear on the windiest job-site test clip: strong took the voice-to-background gap from 16 dB to ~49 dB.
# The old fallback (ffmpeg afftdn + noise gate) made wind worse (16 -> 10 dB), so there is no fallback: DeepFilterNet is required.
# Usage: clean_audio.sh <clip> <out.wav> [--strong|--light|--no-denoise]
#        default: brand.json "cleanup" ("strong" | "light"), else strong.
set -euo pipefail
source "$(dirname "$0")/reel_env.sh"   # Homebrew + ~/.local/bin on PATH (Code tab doesn't load ~/.zprofile)
IN="$1"; OUT="$2"; MODE="${3:-}"
if [ -z "$MODE" ]; then
  MODE="--$(python3 -c "import json,os,sys;p=os.path.expanduser(os.environ.get('REELS_HOME','~/reels'))+'/brand.json';print((json.load(open(p)) if os.path.exists(p) else {}).get('cleanup','strong'))" 2>/dev/null || echo strong)"
fi
TMP="$(mktemp -d)"; trap 'rm -rf "$TMP"' EXIT

# mono 48 kHz, rumble cut (two 2-pole high-pass stages = a steep 24 dB/octave slope at 90 Hz)
ffmpeg -v error -y -i "$IN" -vn -ac 1 -ar 48000 -af "highpass=f=90:p=2,highpass=f=90:p=2" "$TMP/raw.wav"
SRC="$TMP/raw.wav"

if [ "$MODE" != "--no-denoise" ]; then
  if ! command -v deepFilter >/dev/null 2>&1; then
    echo "JG-RUIDO: falta DeepFilterNet (limpieza de ruido). / DeepFilterNet is missing. Fix: bash scripts/setup_denoise.sh" >&2
    exit 1
  fi
  if [ "$MODE" = "--light" ]; then DF=(-a 30); else DF=(--pf); fi   # strong: no attenuation cap + post-filter
  deepFilter "${DF[@]}" "$SRC" -o "$TMP/dfn" >"$TMP/dfn.log" 2>&1 || { echo "DeepFilterNet failed:" >&2; tail -3 "$TMP/dfn.log" >&2; exit 1; }
  SRC="$(ls "$TMP"/dfn/*.wav | head -1)"
fi

# Take out boxiness, add clarity, tame harsh "s" sounds, light compression (natural, not squashed).
# No noise gate: after DeepFilterNet it only made the background pump in and out.
CHAIN="equalizer=f=220:t=q:w=1:g=-2.5,equalizer=f=3200:t=q:w=1:g=2,highshelf=f=9000:g=1.5,deesser=i=0.4:m=0.5:f=0.5,acompressor=ratio=2.5:threshold=-22dB:attack=8:release=120"
LN="loudnorm=I=-14:TP=-1.5:LRA=9"

J="$(ffmpeg -hide_banner -i "$SRC" -af "$CHAIN,$LN:print_format=json" -f null - 2>&1 | sed -n '/^{/,/^}/p')"
m() { printf '%s' "$J" | python3 -c "import sys,json;print(json.load(sys.stdin)['$1'])"; }

ffmpeg -v error -y -i "$SRC" -af "$CHAIN,$LN:measured_I=$(m input_i):measured_TP=$(m input_tp):measured_LRA=$(m input_lra):measured_thresh=$(m input_thresh):offset=$(m target_offset):linear=true" -ar 48000 -c:a pcm_s16le "$OUT"
# Sound-engineer check: voice (90th percentile of 50 ms levels) vs background between words (10th percentile).
read -r VOICE FLOOR <<<"$(python3 - "$OUT" <<'PY'
import array, math, sys, wave
w = wave.open(sys.argv[1]); a = array.array("h"); a.frombytes(w.readframes(w.getnframes()))
hop = int(w.getframerate() * 0.05)
lev = sorted(20 * math.log10(max(1.0, math.sqrt(sum(x * x for x in a[i:i + hop:4]) / (hop / 4))) / 32768) for i in range(0, len(a) - hop, hop))
print(round(lev[len(lev) * 9 // 10]), round(lev[len(lev) // 10]))
PY
)"
echo "cleanup ${MODE#--}: voice ${VOICE} dB, background between words ${FLOOR} dB, gap $((VOICE - FLOOR)) dB (want 30+)" >&2
[ $((VOICE - FLOOR)) -ge 30 ] || echo "WARNING: still noisy - listen before approving (very strong wind or a saw right by the mic can't be fully removed)" >&2
echo "$OUT"
