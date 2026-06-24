# Asset Modes

Translation table from prompt intent to `session.assets.mode` + HTML behavior.

The runtime is always live in the iframe. Setting `mode` at generation time tells the editor sidebar which uploader to open, even when `items: []`. This is the contract for "upload the video/image/audio later in the editor." The HTML must also consume the matching runtime accessor and render a designed fallback for the empty-items state.

## Prompt → mode

| What the user said | `assets.mode` | What the HTML reads | Empty-items fallback |
|---|---|---|---|
| "galeria", "minhas fotos", "carrossel", "use múltiplas imagens", "atlas", "morph entre imagens", "image sequence" | `multi-image` | `getImages()` (array of `<img>`) | procedural shapes / placeholder tiles in the chosen palette |
| "image shader", "use minha foto", "imagem de referência", "amostre uma textura", "use this image", "single image texture" | `single-image` | `getPrimaryImage()` | procedural noise / gradient / shader fallback |
| "audio reactive", "música", "som", "batida", "spectrum", "VU meter", "waveform" | `audio` | `getAudioData()` → `bass`, `mid`, `treble`, `rms`, `peak`, `spectrum[16]`, `waveform[32]` | slow temporal sine driving the same parameter |
| "video shader", "sample frames de vídeo", "video texture", "feedback", "trail from a video", "kaleidoscope a clip", "usar vídeo" | `video` | `getVideoElement()` + `ctx.drawImage` (or `texImage2D`) | animated gradient / generative substitute |
| "svg recolor", "vetorial", "anime os paths", "use this svg", "logo morph" | `svg` | `__VISU_SVG_RUNTIME.inlineNode()`, `applyPaintOverrides`, `getPaintTargets` | inline geometric icon in the same palette |

When the prompt is ambiguous (e.g. *"use mídia"*), prefer `multi-image` and branch at runtime by reading `assetState.mode` inside `onAssetChange`. The user's first upload sets the real mode; the editor will infer it from MIME and update the session.

When image or video assets are drawn into a bounded area, expose a sibling `Fit` select control with options `["cover","fill"]` and default `cover`. `cover` preserves aspect ratio and crops overflow; `fill` stretches and may distort. Use the same rule for webcam video with `webcam_fit`.

## Build command by mode

Use `--asset-mode` whenever the user asks for an editor-uploaded material and no actual asset item is bundled yet:

```bash
python3 scripts/build_visu.py --prompt "video shader with liquid feedback" --html-file work/video.html --out work/video.visu --name "Liquid Video Shader" --asset-mode video
python3 scripts/build_visu.py --prompt "gallery of drifting photos" --html-file work/gallery.html --out work/gallery.visu --name "Drifting Gallery" --asset-mode multi-image
python3 scripts/build_visu.py --prompt "image shader that melts one photo" --html-file work/image.html --out work/image.visu --name "Melting Image Shader" --asset-mode single-image
python3 scripts/build_visu.py --prompt "audio reactive chrome bloom" --html-file work/audio.html --out work/audio.visu --name "Chrome Audio Bloom" --asset-mode audio
```

Use `--assets-json` only when concrete items already exist or when extra metadata is needed. If both are provided, the JSON wins unless it has no mode.

## Default `assets` block per mode

Single-image:

```json
{ "mode": "single-image", "lastMode": "single-image", "revision": 0, "items": [] }
```

Multi-image:

```json
{ "mode": "multi-image", "lastMode": "multi-image", "revision": 0, "items": [] }
```

Audio:

```json
{ "mode": "audio", "lastMode": "audio", "revision": 0, "items": [] }
```

Video:

```json
{ "mode": "video", "lastMode": "video", "revision": 0, "items": [] }
```

SVG:

```json
{ "mode": "svg", "lastMode": "svg", "revision": 0, "items": [] }
```

When the user did not mention assets, leave the default `{ "mode": "none", ... }`. The subscribe still has to be registered — uploads added later will fire it.

## Per-mode minimum wiring

Every asset mode must satisfy both sides:

- Session side: `.visu` has `assets.mode` and `assets.lastMode` set to the chosen mode, even with `items: []`.
- HTML side: code subscribes to `__VISU_ASSET_RUNTIME` and calls the matching accessor in the render path.

Mode gates:

- `video`: update a canvas/WebGL/Three texture every frame from `getVideoElement()` when `readyState >= 2`; fallback is animated, not blank. Do not call `play()`, `setMuted()`, `setLoop()`, `pause()`, `togglePlayback()`, or `setCurrentTime()` from subscribe callbacks, asset-change handlers, or animation loops; the host owns playback setup.
- `single-image`: sample `getPrimaryImage()` or first `getImages()` item only when loaded; fallback is procedural.
- `multi-image`: call `getImages()` and handle 0, 1, and many images cleanly.
- `audio`: call `getAudioData()` inside the animation loop; map `rms`, `bass`, `mid`, `treble`, `spectrum`, or `waveform` to visible motion.
- `svg`: use `__VISU_SVG_RUNTIME` / `getSvg()` and keep a fallback geometric mark.

Never read editor uploads from `session.source`. User uploads always enter `session.assets`.

## Fallback rules

The empty-items branch is part of the design, not an error path. Treat it as the visu's "default look" and the asset path as an enrichment.

- The fallback should look intentional on its own. A polished generative scene that becomes more specific once an asset arrives.
- The transition to the asset state should be visible — the user should feel the upload landed.
- Do not show "no asset loaded" UI, dashed borders, or "drop a file here" text inside the iframe. The editor sidebar already handles upload UI.

## Deciding the design echo

When `assets.mode != none`, the design echo (step 3 in the workflow) names the fallback explicitly. Example:

```
Reading your prompt as:
- Subject: audio-reactive blob bloom
- Material: liquid chrome with iridescence
- Motion: pulse on bass, drift on mid
- Interaction: pointer attracts; release springs back
- Asset: drop an mp3 in the sidebar — until then, a slow sine drives the pulse
- Controls: bloom, palette, motion speed, iridescence, sensitivity
```

This makes the upload step part of the contract before the build runs.
