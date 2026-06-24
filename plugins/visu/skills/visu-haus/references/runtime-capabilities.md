# Runtime Capabilities

Use this reference when writing the HTML inside a `.visu`.

## Core HTML Rules

- Return a complete HTML document.
- Fill the viewport: `body{margin:0;overflow:hidden;background:transparent}`.
- Draw the artwork background inside the scene, not with body CSS. If `background_filled` exists, draw that backdrop only when `background_filled` is true so preview/export can produce real alpha when it is false.
- Use a canvas, SVG, DOM, WebGL, Three.js scene, or hybrid renderer as appropriate.
- Use `var` and `function` syntax in generated runtime code.
- Use `requestAnimationFrame` and keep animation alive.
- Do not depend on a build step.

## Controls

Expose editable controls as:

```js
var cfg = {
  quantity: { value: 40, type: 'slider', label: 'Quantity', group: 'Shapes', min: 1, max: 100, step: 1 },
  size: { value: 72, type: 'slider', label: 'Size', group: 'Shapes', min: 1, max: 200, step: 1, unit: 'px' },
  colorA: { value: '#f24b2f', type: 'color', label: 'Primary', group: 'Colors' }
};
```

Types: `slider`, `number`, `color`, `toggle`, `select`, `text`, `textarea`, `button`, `asset`.

Select example:

```js
blendMode: { value: 'screen', type: 'select', label: 'Blend', group: 'Effects', options: ['normal','multiply','screen','overlay','add'] }
```

Design controls as art-direction knobs for the specific visual, not generic sliders. Include practical controls such as color, size, quantity/count, speed, motion intensity, opacity, spacing, scale, rotation, density, and background when relevant. Include artistic controls when they fit: chaos, order, tension, softness, turbulence, gravity, magnetism, elasticity, rhythm, distortion, contrast, grain, bloom, depth, complexity, randomness, symmetry, fragmentation, fluidity, and atmosphere.

Always include `quantity/count` when the visual has repeated elements, particles, instances, objects, strokes, letters, or generated units. Always include `size` when the visual has scalable shapes, objects, particles, typography, brush marks, images, or model elements. Always include a primary motion speed/intensity control when the visual has automatic animation or procedural motion.

Prefer fewer high-impact controls over many low-value controls. Defaults must produce the best-looking result immediately.

Host-rendered controls should also be declared in:

```html
<script id="visu-metadata" type="application/json">{"toolSchema":{"controls":[{"key":"background_filled","type":"toggle","label":"Filled Background","group":"Background","defaultValue":true},{"key":"shuffle_layout","type":"button","label":"Shuffle Layout","group":"Actions"},{"key":"background_image","type":"asset","kind":"image","label":"Background Image","group":"Layers","maxItems":1}]},"stage":{"background":{"transparent":true,"color":"#ffffff","opacity":1}}}</script>
```

Button controls are momentary actions, not persistent toggles. Listen for `visu:control-action` or `message.type === "visu_control_action"`.

Asset controls are runtime file fields. Allowed asset kinds are `image`, `image-set`, `audio`, `video`, `svg`, and `model3d`. Do not declare `font`, `other`, `generic`, `unknown`, or arbitrary file asset fields.

When drawing an uploaded image asset, video asset, or webcam video into a bounded area, add a sibling `Fit` select control. Use key `<media_key>_fit` for asset fields or `webcam_fit` for webcam, options `["cover","fill"]`, and default `cover`. `cover` preserves aspect ratio and crops overflow; `fill` stretches to the bounds and may distort.

If the visual draws a full-canvas/full-page background, include `background_filled` as a toggle labelled "Filled Background" in group "Background" with `defaultValue:true`. Transparent background is opt-out: when `background_filled` is false, do not draw the scene backdrop. For these visuals, set `stage.background.transparent:true` so disabling the toggle reveals real transparency in preview and PNG export.

## Message Bridge

Every visual must include this contract, adapted as needed:

```js
var _cameraZoom = 1, _cameraPanX = 0, _cameraPanY = 0, _cameraOrbitX = 0, _cameraOrbitY = 0;

window.addEventListener('message', function(e) {
  if (!e.data) return;
  if (e.data.type === 'cfg_update') {
    if (cfg[e.data.key]) cfg[e.data.key].value = e.data.value;
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

- Prefer WebGPU for modern GPU-driven visuals: SDFs, ray marching, flow fields, glows, gradients, particles, feedback textures, reaction-diffusion, image/video processing, simulations, large grids, and multi-pass generative systems. Feature-detect with `navigator.gpu`; if unavailable at runtime, initialize an equivalent WebGL2 path.
- Use WebGL2 for medium-complexity shader visuals or runtime compatibility: SDFs, contours, metaballs, smooth gradients, glows, raymarch-like fields, shader noise, and high-density pixel effects.
- Use Three.js for stylized, toon, abstract, mograph, generative, shader-driven, or lightweight 3D visuals.
- Use Babylon.js when the prompt asks for realistic render quality, product/PBR rendering, physical materials, studio lighting, shadows, reflections, glass, metal, plastic, or premium inspectable 3D objects.
- Use Canvas 2D, p5.js, or another non-GPU/simple renderer only when explicitly requested, or as a last-resort compatibility path to avoid a blank canvas.
- Use hybrid rendering when assets, text, or overlays need a 2D layer over WebGL/Three.js.

Three.js CDN:

```html
<script src="https://cdn.jsdelivr.net/npm/three@0.160.0/build/three.min.js"></script>
```

For WebGPU, use one visible canvas, async initialization, inline WGSL, render pipelines, uniform buffers, storage buffers when useful, and `requestAnimationFrame`. Keep it self-contained: no build tools, bundlers, external shader files, or server GPU work. Update uniforms/buffers from `cfg` so controls stay live and keep snapshot/export support from the visible canvas.

For Babylon.js, use one visible canvas, `Engine`, `Scene`, `ArcRotateCamera`, lights, environment lighting when useful, PBR materials, and GLB/GLTF loading. Keep the uploaded/fallback model centered, scaled, lit, and visible.

## WebGL Rules

- Use `preserveDrawingBuffer:true` for snapshots.
- If using WebGL2 with `#version 300 es`, GLSL must use `in`/`out` varyings, an explicit fragment output, and `texture()`. Do not use `varying`, `gl_FragColor`, or `texture2D()` in WebGL2 shaders. If sharing shader code with WebGL1, gate syntax with `#ifdef WEBGL2` / `#else`.
- Do not declare custom GLSL identifiers beginning with `gl_`; that prefix is reserved for built-in names.
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

- Motion should emerge from the procedural system, not random decoration.
- Use easing, anticipation, follow-through, overshoot, elastic return, damping, inertia, stagger, delay, and rhythm.
- Drift, orbit, breathing, rotation, flow, phase shift, feedback, or kinetic layout.
- Pointer attract/repel/follow/drag/orbit/brush, matched to the concept, with eased response rather than instant jumps.
- Reset pointer state on leave:

```js
canvas.addEventListener('mouseleave', function(){ mx = -9999; my = -9999; });
```

Use damping around `0.96` to `0.99` for physics. Add a small velocity boost to prevent dead particles. Match motion to style: minimal/geometric uses slow easing; organic/fluid uses breathing and soft damping; energetic/chaotic uses bursts and controlled randomness; editorial/type uses readable staggered timing; 3D uses smooth orbit, inertial camera movement, eased zoom, and object rotation.

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
  mode: 'none' | 'single-image' | 'multi-image' | 'audio' | 'video' | 'svg' | 'model3d',
  updatedAt: 1715000000000,
  items: [
    {
      id: 'asset-1',
      kind: 'image' | 'audio' | 'video' | 'svg' | 'model3d',
      name: 'photo.jpg',
      mime: 'image/jpeg',
      size: 12345,
      src: 'data:...' | 'blob:...',  // or `dataUrl` / `url`
      svgText: '<svg>…</svg>',        // svg only
      manifest: null,
      generationContext: ''
    }
  ],
  audio: { playing, currentTime, duration, muted, loop, rms, peak, bass, mid, treble, spectrum: float[16], waveform: float[32], frequencyData, timeDomainData },
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

For asset controls declared in `toolSchema`, use `window.__VISU_ASSET_RUNTIME.getField(fieldKey)`. Field helpers include `getItems()`, `getPrimary()`, `getImage()`, `getImages()`, `getAudioElement()`, `getAudioData()`, `getVideoElement()`, `getSvg()`, `getModel()`, `getModelUrl()`, `getModelBlob()`, `getModelArrayBuffer()`, `hasFiles()`, and `subscribe(fn)`.

For Canvas 2D media drawing, use a fit helper instead of stretching by default:

```js
function drawMediaFitted(ctx, media, x, y, w, h, fit) {
  var mw = media.videoWidth || media.naturalWidth || media.width;
  var mh = media.videoHeight || media.naturalHeight || media.height;
  if (!mw || !mh) return false;
  if (fit === 'fill') {
    ctx.drawImage(media, x, y, w, h);
    return true;
  }
  var scale = Math.max(w / mw, h / mh);
  var sw = w / scale;
  var sh = h / scale;
  var sx = (mw - sw) / 2;
  var sy = (mh - sh) / 2;
  ctx.drawImage(media, sx, sy, sw, sh, x, y, w, h);
  return true;
}
```

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

  The host element plays after the user hits play in the sidebar. `getAudioData()` returns an analysis object, not a raw array: `{ playing, currentTime, duration, rms, peak, bass, mid, treble, spectrum, waveform, frequencyData, timeDomainData }`. Use `rms`, `peak`, `bass`, `mid`, `treble`, `spectrum`, `waveform`, or `frequencyData` for reaction. Do not rely on `audioData.length` or `audioData[i]` as the primary contract. Do not autoplay audio or create separate audio elements.

- **video**:

  ```js
  var v = assetRuntime ? assetRuntime.getVideoElement() : null;
  if (v && v.readyState >= 2) drawMediaFitted(ctx, v, 0, 0, W, H, cfg.video_fit.value);
  else drawAnimatedGradient();
  ```

  The video element is muted, autoplay, looped - sample frames into canvas/WebGL/Three.js textures every frame. Do not call `play()`, `setMuted()`, `setLoop()`, `pause()`, `togglePlayback()`, or `setCurrentTime()` from subscribe callbacks, asset-change handlers, or animation loops; the host owns playback setup. For WebGL video shaders, use this minimum texture update pattern:

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

- **model3d**:

  Use `assetRuntime.getModelUrl()` for global model assets or `assetRuntime.getField(fieldKey).getModelUrl()` for declared `model3d` fields. The host provides a file descriptor or URL, not a ready `THREE.Object3D`. For GLB/GLTF, use the classic compatible loader path: `three@0.160.0/build/three.min.js` plus `three@0.146.0/examples/js/loaders/GLTFLoader.js`, then `new THREE.GLTFLoader()`. Keep the current/fallback model visible until the replacement model finishes loading successfully.

### Mode reference

- `none`: no uploader hint; runtime is still live so listener catches future uploads.
- `single-image`: transform/sample one image.
- `multi-image`: collage, atlas, morph set, particle source, image sequencing.
- `audio`: audio analysis, waveform, spectrum, beat-like amplitude.
- `video`: sample video frames, feedback, masks, chroma-like effects.
- `svg`: recolor, animate paths, use as mask, clone inline nodes, or render as image.
- `model3d`: load GLB/GLTF as the primary scene object, with a procedural fallback while absent.

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
