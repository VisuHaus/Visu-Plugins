# Iteration

Use when the user refines an existing visu instead of creating fresh.

## Detection

Refinement signals — the user is editing, not starting over:

- Comparatives: "more X", "less X", "softer", "denser", "slower", "tighter".
- Continuity: "now", "same but", "keep it but", "instead of", "another version".
- Direct edits: "swap Y for Z", "remove the…", "add a…".
- Reference to the active version's parts: "the petals", "the camera", "the palette", "the bloom".

When in doubt, treat as iteration if a `.visu` was generated earlier in this session, or if the user is referencing one by name from `list_my_visus`.

## Edit Strategy

Identity preservation is the default. Don't redesign — extend.

- Keep palette, composition, density, scale, and renderer choice unchanged unless the user asks.
- Vary motion, interaction, and parameter ranges first.
- If the user asks for a substantial change (new subject, new material), confirm with one line of design echo before proceeding.

## Mechanics

- Read the active version's HTML from the `.visu` (history → activeVersionId).
- Edit only the parts that need to change.
- Append to `history` as `Version 02`, `03`, etc. The new version becomes active unless the user pinned an older one.
- Preserve `cfg` defaults the user is happy with; change only the keys the request touches.
- Re-run the ship gate.

## Asset transitions

If the user uploaded an asset between versions, the session's `assets.mode` now reflects the upload (the editor inferred it from MIME). The next iteration must:

- Preserve the new `assets.mode` — do not reset to `none`.
- If the previous version had no asset consumption hooks, add them: `subscribe(onAssetChange)` plus the matching accessor (`getImages`, `getAudioData`, `getVideoElement`, `__VISU_SVG_RUNTIME`). See `references/asset-modes.md`.
- Use the existing `state.items` shape — do not assume the user re-uploads.
- Keep the procedural fallback intact for the empty-items state, so the visu still looks designed if the user clears the upload.

If the user explicitly says "ignore the upload" or "go back to no asset", set `mode` back to `none` and route through the fallback path. The runtime listener stays.

## Save Semantics

- If the visu is already on the user's account: prefer `save_visu_version` (new version on the same visu) when the user explicitly saves.
- If the visu is local-only: overwrite the local `.visu` with the new active version + extended history.
- If MCP fails on a save attempt, fall back to the local file silently.

## What not to do

- Don't regenerate from scratch when the user said "tweak X".
- Don't surface to the user that you're "iterating" — just deliver the new version using the same final response format.
- Don't break older versions in `history`. Always append.
- Don't change the renderer mid-iteration unless the request requires it (e.g. "make it 3D now"). Renderer changes break visual identity.
