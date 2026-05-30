---
name: 3d-visu
version: 1.0.0
description: Create fast, high-fidelity 3D Visu.Haus .visu visuals using an exclusive Babylon.js + WebGL fragment-shader rendering route: fullscreen canvas, custom post-process shader, SDF/raymarching or equivalent procedural GPU fields, procedural lighting/reflections, and small uniform-driven motion. Use when the user invokes /3D-Visu, /3d-visu, asks for premium fast 3D, shader-quality 3D, procedural 3D visuals, or wants the same performance/graphic fidelity technology path as Liquid Violet Metaballs, while allowing any subject, material, scene, or motion brief.
argument-hint: [3D visual brief, material, motion, or reference]
allowed-tools: [mcp__visu__get_account_status, mcp__visu__get_visu_generation_context, mcp__visu__build_and_save_visu, mcp__visu__get_latest_saved_visu_link]
---

# 3D Visu

Use this skill as the dedicated high-performance 3D rendering route for Visu.Haus. It is intentionally narrow in technology, not in subject matter: generate whatever the user asks for, but preserve the same GPU-first graphics approach that gives Liquid Violet Metaballs its fidelity and speed.

Do not treat Liquid Violet Metaballs as an aesthetic template. Treat it as a technology reference: Babylon.js shell, fullscreen WebGL, custom shader, procedural geometry/materials, compact state, high visual polish.

Also treat it as a lighting/material reference. Preserve the render discipline that makes it feel expensive: environment-driven reflections, rim light, Fresnel edges, soft occlusion in creases, tone mapping, bloom, and a restrained post stack.

The user invoked this with: $ARGUMENTS

Treat `$ARGUMENTS`, the current chat message, attachments, and any referenced saved visu link as the creative brief.

## Technology Contract

For every `/3D-Visu` output, use this stack unless the user explicitly asks for another renderer:

- One fullscreen `<canvas>`.
- Babylon.js loaded from `https://cdn.babylonjs.com/babylon.js`.
- `BABYLON.Engine`, `BABYLON.Scene`, and a camera.
- One custom `BABYLON.PostProcess` backed by a GLSL fragment shader.
- Procedural 3D forms defined as SDFs, procedural fields, signed distance volumes, analytic surfaces, warped spaces, or compact GPU-generated structures.
- Raymarching/sphere tracing in the fragment shader for the primary form whenever the brief implies sculptural 3D, volumetric surfaces, liquid, glass, chrome, organic forms, abstract architecture, or impossible geometry.
- Motion driven by a tiny JS state layer: `time`, pointer/camera values, and compact uniform arrays.
- Procedural environment lighting/reflection in shader. Do not depend on HDR files, model files, texture packs, or remote assets for the core look.
- Optional Babylon pipeline effects: bloom, FXAA, grain, chromatic aberration, tone mapping.

This route is exclusive by design. Do not use Three.js, p5.js, Canvas 2D drawing, CSS animation, SVG animation, physics engines, imported GLB/OBJ models, particle libraries, or DOM-heavy rendering for the core visual.

The subject can be broad: product-like objects, abstract machines, terrain, flowers, typography-inspired forms, architectural spaces, portals, crystals, fabric-like surfaces, energy fields, liquid sculptures, orbital systems, UI-reactive scenes, or symbolic objects. Translate the subject into procedural GPU geometry instead of copying the metaball look by default.

## Why It Is Fast

Keep the performance model intact:

- The GPU draws the image per pixel; JS only updates uniforms.
- Keep live object count tiny: usually 4-24 procedural shapes or one compact field.
- Reuse typed arrays for uniform data.
- Avoid allocating objects inside the render loop when possible.
- Clamp device pixel ratio with `engine.setHardwareScalingLevel(...)`.
- Prefer procedural lighting and reflections over image-based assets.
- Cap raymarch steps based on visual need. Start around 70-110 steps; lower for mobile or soft materials.
- Early-exit raymarching on hit distance and max distance.

## Lighting And Material Direction

Use the Liquid Violet Metaballs lighting/material approach as the default quality bar, adapted to the requested subject:

- Build a procedural environment in the shader instead of relying on a flat background. Let `bgColor` behave like a surrounding light field with sky/ground variation.
- Add two or three soft studio lights through directional lobes in the environment function. One key highlight, one broad fill, and one colored rim are usually enough.
- Use Fresnel/Schlick edges for premium materials. Edges should catch light even when the center is darker.
- Use reflection vectors against the procedural environment for chrome, plastic, glass, gel, polished stone, liquid, and product-like surfaces.
- Blur reflections cheaply by sampling the environment a few times with roughness-based jitter. Keep it low sample count, usually 4 taps.
- Add soft ambient occlusion by sampling the SDF along the normal. This is what makes joins, folds, bevels, grooves, and contact areas feel grounded.
- Add subtle depth fog only when it helps integrate the object with the environment. Do not wash out the subject.
- Apply ACES-style tone mapping and gamma correction in the shader for a polished first frame.
- Use bloom for wet, glass, neon, chrome, energy, and luminous materials. Keep it controlled; bloom should finish the material, not hide weak geometry.
- Use FXAA for smoother edges. Grain and chromatic aberration should be optional behind `_effectsEnabled` and kept subtle.

Material recipes:

- Chrome: high reflection, low roughness, strong Fresnel, bright rim, darker base environment.
- Glass/gel: high Fresnel, soft internal color, rim glow, slightly blurred reflections, low-contrast diffuse.
- Liquid/plastic: medium-high reflection, smooth AO in joins, broad highlights, saturated rim color.
- Stone/mineral: lower reflection, higher roughness, AO emphasized, faceted or noisy normals.
- Energy/portal: emissive-looking bands, bloom, depth falloff, less physical diffuse.
- Product/object: clean bevels, controlled studio reflection, clear silhouette, slow orbit.

## Subject Translation

Start from the user's brief, then choose the procedural form language that best fits:

- Organic or liquid: smooth-min SDF blends, warped spheres, capsules, tendrils, folds.
- Architectural or mechanical: boxes, bevels, repeated modules, cylinders, panels, hard-surface SDF composition.
- Natural terrain or mineral: height fields, domain warping, ridged noise, crystalline planes.
- Portals, energy, aura, atmosphere: raymarched volumes, shells, fresnel bands, noise fields, glow layers.
- Product or object studies: analytic primitives with bevels, studio lighting, reflective material, slow orbit.
- Typographic or logo-like briefs: procedural strokes, rounded extrusions, distance fields, symbolic silhouettes.

Preserve the prompt's identity. The technology should be recognizable in the render quality and performance, not in one repeated visual motif.

## Visual Pattern

Default to one strong 3D material behavior:

- Liquid fusion: smooth-min blended fields.
- Chrome/plastic sculpture: SDF composition with Fresnel reflections.
- Glassy gel: translucent-looking shader with rim light and softened environment.
- Mineral/stone: folded or faceted fields with low-frequency procedural noise.
- Soft inflatable forms: rounded SDF silhouettes with slow breathing.
- Hard-surface object: bevelled SDF primitives with clean studio reflections.
- Volumetric glow: layered fields with bloom and depth falloff.

Use a small set of clear controls:

- `_animEnabled` first in Motion.
- `_effectsEnabled` when bloom/grain/aberration are meaningful.
- Speed, density/count, scale, blend/fusion, spread/twist.
- Material color, background, rim/accent, roughness, reflectivity, metallic/glass.

## Required Visu Wiring

Still obey the normal Visu.Haus contract:

- Use `var` and `function` style inside generated HTML.
- Include `var cfg = { ... }` with editable controls.
- Listen for `cfg_update`, `camera_update`, and `request_snapshot`.
- Post `cfg_schema` after load and `snapshot_ready` for snapshots.
- Include the asset runtime listener even when `assets.mode` is `none`.
- Never call `getUserMedia`, MediaPipe, TensorFlow, or webcam permission UI.
- No debug overlays, tutorials, or technical labels inside the visual.

## Visu Contract Checklist

Every generated `/3D-Visu` must still be a normal editable Visu.Haus session:

- Deliver a saved Visu.Haus link or a `.visu` file, never raw HTML as the final output unless the user explicitly asks for code.
- The `.visu` must include root `code`, `cfg`, `defaults`, `source`, `assets`, `history`, `activeVersionId`, `ratio`, and render quality metadata through the normal builder/server path.
- The active `history` item must carry the same `code`, `cfg`, `defaults`, `source`, `assets`, and `ratio` needed by the editor.
- Keep `session.assets.mode`, `session.assets.lastMode`, active history `assets.mode`, and any metadata capability asset mode aligned.
- Use `assets.mode: "none"` only when the prompt does not imply uploads. If the prompt asks for video, single image, multi-image, audio, or SVG, set that mode even when the item list is empty.
- The HTML must subscribe to the asset runtime and render a designed procedural fallback when no uploaded asset is present.
- The control schema must be stable: `_animEnabled` first in Motion, `_effectsEnabled` only when substantial effects exist, and material/motion controls grouped clearly.
- Camera messages must map host zoom, pan, and orbit into the Babylon camera or shader camera state.
- Snapshot requests must return `canvas.toDataURL("image/png")` through `snapshot_ready`.
- Local fallback must use the shared Visu.Haus builder and strict validation.

## Workflow

1. Read the prompt as a 3D subject/material/motion brief.
2. If the prompt is vague, ask one vibe question only.
3. Give a short design echo in user-facing language. Do not mention Babylon, WebGL, GLSL, SDF, shaders, uniforms, or raymarching unless the user asks for implementation details.
4. Try the Visu.Haus connection first with `get_account_status`. If connected, use `get_visu_generation_context` and save with `build_and_save_visu`.
5. If connection is unavailable, declined, or repeatedly fails, build a local `.visu` with the shared local builder at `../create-visu/scripts/build_visu.py`.
6. Validate before final delivery. The first frame must be non-blank, animation must run, controls must work, camera messages must work, and snapshots must return.
7. Return a saved Visu.Haus link when connected, or a local `.visu` file path when falling back.

## Local Build

When using local fallback from this skill directory, call the shared builder:

```bash
python3 ../create-visu/scripts/build_visu.py --prompt "procedural 3D chrome portal with slow orbit" --html-file work/3d-visu.html --out work/3d-visu.visu --name "Chrome Portal" --ratio free --render-quality high
```

Validate strictly:

```bash
python3 ../create-visu/scripts/build_visu.py --validate work/3d-visu.visu --strict
```

## User-Facing Response

Keep normal replies visual, not technical.

Connected:

```text
Chrome Portal
↳ 1 version · pointer interaction · 8 controls
↳ Visu ready: [saved My Visus link]
```

Local fallback:

```text
Chrome Portal
↳ 1 version · pointer interaction · 8 controls
↳ Visu file ready: [local .visu path]
↳ Upload this .visu in Visu.Haus to edit, save, and share it.
```

If the user asks why it is fast or what tech it uses, answer directly: Babylon.js + WebGL fragment shader + SDF raymarching + procedural lighting, with JS only feeding small uniform values.
