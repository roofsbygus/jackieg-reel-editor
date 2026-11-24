#!/usr/bin/env bash
# One-time: download the caption model (Whisper large-v3, ~3 GB, Spanish + English) so the first edit doesn't stall.
# The pinned HyperFrames downloads it from huggingface.co/ggerganov/whisper.cpp at a fixed revision and checks its sha256.
# It never installs programs: whisper-cli must already be there (brew install whisper.cpp). Safe to re-run.
set -euo pipefail
source "$(dirname "$0")/perlili_env.sh"; hf_required
S="$(cd "$(dirname "$0")" && pwd)"
MODEL="$(python3 -c "import sys;sys.path.insert(0,sys.argv[1]);import perlili_env as p;print(p.whisper_model())" "$S")"
TMP="$(mktemp -d)"; trap 'rm -rf "$TMP"' EXIT
ffmpeg -v error -f lavfi -i anullsrc=r=16000:cl=mono -t 1 "$TMP/silence.wav"
echo "Preparando el modelo de subtítulos $MODEL (la primera vez se descarga, ~3 GB; puede tardar)..."
if "$HF" transcribe "$TMP/silence.wav" -d "$TMP/out" --json --engine whisper --no-runtime-install --model "$MODEL" >"$TMP/log" 2>&1; then
  echo "✅ Modelo $MODEL listo"
else
  echo "❌ No se pudo descargar el modelo [PV-MODELO]. Revisa tu internet y vuelve a correr: bash scripts/setup_models.sh" >&2
  tail -3 "$TMP/log" >&2; exit 1
fi
