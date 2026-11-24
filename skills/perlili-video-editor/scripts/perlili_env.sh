# Shared setup for every Perlili bash script: `source "$(dirname "$0")/perlili_env.sh"`.
# Same rules as perlili_env.py: Homebrew tools on PATH (the Code tab doesn't load ~/.zprofile),
# HyperFrames telemetry and self-updates off, and only the pinned HyperFrames (never npx -y).
PERLILI_SKILL="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
export PATH="/opt/homebrew/bin:/usr/local/bin:$HOME/.local/bin:$PATH"
export HYPERFRAMES_NO_TELEMETRY=1 DO_NOT_TRACK=1 HYPERFRAMES_NO_UPDATE_CHECK=1 HYPERFRAMES_NO_AUTO_INSTALL=1
HF="$PERLILI_SKILL/node_modules/.bin/hyperframes"
hf_required() {
  [ -x "$HF" ] && return 0
  echo "PV-HF: HyperFrames no está instalado en el editor. / HyperFrames isn't installed. Fix: cd \"$PERLILI_SKILL\" && npm ci --ignore-scripts" >&2
  exit 1
}
