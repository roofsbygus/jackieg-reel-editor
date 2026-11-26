"""build_reel.py and catalog motions: brand colours survive the runtime's variable CSS, transparent background,
brand fonts, CustomEase loaded locally, and the marker-checklist-card circle fix.
Run: python3 tests/test_build_reel_motions.py   (needs ffmpeg and the engine from scripts/setup_engine.sh; no network)"""
import json, os, re, subprocess, sys, tempfile
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SKILL = ROOT / "skills/jackieg-reel-editor"
HF = SKILL / "engine/hf/compositions/components"
NEED = ["headline-slam", "marker-checklist-card", "kinetic-center-build", "cta-close", "agent-cursor", "before-after-wipe", "cosmic-orb"]
if not all((HF / f"{m}.html").exists() or (HF.parent / f"{m}.html").exists() for m in NEED) or not (SKILL / "engine/gsap.min.js").exists():
    if os.environ.get("CI"): sys.exit("FAILED: engine motions missing in CI (setup_engine.sh didn't fetch them)")
    print("skipped: run skills/jackieg-reel-editor/scripts/setup_engine.sh first (the test uses its motions)"); raise SystemExit(0)

with tempfile.TemporaryDirectory() as d:
    home = Path(d) / "reels"; reel = home / "2026-01-01-test"; reel.mkdir(parents=True)
    (home / "brand.json").write_text(json.dumps({"colors": {"main": "#474330", "pop": "#CC4932", "light": "#DEDACB", "soft": "#E69101"},
                                                 "fonts": {"head": {"family": "Testface", "weight": 900}, "body": {"family": "Bodyface", "weight": 500}}}))
    subprocess.run(["ffmpeg", "-v", "error", "-y", "-f", "lavfi", "-i", "color=c=gray:s=1080x1920:r=30:d=6",
                    "-f", "lavfi", "-i", "anullsrc=r=48000:cl=stereo", "-t", "6", "-c:v", "libx264", "-pix_fmt", "yuv420p",
                    "-c:a", "aac", str(reel / "master.mp4")], check=True)
    (reel / "edit.json").write_text(json.dumps({"captions": [], "punch": [], "cards": [
        {"type": "motion", "name": "headline-slam", "start": 0.5, "end": 2, "vars": {"text": "WIND DAMAGE", "accent": "pop"}},
        {"type": "motion", "name": "marker-checklist-card", "start": 2, "end": 4, "vars": {"top": "3 STEPS"}},
        {"type": "motion", "name": "kinetic-center-build", "start": 4, "end": 5.5, "vars": {"text": "FREE ROOF INSPECTION"}},
        {"type": "motion", "name": "cta-close", "start": 0, "end": 1, "vars": {"action_line": "CALL US", "button_label": "BOOK"}},
        {"type": "motion", "name": "agent-cursor", "start": 1, "end": 2, "vars": {"agent_name": "GUS"}},
        {"type": "motion", "name": "before-after-wipe", "start": 2, "end": 3, "vars": {"label_a": "BEFORE", "label_b": "AFTER"}},
        {"type": "motion", "name": "cosmic-orb", "start": 3, "end": 4, "vars": {"accent": 30}}]}))
    r = subprocess.run([sys.executable, str(SKILL / "scripts/build_reel.py"), str(reel)], capture_output=True, text=True,
                       env={**os.environ, "REELS_HOME": str(home)})
    assert r.returncode == 0, r.stdout + r.stderr
    proj = reel / "proj"; index = (proj / "index.html").read_text()

    # 1. brand colours on --pv-* (the runtime writes "accent" onto --accent, so that name can't carry the brand colour)
    assert "--pv-accent:#CC4932" in index and "--pv-brand:#474330" in index and "--pv-accent-2:#E69101" in index, "brand tokens missing"
    for m in NEED:
        t = next((proj / "compositions").rglob(f"{m}.html")).read_text()
        assert not re.search(r"var\(--(brand|accent|accent-2)[,)]", t), f"{m}: still reads a colour token a variable can overwrite"
    # "pop" means the catalog's blue slot, which now reads --pv-accent
    vals = [json.loads(v.replace("&quot;", '"')) for v in re.findall(r'data-variable-values="([^"]*)"', index)]
    assert vals[0]["accent"] == "blue", vals[0]                      # named choice: "pop" -> the slot reading --pv-accent
    assert vals[1].get("accent") is None, "a motion without an accent setting got one"
    assert vals[3]["accent"] == "blue", vals[3]                      # left out -> pop
    assert vals[4]["accent"] == "#CC4932", vals[4]                   # free colour setting -> the brand hex, not "blue"
    assert vals[6]["accent"] == 30, vals[6]                          # a hue: passed through untouched
    wipe = (proj / "compositions/components/before-after-wipe.html").read_text()
    assert 'getPropertyValue("--pv-accent")' in wipe and 'getPropertyValue("--accent")' not in wipe, "JS still reads --accent"

    # 2. transparent background and brand font
    hosts = dict(re.findall(r'data-composition-id="([^"]+)"[^>]*style="([^"]*)"', index))
    for m in ("headline-slam", "marker-checklist-card", "kinetic-center-build", "agent-cursor", "before-after-wipe"):
        assert "--bg:transparent" in hosts[m], f"{m} keeps its dark demo background"
    assert "--bg:#DEDACB" in hosts["cta-close"], "cta-close uses --bg as its button text colour: brand light, not transparent"
    assert "--bg:transparent" not in hosts["cosmic-orb"], "background loops keep their base colour"
    assert "--font-display:'Testface'" in index, "motions don't use the brand head font"
    assert "--font-body:'Bodyface'" in index, "motions don't use the brand body font (--font-body)"

    # 3. CustomEase from vendor/, so kinetic-center-build works offline
    if (SKILL / "engine/CustomEase.min.js").exists():
        assert (proj / "vendor/CustomEase.min.js").exists() and 'src="vendor/CustomEase.min.js"' in index, "CustomEase not loaded locally"

    # 4. marker-checklist-card circle: thin stroke in the reel's copy, catalog copy untouched
    card = (proj / "compositions/components/marker-checklist-card.html").read_text()
    assert "stroke-width: 0.6cqmin;" in card and "stroke-width: 1.8cqmin;" not in card, "checklist circle patch not applied"
    assert "stroke-width: 1.8cqmin;" in (HF / "marker-checklist-card.html").read_text(), "patched the cached catalog copy"
    assert "patch for" not in r.stdout, r.stdout

print("PASS: build_reel motions (brand colours incl. JS and colour settings, background rules, brand fonts, local CustomEase, checklist circle)")
