#!/usr/bin/env bash
# JackieG Reel Editor system check. Only checks: never installs or changes anything.
# Spanish or English (the language saved at install, or --lang es|en). Same ✅/⚠️/❌ lines on every Mac, so the
# guide's screenshots match. Each problem has a stable JG-* code and a one-line fix.
# Ends with: LISTO ✅ / READY ✅ · LISTO CON LÍMITES ⚠️ / READY WITH LIMITS ⚠️ · FALTA ALGO ❌ / SOMETHING'S MISSING ❌
# Exit code: 0 ready, 2 ready with limits, 1 something missing.
for a in "$@"; do case "$a" in --lang=*) export REEL_LANG="${a#--lang=}";; en|es) export REEL_LANG="$a";; esac; done
source "$(dirname "$0")/reel_env.sh"   # Homebrew tools on PATH (the Code tab doesn't load ~/.zprofile), language
S="$(cd "$(dirname "$0")" && pwd)"
ok()   { printf '  ✅ %s\n' "$1"; }
warn() { printf '  ⚠️  %s  [%s]\n     %s\n' "$2" "$1" "$3"; LIMITS=1; }
no()   { printf '  ❌ %s  [%s]\n     %s %s\n' "$2" "$1" "$(t "Solución:" "Fix:")" "$3"; MISSING=1; }
MISSING=0; LIMITS=0
INSTALL="$(t "pídele a Claude: \"instala mi editor de reels\" (lo que ya está se salta)" "ask Claude: \"install my reel editor\" (anything already there is skipped)")"
echo "$(t "Revisión del editor de reels JackieG" "JackieG Reel Editor check")"
echo

echo "$(t "Tu Mac" "Your Mac")"
if [ "$(uname)" != "Darwin" ]; then no JG-MAC "$(t "No es una Mac" "This isn't a Mac")" "$(t "este editor solo funciona en Mac." "this editor only works on a Mac.")"
else
  V="$(/usr/bin/sw_vers -productVersion)"; MAJ="${V%%.*}"
  [ "$MAJ" -ge 13 ] && ok "macOS $V" || no JG-MACOS "$(t "macOS $V es muy viejo" "macOS $V is too old")" \
    "$(t "actualiza a macOS 13 o más nuevo (Ajustes del Sistema → General → Actualización de software)." "update to macOS 13 or newer (System Settings → General → Software Update).")"
  [ "$(/usr/sbin/sysctl -n hw.optional.arm64 2>/dev/null)" = 1 ] && ok "$(t "Chip Apple (M1 o más nuevo)" "Apple chip (M1 or newer)")" \
    || no JG-CHIP "$(t "Esta Mac tiene chip Intel" "This Mac has an Intel chip")" "$(t "el editor necesita una Mac con chip Apple (M1 o más nuevo)." "the editor needs a Mac with an Apple chip (M1 or newer).")"
fi
if [ "$(uname)" = "Darwin" ]; then
  RAM_GB=$(( $(/usr/sbin/sysctl -n hw.memsize 2>/dev/null || echo 0) / 1073741824 ))
  if [ "$RAM_GB" -ge 16 ]; then ok "$(t "${RAM_GB} GB de memoria" "${RAM_GB} GB of memory")"
  elif [ "$RAM_GB" -gt 0 ]; then warn JG-MEMORIA "$(t "${RAM_GB} GB de memoria" "${RAM_GB} GB of memory")" "$(t "funciona, pero los subtítulos y el video tardan más: cierra otras apps mientras editas y usa videos de menos de 2 minutos." "it works, but captions and video take longer: close other apps while you edit and use videos under 2 minutes.")"; fi
fi
FREE_GB=$(df -Pk "$HOME" | awk 'NR==2{print int($4/1048576)}')
if [ "$FREE_GB" -ge 15 ]; then ok "$(t "${FREE_GB} GB libres en el disco" "${FREE_GB} GB free on disk")"
elif [ "$FREE_GB" -ge 10 ]; then warn JG-DISCO "$(t "Solo ${FREE_GB} GB libres" "Only ${FREE_GB} GB free")" "$(t "funciona, pero libera espacio hasta tener 15 GB (35 GB o más para videos 4K)." "it works, but free up space to 15 GB (35 GB or more for 4K videos).")"
else no JG-DISCO "$(t "Solo ${FREE_GB} GB libres" "Only ${FREE_GB} GB free")" "$(t "libera espacio hasta tener al menos 15 GB (borra videos viejos o vacía la Papelera)." "free up at least 15 GB (delete old videos or empty the Trash).")"; fi
echo

echo "$(t "Programas" "Programs")"
if [ -x /opt/homebrew/bin/brew ]; then ok "Homebrew $(/opt/homebrew/bin/brew --version 2>/dev/null | head -1 | awk '{print $2}')"
else no JG-BREW "$(t "Falta Homebrew" "Homebrew is missing")" "$(t "descarga e instala Homebrew.pkg desde https://github.com/Homebrew/brew/releases/latest/download/Homebrew.pkg (te pide la contraseña de tu Mac; hazlo tú, no Claude)." "download and install Homebrew.pkg from https://github.com/Homebrew/brew/releases/latest/download/Homebrew.pkg (it asks for your Mac password: you do this, not Claude).")"; fi
BREWFIX() { t "pídele a Claude: \"arregla esto\" (instala $1 con Homebrew)." "ask Claude: \"fix this\" (it installs $1 with Homebrew)."; }
if command -v ffmpeg >/dev/null && command -v ffprobe >/dev/null; then ok "FFmpeg $(ffmpeg -version 2>/dev/null | head -1 | awk '{print $3}')"
else no JG-FFMPEG "$(t "Falta FFmpeg" "FFmpeg is missing")" "$(BREWFIX ffmpeg)"; fi
if command -v node >/dev/null; then
  NV="$(node -v 2>/dev/null | sed 's/^v//')"; NMAJ="${NV%%.*}"
  [ "${NMAJ:-0}" -ge 22 ] && ok "Node.js $NV" || no JG-NODE "$(t "Node.js $NV es muy viejo" "Node.js $NV is too old")" "$(BREWFIX node)"
else no JG-NODE "$(t "Falta Node.js" "Node.js is missing")" "$(BREWFIX node)"; fi
command -v python3 >/dev/null && ok "Python 3" || no JG-PYTHON "$(t "Falta Python 3" "Python 3 is missing")" "$(t "pídele a Claude que te guíe para instalar las herramientas de Apple (xcode-select --install)." "ask Claude to walk you through installing Apple's tools (xcode-select --install).")"
echo

echo "$(t "Motor del editor" "Editor engine")"
WANT="$(python3 -c "import json,sys;print(json.load(open(sys.argv[1]))['dependencies']['hyperframes'])" "$REEL_SKILL/package.json" 2>/dev/null)"
HAVE="$(python3 -c "import json,sys;print(json.load(open(sys.argv[1]))['version'])" "$REEL_SKILL/node_modules/hyperframes/package.json" 2>/dev/null)"
if [ -z "$HAVE" ]; then no JG-HF "$(t "Falta HyperFrames" "HyperFrames is missing")" "$INSTALL."
elif [ "$HAVE" != "$WANT" ]; then no JG-HF "$(t "HyperFrames $HAVE (debe ser $WANT)" "HyperFrames $HAVE (should be $WANT)")" "$INSTALL."
else ok "$(t "HyperFrames $HAVE (versión fija)" "HyperFrames $HAVE (pinned version)")"; fi
OFF=1; for v in HYPERFRAMES_NO_TELEMETRY DO_NOT_TRACK HYPERFRAMES_NO_UPDATE_CHECK HYPERFRAMES_NO_AUTO_INSTALL; do [ "${!v}" = 1 ] || OFF=0; done
[ "$OFF" = 1 ] && ok "$(t "Telemetría y actualizaciones automáticas apagadas" "Telemetry and auto-updates off")" \
  || no JG-TELEMETRIA "$(t "La telemetría no está apagada" "Telemetry isn't off")" "$(t "revisa scripts/reel_env.sh (no debe cambiarse)." "check scripts/reel_env.sh (it must not be changed).")"
WCLI=""; for p in /opt/homebrew/bin/whisper-cli /usr/local/bin/whisper-cli; do [ -x "$p" ] && WCLI="$p" && break; done
[ -n "$WCLI" ] && ok "Whisper (whisper-cli)" || no JG-WHISPER "$(t "Falta Whisper" "Whisper is missing")" "$(BREWFIX whisper-cpp)"
MODEL="$(python3 -c "import sys;sys.path.insert(0,sys.argv[1]);import reel_env as p;print(p.whisper_model())" "$S" 2>/dev/null)"; MODEL="${MODEL:-large-v3}"
MF="$HOME/.cache/hyperframes/whisper/models/ggml-$MODEL.bin"
MIN_MB=50   # a half-downloaded model is smaller than this (bash 3.2 on macOS can't nest case in $(...))
[ "$MODEL" = large-v3 ] && MIN_MB=2900; [ "$MODEL" = medium ] && MIN_MB=1400; [ "$MODEL" = small ] && MIN_MB=450
if [ -f "$MF" ] && [ "$(( $(stat -f%z "$MF") / 1048576 ))" -ge "$MIN_MB" ]; then
  case "$MODEL" in *.en) ok "$(t "Modelo de subtítulos ($MODEL)" "Caption model ($MODEL)")";; *) ok "$(t "Modelo de subtítulos ($MODEL, español e inglés)" "Caption model ($MODEL, Spanish and English)")";; esac
else no JG-MODELO "$(t "Falta el modelo de subtítulos ($MODEL)" "The caption model ($MODEL) is missing")" "$INSTALL. $(t "Descarga ~3 GB una sola vez." "One-time ~3 GB download.")"; fi
case "$MODEL" in *.en) no JG-MODELO "$(t "El modelo $MODEL solo entiende inglés" "The $MODEL model only understands English")" "$(t "quita \"whisper_model\" de brand.json (se usa large-v3, que entiende español e inglés)." "remove \"whisper_model\" from brand.json (large-v3 is used, which understands Spanish and English).")";; esac
ENG="$REEL_SKILL/engine"
if [ -s "$ENG/gsap.min.js" ] && [ -s "$ENG/sfx/whoosh.wav" ] && [ -d "$ENG/hf/compositions" ]; then ok "$(t "Plantillas de video y efectos de sonido" "Video templates and sound effects")"
else no JG-PLANTILLAS "$(t "Faltan las plantillas de video" "The video templates are missing")" "$INSTALL."; fi
[ -s "$ENG/CustomEase.min.js" ] || warn JG-PLANTILLAS "$(t "Falta una pieza de las animaciones (CustomEase)" "One animation piece is missing (CustomEase)")" "$(t "pídele a Claude: \"instala mi editor de reels\" con internet; sin ella, una animación necesita internet al crear el video." "ask Claude: \"install my reel editor\" while online; without it, one animation needs the internet when making the video.")"
if [ -n "$(ls -A "$HOME/.cache/hyperframes/chrome" 2>/dev/null)" ]; then ok "$(t "Navegador para crear el video" "Video browser")"
else warn JG-CHROME "$(t "El navegador para crear el video no está descargado" "The video browser isn't downloaded yet")" "$(t "se descarga solo la primera vez que creas un video (~200 MB)." "it downloads by itself the first time you make a video (~200 MB).")"; fi
command -v uv >/dev/null && ok "$(t "uv (instalador de Python)" "uv (Python installer)")" || no JG-UV "$(t "Falta uv" "uv is missing")" "$(BREWFIX uv)"
if command -v deepFilter >/dev/null && deepFilter --help >/dev/null 2>&1; then ok "$(t "Limpieza de ruido (DeepFilterNet)" "Noise cleanup (DeepFilterNet)")"
else no JG-RUIDO "$(t "Falta la limpieza de ruido" "Noise cleanup is missing")" "$INSTALL. $(t "~1 GB una sola vez; sin ella el viento y el ruido de fondo se oyen mucho." "One-time ~1 GB; without it, wind and background noise come through.")"; fi
echo

echo "$(t "Seguridad" "Safety")"
SET="$HOME/.claude/settings.json"
if [ -f "$SET" ] && grep -q 'Bash(sudo' "$SET" && grep -q '| sh' "$SET"; then ok "$(t "Reglas de seguridad para Claude" "Safety rules for Claude")"
else warn JG-REGLAS "$(t "Faltan las reglas de seguridad para Claude" "Claude's safety rules aren't on")" "$(t "pídele a Claude: \"aplica las reglas de seguridad\" (settings/permisos-seguridad.json)." "ask Claude: \"apply the safety rules\" (settings/permisos-seguridad.json).")"; fi
if [ -f "$HOME/.config/reels/.env" ] && grep -q '^ELEVENLABS_API_KEY=' "$HOME/.config/reels/.env"; then
  python3 -c "import sys;sys.path.insert(0,sys.argv[1]);import reel_env as p;sys.exit(0 if p.brand().get('elevenlabs') else 1)" "$S" \
    && warn JG-ELEVENLABS "$(t "ElevenLabs está prendido" "ElevenLabs is on")" "$(t "tu audio se sube a ElevenLabs y te cobra. Para apagarlo, quita \"elevenlabs\" de brand.json." "your audio is uploaded to ElevenLabs and it charges you. To turn it off, remove \"elevenlabs\" from brand.json.")" \
    || ok "$(t "Hay una clave de ElevenLabs, pero está apagada (todo se queda en tu Mac)" "There's an ElevenLabs key, but it's off (everything stays on your Mac)")"
else ok "$(t "Todo se transcribe en tu Mac (nada se sube)" "Everything is transcribed on your Mac (nothing is uploaded)")"; fi
echo

echo "$(t "Tu marca" "Your brand")"
HOME_DIR="${REELS_HOME:-$HOME/reels-jackieg}"
if [ -f "$HOME_DIR/brand.json" ]; then
  ok "$(t "Archivo de marca" "Brand file") ($HOME_DIR)"
  # every font the brand names must exist, or captions silently fall back to a system font
  python3 - "$HOME_DIR/brand.json" "$REEL_LANG" <<'PY' || LIMITS=1
import json, os, sys
b = json.load(open(sys.argv[1])); en = sys.argv[2] == "en"; bad = 0
for role, f in (b.get("fonts") or {}).items():
    p = f.get("file")
    if p and not os.path.exists(os.path.expanduser(p)):
        print(f"  ⚠️  {'Font missing' if en else 'Falta la letra'} \"{role}\": {p}  [JG-LETRA]\n     "
              + ("captions use another font until that file is there" if en else "los subtítulos usarán otra letra hasta que pongas ese archivo ahí")); bad = 1
    elif p: print(f"  ✅ {'Font' if en else 'Letra'} {role} ({f.get('family')})")
sys.exit(bad)
PY
  if python3 -c "import json,sys;sys.exit(0 if json.load(open(sys.argv[1])).get('capcut') else 1)" "$HOME_DIR/brand.json"; then
    [ -d "${CAPCUT_SKILLS_DIR:-/nonexistent}/capcut-stdraft-builder" ] && ok "$(t "Ayudantes de CapCut" "CapCut helpers")" \
      || warn JG-CAPCUT "$(t "No encontré los ayudantes de CapCut" "CapCut helpers not found")" "$(t "el MP4 funciona igual; para CapCut ve references/capcut.md paso 3." "the MP4 works anyway; for CapCut see references/capcut.md step 3.")"
    CL="$HOME/.local/bin/claude"; [ -x "$CL" ] || CL=claude
    "$CL" mcp list 2>/dev/null | grep -q capcut_creation && ok "$(t "Conector de CapCut" "CapCut connector")" \
      || warn JG-CAPCUT "$(t "Falta el conector de CapCut" "The CapCut connector is missing")" "$(t "el MP4 funciona igual; para CapCut ve references/capcut.md paso 2." "the MP4 works anyway; for CapCut see references/capcut.md step 2.")"
  fi
else
  echo "  ➖ $(t "Todavía no hay archivo de marca: Claude te hará unas preguntas la primera vez" "No brand file yet: Claude asks you a few questions the first time")"
fi
echo "  ℹ️  $(t "La página de revisión necesita las herramientas Artifact de Claude; si no están, la revisión se hace en el chat" "The review page needs Claude's Artifact tools; without them, the review happens in the chat")"
echo

if [ "$MISSING" = 1 ]; then echo "$(t "FALTA ALGO ❌  Arregla los puntos con ❌ y vuelve a correr esta revisión." "SOMETHING'S MISSING ❌  Fix the ❌ items and run this check again.")"; exit 1
elif [ "$LIMITS" = 1 ]; then echo "$(t "LISTO CON LÍMITES ⚠️  Ya puedes editar; los puntos con ⚠️ son opcionales o bajan un poco la calidad." "READY WITH LIMITS ⚠️  You can edit now; the ⚠️ items are optional or lower quality a little.")"; exit 2
else echo "$(t "LISTO ✅" "READY ✅")"; fi
