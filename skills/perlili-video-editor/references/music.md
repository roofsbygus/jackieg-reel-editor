# Music bed (licensed, picked to fit the reel, they approve)

A quiet music track under the voice, chosen by you to match what the reel says and how it feels. It is mixed into the video file itself (so it goes out through WoopSocial or any upload), about 18 dB under the voice, ducking further while they talk, fading in and out. Sound effects are separate and already automatic (brand.json `"sfx"`).

Instagram's own music (the song picker in the app, trending sounds) can't be used here: it's licensed for personal, non-commercial use, it can't be added through WoopSocial or any posting API, and a business account is commercial. A track from Spotify, YouTube or a "copyright free" compilation isn't licensed either. Only the sources below.

## Approved sources

| `--source` | Where | Cleared for | Notes |
|---|---|---|---|
| `meta` | Meta Sound Collection (facebook.com/sound/collection; sign in and accept its terms first, they do that) | Instagram and Facebook only | Commercial use is allowed, but not on TikTok or YouTube. `music.py` blocks it for those. |
| `pixabay` | pixabay.com/music | Every network | Free, no credit needed. Anyone can upload there, so now and then a track gets a copyright claim: keep the license URL (it's saved in the library) to dispute it. |
| `mixkit` | mixkit.co/free-stock-music | Every network | Free, no credit needed. |
| `cc0` | A track marked CC0 (e.g. Free Music Archive) | Every network | No conditions. |
| `cc-by` | A track marked CC BY (e.g. Free Music Archive) | Every network | Needs the credit line its page asks for; `music.py check` makes sure it's in the caption. |
| `own` | Music they made or bought outright | Every network | Ask what license they have if they bought it. |

Never: anything marked NC (NonCommercial) or ND (NoDerivatives), YouTube Audio Library tracks (each one has its own rules; skip them), or a track whose page doesn't show its license.

## The library (one per brand)

Tracks live in `<brand>/music/` with `library.json`, so every reel's music traces back to its license. Build it once with 8-15 tracks across moods, so picking is automatic afterwards; add more whenever nothing fits.

1. Search the approved sites for tracks that suit the brand (their brand file: tone, audience) and the moods they post most. Instrumental only (no singing under a talking voice), steady, no big drops. Give them 2-3 links per mood with one line each on why it fits.
2. **Downloading is theirs to approve.** Ask before downloading anything. On Meta Sound Collection they sign in and accept the terms themselves; never sign in to their Facebook.
3. Check the license on the track's own page, then add it:
   `python3 scripts/music.py add <downloaded file> --source pixabay --license-url <the track's page> --title "<title>" --artist "<artist>" --mood calm,warm`
   (`--credit "<exact line>"` for CC BY.) The download is copied in, never changed.
4. `python3 scripts/music.py list` shows what's there.

Mood words (use the same ones every time): calm, warm, upbeat, energetic, inspiring, serious, playful, dramatic, ballad, lofi, corporate.

## Each reel

1. Brand says `"music": "none"`? Skip: `python3 scripts/music.py none <reel>`.
2. Read the kept lines and pick 1-3 mood words that fit what they say and how they say it (a storm-damage warning is serious, a finished-roof reveal is upbeat or inspiring).
3. `python3 scripts/music.py pick <reel> --mood serious,calm` (add `--platforms INSTAGRAM,TIKTOK` if this reel goes somewhere the brand's usual accounts don't). It writes `music.json` with the choice and up to 3 alternatives. Exit 2 = nothing fits: say so and offer to find tracks (library steps above). Never grab an unlicensed track to fill the gap.
4. `render.sh` mixes it in. Tell them the track's name and source and ask them to **listen**. Don't approve for them.
   - Another one: `python3 scripts/music.py swap <reel> 1` (or a title), then `bash scripts/mix_music.sh <reel>`. Seconds, no re-render.
   - Louder or quieter: change `gain_db` in `music.json` (default -18; between -24 and -14), then `mix_music.sh` again.
   - No music after all: `python3 scripts/music.py none <reel>`, then `mix_music.sh`.
5. On their yes: `python3 scripts/music.py approve <reel>`. CC BY: put the credit line at the end of the caption in `post.md`.
6. `python3 scripts/music.py check <reel>` must pass before delivering. `woop_posts.py` runs the same check for the networks it posts to and refuses a track that isn't cleared there (a Meta Sound Collection track on TikTok, say).
