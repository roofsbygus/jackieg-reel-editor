---
name: jackieg-reel-editor
description: JackieG Reel Editor (/jackieg-reel-editor). Use when someone drops a raw talking-head video (phone clip, selfie video, webcam recording) and wants it edited into a short-form reel, TikTok or YouTube Short in their own brand style - "edit this", "make this a reel", "cut this down", "add captions and graphics", "send it to CapCut", or in Spanish "edita mi reel", "hazlo reel", "junta estos videos". Also use the first time someone installs this skill or says "set up my brand", and when they want a cover or thumbnail for a reel ("open my thumbnail studio", "make a cover").
---

# JackieG Reel Editor

**Language:** talk to the person in the language they write in. Their install choice is in `~/.config/jackieg-reel-editor/lang` (es/en): the setup check and the review page use it, and the page has an EN/ES button.

Turns a raw talking-head clip into a finished, on-brand vertical reel. Every brand choice (colours, fonts, caption style, sounds, CTA) comes from the person's **brand file**, never from defaults baked into this skill. You do the editing; they only make the calls that are theirs.

## Install and check (as a plugin, this replaces the repo's CLAUDE.md)

Talk to them in the language they write in (Spanish or English), in plain words; most are not technical and never use Terminal. `scripts/` below means this skill's own `scripts/` folder; the plugin root is two folders up from this file.

- **"Instala mi editor de reels"** / "install my reel editor": run `bash scripts/install.sh es` if they write in Spanish, `bash scripts/install.sh en` if in English (it saves that language for the check and the review page). The first time takes 20 to 40 minutes: run it in the background and say which step it's on. If it stops with ❌ and a `JG-...` code, explain the fix it printed simply. Homebrew and anything that asks for the Mac password, the person installs themselves, never you. If the check reports `JG-REGLAS`, offer the safety rules: show what `<plugin root>/settings/permisos-seguridad.json` does, get their yes, back up `~/.claude/settings.json` first and merge without removing what's there. Then tell them they can type `/jackieg-reel-editor` or say "edita mi reel" / "edit my reel".
- **"Revisa mi editor de reels"** / "check my reel editor": run `bash scripts/doctor.sh` and explain it simply. The last line rules: LISTO ✅ / READY ✅ or LISTO CON LÍMITES ⚠️ / READY WITH LIMITS ⚠️ = ready (⚠️ JG-CHROME before the first reel is normal); FALTA ALGO ❌ / SOMETHING'S MISSING ❌ = fix each ❌ first.
- **"Cambia el idioma"** / "switch to English": `bash scripts/install.sh en` (or `es`) only saves the language. The review page also has an EN/ES button.
- Never use `npx -y`, `sudo` or `curl | sh`. Never delete or change their original videos.

## Before anything else: which brand, and is there a brand file?

The workspace is `~/reels-jackieg/` unless `REELS_HOME` is set. One person can have several brands (their own business, a client, LERU): each brand is a folder with its own `brand.json`, `brand.md`, `fonts/`, `assets/` and reels, either `~/reels-jackieg` itself or a folder inside `~/reels-jackieg/` or `~/reels-jackieg/brands/`.

1. **Pick the brand.** If they named one ("edit my Trust In Gus reel"), run `python3 scripts/brands.py "<the name they said>"`: exit 0 prints that brand's folder. Exit 3 means more than one matches and exit 2 means none does: show them the list it printed and ask which one. If they named none, run `python3 scripts/brands.py`: with one brand use it; with several, ask which (show the names). Tell them which brand you're using.
2. **Use it for the whole edit.** Put `REELS_HOME=<that folder>` in front of every script you run for this reel (each command runs on its own, so set it every time), e.g. `REELS_HOME=~/reels-jackieg/leru python3 scripts/transcribe.py ...`. The reel folder goes inside that brand's folder. Never mix brands within one reel.
3. **A new brand** ("set up a brand for my client X"): make `~/reels-jackieg/<short-name>/` and run the setup interview with `REELS_HOME` set to it. With only one brand, `~/reels-jackieg` itself stays fine.

Below, `~/reels-jackieg/` means the chosen brand's folder.

- **No `~/reels-jackieg/brand.md`** → run the setup interview in `references/setup-interview.md` first. Do not edit a clip without a brand file, even if they say "just use whatever". The interview takes 5 minutes and it is the whole point of this skill.
- **Brand file exists** → read `brand.md` and `brand.json` in full, then continue.

## Check the tools (once per machine)

First install: `bash scripts/install.sh` (7 fixed steps, safe to re-run, ends with the doctor). `bash scripts/doctor.sh` - checks ffmpeg, Node, the pinned HyperFrames (`npm ci --ignore-scripts` in this skill folder; never `npx -y`) and (if the brand file says CapCut) the CapCut connector. Fix anything it flags before editing. Install steps are in the repo README.

## The edit, in order

Each reel gets its own folder: `~/reels-jackieg/<yyyy-mm-dd>-<short-name>/`. Copy the raw clip in as `raw.<ext>` (e.g. `raw.mov`), never edit the original. The thumbnail studio only finds footage named `raw.*`.

**Several clips for one reel** (they say "junta estos videos" / "join these", or drop more than one video): `python3 scripts/join_clips.py <folder> <clip> <clip> ...` instead of copying. It joins them oldest first (their phone's recording time; `--keep-order` keeps the order they gave) into `raw.mov` + `clips.json`, filling the vertical frame. Tell them the order and ask them to confirm it. If it flags a clip as horizontal, say its sides get cropped. Everything after this works as for one clip: `transcribe.py` transcribes each clip on its own (so words can't drift across a join) and drops words Whisper invents on clips with no talking; the review page marks where each clip starts.

1. **Transcribe** - `python3 scripts/transcribe.py <clip> transcript.json`. Local Whisper (`large-v3`) through the pinned HyperFrames: free, on this Mac. It **detects Spanish or English** and saves it in `language.json`; every later step in this folder uses the same language. **Tell the person which language was detected** and ask them to confirm before the review. If they say it's wrong, re-run with `--language es` or `--language en`. Never assume English. Spanglish is normal: English words stay English inside Spanish captions. **Caption language:** by default captions are in the language they speak. Ask once per reel (and remember a standing answer in brand.json `"captions": {"translate": {"to": "en", "mode": "bilingual"}}`): same language, **translated** (e.g. English captions on a Spanish video, to reach more people) or **bilingual** (their words plus a smaller translated line, same pill). For translated/bilingual, after the review export: you translate every line of `captions_to_translate.txt` yourself (natural, short, the trade words they'd say: "drip edge" stays "drip edge"; star the key word, `*arriba*`), save it as `translations.txt` with the same numbers, and run `python3 scripts/review_sync.py translate <folder> translations.txt <es|en> <translated|bilingual>`. No paid translation service. They check and fix the translations on the page. Names Whisper mishears go in `brand.json` `"corrections"` (e.g. `{"trusting gus": "Trust In Gus"}`). ElevenLabs Scribe is used only if `brand.json` has `"elevenlabs": true` and a key is in `~/.config/reels/.env`; it uploads the audio and costs money, so never turn it on yourself. If it prints `NO SPEECH FOUND`, the clip has no talking: no captions for it.
2. **Clean the voice** - `bash scripts/clean_audio.sh <clip> voice.wav`: rumble cut, DeepFilterNet voice isolation (strong by default, for wind and job-site noise; `--light` or brand.json `"cleanup": "light"` for quiet rooms), then -14 LUFS, the level Instagram and TikTok expect. It prints the voice-to-background gap; under 30 dB, tell the person to listen to the Sound tab before approving.
3. **Review (their call)** - propose: lines to cut (repeats, false starts, rambles), fillers to drop, CTA moved to the end, target under 60 s, and the graphics plan. **Wait for their yes before cutting.** This is the step people care most about.
   **Look at the start and end before proposing cuts:** grab a frame every 0.5 s for the first and last 4 s. Cut any camera setup (pointing at the floor/garden, flipping the camera, reaching for the phone) even if words are spoken over it. Start on the first frame where they're settled in shot, and on a word that works as an opener.
   - **Main path: the Reel Review page.** First check that the `Artifact` and `ArtifactData` tools exist in this session (load them through tool search if they're deferred). If they do, follow `references/review.md`: they tap words to cut, watch the live rough cut, check graphics, captions, sound and colour, then say "build preview". Its import step writes `edl.json` + `edit.json`, so skip to step 4's cut and step 5.4's music.
   - **Fallback: review in chat** when those tools aren't there (older Claude Code, other apps). Show the transcript as numbered lines (format in `references/rough-cut.md`), then the card list in step 5.
4. **Tighten, then cut + speed** - write `edl.json` from the approved lines, then `python3 scripts/tighten.py <folder>`: it removes fillers and shortens pauses inside the kept lines, as hard as the brand's `"pacing"` says (`natural` default, `tight`, `fast`; presets in `scripts/pacing.py`). They never approve these one by one. Then `REEL_PREVIEW=1 python3 scripts/cut.py <folder>` (cuts at 1080p; a 4K brand's `--final` render re-cuts at 4K later). Speed comes from the same preset unless `brand.json` sets `"speed"`. Listen-check: re-transcribe `master.mp4` and confirm no clipped words at the joins.
5. **Graphics + captions: fill the template, don't design.** You are the editor here, not the designer - the look is already built from the brand file.
   1. `python3 scripts/transcribe.py master.mp4 master_transcript.json`
   2. `python3 scripts/auto_edit.py <folder>` → drafts `edit.json` (captions in their caption mode, punch-ins)
   3. Edit `edit.json` yourself, in one pass (on the chat-review route, translated/bilingual captions go here too: each caption's `"tr"` plus top-level `"caption_mode"`): set `"accent": true` on the one key word per sentence, and add cards at the density `brand.json` `"graphics"` asks for: `minimal` about one every 8-12 s, `balanced` (default) every 4-6 s, `busy` every 2-4 s. A line with nothing to show gets no card; don't chart every number or screenshot every tool just to fill the gap. Card types and fields are in the header of `scripts/build_reel.py`; HyperFrames catalog motions (carousels, charts, counters, notifications, cursor, follow cards) are in `references/motions.md`. Every card must show what that exact line says.
      - **Hook title:** max ~10 characters per line, 2-3 lines (`"still / uploading / screenshots?"`), so it renders big. It's the only text with an outline.
      - **Carousel:** if `brand.json` has `"require_carousel": true`, every reel gets one (`motion` card, a `carousel-*` name, `images` from screenshots/their assets). If no line suits one, ask them; if they say no, set `"no_carousel_ok": true`.
      - **Screenshots:** for a tool or site they name that the line is about, run `bash scripts/screenshot.sh <url> shots/<name>.png`. Exit code 2 means the site blocked it: try the tool's marketing page, or ask them for a screenshot. Never use a blank one.
      - Mix the kinds: website shots, a colour block, a list card (`"glass": true` for liquid glass), a sticker from their assets, a `follow` card for the big moment, a counter or chart when they say a number.
   4. **Music** - unless brand.json says `"music": "none"`, pick 1-3 mood words from what the kept lines say and how they say it, then `python3 scripts/music.py pick <folder> --mood <words>`: a licensed track from the shared music library (all their brands use it), cleared for where the reel goes. Exit 2 means nothing fits: offer to find tracks. Never use Instagram's in-app or trending songs or any unlicensed track. Library, sources and licenses: `references/music.md`.
   5. `REEL_PREVIEW=1 bash scripts/render.sh <folder>` → draft `final.mp4` + stage timings (1080x1920, low priority). At 1080p (the default) the approved draft is the final: render again only if `edit.json` changed, or with `--capcut` on the CapCut route. If `brand.json` asks for 4K, run `bash scripts/render.sh <folder> --final` after they approve (it re-cuts the master at 4K first; `--final --capcut` on the CapCut route).
   Do **not** hand-write composition HTML or use other HyperFrames workflows here: they are slower and ignore the brand template. Only if they explicitly ask for an effect the template lacks (e.g. text behind their head), say it's slower, then use the `hyperframes` skill for that one effect.
6. **QA** - write the approved script (the kept lines) to `<folder>/expected.txt` so the missing-words check runs, then `python3 scripts/qa.py <folder>` (on a 4K brand: `REEL_PREVIEW=1` for the draft, plain again after `--final`) (loudness, size, length, missing words). Then grab a frame at every card and look: text inside the frame, readable over the background, on brand. Fix `edit.json` and re-run render.sh until it passes.
7. **Post draft, then deliver** - the music must be approved first: they listened and said yes (`python3 scripts/music.py approve <folder>`; swap or remix with `references/music.md`). Then write `<folder>/post.md` (caption, 3-8 hashtags, a YouTube Shorts title) from their own words and their brand file only, following `references/post-copy.md` (a CC BY track: its credit line ends the caption), and run `python3 scripts/check_post.py <folder>` and `python3 scripts/music.py check <folder>` until both pass. Then `bash scripts/deliver.sh <final.mp4> "<clear name>"` → its own folder `<delivery folder>/<clear name>/` with the upload-ready MP4 and `<clear name> - post.txt`. Show them the caption in chat too.
8. **WoopSocial draft (when WoopSocial is connected)** - upload the delivered MP4 and create one post per chosen account as a **draft** with the checked caption: `references/woopsocial.md`. Publish now or schedule only when they say so for that post. Not connected: say so in one line with the connect steps; the delivered video and post.txt are enough.
9. **CapCut (only if `brand.json` has `"capcut": true`)** - build the editable CapCut draft and give them the link. `references/capcut.md`.

Tell them what changed, and what to check by ear (cuts, names, brand words spelled right).

## Cover / thumbnail

The review page's **Cover** tab links to the thumbnail studio, a local page for picking the cover frame, adding a headline in their brand fonts and downloading 1080x1920, 1080x1440 and 1080x1080 PNGs. Start it with `python3 scripts/thumbnail_studio.py <reel>` in the background, check it answers, then send the link. When they say "open my thumbnail studio", start it the same way (safe if it's already running). Details: "Thumbnail studio" in `references/review.md`. No review page? Start it with `--open` and send the link in chat.

## Their brand rules win

If the brand file and your taste disagree, the brand file wins. If they correct something during an edit ("no, never outline captions"), add it to `brand.md` under "Rules" straight away so the next edit gets it right.

## Common mistakes

| Mistake | Instead |
|---|---|
| Editing before a brand file exists | Run the setup interview |
| Cutting on Whisper word times blindly | Check the joins; nudge cuts into the quiet gap between words |
| Graphics that decorate instead of illustrate | Each card shows what this exact line says |
| Captions in a font the brand file bans | Re-read brand.md "Rules" before step 5 |
| Saying CapCut works everywhere | It doesn't (see capcut.md). The MP4 route always works |
| Fixing QA failures by lowering the bar | Fix the edit, re-run QA |
