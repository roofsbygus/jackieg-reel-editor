"""Plugin + marketplace manifests stay valid and in step (name, version, skill folder)."""
import json, pathlib, sys

root = pathlib.Path(__file__).resolve().parent.parent
plugin = json.loads((root / ".claude-plugin/plugin.json").read_text(encoding="utf-8"))
market = json.loads((root / ".claude-plugin/marketplace.json").read_text(encoding="utf-8"))
errors = []
if plugin.get("name") != "jackieg-reel-editor": errors.append("plugin.json name must be jackieg-reel-editor")
entries = [p for p in market.get("plugins", []) if p.get("name") == plugin.get("name")]
if len(entries) != 1: errors.append("marketplace.json must list the plugin exactly once")
elif entries[0].get("version") != plugin.get("version"): errors.append("marketplace and plugin versions differ")
if not market.get("name") or not market.get("owner", {}).get("name"): errors.append("marketplace needs name and owner.name")
if not (root / "skills" / plugin["name"] / "SKILL.md").is_file(): errors.append("skills/<name>/SKILL.md missing")
if not (root / "settings/permisos-seguridad.json").is_file(): errors.append("settings/permisos-seguridad.json missing")
json.loads((root / "settings/permisos-seguridad.json").read_text(encoding="utf-8"))
if errors:
    print("\n".join(errors)); sys.exit(1)
print("plugin manifest ok")
