#!/usr/bin/env bash
# JackieG Reel Editor install, in fixed steps. Safe to re-run: anything already installed is skipped.
# Usage: bash install.sh [es|en]   (the language the person writes in; saved for the check and the review page)
# What it does, in order: checks the Mac, installs the 4 Homebrew tools that are missing (never Homebrew itself, never
# sudo), the pinned HyperFrames (npm ci --ignore-scripts), the video templates, the caption model, the noise cleanup,
# links the skill into ~/.claude/skills (so /jackieg-reel-editor works), then runs the check. It never touches
# ~/.claude/settings.json (the safety rules are applied separately, with the person's OK) and never pays for or
# uploads anything.
set -uo pipefail
for a in "$@"; do case "$a" in --lang=*) export REEL_LANG="${a#--lang=}";; en|es) export REEL_LANG="$a";; esac; done
source "$(dirname "$0")/reel_env.sh"
S="$(cd "$(dirname "$0")" && pwd)"
mkdir -p "$REEL_CONF" && printf '%s\n' "$REEL_LANG" > "$REEL_CONF/lang"   # the check and the review page use the same language
paso() { printf '\n%s\n' "── $(t "Paso $1 de 7" "Step $1 of 7"): $2"; }
falla() { printf '\n❌ %s  [%s]\n   %s %s\n' "$2" "$1" "$(t "Solución:" "Fix:")" "$3" >&2; exit 1; }
AGAIN="$(t "revisa tu internet y vuelve a decirle a Claude: \"instala mi editor de reels\"." "check your internet and tell Claude again: \"install my reel editor\".")"

echo "$(t "Instalación del editor de reels JackieG" "Installing the JackieG Reel Editor")"

paso 1 "$(t "Revisar tu Mac" "Check your Mac")"
[ "$(uname)" = Darwin ] || falla JG-MAC "$(t "No es una Mac" "This isn't a Mac")" "$(t "este editor solo funciona en Mac." "this editor only works on a Mac.")"
[ "$(/usr/sbin/sysctl -n hw.optional.arm64 2>/dev/null)" = 1 ] || falla JG-CHIP "$(t "Esta Mac tiene chip Intel" "This Mac has an Intel chip")" "$(t "el editor necesita una Mac con chip Apple (M1 o más nuevo)." "the editor needs a Mac with an Apple chip (M1 or newer).")"
FREE_GB=$(df -Pk "$HOME" | awk 'NR==2{print int($4/1048576)}')
[ "$FREE_GB" -ge 10 ] || falla JG-DISCO "$(t "Solo ${FREE_GB} GB libres" "Only ${FREE_GB} GB free")" "$(t "libera espacio hasta tener al menos 15 GB y vuelve a empezar." "free up at least 15 GB and start again.")"
[ -x /opt/homebrew/bin/brew ] || falla JG-BREW "$(t "Falta Homebrew" "Homebrew is missing")" "$(t "descarga e instala Homebrew.pkg desde https://github.com/Homebrew/brew/releases/latest/download/Homebrew.pkg (te pide la contraseña de tu Mac; hazlo tú, no Claude). Después vuelve a decir \"instala mi editor de reels\"." "download and install Homebrew.pkg from https://github.com/Homebrew/brew/releases/latest/download/Homebrew.pkg (it asks for your Mac password: you do this, not Claude). Then say \"install my reel editor\" again.")"
echo "  ✅ $(t "Mac con chip Apple, ${FREE_GB} GB libres, Homebrew listo" "Apple-chip Mac, ${FREE_GB} GB free, Homebrew ready")"

paso 2 "$(t "Programas de Homebrew (FFmpeg, Node.js, Whisper, uv)" "Homebrew programs (FFmpeg, Node.js, Whisper, uv)")"
FALTAN=()
command -v ffmpeg >/dev/null || FALTAN+=(ffmpeg)
NMAJ="$(node --version 2>/dev/null | sed 's/^v//; s/\..*//')"; [ "${NMAJ:-0}" -ge 22 ] || FALTAN+=(node)
command -v whisper-cli >/dev/null || FALTAN+=(whisper-cpp)
command -v uv >/dev/null || FALTAN+=(uv)
if [ ${#FALTAN[@]} -eq 0 ]; then echo "  ✅ $(t "Ya estaban todos" "All already there")"
else
  echo "  $(t "Instalando" "Installing"): ${FALTAN[*]} ($(t "puede tardar unos minutos" "this can take a few minutes"))..."
  /opt/homebrew/bin/brew install "${FALTAN[@]}" || falla JG-BREW-INSTALL "$(t "Homebrew no pudo instalar" "Homebrew couldn't install") ${FALTAN[*]}" "$AGAIN"
  echo "  ✅ $(t "Listo" "Done")"
fi

paso 3 "$(t "Motor de video (HyperFrames, versión fija)" "Video engine (HyperFrames, pinned version)")"
WANT="$(python3 -c "import json,sys;print(json.load(open(sys.argv[1]))['dependencies']['hyperframes'])" "$REEL_SKILL/package.json")"
HAVE="$(python3 -c "import json,sys;print(json.load(open(sys.argv[1]))['version'])" "$REEL_SKILL/node_modules/hyperframes/package.json" 2>/dev/null)"
if [ "$HAVE" = "$WANT" ]; then echo "  ✅ HyperFrames $HAVE $(t "ya estaba" "already there")"
else
  (cd "$REEL_SKILL" && NPM_CONFIG_UPDATE_NOTIFIER=false npm ci --ignore-scripts --no-audit --no-fund --loglevel=error >/dev/null) || falla JG-HF "$(t "No se pudo instalar HyperFrames" "Couldn't install HyperFrames")" "$AGAIN"
  echo "  ✅ HyperFrames $WANT $(t "instalado" "installed")"
fi

paso 4 "$(t "Plantillas y efectos de sonido" "Templates and sound effects")"
bash "$S/setup_engine.sh" >/dev/null || falla JG-PLANTILLAS "$(t "No se pudieron bajar las plantillas" "Couldn't download the templates")" "$AGAIN"
echo "  ✅ $(t "Listas" "Ready")"

paso 5 "$(t "Modelo de subtítulos (español e inglés, ~3 GB la primera vez)" "Caption model (Spanish and English, ~3 GB the first time)")"
bash "$S/setup_models.sh" || exit 1

paso 6 "$(t "Limpieza de ruido (DeepFilterNet, ~1 GB la primera vez)" "Noise cleanup (DeepFilterNet, ~1 GB the first time)")"
if uv tool list 2>/dev/null | grep -q '^deepfilternet v0\.5\.6$' && deepFilter --help >/dev/null 2>&1; then echo "  ✅ $(t "Ya estaba" "Already there")"
else bash "$S/setup_denoise.sh" || exit 1; fi

paso 7 "$(t "Conectar el editor con Claude" "Connect the editor to Claude")"
mkdir -p "$HOME/.claude/skills"
L="$HOME/.claude/skills/jackieg-reel-editor"
if [ -L "$L" ] && [ "$(readlink "$L")" = "$REEL_SKILL" ]; then echo "  ✅ $(t "Ya estaba conectado" "Already connected")"
elif [ -e "$L" ]; then echo "  ⚠️  $(t "Ya existe $L y no es este editor: no lo toqué." "$L already exists and isn't this editor: left it alone.")"
else ln -s "$REEL_SKILL" "$L" && echo "  ✅ $(t "Conectado: en cualquier chat escribe /jackieg-reel-editor o di \"edita mi reel\"" "Connected: in any chat type /jackieg-reel-editor or say \"edit my reel\"")"; fi

printf '\n%s\n\n' "── $(t "Revisión final" "Final check")"
bash "$S/doctor.sh"; RC=$?
# READY WITH LIMITS (2) is a finished install: only optional items are missing
[ "$RC" -eq 2 ] && exit 0; exit "$RC"
