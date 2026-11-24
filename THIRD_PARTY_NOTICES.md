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
- HyperFrames' own `CREDITS.md` lists further licenses for optional parts. Perlili doesn't use: the Parakeet model (CC-BY-4.0) or the 3D-motion catalog pieces that include GSAP (GSAP Standard License, not open source).

## Speech recognition
- whisper.cpp (MIT, https://github.com/ggml-org/whisper.cpp), installed with Homebrew, and OpenAI Whisper model weights (MIT), downloaded by HyperFrames from https://huggingface.co/ggerganov/whisper.cpp. Neither is included in this repository.
