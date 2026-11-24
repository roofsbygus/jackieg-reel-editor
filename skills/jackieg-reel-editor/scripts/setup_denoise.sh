#!/usr/bin/env bash
# One-time: install DeepFilterNet (voice isolation for job-site noise), free and local, with pinned versions.
# DeepFilterNet 0.5.6 doesn't declare its AI library, and only works with older PyTorch: these pins are the tested set
# (2026-11-23, Apple Silicon). Needs uv (brew install uv). About 1 GB. No password, nothing paid, nothing uploaded.
set -euo pipefail
source "$(dirname "$0")/reel_env.sh"
command -v uv >/dev/null || { echo "❌ $(t "Falta uv [JG-UV]. Pídele a Claude: \"arregla esto\"" "uv is missing [JG-UV]. Ask Claude: \"fix this\"")" >&2; exit 1; }
echo "$(t "Instalando la limpieza de ruido (DeepFilterNet, ~1 GB, una sola vez)..." "Installing noise cleanup (DeepFilterNet, ~1 GB, one time)...")"
uv -q tool install --force --python 3.11 deepfilternet==0.5.6 \
  --with torch==2.2.2 --with torchaudio==2.2.2 --with "numpy<2" --with soundfile==0.14.0 >/dev/null 2>&1 || { echo "❌ $(t "No se pudo instalar DeepFilterNet [JG-RUIDO]. Revisa tu internet y vuelve a decirle a Claude: \"instala mi editor de reels\"" "Couldn't install DeepFilterNet [JG-RUIDO]. Check your internet and tell Claude again: \"install my reel editor\"")" >&2; exit 1; }
# first run downloads the DeepFilterNet3 model; do it now on one second of silence so the first edit doesn't wait
TMP="$(mktemp -d)"; trap 'rm -rf "$TMP"' EXIT
ffmpeg -v error -f lavfi -i anullsrc=r=48000:cl=mono -t 1 "$TMP/s.wav"
deepFilter --pf "$TMP/s.wav" -o "$TMP/o" >/dev/null 2>&1 && echo "✅ $(t "Limpieza de ruido lista" "Noise cleanup ready")" \
  || { echo "❌ $(t "DeepFilterNet no arrancó [JG-RUIDO]. Vuelve a decirle a Claude: \"instala mi editor de reels\"" "DeepFilterNet didn't start [JG-RUIDO]. Tell Claude again: \"install my reel editor\"")" >&2; exit 1; }
