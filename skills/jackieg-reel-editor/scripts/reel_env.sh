# Shared setup for every JackieG Reel Editor bash script: `source "$(dirname "$0")/reel_env.sh"`.
# Same rules as reel_env.py: Homebrew tools on PATH (the Code tab doesn't load ~/.zprofile),
# HyperFrames telemetry and self-updates off, and only the pinned HyperFrames (never npx -y).
# Language: what the person picked at install (~/.config/jackieg-reel-editor/lang), overridden by REEL_LANG=es|en.
# t "español" "English" prints the one that matches.
REEL_SKILL="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
REEL_CONF="$HOME/.config/jackieg-reel-editor"
export PATH="/opt/homebrew/bin:/usr/local/bin:$HOME/.local/bin:$PATH"
export HYPERFRAMES_NO_TELEMETRY=1 DO_NOT_TRACK=1 HYPERFRAMES_NO_UPDATE_CHECK=1 HYPERFRAMES_NO_AUTO_INSTALL=1
REEL_LANG="${REEL_LANG:-$(cat "$REEL_CONF/lang" 2>/dev/null)}"
[ "$REEL_LANG" = en ] || REEL_LANG=es
export REEL_LANG
t() { if [ "$REEL_LANG" = en ]; then printf '%s' "$2"; else printf '%s' "$1"; fi; }
HF="$REEL_SKILL/node_modules/.bin/hyperframes"
hf_required() {
  [ -x "$HF" ] && return 0
  echo "JG-HF: $(t "HyperFrames no está instalado. Pídele a Claude: \"instala mi editor de reels\"" "HyperFrames isn't installed. Ask Claude: \"install my reel editor\"")" >&2
  exit 1
}
