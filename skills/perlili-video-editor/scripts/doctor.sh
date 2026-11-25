#!/usr/bin/env bash
# Revisión del sistema de Perlili Video Editor. Solo revisa: nunca instala ni cambia nada.
# Same ✅/⚠️/❌ lines on every Mac, so the lesson screenshots match. Each problem has a stable PV-* code and a one-line fix.
# Ends with: LISTO ✅ · LISTO CON LÍMITES ⚠️ (works, something optional is missing) · FALTA ALGO ❌ (fix before editing).
# Exit code: 0 ready, 2 ready with limits, 1 something missing.
source "$(dirname "$0")/perlili_env.sh"   # Homebrew tools on PATH (the Code tab doesn't load ~/.zprofile)
S="$(cd "$(dirname "$0")" && pwd)"
ok()   { printf '  ✅ %s\n' "$1"; }
warn() { printf '  ⚠️  %s  [%s]\n     %s\n' "$2" "$1" "$3"; LIMITS=1; }
no()   { printf '  ❌ %s  [%s]\n     Solución: %s\n' "$2" "$1" "$3"; MISSING=1; }
MISSING=0; LIMITS=0
echo "Revisión del editor Perlili"
echo

echo "Tu Mac"
if [ "$(uname)" != "Darwin" ]; then no PV-MAC "No es una Mac" "este editor solo funciona en Mac."
else
  V="$(/usr/bin/sw_vers -productVersion)"; MAJ="${V%%.*}"
  [ "$MAJ" -ge 13 ] && ok "macOS $V" || no PV-MACOS "macOS $V es muy viejo" "actualiza a macOS 13 o más nuevo (Ajustes del Sistema → General → Actualización de software)."
  [ "$(/usr/sbin/sysctl -n hw.optional.arm64 2>/dev/null)" = 1 ] && ok "Chip Apple (M1 o más nuevo)" \
    || no PV-CHIP "Esta Mac tiene chip Intel" "el editor necesita una Mac con chip Apple (M1 o más nuevo)."
fi
FREE_GB=$(df -Pk "$HOME" | awk 'NR==2{print int($4/1048576)}')
if [ "$FREE_GB" -ge 15 ]; then ok "${FREE_GB} GB libres en el disco"
elif [ "$FREE_GB" -ge 10 ]; then warn PV-DISCO "Solo ${FREE_GB} GB libres" "funciona, pero libera espacio hasta tener 15 GB (35 GB o más para videos 4K)."
else no PV-DISCO "Solo ${FREE_GB} GB libres" "libera espacio hasta tener al menos 15 GB (borra videos viejos o vacía la Papelera)."; fi
echo

echo "Programas"
if [ -x /opt/homebrew/bin/brew ]; then ok "Homebrew $(/opt/homebrew/bin/brew --version 2>/dev/null | head -1 | awk '{print $2}')"
else no PV-BREW "Falta Homebrew" "instálalo con el instalador .pkg de https://brew.sh (te pide la contraseña de tu Mac; hazlo tú, no Claude)."; fi
if command -v ffmpeg >/dev/null && command -v ffprobe >/dev/null; then ok "FFmpeg $(ffmpeg -version 2>/dev/null | head -1 | awk '{print $3}')"
else no PV-FFMPEG "Falta FFmpeg" "pídele a Claude: \"instala ffmpeg con brew\" (comando: brew install ffmpeg)."; fi
if command -v node >/dev/null; then
  NV="$(node -v 2>/dev/null | sed 's/^v//')"; NMAJ="${NV%%.*}"
  [ "${NMAJ:-0}" -ge 22 ] && ok "Node.js $NV" || no PV-NODE "Node.js $NV es muy viejo" "instala Node.js 22 o más nuevo (comando: brew install node)."
else no PV-NODE "Falta Node.js" "instala Node.js 22 o más nuevo (comando: brew install node)."; fi
command -v python3 >/dev/null && ok "Python 3" || no PV-PYTHON "Falta Python 3" "instala las herramientas de Apple (comando: xcode-select --install)."
echo

echo "Motor del editor"
WANT="$(python3 -c "import json,sys;print(json.load(open(sys.argv[1]))['dependencies']['hyperframes'])" "$PERLILI_SKILL/package.json" 2>/dev/null)"
HAVE="$(python3 -c "import json,sys;print(json.load(open(sys.argv[1]))['version'])" "$PERLILI_SKILL/node_modules/hyperframes/package.json" 2>/dev/null)"
if [ -z "$HAVE" ]; then no PV-HF "Falta HyperFrames" "pídele a Claude: \"instala mi editor Perlili\" (lo que ya está se salta)."
elif [ "$HAVE" != "$WANT" ]; then no PV-HF "HyperFrames $HAVE (debe ser $WANT)" "pídele a Claude: \"instala mi editor Perlili\" (lo que ya está se salta)."
else ok "HyperFrames $HAVE (versión fija)"; fi
OFF=1; for v in HYPERFRAMES_NO_TELEMETRY DO_NOT_TRACK HYPERFRAMES_NO_UPDATE_CHECK HYPERFRAMES_NO_AUTO_INSTALL; do [ "${!v}" = 1 ] || OFF=0; done
[ "$OFF" = 1 ] && ok "Telemetría y actualizaciones automáticas apagadas" || no PV-TELEMETRIA "La telemetría no está apagada" "revisa scripts/perlili_env.sh (no debe cambiarse)."
WCLI=""; for p in /opt/homebrew/bin/whisper-cli /usr/local/bin/whisper-cli; do [ -x "$p" ] && WCLI="$p" && break; done
[ -n "$WCLI" ] && ok "Whisper (whisper-cli)" || no PV-WHISPER "Falta Whisper" "pídele a Claude: \"instala whisper-cpp con brew\" (comando: brew install whisper.cpp)."
MODEL="$(python3 -c "import sys;sys.path.insert(0,sys.argv[1]);import perlili_env as p;print(p.whisper_model())" "$S" 2>/dev/null)"; MODEL="${MODEL:-large-v3}"
MF="$HOME/.cache/hyperframes/whisper/models/ggml-$MODEL.bin"
MIN_MB=50   # a half-downloaded model is smaller than this (bash 3.2 on macOS can't nest case in $(...))
[ "$MODEL" = large-v3 ] && MIN_MB=2900; [ "$MODEL" = medium ] && MIN_MB=1400; [ "$MODEL" = small ] && MIN_MB=450
if [ -f "$MF" ] && [ "$(( $(stat -f%z "$MF") / 1048576 ))" -ge "$MIN_MB" ]; then case "$MODEL" in *.en) ok "Modelo de subtítulos ($MODEL)";; *) ok "Modelo de subtítulos ($MODEL, español e inglés)";; esac
else no PV-MODELO "Falta el modelo de subtítulos ($MODEL)" "pídele a Claude: \"instala mi editor Perlili\" (lo que ya está se salta). Descarga ~3 GB una sola vez."; fi
case "$MODEL" in *.en) no PV-MODELO "El modelo $MODEL solo entiende inglés" "quita \"whisper_model\" de brand.json (se usa large-v3, que entiende español e inglés).";; esac
ENG="$PERLILI_SKILL/engine"
if [ -s "$ENG/gsap.min.js" ] && [ -s "$ENG/sfx/whoosh.wav" ] && [ -d "$ENG/hf/compositions" ]; then ok "Plantillas de video y efectos de sonido"
else no PV-PLANTILLAS "Faltan las plantillas de video" "pídele a Claude: \"instala mi editor Perlili\" (lo que ya está se salta)."; fi
[ -s "$ENG/CustomEase.min.js" ] || warn PV-PLANTILLAS "Falta una pieza de las animaciones (CustomEase)" "pídele a Claude: \"instala mi editor Perlili\" con internet; sin ella, una animación necesita internet al crear el video."
if [ -n "$(ls -A "$HOME/.cache/hyperframes/chrome" 2>/dev/null)" ]; then ok "Navegador para crear el video"
else warn PV-CHROME "El navegador para crear el video no está descargado" "se descarga solo la primera vez que creas un video (~200 MB)."; fi
command -v uv >/dev/null && ok "uv (instalador de Python)" || no PV-UV "Falta uv" "pídele a Claude: \"instala uv con brew\" (comando: brew install uv)."
if command -v deepFilter >/dev/null && deepFilter --help >/dev/null 2>&1; then ok "Limpieza de ruido (DeepFilterNet)"
else no PV-RUIDO "Falta la limpieza de ruido" "pídele a Claude: \"instala mi editor Perlili\" (lo que ya está se salta). ~1 GB una sola vez; sin ella el viento y el ruido de obra se oyen mucho."; fi
echo

echo "Seguridad"
SET="$HOME/.claude/settings.json"
if [ -f "$SET" ] && grep -q 'Bash(sudo' "$SET" && grep -q '| sh' "$SET"; then ok "Reglas de seguridad para Claude"
else warn PV-REGLAS "Faltan las reglas de seguridad para Claude" "pídele a Claude: \"aplica las reglas de seguridad de Perlili\" (settings/perlili-permisos.json)."; fi
if [ -f "$HOME/.config/reels/.env" ] && grep -q '^ELEVENLABS_API_KEY=' "$HOME/.config/reels/.env"; then
  python3 -c "import sys;sys.path.insert(0,sys.argv[1]);import perlili_env as p;sys.exit(0 if p.brand().get('elevenlabs') else 1)" "$S" \
    && warn PV-ELEVENLABS "ElevenLabs está prendido" "tu audio se sube a ElevenLabs y te cobra. Para apagarlo, quita \"elevenlabs\" de brand.json." \
    || ok "Hay una clave de ElevenLabs, pero está apagada (todo se queda en tu Mac)"
else ok "Todo se transcribe en tu Mac (nada se sube)"; fi
echo

echo "Tu marca"
HOME_DIR="${REELS_HOME:-$HOME/reels}"
if [ -f "$HOME_DIR/brand.json" ]; then
  ok "Archivo de marca ($HOME_DIR)"
  # every font the brand names must exist, or captions silently fall back to a system font
  python3 - "$HOME_DIR/brand.json" <<'PY' || LIMITS=1
import json, os, sys
b = json.load(open(sys.argv[1])); bad = 0
for role, f in (b.get("fonts") or {}).items():
    p = f.get("file")
    if p and not os.path.exists(os.path.expanduser(p)):
        print(f"  ⚠️  Falta la letra \"{role}\": {p}  [PV-LETRA]\n     los subtítulos usarán otra letra hasta que pongas ese archivo ahí"); bad = 1
    elif p: print(f"  ✅ Letra {role} ({f.get('family')})")
sys.exit(bad)
PY
  if python3 -c "import json,sys;sys.exit(0 if json.load(open(sys.argv[1])).get('capcut') else 1)" "$HOME_DIR/brand.json"; then
    [ -d "${CAPCUT_SKILLS_DIR:-/nonexistent}/capcut-stdraft-builder" ] && ok "Ayudantes de CapCut" \
      || warn PV-CAPCUT "No encontré los ayudantes de CapCut" "el MP4 funciona igual; para CapCut ve references/capcut.md paso 3."
    CL="$HOME/.local/bin/claude"; [ -x "$CL" ] || CL=claude
    "$CL" mcp list 2>/dev/null | grep -q capcut_creation && ok "Conector de CapCut" \
      || warn PV-CAPCUT "Falta el conector de CapCut" "el MP4 funciona igual; para CapCut ve references/capcut.md paso 2."
  fi
else
  echo "  ➖ Todavía no hay archivo de marca: Claude te hará unas preguntas la primera vez"
fi
echo "  ℹ️  La página de revisión necesita las herramientas Artifact de Claude; si no están, la revisión se hace en el chat"
echo

if [ "$MISSING" = 1 ]; then echo "FALTA ALGO ❌  Arregla los puntos con ❌ y vuelve a correr esta revisión."; exit 1
elif [ "$LIMITS" = 1 ]; then echo "LISTO CON LÍMITES ⚠️  Ya puedes editar; los puntos con ⚠️ son opcionales o bajan un poco la calidad."; exit 2
else echo "LISTO ✅"; fi
