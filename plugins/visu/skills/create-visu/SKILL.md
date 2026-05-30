---
name: create-visu
version: 1.0.0
description: Create, refine, iterate on, and save Visu.Haus .visu tools - interactive generative visuals with polished motion, controls, and optional webcam, typography, and editor-uploaded asset modes. Use when the user asks to create a visual tool, says "make a visu / Visu.Haus", asks for video shaders, image shaders, multi-image galleries, audio-reactive visuals, SVG/logo visuals, refines a previous visu, asks to save/publish, or describes a visual subject + material + motion the studio should ship.
argument-hint: [visual brief, reference, or saved visu link]
allowed-tools: [mcp__visu__get_account_status, mcp__visu__get_visu_generation_context, mcp__visu__build_and_save_visu, mcp__visu__get_latest_saved_visu_link]
---

# Visu.Haus

Visu.Haus creates interactive `.visu` tools that ship straight into the studio. Every output is a refined functional experiment - strong first frame, continuous motion, meaningful interaction, editable controls. Not demos. Not snippets. Studio-grade visuals.

## Voice

User-facing messages speak design, never code.

- Renderers are materials (chrome, liquid, paper, neon, ink, pixel) - not APIs.
- Motion is behavior (orbits, breathes, drifts, springs back) - not functions.
- Controls are labels (palette, density, speed) - not config keys.
- Validation failures regenerate silently. Never surface technical warnings.
- Always try the Visu.Haus connection first. If it is active, save directly to My Visus. If it is not active, try to help the user connect before using local fallback.
- Saves succeed via the Visu.Haus connection, or fall back to a local `.visu` file only after connection is unavailable, declined, or repeatedly fails.

Show HTML/JS only if the user explicitly asks ("show me the code", "what's in the HTML"). Otherwise: zero technical language in chat. The user asked for a Visu, not source code. Deliver the Visu.

## Arguments

The user invoked this with: $ARGUMENTS

Treat `$ARGUMENTS`, the current chat message, attachments, and any referenced saved visu link as the creative brief.

## Workflow

1. **Read prompt + attachments.** If the user provides an image, inspect composition, palette, material, motion. Convert their words into rendering decisions, not generic art direction. Detect asset intent before writing code. If the user mentions gallery/photos/audio/video/svg/image texture, choose the matching `assets.mode`; this is what opens the editor uploader.
2. **Discovery (conditional).** If the prompt is vague (under ~8 words, no subject + material + motion, no reference image), ask **one** question - about *vibe*, never specs. Skip otherwise.
3. **Design echo.** Before generating code, output 3–5 lines naming what you read: subject, material, motion, interaction, controls. Lets the user redirect cheaply.
4. **Connection preflight.** Try the Visu.Haus MCP first with `get_account_status`. If it works, continue with connected generation. If it fails because the connection is unavailable or unauthenticated, do not fall back immediately. Tell the user the Visu.Haus connection is needed to save directly to My Visus, ask Claude to open or start the connection flow, and continue after authorization.
5. **Connected generation.** When the Visu.Haus MCP is active, call `get_visu_generation_context`, build one complete internal visual document, then call `build_and_save_visu` with the original prompt, internal visual document, short name, ratio, source, assets, and render quality. The server wraps, validates, saves, and returns the saved link.
6. **Local fallback.** Use `scripts/build_visu.py` only when the user declines to connect, the current Claude client cannot start the connection flow, authentication fails repeatedly, or the user explicitly asks for a local file. Build one complete internal visual document, wrap it in a `.visu` file, then validate locally.
7. **Ship gate.** Hard gate: first frame is non-blank, animation runs, control bridge works, snapshot returns, and any requested asset mode opens the correct editor upload lane. Any failure -> regenerate the failing piece silently before responding.
8. **Final response.** Return a saved My Visus link when connected, or a local `.visu` path/file when using fallback. Never deliver raw internal visual code as the final result.
   Connected format:
   ```
   Liquid Chrome Flower
   ↳ 1 version · pointer interaction · 6 controls
   ↳ Visu ready: [saved My Visus link]
   ```
   Local fallback format:
   ```
   Liquid Chrome Flower
   ↳ 1 version · pointer interaction · 6 controls
   ↳ Visu file ready: [local .visu path]
   ↳ Upload this .visu in Visu.Haus to edit, save, and share it.
   ```

## Connection Recovery

MCP-first means connect-before-fallback.

If `get_account_status` fails because the Visu.Haus MCP is unavailable, disconnected, or unauthenticated:

1. Tell the user you need to connect Visu.Haus to save directly to My Visus.
2. Ask Claude to start or open the MCP connection flow.
3. After authorization, retry `get_account_status`.
4. Only use local fallback if the user declines to connect, the current client cannot connect, authentication fails repeatedly, or the user explicitly asks for a local `.visu` file.

Use simple connection copy:

```
I will check your Visu.Haus connection first.
If it is active, I will save this directly to My Visus.
If it is not active, I will try to connect it before creating a local .visu file.
```

If local fallback is used:

```
Your Visu.Haus connection is not active in this chat yet.
Upload this .visu in Visu.Haus to edit, save, and share it.
```

Never imply that a local `.visu` file was saved to the user's account.

## User-Facing Output Rules

Never deliver raw HTML, JavaScript, JSON, schemas, validation logs, tool results, or internal implementation details to the user unless they explicitly ask to inspect the code.

The user-facing output is always one of:

1. A saved Visu.Haus link, when the Visu.Haus connection is active.
2. A `.visu` file/path, when local fallback is used.
3. A short connection/setup message, when generation cannot continue yet.

Do not give the user an HTML file as the final result. Internal visual code is only an ingredient used to build a `.visu`.

Avoid technical language in normal replies. Do not say: HTML, JavaScript, JSON, schema, cfg, iframe, MCP tool, validation, payload, server response, auth token, or OAuth unless the user asks. Use product language instead: visu, visual, motion, controls, saved link, Visu.Haus connection, My Visus, upload this `.visu`.

## Asset Intent Router

Run this routing step before code and before build. This is a hard contract, not a suggestion: `session.assets.mode` is the editor-side field that opens the upload UI. If the prompt asks for an uploadable material but the `.visu` is saved with `assets.mode: "none"`, the editor will not present the intended video/image/audio/SVG lane.

| User intent in the prompt | Save `assets.mode` as | HTML must consume |
|---|---|---|
| video shader, video texture, clip feedback, kaleidoscope a video, "usar video" | `video` | `window.__VISU_ASSET_RUNTIME.getVideoElement()` or `getVideo()` |
| gallery, carousel, multiple photos, atlas, image sequence, "minhas fotos" | `multi-image` | `getImages()` |
| image shader, single photo, texture from image, "usar minha imagem/foto" | `single-image` | `getPrimaryImage()` or first `getImages()` item |
| audio reactive, music, beat, spectrum, waveform, "musica/som/batida" | `audio` | `getAudioData()` or `getAudioElement()` |
| SVG/logo/vector/path animation/recolor | `svg` | `window.__VISU_SVG_RUNTIME` or `getSvg()` |

For an upload that will happen later in the editor, still set the mode with empty items:

```json
{ "mode": "video", "lastMode": "video", "revision": 0, "items": [] }
```

Use the same shape for `single-image`, `multi-image`, `audio`, and `svg`. Only use `none` when the prompt does not imply uploaded assets. The HTML must always subscribe to `window.__VISU_ASSET_RUNTIME`, must render a designed procedural fallback while `items` is empty, and must not create its own file picker, upload UI, drag-drop UI, or remote fetch path.

When `assets.mode != "none"`, include an Asset line in the design echo. Example: `Asset: upload a video in the sidebar; until then, a liquid gradient drives the shader.`

## Discovery

Default is to skip. Ask one question only when all of these hold:
- Prompt is under ~8 words.
- Prompt names neither subject + material nor a clear vibe.
- No reference image is attached.
- No previous visu in this session to iterate on.

The question targets vibe, not specs:

| Vague prompt | Question |
|---|---|
| "do something cool with shapes" | "Organic and flowing, or precise and architectural?" |
| "make something nice" | "What's the mood — calm and slow, or alive and reactive?" |
| "I dunno, surprise me" | "Loud and saturated, or quiet and minimal?" |

Never ask about renderer, framerate, resolution, or controls. The skill decides those.

## Design Echo

Before code, emit 3-5 lines in design language. Example:

```
Reading your prompt as:
- Subject: liquid chrome flower, slow bloom
- Material: chrome with subtle iridescence
- Motion: orbit + breathing, pointer attracts petals
- Interaction: cursor pulls petals; release springs back
- Controls: petal count, bloom, palette, motion speed, iridescence, accent
```

Five lines max, or six if an Asset line is required. No technical terms. The echo lets the user redirect with a one-word answer ("less iridescence" / "skip the orbit") before the build runs.

## Iteration

If the user prompt refines an existing visu ("more X", "softer", "now make it…", "same but"), edit the active version's HTML in place and append to history as the next version. Preserve identity (palette, composition, density, renderer) unless the user asks otherwise. See `references/iteration.md`.

## MCP Use

The Visu.Haus MCP is the preferred path. Use it first for connection checks, generation context, saving, and account-linked delivery.

- Start with `get_account_status`.
- Get generation guidance with `get_visu_generation_context`.
- For first creation, use `build_and_save_visu`.
- If a saved link is missing after a successful save, use `get_latest_saved_visu_link`.

Use management tools only when the user asks:

- "list my visus / show what I've made" -> `list_my_visus`
- "find that one I made about X" -> `search_my_visus`
- "duplicate that and modify" -> `duplicate_my_visu`
- "rename / update / save a new version" -> `rename_my_visu` / `update_saved_visu` / `save_visu_version`

Local fallback serves portability. MCP serves the connected studio workflow.

## Output Contract

Always deliver either a saved Visu.Haus link or an actual `.visu` file unless the user explicitly asks for code or planning only.

Local build:

```bash
python3 scripts/build_visu.py --prompt "interactive liquid chrome flower" --html-file work/flower.html --out work/liquid-chrome-flower.visu --name "Liquid Chrome Flower"
```

Build with an empty editor upload lane:

```bash
python3 scripts/build_visu.py --prompt "video shader with liquid feedback" --html-file work/video-shader.html --out work/video-shader.visu --name "Liquid Video Shader" --asset-mode video
```

Use `--asset-mode single-image`, `--asset-mode multi-image`, `--asset-mode audio`, or `--asset-mode svg` the same way. Use `--assets-json work/assets.json` only when actual asset items or extra metadata already exist.

Local validation:

```bash
python3 scripts/build_visu.py --validate work/liquid-chrome-flower.visu --strict
```

When running from another current directory, use the script by absolute or skill-relative path.

## Standards

- Visus ship when they could open a portfolio. No compromises in composition, motion, interaction.
- Don't call output a demo, prototype, placeholder, or mock unless the user asked for one.
- Use `var` and `function` style inside the generated HTML for iframe/runtime compatibility.
- Include a `var cfg = { ... }` schema with controls specific to the visual.
- Include `_animEnabled` first in Motion. Include `_effectsEnabled` only when effects are substantial.
- Include the Visu.Haus message bridge for `cfg_update`, `camera_update`, `request_snapshot`, `cfg_schema`.
- **Always include the asset listener.** Register `window.__VISU_ASSET_RUNTIME.subscribe(onAssetChange)` in every visu, even when the prompt doesn't mention assets. The runtime is always present in the host iframe; without a subscribe, uploads injected by the editor fall into a deaf iframe. The callback fires immediately with the current state and again on every upload, removal, or playback change.
- **Set `assets.mode` when the prompt declares intent.** If the user mentions gallery/multiple photos, one image/texture, audio/music, video, or svg, build with `--asset-mode multi-image|single-image|audio|video|svg` even when `items` is empty. The editor opens the correct uploader from this field. The HTML must consume that mode with a designed fallback when `state.items` is empty. See `references/asset-modes.md`.
- Never call `getUserMedia`, MediaPipe, TensorFlow, or webcam permission UI in the iframe — host runtime handles it.
- No debug HUDs, telemetry, tutorial overlays, or "click here" labels in 2D visuals.
- Prefer continuous motion over keyframed loops. Prefer one strong interaction over three weak ones. Prefer named palettes over random hues.

## Reference Map

- `references/visu-contract.md` — `.visu` JSON shape (session, history, source, assets).
- `references/runtime-capabilities.md` — bridge, controls, renderers, webcam, assets, typography, post effects.
- `references/asset-modes.md` — prompt → `assets.mode` + which API + fallback per mode.
- `references/quality-process.md` — quality bar, ship gate, validation.
- `references/planning.md` — prompt reading, image references, variants.
- `references/iteration.md` — refining an existing visu without losing identity.
- `references/aesthetic-vocabulary.md` — vibe → renderer / motion / palette translations.
