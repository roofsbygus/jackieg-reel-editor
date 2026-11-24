"""Pacing presets: how hard the edit trims. One place, so cut.py, tighten.py and the review page agree.
brand.json "pacing": "natural" (default) | "tight" | "fast". An explicit brand.json "speed" still wins.

Fillers depend on the spoken language (perlili_env.reel_language). Spanish reels also get the English list,
because Spanglish speakers use both ("eh... um...").
- fillers: cut automatically (the person can tap any of them back on the review page)
- hesitations: cut only when a pause follows (Spanish "este..." is a filler, "este mes" is a real word)
- suggested: never cut automatically. Claude proposes them in the rough cut and the person decides ("pues", "bueno", "o sea")
brand.json "fillers" (a list) replaces the automatic list for every language; [] keeps every filler."""

FILLERS = {
    "en": {"natural": ["um", "uh", "umm", "uhm", "erm", "hmm", "mm"],
           "tight":   ["um", "uh", "umm", "uhm", "erm", "er", "ah", "hmm", "mm"]},
    "es": {"natural": ["eh", "ehh", "em", "emm", "mmm", "mm", "hmm"],
           "tight":   ["eh", "ehh", "em", "emm", "mmm", "mm", "hmm", "ah", "aah"]},
}
HESITATIONS = {"en": [], "es": ["este"]}
SUGGESTED = {"en": ["like", "you know", "basically", "kind of", "sort of"], "es": ["pues", "bueno", "o sea", "verdad", "okay"]}

PRESETS = {
    # pauses longer than pause_min get shortened, leaving `air` seconds either side of the cut
    "natural": {"speed": 1.0, "pause_min": 0.6, "air": 0.15},
    "tight":   {"speed": 1.1, "pause_min": 0.25, "air": 0.06},
    "fast":    {"speed": 1.15, "pause_min": 0.2, "air": 0.05},
}


def pacing(brand, lang="en"):
    name = brand.get("pacing", "natural")
    p = dict(PRESETS.get(name, PRESETS["natural"]))
    level = "natural" if name == "natural" else "tight"
    langs = ["es", "en"] if lang == "es" else ["en"]
    p["fillers"] = sorted({f for l in langs for f in FILLERS[l][level]})
    p["hesitations"] = sorted({f for l in langs for f in HESITATIONS[l]})
    p["suggested"] = [s for l in langs for s in SUGGESTED[l]]
    if brand.get("speed"): p["speed"] = float(brand["speed"])
    if brand.get("fillers") is not None: p["fillers"] = list(brand["fillers"])   # [] = keep every filler
    return p
