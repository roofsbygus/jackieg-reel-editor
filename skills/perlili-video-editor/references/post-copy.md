# Post draft (caption, hashtags, title)

Every finished reel gets a ready-to-paste post draft next to the video. The person posts it themselves: never post, schedule or upload anything for them, even if a social tool is connected.

## Where the words come from
Only from three places: what they say in the reel (`master_transcript.json`), their brand file (`brand.md` / `brand.json`: website, call to action, account description), and anything they tell you for this post. Nothing else.
- No numbers they didn't say: prices, years in business, star ratings, "100+ roofs", percentages, phone numbers.
- No promises they didn't make ("free roof", "we'll get you approved"): use their own wording ("It starts with a free roof inspection").
- No customer details: no street, house number or client name, even if they said one on camera. A city they said is fine.
- Missing something you'd want (a phone number, an offer, a deadline)? Leave it out and mention it in one line. Don't invent it.

## Language
Write in the reel's language (`language.json`). Spanglish stays Spanglish: trade words they say in English stay English ("drip edge", "claim"). Bilingual captions in the reel → write the caption in both languages, theirs first.

## Format: `<reel folder>/post.md`
```
# <clear name of the reel>
Language: <en|es>

## Caption
<hook: the reel's main point in their words, one short line>
<1-3 short lines: what they'll learn or see, in their words>
<call to action from brand.json "cta">
<website from brand.md, if it has one>

## Hashtags
#tag #tag #tag

## Title (YouTube Shorts)
<under 100 characters>
```
- Caption: short. The first line is the hook (only that line shows before "more"). At most 2 emojis, none if the brand file says no emojis.
- Hashtags: 3 to 8. Built only from the reel's topic (words they say: #RoofReplacement, #DripEdge) and the area in the brand file (#DFWRoofing for a Dallas–Fort Worth brand). Never brand names of products they didn't name.
- Title: what the reel is, plainly ("How a roof insurance claim works").

## Check, then deliver
Run `python3 scripts/check_post.py <reel folder>`. It fails on any number, link, @handle or email that isn't in the transcript or the brand file, and on lengths over the platform limits. Fix `post.md` until it passes (don't loosen the check). `deliver.sh` then saves it next to the video as `<clear name> - post.txt`. Show them the caption in chat too, so they can copy it from their phone.
