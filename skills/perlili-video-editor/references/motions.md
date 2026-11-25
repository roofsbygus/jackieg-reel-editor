# Motions (HyperFrames catalog, cached in engine/hf)

Use with a `motion` card in edit.json: `{"type":"motion","name":"<name>","start":..,"end":..,"vars":{..},"box":[x,y,w,h]}`.
Carousels also take `"images": [..]` and every slot is filled for you. `box` is where it sits on the 1080x1920 frame (default: full width, top).
Add more from the 456-item catalog: `cd engine/hf && ../../node_modules/.bin/hyperframes add <name> --no-clipboard` (browse with `../../node_modules/.bin/hyperframes catalog`; never `npx`, which would fetch an unpinned version).

| motion | size | use it for | settings (vars) |
|---|---|---|---|
| carousel-circle-1 | 1920x1080 | lists of tools/examples (the brand's required carousel) | `image1..N` (use images), `speed`, `background` |
| carousel-orbit-1 | 1920x1080 | lists of tools/examples (the brand's required carousel) | `image1..N` (use images), `speed`, `background` |
| carousel-path-1 | 1920x1080 | lists of tools/examples (the brand's required carousel) | `image1..N` (use images), `speed`, `background` |
| carousel-vision-1 | 1920x1080 | lists of tools/examples (the brand's required carousel) | `image1..N` (use images), `speed`, `background` |
| animated-bar-chart | fits box | comparing a few numbers | none (text is in the file) |
| caption-camera-follow | fits box | use the `follow` card instead (brand font + colours) | `accent`, `framing`, `smear` |
| caption-editorial-emphasis | 1920x1080 | don't mount: the template's editorial caption style does this in brand fonts | none (text is in the file) |
| chart-story | fits box | a chart that builds with exact values | `type`, `data`, `labels`, `emphasize`, `unit`, `accent`, `exit` |
| chat-message | fits box | a DM or chat bubble | `type`, `text`, `cardTitle`, `cardDomain`, `tail`, `delivered` |
| code-terminal-run | fits box | a command being typed | `prompt_glyph`, `cadence`, `cues`, `accent`, `exit` |
| count-up | fits box | a number that matters (stats, results) | `start`, `end`, `prefix`, `suffix`, `accent`, `glow`, `exit` |
| hw-arrow | 1920x1080 | point at something on screen | none (text is in the file) |
| hw-underline | 1920x1080 | circle/underline a word or UI element | none (text is in the file) |
| native-notification-pop | fits box | one iOS/macOS notification | `title`, `body`, `app_label`, `os`, `at`, `accent`, `exit` |
| notification-stack | fits box | results / alerts stacking up | `titles`, `bodies`, `expand`, `cues`, `accent`, `exit` |
| oversized-cursor | fits box | a click on a button in a screenshot | `cursor_variant`, `target_x`, `target_y`, `click_label`, `exit` |
| x-follow-card | fits box | follow CTA (X) | none (text is in the file) |
| instagram-follow | 1080x1920 | follow CTA at the end | none (text is in the file) |
| mk-line-graph | 1920x1080 | growth over time | none (text is in the file) |
| yt-comment-card | 1920x1080 | a comment you're replying to | none (text is in the file) |

## More motions, for every kind of reel

These all take your own words, images or colours through `vars`, so nothing from the catalog's demo has to show.
- Fill every text setting the line needs. A setting you leave out falls back to the catalog's sample text (some samples name HeyGen or HyperFrames).
- Settings that hold a list (`steps`, `nodes`, `items`, `messages`, `series` and the like) have their own format. Before filling one, read that setting's `description` and `example` in the motion's `data-composition-variables` (in `engine/hf/compositions/` or `engine/hf/compositions/components/`).
- Background loops (`aurora-drift`, `grain-field`, `snow`, `starfield`, `cosmic-orb`, `spiral-galaxy`, `halftone-field`, `vfx-anamorphic-flare`, `beat-pulse-background`) have no words; use them behind a title or a `page` card.
- Carousels: any name with `carousel` counts for the brand's carousel rule.
- Brand look is automatic: every motion gets a transparent background (no dark demo backdrop over the footage) and the brand's head font. `accent` picks a brand colour: `"pop"` (default when you leave it out), `"main"` or `"soft"`; the catalog names `blue` / `green` / `violet` mean the same three.
- Text sizes are set by each motion. A "fits box" motion lays out on a 1080x1080 stage: give it `"box": [0, 0, 1080, 1080]` (or wider, e.g. `[-110, -300, 1300, 1300]`) so its words read on a phone, and keep it over sky or a plain wall: olive text over a busy roof is hard to read.
- `marker-checklist-card` works with short words only: `circled` 3 letters or fewer, `top` / `rest` / row values about 8 characters (longer ones run off the card). Its circle is fixed automatically (it rendered too thick).
- Don't use `state-chip-rail` on a vertical reel (tested Nov 2026): the chips are too small to read. For steps, use `marker-checklist-card` or one motion per step (`char-slam-explode`, `scramble-reveal`, `line-swap`, `kinetic-center-build`).

| motion | size | use it for | settings (vars) |
|---|---|---|---|
| agent-cursor | fits box | Agent Cursor: An AI agent operating a UI: a cursor with an accent name label that types out each step, clicks each target with a... | `agent_name`, `steps`, `targets`, `accent` |
| ai-answer-rank | 1080x1080 | AI Answer Rank: Is your brand in the AI answer? A question types into a chat card, the assistant answers with a ranked list of three... | `prompt`, `lead`, `rowA`, `rowB`, `rowC`, `brand`, `brandRank`, `accent`, `ink`, `ground` |
| ai-chat-reveal | 1080x1920 | AI Chat Reveal: A question is typed on a rising keyboard, sent, and answered by an AI that streams its reply word by word on a measured... | `botName`, `userMessage`, `answer1`, `answer2`, `answer3`, `bullet1`, `bullet2`, `bullet3`, `ecHeadline`, `ecSub`, `ecCta`, `ecFooter`, `brandLogo` |
| ascii-trail-reveal | fits box | ASCII Trail Reveal: An authored S-curve sweeps through a deterministic ASCII grid, flipping cells away to reveal a labeled panel | `label`, `accent`, `trail_width` |
| aurora-drift | fits box | Aurora Drift: Three soft accent-derived aurora fields drift in an exact ambient loop over a deep base and faint vignette | `accent`, `mood` |
| avatar-cloud | fits box | Avatar Cloud: Lettermark avatars populate a loose elliptical cloud while fine SVG links draw between the community and its central... | `avatarCount`, `showLinks`, `label` |
| bar-chart-race | 1920x1080 | Bar Chart Race: Ranked bars grow and overtake each other as a time series advances, with the axis rescaling as values climb and the... | `title`, `subtitle`, `periods`, `series`, `barCount`, `periodDuration`, `valuePrefix`, `valueSuffix`, `valueDecimals`, `accent` |
| beat-accent | fits box | Beat Accent: A single music-hit sting: impact flash, micro scale-pulse on the subject, immediate decay | `text`, `flashColor`, `intensity` |
| beat-pulse-background | fits box | Beat Pulse Background: An accent-derived backdrop pulses its glow intensity and saturation on a deterministic, supplied beat grid | `beats`, `accent`, `intensity` |
| beat-timeline | fits box | Beat Timeline: A paused master-timeline orchestration spine that pins titled beat rows to evenly spaced named labels | `beatCount`, `interval`, `labels` |
| before-after-wipe | fits box | Before After Wipe: Two full-bleed content slots compare before and after states as a persistent divider wipes the after layer over the... | `label_a`, `label_b`, `rest_split`, `wipe_at`, `accent`, `exit` |
| browser-device-stage | fits box | Browser Device Stage: A generic app surface in token-native device chrome (browser, window, or phone) | `chrome`, `title`, `swap_at`, `accent`, `exit` |
| camera-scan-gate | fits box | Camera Scan Gate: A camera and QR recognition moment with a viewfinder sweep, bracket lock, confirmation pulse, and verified next beat | `scanColor`, `targetLabel`, `sweepSpeed` |
| carousel-circle-2 | 1920x1080 | Circle Carousel 2: Image cards ride a circle with a size gradient by depth angle, sweeping in fast-slow-fast swings (Circle style 2); 12... | `image1..N` (use images), `speed`, `background` |
| carousel-circle-3 | 1920x1080 | Circle Carousel 3: Image cards ride a circle with a size gradient by depth angle, sweeping in fast-slow-fast swings (Circle style 3); 12... | `image1..N` (use images), `speed`, `background` |
| carousel-circle-4 | 1920x1080 | Circle Carousel 4: Image cards ride a circle with a size gradient by depth angle, sweeping in fast-slow-fast swings (Circle style 4); 12... | `image1..N` (use images), `speed`, `background` |
| carousel-circle-5 | 1920x1080 | Circle Carousel 5: Image cards ride a circle with a size gradient by depth angle, sweeping in fast-slow-fast swings (Circle style 5); 12... | `image1..N` (use images), `speed`, `background` |
| carousel-orbit-2 | 1920x1080 | Orbit Carousel 2: Image cards on a spinning 3D Fibonacci sphere, billboarded to the camera, sized by camera distance (Orbit style 2); 24... | `image1..N` (use images), `speed`, `background` |
| carousel-orbit-3 | 1920x1080 | Orbit Carousel 3: Image cards on a spinning 3D Fibonacci sphere, billboarded to the camera, sized by camera distance (Orbit style 3); 24... | `image1..N` (use images), `speed`, `background` |
| carousel-orbit-4 | 1920x1080 | Orbit Carousel 4: Image cards on a spinning 3D Fibonacci sphere, billboarded to the camera, sized by camera distance (Orbit style 4); 24... | `image1..N` (use images), `speed`, `background` |
| carousel-orbit-5 | 1920x1080 | Orbit Carousel 5: Image cards on a spinning 3D Fibonacci sphere, billboarded to the camera, sized by camera distance (Orbit style 5); 24... | `image1..N` (use images), `speed`, `background` |
| carousel-path-2 | 1920x1080 | Path Carousel 2: Image cards ride an open bezier path (arc, V, diagonal, wave, S-curve) with depth scaling and tangent rotation (Path... | `image1..N` (use images), `speed`, `background` |
| carousel-path-3 | 1920x1080 | Path Carousel 3: Image cards ride an open bezier path (arc, V, diagonal, wave, S-curve) with depth scaling and tangent rotation (Path... | `image1..N` (use images), `speed`, `background` |
| carousel-path-4 | 1920x1080 | Path Carousel 4: Image cards ride an open bezier path (arc, V, diagonal, wave, S-curve) with depth scaling and tangent rotation (Path... | `image1..N` (use images), `speed`, `background` |
| carousel-path-5 | 1920x1080 | Path Carousel 5: Image cards ride an open bezier path (arc, V, diagonal, wave, S-curve) with depth scaling and tangent rotation (Path... | `image1..N` (use images), `speed`, `background` |
| carousel-text-circle-1 | 1920x1080 | Text + Circle Carousel 1: A headline mask-reveals word by word while a circle carousel converges from off-frame and threads the line, collapses... | `image1..N` (use images), `line1`, `line2`, `speed`, `background` |
| carousel-text-circle-2 | 1920x1080 | Text + Circle Carousel 2: A headline mask-reveals word by word while a circle carousel converges from off-frame and threads the line, collapses... | `image1..N` (use images), `line1`, `line2`, `speed`, `background` |
| carousel-text-circle-3 | 1920x1080 | Text + Circle Carousel 3: A headline mask-reveals word by word while a circle carousel converges from off-frame and threads the line, collapses... | `image1..N` (use images), `line1`, `line2`, `speed`, `background` |
| carousel-text-circle-4 | 1920x1080 | Text + Circle Carousel 4: A headline mask-reveals word by word while a circle carousel converges from off-frame and threads the line, collapses... | `image1..N` (use images), `line1`, `line2`, `speed`, `background` |
| carousel-text-circle-5 | 1920x1080 | Text + Circle Carousel 5: A headline mask-reveals word by word while a circle carousel converges from off-frame and threads the line, collapses... | `image1..N` (use images), `line1`, `line2`, `speed`, `background` |
| carousel-vision-2 | 1920x1080 | Vision Carousel 2: A ring of large image cards tilted into a row under a 3D camera, each card turning toward the centre (Vision style 2)... | `image1..N` (use images), `speed`, `background` |
| carousel-vision-3 | 1920x1080 | Vision Carousel 3: A ring of large image cards tilted into a row under a 3D camera, each card turning toward the centre (Vision style 3)... | `image1..N` (use images), `speed`, `background` |
| carousel-vision-4 | 1920x1080 | Vision Carousel 4: A ring of large image cards tilted into a row under a 3D camera, each card turning toward the centre (Vision style 4)... | `image1..N` (use images), `speed`, `background` |
| carousel-vision-5 | 1920x1080 | Vision Carousel 5: A ring of large image cards tilted into a row under a 3D camera, each card turning toward the centre (Vision style 5)... | `image1..N` (use images), `speed`, `background` |
| char-slam-explode | fits box | Char Slam Explode: Headline glyphs hold in a deterministic scatter, then reassemble with an overshooting slam and a three-frame landing... | `text`, `accent`, `spread` |
| chat-thread | fits box | Chat Thread: The measured conversation as one mountable scene at full fidelity: status bar, back badge, avatar and name pill... | `contact`, `unread`, `messages`, `beat`, `dots`, `receipt` |
| chatgpt-exchange | 1080x1920 | ChatGPT Exchange: A portrait ChatGPT-style exchange types and sends a prompt, streams an answer, assembles a comparison table, and... | `prompt`, `intro1`, `intro2`, `tableHeadUse`, `tableHeadTool`, `tableHeadWhy`, `row1Use`, `row1Tool`, `row1Why`, `row1Chip`, `row2Use`, `row2Tool`, `row2Why`, `row2Chip`, `row3Use`, `row3Tool`, `row3Why`, `row3Chip`, `row4Use`, `row4Tool`, `row4Why`, `row4Chip` |
| claude-exchange | 1080x1920 | Claude Exchange: A portrait Claude-style exchange types a prompt, works through search and reasoning steps, then streams a detailed... | `prompt`, `thinking`, `lead`, `search`, `answer1`, `answer2`, `answer3`, `answer4`, `answer5`, `answer6`, `answer7`, `answer8`, `answer9`, `answer10` |
| comparison-split | fits box | Comparison Split: Two full-bleed panels compare before and after states as a persistent divider wipes the vivid after layer over the... | `split`, `orientation`, `labelA`, `labelB` |
| conic-progress-ring | fits box | Conic Progress Ring: A token-driven conic progress ring whose angular fill and center count settle together from one registered percentage | `progress`, `thickness`, `label` |
| constellation-hub | fits box | Constellation Hub: Feature nodes brighten in narration order as real-length SVG connectors draw outward from a fixed central hub, then... | `hub_label`, `nodes`, `cues`, `accent`, `exit` |
| cosmic-orb | 1920x1080 | Cosmic Orb: An iridescent soap-bubble planet: a slowly spinning sphere of nebula bands, dust lanes and twinkling stars wrapped in a... | `hue`, `accent`, `spin`, `stars`, `glow`, `size`, `pulse`, `pulseEnvelope`, `backdrop` |
| cta-close | fits box | CTA Close: A display-scale action line lands per word and fills the frame with air, one generous CTA capsule pops beneath it with... | `action_line`, `button_label`, `accent`, `exit` |
| cta-lockup | fits box | CTA Lockup: A canonical closing lockup that reveals an action line, pops in an accent CTA capsule, settles supporting microcopy... | `action_line`, `button_label`, `microcopy`, `accent` |
| cursor-context-menu | fits box | Context Menu Cursor: A cursor right-clicks a file, a context menu blooms from its tip, the hover highlight tracks the item under it, and the... | `items`, `pick`, `tone` |
| cursor-drag-drop | fits box | Drag and Drop Cursor: A cursor grabs a task card, lifts and tilts it into its motion, carries it in lockstep to an empty column, drops it... | `card_label`, `accent`, `tone` |
| cursor-marquee-select | fits box | Marquee Select Cursor: A cursor drags a selection rectangle across a photo grid; each tile rings and pops a check the frame the rectangle... | `accent`, `start_x`, `start_y`, `end_x`, `end_y`, `pill_label` |
| cursor-text-select | fits box | Text Select Cursor: An arrow turns into an I-beam over a document, drags a selection across a phrase character by character, raises a... | `title`, `text`, `phrase`, `accent` |
| cursor-zoom-follow | fits box | Zoom Follow Cursor: Screen-recording auto-zoom: the camera pushes in toward each upcoming click, trails the cursor on a smooth spring... | `image`, `zoom`, `click1_x`, `click1_y`, `click2_x`, `click2_y`, `click3_x`, `click3_y`, `accent` |
| dart-cursor | fits box | Dart Cursor: A bold outlined arrowhead that dives in from camera depth, flies nose-first with motion blur along its path, squashes... | `tone`, `target_x`, `target_y`, `target2_x`, `target2_y`, `enter_from`, `exit_to`, `blur` |
| decline-chart | fits box | Decline Chart: A metric line draws downward as its value counts down and the ambient background darkens in lockstep | `label`, `start_value`, `end_value` |
| device-frame-stage | 1920x1080 | Device Frame Stage: A phone or tablet mockup staged as a physical scene prop with a screen slot for arbitrary reconstructed UI, rising onto... | `device`, `cutout`, `body` |
| drift-hold | fits box | Drift Hold: A centered content card stays subtly alive through loop-exact rotation, scale breathing, and a slow light sweep | `text`, `intensity` |
| exploded-stack | 1920x1080 | Exploded Stack: Isometric layer plates explode apart with a label beside each layer, hold, then collapse back into one stack | `title`, `layer_1`, `layer_2`, `layer_3`, `layer_4`, `accent`, `background` |
| focus-rack | fits box | Focus Rack: Focus shifts once between two cards at different apparent depths through synchronized blur, dimming, scale, and parallax | `label_a`, `label_b`, `accent` |
| gesture-tap | fits box | Gesture Tap: A contact circle taps a mobile pill button, releases it into a new labeled accent state, and lifts away | `tap_label`, `response_label`, `accent` |
| glass-hero | 1920x1080 | Glass Hero: A solid glass object rises in front of a giant headline and keeps turning, so the type bends and splits into colour... | `headline`, `subline`, `shape`, `glass_tint`, `type_color`, `background` |
| gloss-sweep | fits box | Gloss Sweep: A card lands with a restrained slam, catches one diagonal specular gloss, and holds perfectly still | `text`, `accent`, `sweep_angle` |
| grade-split-reveal | fits box | Grade Split Reveal: The same picture twice, one flat and one finished, with a hard edge sweeping between them | `look`, `split`, `edge`, `labels` |
| grain-field | fits box | Grain Field: A clearly visible accent-tinted dot field drifts over a subtle luminance gradient in an exact ambient loop | `density`, `accent` |
| grid-card-assemble | fits box | Grid Card Assemble: N capability cards (thin-line icon that draws on, mono label, optional muted body) stagger-assemble into a grid or... | `items`, `layout`, `columns`, `cues`, `accent`, `exit` |
| halftone-field | 1920x1080 | Halftone Field: A full-bleed halftone light field: a grid of dots whose size and colour track a slow flowing simplex-noise field, so... | `frequency`, `speed`, `cellSize`, `gamma`, `paletteBias`, `palette1`, `palette2`, `palette3`, `palette4`, `background`, `quantize` |
| headline-slam | fits box | Headline Slam: A heavyweight headline scales down into frame, lands with a deterministic three-frame shake, holds with subtle drift... | `text`, `accent_word_index`, `accent`, `shadow` |
| kinetic-center-build | fits box | Kinetic Center Build: Words enter from the right and push the growing phrase left until the final line locks centered | `text`, `font_size`, `entry_offset`, `color`, `font_weight` |
| kinetic-type-swap | fits box | Kinetic Type Swap: A held sentence keeps its fixed text in place while one widest-word masked slot rolls through alternatives and settles... | `prefix`, `options`, `suffix`, `cues`, `accent`, `exit` |
| line-swap | fits box | Line Swap: A masked full-line beat replacement: line A holds center then exits up through an overflow-hidden mask as line B enters... | `line_a`, `line_b`, `swap_at`, `underline_word`, `accent`, `exit` |
| locked-nucleus-orbit | fits box | Locked Nucleus Orbit: A fixed center nucleus anchors deterministic satellite orbits that settle into a composed lockup | `label`, `accent`, `satellites` |
| logo-brand-close | fits box | Logo Brand Close: A display-scale wordmark cascades letter by letter into a centered lockup, the accent brand period lands last, an... | `wordmark`, `tagline`, `url`, `accent`, `exit` |
| logo-sting | fits box | Logo Sting: A wordmark slams into its final scale, fires one accent ring and one white impact frame, then holds completely still | `wordmark`, `accent` |
| logo-wall | fits box | Logo Wall: A trusted-by wall of placeholder lettermark logos that fades and scales into place with a deterministic per-cell stagger | `rows`, `cols`, `stagger` |
| lt-neon-border | 1920x1080 | Neon Border: Two arcs of light travel the edge of a rounded panel and snap corner to corner, trailing a soft three-layer bloom | `name`, `role`, `accent`, `movement`, `speed`, `cornerRadius`, `thickness`, `arcLength`, `glow` |
| marker-checklist-card | fits box | Marker Checklist Card: A hand-lettered paper card: marker headline with an underline and a drawn ellipse around one word, then three checklist... | `top`, `mid`, `circled`, `rest`, `l1`, `v1`, `l2`, `v2`, `l3`, `v3` |
| marker-highlight | fits box | Marker Highlight: Display text settles in, then one hand-drawn marker stroke (highlight, circle, underline, or scribble) draws over the... | `text`, `emphasis_word`, `style`, `draw_at`, `accent`, `exit` |
| match-cut | fits box | Match Cut: A circle accelerates into a hard single-frame scene swap, matches the incoming circle exactly, and continues into a... | `accent`, `label_a`, `label_b` |
| message-thread-reveal | 1080x1920 | Message Thread Reveal: A full text conversation plays out on a phone - bubbles popping in, typing indicators, a shared link card, emoji... | `contactName`, `questionMessage`, `teaserMessage`, `cardImage`, `cardTitle`, `cardDomain`, `reactionMessage`, `reactionEmoji`, `benefitMessage`, `discoveryMessage`, `sourceMessage`, `workflowMessage`, `ownershipMessage`, `installMessage`, `thanksMessage`, `brandLogo`, `ecProof`, `ecFeature1`, `ecFeature2`, `ecFeature3`, `ecCta` |
| modal-morph | fits box | Modal Morph: A small card expands into a full panel, shared-element style: both layouts measured once at mount, the container morphs... | `from_scale`, `expand_at`, `register`, `accent`, `exit` |
| multiplayer-cursors | fits box | Multiplayer Cursors: Labeled collaborator cursors with token-derived colors and soft glows drift from spread positions into a shared center... | `cursorCount`, `labels` |
| notes-reveal | 1080x1920 | Notes Reveal: A personal note is typed character by character in a notes app - caret riding every letter, the page scrolling up on... | `titleL1`, `titleL2`, `noteLine1`, `noteLine2`, `noteLine3`, `noteLine4`, `noteLine5`, `noteLine6`, `noteLine7`, `cardTop`, `cardMid`, `cardBottom`, `check1Label`, `check1Value`, `check2Label`, `check2Value`, `check3Label`, `check3Value`, `brandLogo`, `brandDomain` |
| notes-typing | fits box | Notes Typing: The notes-app confession as a mountable scene: a bold title, then body lines typed character by character on the... | `title`, `lines`, `speed` |
| notification-cascade | 1080x1920 | Notification Cascade: Phone notifications land one after another and stack up the screen, each banner pushing the pile down as it arrives... | `notifTitle`, `message1`, `message2`, `message3`, `message4`, `appName`, `headlineTop`, `headlineAccent`, `footerText`, `brandLogo` |
| notification-pileup | fits box | Notification Pileup: Mobile notification cards arrive faster and faster, each new alert pushing the existing stack downward into a dense... | `count`, `speed`, `showBadges` |
| offset-path-traveler | fits box | Offset Path Traveler: A slotted traveler follows an authored path with tangent rotation, curved entry, and curved exit | `path`, `traveler_label`, `accent` |
| oscilloscope-trace | 1920x1080 | Oscilloscope Trace: CRT oscilloscope beam sweeping a waveform across a 10x8 graticule, with closed-form phosphor persistence: the tail... | `waveform`, `frequency`, `amplitude`, `persistenceMs`, `phosphorColor`, `sweepRate`, `dataSeries` |
| overwhelm-surround | fits box | Overwhelm Surround: Tasks, tabs, pings, and notification bubbles accelerate inward around a calm central subject, turning overload into... | `count`, `centerLabel`, `intensity` |
| pan-stations | fits box | Pan Stations: A lateral camera move across a continuous row of labeled feature stations, with a steady dwell at each stop before the... | `stationCount`, `labels`, `dwell` |
| parallax-device-dive | fits box | Parallax Device Dive: A canonical phone rises into view before the camera pushes through its screen and layered app UI expands to fill the... | `accent`, `app_title` |
| particle-text-dissolve | fits box | Particle Text Dissolve: Text assembles from a seeded particle cloud (or dissolves into it): per-particle targets sampled once from the rendered... | `text`, `direction`, `density`, `accent`, `exit` |
| per-word-rise | fits box | Per Word Rise: Words or characters rise into place in a controlled blur-to-sharp cascade, settle softly on landing, and hold still... | `text`, `split`, `cues`, `accent`, `exit` |
| physical-exit | fits box | Physical Exit: A card exits with physical momentum in toss, drop, or slide mode, carrying acceleration and rotation through the final... | `mode`, `text`, `accent` |
| press-ripple | fits box | Press Ripple: A cursor decel-arrives from off-stage, lands slightly off-center on a caller-positioned target, compresses with it in... | `label`, `done_label`, `target_x`, `target_y`, `press_at`, `cursor`, `accent`, `exit` |
| product-turntable | 1920x1080 | Product Turntable: A product turns a full revolution on a studio plinth in a seamless loop | `model_url`, `product_name`, `flavor`, `caption`, `label_color`, `ink_color`, `background`, `turns` |
| pull-back-reveal | fits box | Pull Back Reveal: A tight stat detail holds, then one decelerating camera pull-back reveals the headline and supporting cards that... | `detail_text`, `headline`, `accent` |
| push-in | fits box | Push In: A centered headline gains focus through one slow, continuous camera push and a gentle fade out | `text`, `intensity` |
| radial-surround | fits box | Radial Surround: Labeled hairline chips assemble around a centered subject on an elliptical ring, then optionally converge inward with a... | `center_label`, `chips`, `close_in`, `cues`, `accent`, `exit` |
| scan-band | fits box | Scan Band: A diagonal distortion band sweeps once across a clean wordmark, revealing clipped red and cyan offsets only inside the... | `wordmark`, `band_angle` |
| scramble-reveal | fits box | Scramble Reveal: A deterministic hacker-style text reveal that cycles fixed glyph rows and locks the target string from left to right | `text`, `accent`, `style`, `exit` |
| screen-flow-carousel | fits box | Screen Flow Carousel: Two to five app screens ride a horizontal rail: one primary at center, neighbors receded, advancing on cues with a... | `screens`, `captions`, `cues`, `accent`, `exit` |
| scroll-feed | fits box | Scroll Feed: A loop-friendly column of varied skeleton post cards scrolls upward with subtle motion trails and an agitated pace | `speed`, `card_count`, `cues`, `exit` |
| share-sheet-carousel | 1080x1920 | Share-Sheet Carousel: A share sheet springs up from the bottom of the phone and cycles previews inside its card on a fast cut rhythm while... | `shareTitle`, `senderName`, `itemLabel`, `stripText`, `acceptLabel`, `declineLabel`, `slideImage1`, `slideImage2`, `slideImage3`, `slideImage4`, `brandLogo` |
| shutter-slam | fits box | Shutter Slam: One word thrown through six single-property beats under integrated shutter blur — two translate slams, a scale punch... | `text`, `accent`, `blur`, `cues`, `exit` |
| snow | 1920x1080 | Snow: Seek-safe falling-snow overlay: sparse or dense flakes drift down with size, speed and opacity correlated per flake for... | `density`, `speed` |
| social-proof-card | fits box | Social Proof Card: The app-store close as one mountable scene: wordmark, five stars, a proof line, three feature icons and a CTA capsule... | `brand`, `proof`, `cta`, `f1`, `f2`, `f3` |
| spiral-galaxy | 1920x1080 | Spiral Galaxy: A spiral galaxy seen from outside, turning with real differential rotation: inner stars orbit faster than outer ones... | `stars`, `arms`, `rate`, `glow`, `size`, `core`, `rim` |
| split-flap-board | 1920x1080 | Split-Flap Board: Solari-style departure board: every cell walks its drum forward through the intervening characters of a fixed alphabet... | `boardText`, `flapAlphabet`, `flipDuration`, `cellStagger`, `cellCount` |
| split-tilt-cards | fits box | Split Tilt Cards: Two equal-weight cards arrive from opposite wings with mirrored rotateY book-open tilts under one shared perspective... | `label_a`, `label_b`, `badge_a`, `badge_b`, `accent`, `exit` |
| spring-pop | fits box | Spring Pop: A badge pops in from a visible near-rest scale, overshoots full size once, and settles cleanly | `overshoot`, `fromScale`, `text` |
| spring-stack-shuffle | fits box | Spring Stack Shuffle: A stack of 3 to 5 slotted cards reshuffles on cues: the back card throws over the top and lands at the front with real... | `cards`, `cues`, `accent`, `exit` |
| stagger-cascade | fits box | Stagger Cascade: A responsive grid of tile cards that fades and travels into place with an evenly spaced per-item GSAP stagger | `itemCount`, `stagger`, `direction` |
| star-rating-fill | fits box | Star Rating Fill: A token-driven star row whose colored layer sweeps to a rating, preserves the fractional final star, and can count the... | `rating`, `starCount`, `showValue` |
| starfield | 1920x1080 | Starfield: Seek-safe night-sky overlay: sparse or dense stars in three size tiers that twinkle and drift in two parallax layers... | `density`, `tone`, `speed` |
| state-chip-rail | fits box | State Chip Rail: A rail of mono status chips advances a seek-safe data-state snap machine on a cue schedule: active chip ink on surface... | `states`, `times`, `badge_state`, `badges`, `accent`, `exit` |
| sticky-mock-swap | fits box | Sticky Mock Swap: A pinned product mock cross-fades through accent-tinted feature states while matching captions rise, hold, and exit... | `captions`, `accent` |
| stitched-text-draw | fits box | Stitched Text Draw: Text drawn as thread stitches: a single-stroke display alphabet draws via attribute-driven dashoffset with stitch-tuned... | `text`, `stitch`, `accent`, `exit` |
| store-badge-lockup | fits box | Store Badge Lockup: Settles a short headline above equal-size App Store and Google Play badges as a token-driven mobile end-card call to... | `headline`, `showApple`, `showGoogle` |
| svg-mask-reveal | fits box | SVG Mask Reveal: A soft token-colored sweep reveals media only through an editable SVG wordmark mask | `text`, `revealProgress`, `featherPx` |
| swipe-rail | fits box | Swipe Rail: A contact circle leads a horizontal card rail through a fast drag, momentum carry, and settled snap to the next card | `card_count`, `accent`, `card_label_prefix` |
| testimonial-card | fits box | Testimonial Card: Reveals a customer quote at reading pace, then settles its avatar, author name, and handle beneath as a clean proof beat | `quote`, `author`, `handle`, `rating` |
| testimonial-proof-card | fits box | Testimonial Proof Card: A quote card whose testimonial reveals per-line through a soft mask, with an avatar disc (initials default, image... | `quote`, `name`, `role`, `company`, `emphasis`, `accent`, `exit` |
| text-match-cut | fits box | Text Match Cut: One line of text becomes another mid-move: both ride a single 85 % easy-ease curve and hard-swap at the speed peak, as... | `text_a`, `text_b`, `mode`, `sweep`, `background` |
| text-shimmer | fits box | Text Shimmer: A static headline receives one clean specular gradient sweep through its glyphs, then returns to its ordinary text color | `text`, `accent`, `sweep_at` |
| ticker-takeover | fits box | Ticker Takeover: A mono ticker rolls through options, locks on a final word with an accent flash, and promotes it into a full-frame... | `options`, `final_word`, `accent` |
| titlecard-calm | fits box | Titlecard Calm: A restrained title card where a mono kicker and generous grotesque headline fade upward, drift almost imperceptibly... | `headline`, `kicker` |
| titlecard-lockup | fits box | Titlecard Lockup: The calm breather titlecard: an optional mono kicker fades up, the wordmark settles dead-center with one restrained... | `wordmark`, `label`, `kicker`, `rule`, `accent`, `exit` |
| toggle-flip | fits box | Toggle Flip: An oversized UI toggle switch that flips with real physicality: thumb overshoot, track color crossfade, and a soft... | `direction`, `label`, `size` |
| tracing-beam | fits box | Tracing Beam: A glowing dash follows one SVG path through three UI elements, lifting and brightening each element in sequence | `labels`, `accent` |
| trust-strip | fits box | Trust Strip: A monochrome trust row of wide-tracked mono wordmarks that fade in with an opacity-only left-to-right stagger, then... | `marks`, `tone`, `cues`, `accent`, `exit` |
| type-match-cut | fits box | Type Match Cut: A headline splits vertically around an incoming panel, which grows from the negative space and takes the frame as the... | `text`, `accent` |
| typed-prompt | fits box | Typed Prompt: A prompt line types itself in chunked human cadence behind a deterministic blinking caret, with optional... | `text`, `prompt_glyph`, `cadence`, `caret`, `correction`, `cues`, `accent`, `exit` |
| variable-axis-type | fits box | Variable Axis Type: A locked one-line headline whose weight or width axis morphs into a decisive emphasis beat | `text`, `axis`, `fromValue`, `toValue` |
| variable-font-flex | fits box | Variable Font Flex: A word lands while its variable-font weight and width axes flex from hairline-condensed to black-wide with... | `text`, `axis`, `stagger`, `accent`, `exit` |
| vector-editor-rig | fits box | Vector Editor Rig: A dark design-tool app chrome with a live vector pen path, sequential anchor points, bezier handles, a selection frame... | `tool`, `pathLabel` |
| velocity-throw-snap | fits box | Velocity Throw Snap: A five-shot rail whips past on a fast decaying curve, then overshoots and snaps the selected hero shot exactly to center | `hero_index`, `accent`, `card_label_prefix` |
| vfx-anamorphic-flare | 1920x1080 | Anamorphic Streak Flare: A drifting field of bright points, each one throwing the long horizontal blue-violet streak a real anamorphic cinema... | `intensity`, `threshold`, `streakLength`, `tint`, `bloomRadius`, `timeScale`, `emitters`, `backdrop` |
| vox-annotate | fits box | Vox Annotate: The Vox-style annotate gesture: a keyword in a held sentence gets a hand-drawn marker while a thin connector draws up... | `text`, `keyword`, `note`, `style`, `draw_at`, `accent`, `exit` |
| whip-pan-cut | fits box | Whip Pan Cut: A full-frame whip pan: scene A whips off laterally with capped directional motion blur while scene B enters in the same... | `direction`, `whip_at`, `accent`, `exit` |
| whiteboard-ink | fits box | Whiteboard Ink: A whiteboard sketch draws one measured stroke at a time while a pen nib follows the active tip | `sketch`, `caption`, `pen`, `accent`, `exit` |
| wordmark-tiles | fits box | Wordmark Tiles: A wordmark resolves from deterministic color noise into correctly cropped glyph tiles through a spatially modulated... | `text`, `columns`, `waveStagger` |
| zoom-through-transition | fits box | Zoom Through Transition: A transition that zooms through a focal card into the next scene | `from-label`, `to-label`, `depth`, `accent` |
