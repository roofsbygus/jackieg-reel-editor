#!/usr/bin/env bash
# Build the reel from edit.json and render it. Logs how long each part took to <reel>/timings.log.
# Usage: render.sh <reel-folder> [--capcut] [--final]
# Gentle by default: 2 Chrome workers at low priority, 1080p preview. --final renders at the brand resolution (1080p by default).
set -euo pipefail
REEL="$(cd "$1" && pwd)"; shift
FINAL=0; ARGS=(); for a in "$@"; do [ "$a" = "--final" ] && FINAL=1 || ARGS+=("$a"); done
WORKERS="${REEL_WORKERS:-2}"                     # each worker is a Chrome; 2 keeps a 16 GB Mac usable
S="$(cd "$(dirname "$0")" && pwd)"
source "$S/perlili_env.sh"; hf_required
BRAND="${REELS_HOME:-$HOME/reels}/brand.json"
RES="$(python3 -c "import json;r=json.load(open('$BRAND')).get('resolution',[1080,1920]);print('portrait-4k' if r[0]>=2160 else 'portrait')")"
[ "$FINAL" = 1 ] || RES=portrait                 # previews at 1080p: a quarter of the pixels of 4K
stamp() { echo "$(date +%s) $1" >> "$REEL/timings.log"; }

# a preview cut leaves a 1080p master.mp4; re-cut it at the brand resolution so the final isn't an upscale
if [ "$FINAL" = 1 ]; then
  WANT="$(python3 -c "import json;print(json.load(open('$BRAND')).get('resolution',[1080,1920])[1])")"
  HAVE="$(ffprobe -v error -select_streams v:0 -show_entries stream=height -of csv=p=0 "$REEL/master.mp4")"
  if [ "$HAVE" -lt "$WANT" ]; then echo "master.mp4 is ${HAVE}p, re-cutting at ${WANT}p for the final"; env -u REEL_PREVIEW python3 "$S/cut.py" "$REEL"; fi
fi

[ -s "$S/../engine/gsap.min.js" ] || bash "$S/setup_engine.sh"
[ -s "$S/../engine/CustomEase.min.js" ] || bash "$S/setup_engine.sh" || echo "note: engine setup didn't finish; rendering anyway" >&2   # older installs: optional, never blocks a render
stamp "build:start"; python3 "$S/build_reel.py" "$REEL" ${ARGS[@]+"${ARGS[@]}"}; stamp "build:end"
stamp "render:start"
nice -n 15 "$HF" render "$REEL/proj" --workers "$WORKERS" -o "$REEL/final_voice.mp4" --resolution "$RES" --quality delivery --quiet
stamp "render:end"
# Final mix: the reel's music bed (music.json from music.py, else brand.json "music": path) under the voice, then
# -14 LUFS -> final.mp4. final_voice.mp4 is kept, so a music swap is just: bash mix_music.sh <reel>
bash "$S/mix_music.sh" "$REEL"
python3 "$S/timings.py" "$REEL"
