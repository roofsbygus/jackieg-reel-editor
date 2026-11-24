#!/usr/bin/env bash
# Instalación del editor Perlili, en pasos fijos. Se puede volver a correr: lo que ya está instalado se salta.
# What it does, in order: checks the Mac, installs the 4 Homebrew tools that are missing (never Homebrew itself, never
# sudo), the pinned HyperFrames (npm ci --ignore-scripts), the video templates, the caption model, the noise cleanup,
# links the skill into ~/.claude/skills, then runs the doctor. It never touches ~/.claude/settings.json (the safety
# rules are applied separately, with the person's OK) and never pays for or uploads anything.
set -uo pipefail
source "$(dirname "$0")/perlili_env.sh"
S="$(cd "$(dirname "$0")" && pwd)"
paso() { printf '\n%s\n' "── Paso $1 de 7: $2"; }
falla() { printf '\n❌ %s  [%s]\n   Solución: %s\n' "$2" "$1" "$3" >&2; exit 1; }

echo "Instalación del editor Perlili"

paso 1 "Revisar tu Mac"
[ "$(uname)" = Darwin ] || falla PV-MAC "No es una Mac" "este editor solo funciona en Mac."
[ "$(/usr/sbin/sysctl -n hw.optional.arm64 2>/dev/null)" = 1 ] || falla PV-CHIP "Esta Mac tiene chip Intel" "el editor necesita una Mac con chip Apple (M1 o más nuevo)."
FREE_GB=$(df -Pk "$HOME" | awk 'NR==2{print int($4/1048576)}')
[ "$FREE_GB" -ge 10 ] || falla PV-DISCO "Solo ${FREE_GB} GB libres" "libera espacio hasta tener al menos 15 GB y vuelve a empezar."
[ -x /opt/homebrew/bin/brew ] || falla PV-BREW "Falta Homebrew" "instálalo con el instalador .pkg de https://brew.sh (te pide la contraseña de tu Mac; hazlo tú, no Claude). Después vuelve a decir \"instala mi editor Perlili\"."
echo "  ✅ Mac con chip Apple, ${FREE_GB} GB libres, Homebrew listo"

paso 2 "Programas de Homebrew (FFmpeg, Node.js, Whisper, uv)"
FALTAN=()
command -v ffmpeg >/dev/null || FALTAN+=(ffmpeg)
NMAJ="$(node --version 2>/dev/null | sed 's/^v//; s/\..*//')"; [ "${NMAJ:-0}" -ge 22 ] || FALTAN+=(node)
command -v whisper-cli >/dev/null || FALTAN+=(whisper-cpp)
command -v uv >/dev/null || FALTAN+=(uv)
if [ ${#FALTAN[@]} -eq 0 ]; then echo "  ✅ Ya estaban todos"
else
  echo "  Instalando: ${FALTAN[*]} (puede tardar unos minutos)..."
  /opt/homebrew/bin/brew install "${FALTAN[@]}" || falla PV-BREW-INSTALL "Homebrew no pudo instalar ${FALTAN[*]}" "revisa tu internet y vuelve a correr la instalación."
  echo "  ✅ Listo"
fi

paso 3 "Motor de video (HyperFrames, versión fija)"
WANT="$(python3 -c "import json,sys;print(json.load(open(sys.argv[1]))['dependencies']['hyperframes'])" "$PERLILI_SKILL/package.json")"
HAVE="$(python3 -c "import json,sys;print(json.load(open(sys.argv[1]))['version'])" "$PERLILI_SKILL/node_modules/hyperframes/package.json" 2>/dev/null)"
if [ "$HAVE" = "$WANT" ]; then echo "  ✅ HyperFrames $HAVE ya estaba"
else
  (cd "$PERLILI_SKILL" && NPM_CONFIG_UPDATE_NOTIFIER=false npm ci --ignore-scripts --no-audit --no-fund --loglevel=error >/dev/null) || falla PV-HF "No se pudo instalar HyperFrames" "revisa tu internet y vuelve a correr la instalación."
  echo "  ✅ HyperFrames $WANT instalado"
fi

paso 4 "Plantillas y efectos de sonido"
bash "$S/setup_engine.sh" >/dev/null || falla PV-PLANTILLAS "No se pudieron bajar las plantillas" "revisa tu internet y vuelve a correr la instalación."
echo "  ✅ Listas"

paso 5 "Modelo de subtítulos (español e inglés, ~3 GB la primera vez)"
bash "$S/setup_models.sh" || exit 1

paso 6 "Limpieza de ruido (DeepFilterNet, ~1 GB la primera vez)"
if uv tool list 2>/dev/null | grep -q '^deepfilternet v0\.5\.6$' && deepFilter --help >/dev/null 2>&1; then echo "  ✅ Ya estaba"
else bash "$S/setup_denoise.sh" || exit 1; fi

paso 7 "Conectar el editor con Claude"
mkdir -p "$HOME/.claude/skills"
L="$HOME/.claude/skills/perlili-video-editor"
if [ -L "$L" ] && [ "$(readlink "$L")" = "$PERLILI_SKILL" ]; then echo "  ✅ Ya estaba conectado"
elif [ -e "$L" ]; then echo "  ⚠️  Ya existe $L y no es este editor: no lo toqué. Pídele ayuda a Perlili."
else ln -s "$PERLILI_SKILL" "$L" && echo "  ✅ Conectado: en cualquier chat puedes decir \"edita mi reel\""; fi

printf '\n%s\n\n' "── Revisión final"
bash "$S/doctor.sh"; RC=$?
# LISTO CON LÍMITES (2) is a finished install: only optional items are missing
[ "$RC" -eq 2 ] && exit 0; exit "$RC"
