# Planning

Use this reference when the prompt is broad, image-based, or asks for variants.

## Prompt Reading

Preserve the user's language and odd specificity. Do not normalize a vivid prompt into generic art direction. Translate it into concrete rendering decisions:

- Subject: what appears.
- Material: what it seems made of.
- Composition: where things live on the canvas.
- Motion: how it behaves over time.
- Interaction: what the user changes through pointer, camera, audio, or assets.
- Controls: what should be editable.
- Capability needs: webcam, typography, advanced text layout, assets, post effects, overlays.

## Image References

When an image is provided:

- Inspect composition, palette, scale, texture, lighting, geometry, typography, and negative space.
- Decide whether the output should faithfully recreate the image, use it as inspiration, or transform it as an asset.
- If the image contains brand marks, faces, or product forms, preserve the user's requested intent while avoiding accidental distortion.
- If the image should be used live, embed it as `source` or `assets` and use the asset runtime.
- If the image is only a reference, generate code that recreates its visual logic rather than requiring the image file.

## Runtime Plan Shape

For complex prompts, create an internal plan:

```json
{
  "runtime": "webgl",
  "suggestedName": "Sunlit Dust Drift",
  "capabilities": {
    "webcam": { "enabled": false, "features": [] },
    "typography": { "enabled": false },
    "advancedTextLayout": { "enabled": false }
  },
  "assetUsage": { "mode": "none", "required": false, "strategy": "" },
  "variants": [
    { "id": "core", "delta": "Faithful to the prompt with default motion and no extra interaction layer." },
    { "id": "elastic", "delta": "Same look; motion gains overshoot and springy decay." }
  ]
}
```

Runtime values: `webgl`, `canvas2d`, `three`, `hybrid`.

## Variants

When generating multiple versions:

- Version 01 is the anchor and must be the most faithful interpretation.
- Later versions should keep palette, composition, density, and visual identity stable unless the user requests broader variation.
- Vary motion and interaction first: timing, easing, force behavior, orbit, input mapping, reactivity.
- Store each variant in `history`; set the first as active unless the user chooses another.

## Capability Decisions

Enable webcam only if face, body, hand, gesture, camera feed, or live presence improves the result.

Enable typography only if visible text/glyphs are core to the artwork.

Enable advanced text layout only if multiline reflow, poems, paragraphs, editorial layouts, or text wrapping are central.

Use assets only when the user provides files or explicitly requests an asset-driven visual. Do not pretend unavailable assets exist.

Use post effects when the effect should remain host-editable. Bake effects into HTML when they are central to the renderer.

## Naming

Use a short evocative `fileBaseName`, ideally 2 to 4 words. Avoid slashes, emoji, quotes, and punctuation-heavy names. If the prompt is empty or generic, use `Untitled`.
