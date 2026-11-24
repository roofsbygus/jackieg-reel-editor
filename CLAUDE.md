# JackieG Reel Editor

The people using this folder are Jackie G's students (Latinos en Roofing University, Latinos in Business) and her followers. Most are not technical. Talk to them in the language they write in (Spanish or English), in plain words. They never use Terminal: you run everything here and ask permission.

## "Instala mi editor de reels" / "install my reel editor" (or "instala el editor", "set up the editor")

1. Run `bash skills/jackieg-reel-editor/scripts/install.sh es` if they write in Spanish, `... install.sh en` if in English. It saves that language for the check and the review page. The first time can take 20 to 40 minutes: run it in the background and tell them which step it's on.
2. If it stops with ❌ and a `JG-...` code, explain the fix it printed in simple words. Homebrew, and anything else that asks for the Mac's password, the person installs themselves, never you.
3. At the end, if the check says the safety rules are missing (`JG-REGLAS`), offer to apply them: show what `settings/permisos-seguridad.json` does, ask for their yes, back up `~/.claude/settings.json` first, and merge without removing what they already have.
4. Tell them they can now type `/jackieg-reel-editor` or say "edita mi reel" / "edit my reel" in any Code-tab chat.

## "Revisa mi editor de reels" / "check my reel editor"

Run `bash skills/jackieg-reel-editor/scripts/doctor.sh` and explain the result in simple words. The last line decides: LISTO ✅ / READY ✅ or LISTO CON LÍMITES ⚠️ / READY WITH LIMITS ⚠️ = they can edit (before the first reel, ⚠️ JG-CHROME is normal); FALTA ALGO ❌ / SOMETHING'S MISSING ❌ = help them fix each ❌ before editing.

## "Cambia el idioma" / "switch to English"

Run `bash skills/jackieg-reel-editor/scripts/install.sh en` (or `es`): it only saves the new language and skips everything already installed. The review page also has an EN/ES button.

Never use `npx -y`, `sudo` or scripts downloaded with `curl | sh`. Never delete or change their original videos.
