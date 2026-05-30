# Quality Process

Use this reference for every `.visu` generation.

## North Star

A visu is a functional, refined interactive experiment. It should feel like something a strong creative coding engineer would ship into the Visu.Haus editor, not like a starter demo.

## Build Process

1. Extract the visual thesis: subject, material, palette, composition, rhythm, and interaction.
2. Choose the renderer that best serves the thesis. Do not choose WebGL or Three.js for prestige alone.
3. Define the first frame. The visual should look intentional before the user touches it.
4. Define motion as part of the concept, not a generic animation layer.
5. Define one or two interaction loops that change the artwork materially.
6. Add only controls that make the result more editable and expressive.
7. If the prompt implies video/image-gallery/single-image/audio/SVG upload, set the matching `assets.mode` before build, even with empty `items`.
8. Add capabilities only when they strengthen the idea.
9. Validate that the session opens, animates, responds, snapshots, opens the intended upload lane, and degrades gracefully.

## Visual Bar

- Strong composition: focal structure, rhythm, negative space, scale relationships.
- Clear palette: avoid muddy randomness; use controlled accents and enough contrast.
- Material behavior: liquid, paper, chrome, glass, pixel, cloth, ink, neon, etc. should have matching motion and rendering.
- No blank areas unless intentional.
- No generic particle spray unless the prompt asks for it.
- No stock loading screens, tutorial text, "click here" labels, or debug panels.
- 2D visuals should not show control hints. 3D can show a tiny, tasteful orbit hint if necessary.

## Motion Bar

- Motion must be continuous and perceptible at rest.
- Motion should include layered time scales: slow structure plus faster detail.
- Interaction should affect the scene locally or semantically, not only change a color.
- Pausing via `_animEnabled` should stop autonomous motion while still allowing the current frame to render.
- On pointer leave, reset interaction state so forces do not stick.
- For webcam, camera-denied fallback must still look designed.

## Control Bar

Good controls are specific to the visual:

- Required baseline: `_animEnabled`, quantity/count, size/scale, motion speed, main colors.
- Add effect controls only for essential effects.
- Use clear labels and stable groups: Motion, Shapes, Colors, Effects, Image, Audio, Video, Typography, Camera, Material.
- Avoid exposing internal variables that users cannot understand.
- Defaults must produce the best version, not a neutral midpoint.

## Performance Bar

- Target smooth animation on ordinary laptops.
- Avoid expensive per-frame DOM reads.
- Avoid reinitializing scenes or particle systems on resize; preserve positions when possible.
- Limit heavy blur/filter stacks.
- For high-density loops, cap counts with constants and expose controls within safe ranges.
- Use `devicePixelRatio` carefully; cap it if the renderer becomes too heavy.

## Ship Gate

These are blockers, not warnings. If any fail, regenerate the failing piece silently before responding. Never surface technical failure messages to the user.

- The `.visu` file is valid JSON.
- `code` is a complete HTML document.
- The visual has a render target and a non-blank first frame.
- The animation loop runs.
- Pointer interaction exists and resets on leave.
- `var cfg` exists and posts `cfg_schema`.
- The message bridge handles `cfg_update`, `camera_update`, and `request_snapshot`.
- Snapshot posts `{ type: 'snapshot_ready', dataUrl }`.
- Webcam visuals do not call browser camera APIs directly.
- HTML registers `window.__VISU_ASSET_RUNTIME.subscribe(...)` (or the `visu:asset-change` event). This is required even when `assets.mode` is `none`, so future uploads have a destination.
- If the prompt asks for video, single-image, multi-image/gallery, audio, or SVG upload, `session.assets.mode` and `session.assets.lastMode` are not `none`; they match the user intent.
- When `session.assets.mode != 'none'`, the HTML consumes the matching API: `getPrimaryImage`/`getImages` for image modes, `getAudioData`/`getAudioElement` for audio, `getVideoElement`/`getVideo` for video, `__VISU_SVG_RUNTIME` for svg.
- Empty-items state renders a designed procedural fallback - never a blank canvas, error message, or "drop a file" placeholder.
- Uploads are read from `assets`, not from `source`.
- Typography visuals declare metadata and use the host typography runtime.
- Any external CDN dependency is justified.

If browser verification is available, open the HTML or `.visu` and inspect desktop and mobile proportions. If not, proceed silently — do not tell the user "browser verification was not run."
