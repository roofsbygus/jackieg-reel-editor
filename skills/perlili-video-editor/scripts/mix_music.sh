#!/usr/bin/env bash
# Final sound mix: the rendered reel (final_voice.mp4, never changed) + the reel's music bed (music.py resolve),
# then the whole mix at -14 LUFS -> final.mp4. Video is copied, not re-encoded, so a music swap remixes in seconds.
# The bed sits ~18 dB under the voice, ducks further while they talk, fades in, and (per-reel music) fades out.
# Usage: mix_music.sh <reel-folder>
set -euo pipefail
REEL="$(cd "$1" && pwd)"
S="$(cd "$(dirname "$0")" && pwd)"
source "$S/perlili_env.sh"
SRC="$REEL/final_voice.mp4"
[ -f "$SRC" ] || { echo "no final_voice.mp4 in $REEL: render the reel first (render.sh)" >&2; exit 1; }
LN="loudnorm=I=-14:TP=-1.5:LRA=7"
OUT="$REEL/final_ln.mp4"
PICK="$(python3 "$S/music.py" resolve "$REEL")"
if [ "$PICK" = "none" ]; then
  ffmpeg -v error -y -i "$SRC" -c:v copy -af "$LN" -ar 48000 -c:a aac -b:a 256k "$OUT"
  echo "mixed: no music"
else
  IFS=$'\t' read -r MUSIC GAIN START FADE <<< "$PICK"
  [ -f "$MUSIC" ] || { echo "music file missing: $MUSIC" >&2; exit 1; }
  OUTF=""
  if python3 -c "import sys;sys.exit(0 if float('$FADE')>0 else 1)"; then
    DUR="$(ffprobe -v error -show_entries format=duration -of csv=p=0 "$SRC")"
    ST="$(python3 -c "print(max(0.0, $DUR - $FADE))")"
    OUTF=",afade=t=out:st=$ST:d=$FADE"
  fi
  ffmpeg -v error -y -i "$SRC" -stream_loop -1 -ss "$START" -i "$MUSIC" -filter_complex \
    "[1:a]volume=${GAIN}dB,afade=t=in:d=0.5${OUTF}[m];[0:a]asplit[v][key];[m][key]sidechaincompress=threshold=0.02:ratio=6:attack=15:release=350[md];[v][md]amix=inputs=2:duration=first:normalize=0,$LN[a]" \
    -map 0:v -map "[a]" -c:v copy -ar 48000 -c:a aac -b:a 256k "$OUT"
  echo "mixed: $(basename "$MUSIC")"
fi
mv "$OUT" "$REEL/final.mp4"
