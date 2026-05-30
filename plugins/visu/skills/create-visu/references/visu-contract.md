# Visu Contract

Use this reference before writing or validating a `.visu` file.

## File Format

A `.visu` file is UTF-8 JSON containing a serialized Visu.Haus session. It is not a zipped project and not raw HTML. The core payload is:

```json
{
  "fileBaseName": "Liquid Chrome Flower",
  "fileNameManual": false,
  "prompt": "interactive liquid chrome flower",
  "motion": "",
  "autoControls": true,
  "customControls": [],
  "code": "<!DOCTYPE html>...",
  "cfg": null,
  "defaults": null,
  "ratio": "free",
  "analysis": null,
  "source": { "mode": "image" },
  "assets": { "mode": "none", "lastMode": "none", "revision": 0, "items": [] },
  "history": [],
  "activeVersionId": null,
  "renderQuality": 1,
  "typographyUi": null,
  "capabilitiesUi": null,
  "webcamUi": { "canvasFeedVisible": false }
}
```

Generated sessions may set `cfg` and `defaults` to `null` because the iframe posts `cfg_schema` to the host. If the current control values are known, set both to the same JSON-safe object used by `var cfg`.

## Required Practical Fields

- `prompt`: original user intent, not a generic rewrite.
- `code`: complete HTML document. It must include `<html>`, a rendering target, runtime code, and bridge handlers.
- `autoControls`: normally `true`.
- `customControls`: normally `[]`.
- `ratio`: use `"free"` unless the user requests a fixed aspect ratio.
- `source`: reference input metadata. Use `{ "mode": "image" }` when no specific reference is embedded.
- `assets`: uploaded/embedded asset metadata.
- `history`: at least one version is preferred. The active version should mirror `code`, `source`, `assets`, `cfg`, `defaults`, `ratio`, and UI state.
- `activeVersionId`: id of the active history version, or `null` if there is no history.
- `webcamUi`: include at least `{ "canvasFeedVisible": false }`.

## History Versions

Use history to preserve generated variants or the active version:

```json
{
  "id": "1710000000000-1",
  "time": "10:24 AM",
  "title": "Version 01",
  "code": "<!DOCTYPE html>...",
  "cfg": null,
  "defaults": null,
  "source": { "mode": "image" },
  "assets": { "mode": "none", "lastMode": "none", "revision": 0, "items": [] },
  "ratio": "free",
  "typographyUi": null,
  "capabilitiesUi": null,
  "webcamUi": { "canvasFeedVisible": false },
  "thumbnail": null
}
```

For multiple variants, keep the visual identity shared unless the user asks otherwise. Version 01 should be the faithful anchor; later versions should vary motion and interaction first.

## Source

`source` describes the primary reference, usually the prompt-engine reference image:

```json
{
  "mode": "image",
  "name": "reference.png",
  "mime": "image/png",
  "data": "base64-without-data-url-prefix",
  "svgText": "<svg>...</svg>",
  "manifest": null
}
```

Use `data` for base64 image payloads without the `data:mime;base64,` prefix. Use `svgText` only for SVG source text.

> **`source` is reserved for AI-generated reference imagery** (svg-from-prompt, generated thumbnails, the prompt-engine companion). User uploads from the editor sidebar always go to `assets`, never to `source`. Do not instruct the HTML to read uploads from `source` — `__VISU_ASSET_RUNTIME` only sees `assets`.

## Assets

`assets` describes optional files available to the visual:

```json
{
  "mode": "single-image",
  "lastMode": "single-image",
  "revision": 1,
  "items": [
    {
      "id": "asset-1",
      "kind": "image",
      "name": "texture.png",
      "mime": "image/png",
      "size": 12345,
      "dataUrl": "data:image/png;base64,...",
      "manifest": null,
      "generationContext": "short description for the generator"
    }
  ]
}
```

Supported modes: `none`, `single-image`, `multi-image`, `audio`, `video`, `svg`.

Supported item kinds: `image`, `audio`, `video`, `svg`. Multi-image mode uses multiple `image` items.

SVG items should include sanitized `svgText` and may include `manifest` / `generationContext` describing paint targets, dimensions, ids, or semantic regions.

> **`mode` is a UI hint, not a runtime toggle.** Setting `mode` to a non-`none` value at generation time tells the editor sidebar to open the matching uploader. `items` can be empty `[]` — the user fills them later. The `__VISU_ASSET_RUNTIME` is always live in the iframe regardless of `mode`, so registering a `subscribe` is the right default even when `mode` is `none`. See `references/asset-modes.md` for prompt-to-mode mapping and `references/runtime-capabilities.md` for the consumption snippets.

## Post Effects And Overlays

Optional fields:

- `postEffects`: host-side effect state for brightness, contrast, saturation, hue, clarity, invert, grain, halftone, threshold, duotone, vignette, bloom, blur, paperTexture, plasticTexture.
- `imageOverlays`: array of overlay images with `id`, `name`, `dataUrl`, `opacity`, `blendMode`, `fitMode`, `x`, `y`, `width`, `height`, `rotation`.
- `overlayLayerOrder`: array of overlay ids.
- `controlLayout`: optional sidebar ordering/hiding/label overrides for controls and cards.

Only set these when they materially support the requested output.
