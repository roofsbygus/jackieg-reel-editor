#!/usr/bin/env bash
# One-time: install DeepFilterNet (voice isolation for job-site noise), free and local, with pinned versions.
# DeepFilterNet 0.5.6 doesn't declare its AI library, and only works with older PyTorch: these pins are the tested set
# (2026-11-23, Apple Silicon). Needs uv (brew install uv). About 1 GB. No password, nothing paid, nothing uploaded.
set -euo pipefail
source "$(dirname "$0")/perlili_env.sh"
command -v uv >/dev/null || { echo "❌ Falta uv [PV-UV]. Solución: brew install uv" >&2; exit 1; }
echo "Instalando la limpieza de ruido (DeepFilterNet, ~1 GB, una sola vez)..."
uv -q tool install --force --python 3.11 deepfilternet==0.5.6 \
  --with torch==2.2.2 --with torchaudio==2.2.2 --with "numpy<2" --with soundfile==0.14.0 >/dev/null 2>&1 || { echo "❌ No se pudo instalar DeepFilterNet [PV-RUIDO]. Revisa tu internet y vuelve a decirle a Claude: instala mi editor Perlili" >&2; exit 1; }
# first run downloads the DeepFilterNet3 model; do it now on one second of silence so the first edit doesn't wait
TMP="$(mktemp -d)"; trap 'rm -rf "$TMP"' EXIT
ffmpeg -v error -f lavfi -i anullsrc=r=48000:cl=mono -t 1 "$TMP/s.wav"
deepFilter --pf "$TMP/s.wav" -o "$TMP/o" >/dev/null 2>&1 && echo "✅ Limpieza de ruido lista" \
  || { echo "❌ DeepFilterNet no arrancó [PV-RUIDO]. Vuelve a correr: bash scripts/setup_denoise.sh" >&2; exit 1; }
