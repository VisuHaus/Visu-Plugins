# Runtime Capabilities

Use this reference when writing the HTML inside a `.visu`.

## Core HTML Rules

- Return a complete HTML document.
- Fill the viewport: `body{margin:0;overflow:hidden;background:#000}`.
- Use a canvas, SVG, DOM, WebGL, Three.js scene, or hybrid renderer as appropriate.
- Use `var` and `function` syntax in generated runtime code.
- Use `requestAnimationFrame` and keep animation alive unless `_animEnabled` is false.
- Do not depend on a build step.

## Controls

Expose editable controls as:

```js
var cfg = {
  _animEnabled: { value: true, type: 'toggle', label: 'Animate', group: 'Motion' },
  quantity: { value: 40, type: 'slider', label: 'Quantity', group: 'Shapes', min: 1, max: 100, step: 1 },
  size: { value: 72, type: 'slider', label: 'Size', group: 'Shapes', min: 1, max: 200, step: 1, unit: 'px' },
  colorA: { value: '#f24b2f', type: 'color', label: 'Primary', group: 'Colors' }
};
```

Types: `slider`, `color`, `text`, `toggle`, `dropdown`.

Dropdown example:

```js
blendMode: { value: 'screen', type: 'dropdown', label: 'Blend', group: 'Effects', options: ['normal','multiply','screen','overlay','add'] }
```

Design controls for the specific visual. Include quantity/count, size/scale, core motion speed, palette controls, and only the effects that matter.

## Message Bridge

Every visual must include this contract, adapted as needed:

```js
var _cameraZoom = 1, _cameraPanX = 0, _cameraPanY = 0, _cameraOrbitX = 0, _cameraOrbitY = 0;
var _animEnabled = true, _effectsEnabled = true;

window.addEventListener('message', function(e) {
  if (!e.data) return;
  if (e.data.type === 'cfg_update') {
    if (e.data.key === '_animEnabled') _animEnabled = e.data.value;
    else if (e.data.key === '_effectsEnabled') _effectsEnabled = e.data.value;
    else if (cfg[e.data.key]) cfg[e.data.key].value = e.data.value;
  }
  if (e.data.type === 'camera_update') {
    _cameraZoom = e.data.zoom || 1;
    _cameraPanX = e.data.panX || 0;
    _cameraPanY = e.data.panY || 0;
    _cameraOrbitX = e.data.orbitX || 0;
    _cameraOrbitY = e.data.orbitY || 0;
  }
  if (e.data.type === 'request_snapshot') {
    var cv = document.getElementById('c');
    if (cv) parent.postMessage({ type: 'snapshot_ready', dataUrl: cv.toDataURL('image/png') }, '*');
  }
});

window.addEventListener('load', function() {
  parent.postMessage({ type: 'cfg_schema', cfg: cfg }, '*');
});
```

For Canvas 2D viewport controls:

```js
ctx.save();
ctx.translate(W / 2, H / 2);
ctx.scale(_cameraZoom, _cameraZoom);
ctx.translate(-W / 2 + _cameraPanX, -H / 2 + _cameraPanY);
// draw scene
ctx.restore();
```

For Three.js camera controls, map zoom/pan/orbit to the camera and call `camera.lookAt(0,0,0)`.

## Renderer Choice

- Use WebGL 2D for SDFs, contours, metaballs, smooth gradients, glows, raymarch-like fields, shader noise, and high-density pixel effects.
- Use Canvas 2D for particles, dot grids, line systems, typography masks, image sampling, and simpler geometry.
- Use Three.js when the prompt asks for 3D, perspective, meshes, depth, orbiting camera, cube, sphere, torus, room, sculpture, or physical materials.
- Use hybrid rendering when assets, text, or overlays need a 2D layer over WebGL/Three.js.

Three.js CDN:

```html
<script src="https://cdn.jsdelivr.net/npm/three@0.160.0/build/three.min.js"></script>
```

## WebGL Rules

- Use `preserveDrawingBuffer:true` for snapshots.
- Avoid uniform loop bounds. Use literal constants:

```glsl
const int MAX_SHAPES = 40;
for (int i = 0; i < MAX_SHAPES; i++) {
  if (i >= u_shapeCount) break;
}
```

- Size arrays with constants.
- Avoid hard SDF edges with `if`, `step`, or raw thresholds. Use `smoothstep` and `fwidth` for antialiasing.

## Motion And Pointer Interaction

Every visual needs continuous motion and interaction:

- Drift, orbit, breathing, rotation, flow, phase shift, feedback, or kinetic layout.
- Pointer attract/repel/follow/drag/orbit/brush, matched to the concept.
- Reset pointer state on leave:

```js
canvas.addEventListener('mouseleave', function(){ mx = -9999; my = -9999; });
```

Use damping around `0.96` to `0.99` for physics. Add a small velocity boost to prevent dead particles.

## Webcam Capability

Declare webcam only when it is meaningful:

```html
<script id="visu-metadata" type="application/json">{"capabilities":{"webcam":{"enabled":true,"required":true,"features":["video","motion","face","hands","gestures"],"hint":"Face yaw and hand openness shape the field."}}}</script>
```

Do not call `getUserMedia`, MediaPipe, TensorFlow, or render camera permission UI. The host handles stream, permissions, preview, and tracking.

Runtime API:

- `window.__VISU_WEBCAM_RUNTIME.getVideoElement()`
- `window.__VISU_WEBCAM_RUNTIME.getMetrics()`
- `window.__VISU_WEBCAM_RUNTIME.requestAccess()`
- `window.__VISU_WEBCAM_RUNTIME.setControlInfluence(key, { text, amount })`

Useful metrics:

- Summary: `motionAmount`, `motionX`, `motionY`, `centerX`, `centerY`, `brightness`, `averageColor`, `timestamp`.
- Face: `face.detected`, `face.position.x/y/z`, `face.rotation.yaw/pitch/roll`, `face.mouthOpen`, `face.smile`, `face.eyeLeftOpen`, `face.eyeRightOpen`, `face.browRaise`.
- Fine face: `face.mouth.*`, `face.eyes.*`, `face.brows.*`, `face.jaw.*`, `face.blendshapes`, `face.raw.landmarks`.
- Hands: `hands.count`, `hands.left/right.detected`, `hands.left/right.palm`, `indexTip`, `thumbTip`, `pinch`, `open`, `rotation`, `fingers.*`, `pinches.*`, `spread.*`, raw landmarks.
- Gestures: `gestures.left`, `gestures.right`, `gestures.primary`, `gestures.confidence`.

Always provide graceful fallback values when camera access is missing.

If webcam modulates a control, update the host mapping:

```js
window.__VISU_WEBCAM_RUNTIME.setControlInfluence('rotationSpeed', {
  text: 'Face yaw -> Rotation',
  amount: face.rotation.yaw
});
```

## Assets Capability

`window.__VISU_ASSET_RUNTIME` is **always injected** by the host, regardless of `session.assets.mode`. Always register a `subscribe` - the host calls it immediately with the current state and again every time the user uploads, removes, or plays an asset. Without a subscribe, uploads that arrive after generation have no destination.

There is no `capabilities.assets` metadata block. The host decides which uploader to open from `session.assets.mode` in the `.visu` and from implicit usage detection of `__VISU_ASSET_RUNTIME` / `getImages` / `getAudioData` / `getVideoElement` / `__VISU_SVG_RUNTIME` in the HTML. Setting `mode` to a non-`none` value at generation time is a hint to the editor sidebar - the runtime works with any value of `mode`.

User uploads always land in `session.assets`. `session.source` is reserved for AI-generated reference images; never read uploads from it.

### State shape

`getState()` and `subscribe` callbacks receive:

```js
{
  version: 1,
  mode: 'none' | 'single-image' | 'multi-image' | 'audio' | 'video' | 'svg',
  updatedAt: 1715000000000,
  items: [
    {
      id: 'asset-1',
      kind: 'image' | 'audio' | 'video' | 'svg',
      name: 'photo.jpg',
      mime: 'image/jpeg',
      size: 12345,
      src: 'data:...' | 'blob:...',  // or `dataUrl` / `url`
      svgText: '<svg>…</svg>',        // svg only
      manifest: null,
      generationContext: ''
    }
  ],
  audio: { playing, currentTime, duration, muted, loop, rms, peak, bass, mid, treble, spectrum: float[16], waveform: float[32] },
  video: { playing, currentTime, duration, muted, loop }
}
```

`audio` and `video` are only present when the corresponding element exists.

### Default subscribe block

Drop this in every visu (paired with the message bridge):

```js
var assetState = { mode: 'none', items: [] };
var assetRuntime = null;
function onAssetChange(s) {
  assetState = s || assetState;
  // re-bind buffers, swap textures, reset audio analyser, redraw if static.
}
if (window.__VISU_ASSET_RUNTIME) {
  assetRuntime = window.__VISU_ASSET_RUNTIME;
  assetRuntime.subscribe(onAssetChange);
}
window.addEventListener('visu:asset-change', function(e){ onAssetChange(e.detail); });
```

`subscribe` returns an unsubscribe function (you rarely need it inside an iframe). The `visu:asset-change` event is the same payload as a bound listener fallback.

### Per-mode consumption

Pick the right accessor based on `assetState.mode` (or call without checking - the runtime returns null/empty when nothing is loaded). Always render a designed fallback when the asset is absent. If the HTML is opened outside the editor, `assetRuntime` may be null; keep the fallback alive.

- **single-image** / **multi-image**:

  ```js
  var imgs = assetRuntime ? assetRuntime.getImages() : [];
  var img = assetState.mode === 'single-image'
    ? (assetRuntime ? assetRuntime.getPrimaryImage() : null)
    : imgs[Math.floor((time * cfg.sequenceSpeed.value) % Math.max(1, imgs.length))];
  if (img && img.complete && img.naturalWidth) drawWithImage(img);
  else drawProceduralFallback();
  ```

  Use `getPrimaryImage()` for single-image. Multi-image returns the full array - index, atlas, morph between, or sequence frames. Handle 0, 1, and many images.

- **audio**:

  ```js
  var a = assetRuntime ? assetRuntime.getAudioData() : null;
  // a.bass / a.mid / a.treble / a.rms / a.peak (0..1)
  // a.spectrum (16 bins, 0..1) / a.waveform (32 samples, -1..1)
  var pulse = a ? Math.max(0.05, a.rms) : 0.12 + 0.05 * Math.sin(time);
  ```

  The host element auto-plays after the user hits play in the sidebar. `setMuted`, `setLoop`, `setCurrentTime` control playback.

- **video**:

  ```js
  var v = assetRuntime ? assetRuntime.getVideoElement() : null;
  if (v && v.readyState >= 2) ctx.drawImage(v, 0, 0, W, H);
  else drawAnimatedGradient();
  ```

  The video element is muted, autoplay, looped - sample frames into canvas/WebGL/Three.js textures every frame. For WebGL video shaders, use this minimum texture update pattern:

  ```js
  var videoTex = gl.createTexture();
  gl.bindTexture(gl.TEXTURE_2D, videoTex);
  gl.texParameteri(gl.TEXTURE_2D, gl.TEXTURE_MIN_FILTER, gl.LINEAR);
  gl.texParameteri(gl.TEXTURE_2D, gl.TEXTURE_MAG_FILTER, gl.LINEAR);
  gl.texParameteri(gl.TEXTURE_2D, gl.TEXTURE_WRAP_S, gl.CLAMP_TO_EDGE);
  gl.texParameteri(gl.TEXTURE_2D, gl.TEXTURE_WRAP_T, gl.CLAMP_TO_EDGE);

  function updateVideoTexture() {
    var v = assetRuntime ? assetRuntime.getVideoElement() : null;
    if (!v || v.readyState < 2) return false;
    gl.bindTexture(gl.TEXTURE_2D, videoTex);
    gl.pixelStorei(gl.UNPACK_FLIP_Y_WEBGL, true);
    gl.texImage2D(gl.TEXTURE_2D, 0, gl.RGBA, gl.RGBA, gl.UNSIGNED_BYTE, v);
    return true;
  }
  ```

  The fragment shader should branch from a uniform such as `u_hasVideo` so the fallback shader remains polished until the user uploads a clip.

- **svg** (uses a separate global):

  ```js
  if (window.__VISU_SVG_RUNTIME) {
    var node = window.__VISU_SVG_RUNTIME.inlineNode();
    window.__VISU_SVG_RUNTIME.applyPaintOverrides(node, { fill: cfg.colorA.value });
    document.body.appendChild(node);
  }
  ```

  Other helpers: `parse()`, `mountHidden()`, `loadImage()` (rasterizes), `getPaintTargets(root)`.

### Mode reference

- `none`: no uploader hint; runtime is still live so listener catches future uploads.
- `single-image`: transform/sample one image.
- `multi-image`: collage, atlas, morph set, particle source, image sequencing.
- `audio`: audio analysis, waveform, spectrum, beat-like amplitude.
- `video`: sample video frames, feedback, masks, chroma-like effects.
- `svg`: recolor, animate paths, use as mask, clone inline nodes, or render as image.

Do not invent asset files. Use what `state.items` exposes, and fall back gracefully when absent.

## Typography Capability

If visible text is central, declare typography:

```html
<script id="visu-metadata" type="application/json">{"capabilities":{"typography":{"enabled":true,"required":true,"fontSelectable":true,"defaultFamily":"Georgia","fallbackFamily":"serif","hint":"The typeface controls the visual tone."}}}</script>
```

Use `window.__VISU_TYPOGRAPHY_RUNTIME`:

- `getState()`
- `getSelectedFamily()`
- `getSelectedFace()`
- `getFontStack(fallback)`
- `loadFont(descriptor, sampleText)`
- `applyToElements(selector, options)`
- `subscribe(fn)`

For Canvas text, rebuild `ctx.font` from runtime state and call `loadFont` before measurement when possible.

## Advanced Text Layout

Use only when multiline text layout/reflow is central. Declare it with typography:

```html
<script id="visu-metadata" type="application/json">{"capabilities":{"typography":{"enabled":true,"required":true,"fontSelectable":true,"defaultFamily":"Georgia","fallbackFamily":"serif"},"advancedTextLayout":{"enabled":true,"required":true,"mode":"advanced_layout","engine":"pretext","hint":"Multiline layout is the visual material."}}}</script>
```

Use `window.__VISU_TEXT_RUNTIME` for measurement and layout: `ensureReady()`, `isReady()`, `prepare()`, `layout()`, `prepareWithSegments()`, `layoutWithLines()`, `layoutNextLine()`, `createLayout()`, `createSegmentLayout()`, `measure()`.

Do not rely on repeated DOM measurements inside the animation loop.

## Host Post Effects And Overlays

If the requested output needs host-level effects, set session `postEffects` instead of baking everything into the HTML. Available effect keys include brightness, contrast, saturation, hue, clarity, invert, grain, halftone, threshold, duotone, vignette, bloom, blur, paperTexture, and plasticTexture.

Use `imageOverlays` for explicit composited images that should remain user-editable in the host.
