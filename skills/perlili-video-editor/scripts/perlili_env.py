"""Shared setup for every Perlili script. Import it first: `import perlili_env` (scripts/ is on sys.path when a script runs).

- PATH: Claude Desktop's Code tab doesn't load ~/.zprofile, so Homebrew's ffmpeg, ffprobe and whisper-cli aren't found by name.
  Put the usual install folders in front, for this process and everything it starts.
- Telemetry and self-updates of HyperFrames: off.
- HyperFrames: only the pinned copy in this skill (package.json + package-lock.json), never `npx -y`.
- Language: one place that decides es / en for a reel folder, so transcription, filler detection, review and QA agree."""
import json, os, sys
from pathlib import Path

SKILL = Path(__file__).resolve().parent.parent
HOME = Path(os.environ.get("REELS_HOME", "~/reels")).expanduser()

_extra = ["/opt/homebrew/bin", "/usr/local/bin", str(Path("~/.local/bin").expanduser())]
os.environ["PATH"] = os.pathsep.join(_extra + [p for p in os.environ.get("PATH", "").split(os.pathsep) if p and p not in _extra])
for k in ("HYPERFRAMES_NO_TELEMETRY", "DO_NOT_TRACK", "HYPERFRAMES_NO_UPDATE_CHECK", "HYPERFRAMES_NO_AUTO_INSTALL"):
    os.environ[k] = "1"

HF_BIN = SKILL / "node_modules" / ".bin" / "hyperframes"
LANGS = ("es", "en")
DEFAULT_MODEL = "large-v3"   # picked by the caption test, docs/pruebas/prueba-subtitulos-2026-11-23.md


def hyperframes():
    """Path to the pinned HyperFrames, or stop with a fix the person can follow."""
    if not HF_BIN.exists():
        sys.exit("PV-HF: HyperFrames no está instalado en el editor. / HyperFrames isn't installed. "
                 f"Fix: cd \"{SKILL}\" && npm ci --ignore-scripts")
    return str(HF_BIN)


def brand():
    f = HOME / "brand.json"
    return json.load(open(f)) if f.exists() else {}


def whisper_model(b=None):
    return (b if b is not None else brand()).get("whisper_model", DEFAULT_MODEL)


def reel_language(folder, b=None):
    """The reel's spoken language: brand.json "language" if fixed to es/en, else what transcribe.py detected
    for this folder (language.json), else None (not known yet: let Whisper detect it)."""
    b = b if b is not None else brand()
    if b.get("language") in LANGS:
        return b["language"]
    f = Path(folder) / "language.json"
    if f.exists():
        lang = json.load(open(f)).get("language")
        if lang in LANGS:
            return lang
    return None


def save_language(folder, lang, source, model):
    json.dump({"language": lang, "source": source, "model": model}, open(Path(folder) / "language.json", "w"))
