#!/usr/bin/env bash
# Make the upload copy: same resolution, high-bitrate H.264, fast-start, saved in its own folder inside the brand's
# delivery folder (<deliver_dir>/<name>/<name>.mp4, with "<name> - post.txt" next to it).
# Usage: deliver.sh <final.mp4> "<clear name>"
set -euo pipefail
source "$(dirname "$0")/perlili_env.sh"   # Homebrew tools on PATH (Code tab doesn't load ~/.zprofile)
SRC="$1"; NAME="${2:-$(basename "${SRC%.*}")}"
BRAND="${REELS_HOME:-$HOME/reels}/brand.json"
DIR="$(python3 -c "import json,os;print(os.path.expanduser(json.load(open('$BRAND')).get('deliver_dir','~/Movies/Reels')))")"
DIR="$DIR/$NAME"   # each reel gets its own folder: the video, its post draft and anything else made for it
mkdir -p "$DIR"; OUT="$DIR/$NAME.mp4"

H="$(ffprobe -v error -select_streams v:0 -show_entries stream=height -of csv=p=0 "$SRC")"
if [ "$H" -ge 3000 ]; then RATE=35M; MAX=45M; else RATE=16M; MAX=20M; fi   # 4K vs 1080p

if [ "$(uname)" = "Darwin" ]; then
  VENC=(-c:v h264_videotoolbox -profile:v high -b:v "$RATE" -maxrate "$MAX" -bufsize "$MAX")   # Apple hardware encoder: fast, quiet
else
  VENC=(-c:v libx264 -preset slow -b:v "$RATE" -maxrate "$MAX" -bufsize "$MAX")
fi
ffmpeg -hide_banner -loglevel error -y -i "$SRC" "${VENC[@]}" -pix_fmt yuv420p -tag:v avc1 \
  -c:a aac -b:a 256k -movflags +faststart "$OUT"
POST="$(dirname "$SRC")/post.md"   # the post draft (references/post-copy.md) goes next to the video
if [ -s "$POST" ]; then cp "$POST" "$DIR/$NAME - post.txt"; echo "$DIR/$NAME - post.txt"; fi
echo "$OUT"
