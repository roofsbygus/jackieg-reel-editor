# Third-party notices

## claude-reel-editor (base of this project)
- Source: https://github.com/nicolapocock/claude-reel-editor, forked at commit `c6939d937900e321cb0c74000457c975dab5f425` (2026-11-01)
- Author: Nicola Pocock (getgitgirl)
- License: MIT. The original copyright and permission notice are kept in [LICENSE](LICENSE).
- Perlili changed: the name (skill folder `reel-editor` → `perlili-video-editor`), the README, and the changes listed in the commit history after that commit.

## HyperFrames (used to transcribe, build and render; not included in this repository)
- Source: https://github.com/heygen-com/hyperframes, used at version `0.9.86` (commit `574b5e3d3bbf526809d268a6728f9c5ce52e18bb`), npm package `hyperframes@0.9.86`
- Copyright 2026 HeyGen, Inc.
- License: Apache License 2.0. Full text in [licenses/HyperFrames-Apache-2.0.txt](licenses/HyperFrames-Apache-2.0.txt).
- HyperFrames has no NOTICE file at that version.
- HyperFrames is installed from npm on the user's Mac. Perlili doesn't change HyperFrames' code. "HyperFrames" and "HeyGen" are names of their owners; Perlili isn't affiliated with or endorsed by them.
- HyperFrames' own `CREDITS.md` lists further licenses for optional parts. Perlili doesn't use the Parakeet model (CC-BY-4.0) or the 3D-motion catalog pieces that ship their own copy of GSAP.

## GSAP (animation library; not included in this repository)
- Source: https://gsap.com, version `3.13.0` (`gsap.min.js` and `CustomEase.min.js`), downloaded by `scripts/setup_engine.sh` on the user's Mac and checked against a pinned sha256. The catalog motions also load GSAP.
- Copyright GreenSock / Webflow. License: the Standard "No Charge" GSAP License (https://gsap.com/standard-license): free, including commercial use, but not open source and with its own restrictions.
- The catalog motions load their own GSAP (3.14.2) from a CDN when online; the downloaded 3.13.0 copy is what renders offline.

## Other pieces installed with HyperFrames (not included in this repository)
- sharp's libvips binaries (`@img/sharp-libvips-*`): LGPL-3.0-or-later, installed from npm as a HyperFrames dependency and not modified.
- Fonts in the HyperFrames motion assets that get copied into each reel's project: Permanent Marker (Apache-2.0) and Courier Prime (SIL OFL 1.1), used by `marker-checklist-card`, plus others listed in HyperFrames' assets.

## Speech recognition
- whisper.cpp (MIT, https://github.com/ggml-org/whisper.cpp), installed with Homebrew, and OpenAI Whisper model weights (MIT), downloaded by HyperFrames from https://huggingface.co/ggerganov/whisper.cpp. Neither is included in this repository.
