# Aesthetic Vocabulary

Lookup table from user vibe to concrete rendering decisions. Use when the prompt names a material/feel without specifying renderer or motion.

## Materials

| Vibe | Renderer | Motion default | Palette default |
|---|---|---|---|
| **liquid** | WebGL — SDF metaballs / smooth fields | slow flow, displacement, inertia | saturated gradients, single accent |
| **chrome** | Three.js — envMap, IBL, anisotropy | continuous orbit, sharp highlights | mirror reflections, iridescent shifts |
| **paper** | Canvas 2D — layered, soft shadow | almost still + parallax breath | off-white base, ink accent, light grain |
| **neon** | WebGL — bloom, dark backdrop | pulse, decay, light bleed | black ground, saturated cores |
| **ink** | Canvas 2D — wet brush, bleed | dispersion, edge bleed | black on off-white |
| **pixel** | Canvas 2D — nearest-neighbor | step time, grid quantize | limited palette (4–8 colors) |
| **glass** | Three.js — transmission, IOR | slow rotation, refraction shimmer | cool tints, white highlights |
| **cloth** | Canvas 2D or WebGL — verlet/grid | wave + settle, drape | muted, fabric-like |
| **smoke** | WebGL — fluid sim or noise advection | drift + dissipation | soft monochrome with single hue |
| **plasma** | WebGL — domain-warped noise | constant churn, energy bleed | high-contrast pairs |
| **wire** | Canvas 2D / Three.js lines | rotation, slow morph | single line color on dark |
| **tape** | Canvas 2D — overlap, slight rotation | settle, layered drift | analog warm, paper texture |
| **stone** | Three.js — matte, normal detail | very slow rotation, weight | desaturated earth tones |

## Compositions

- **single subject**: focal center, generous negative space, scale dominance.
- **field**: many small elements with rhythmic distribution, low individual weight.
- **stack**: layered depth bands, parallax on motion.
- **edge**: subject anchored to one side, motion sweeps across.
- **grid**: quantized lattice, motion as phase shift.
- **horizon**: split composition, contrast between halves.

## Motion vocabulary

- **breathe**: slow scale or opacity oscillation, period > 4s.
- **drift**: low-velocity translation with no destination.
- **orbit**: continuous rotation around an anchor.
- **pulse**: discrete intensity events, decaying.
- **flow**: directional field, advected particles.
- **settle**: physics with damping toward rest, never quite still.
- **shimmer**: high-frequency low-amplitude variation in color or normal.
- **bloom**: scale-up from a point with optional alpha trail.

## Interaction vocabulary

- **attract / repel**: pointer is a force source.
- **brush**: pointer leaves a trace that decays.
- **gaze**: subject orients toward pointer.
- **scrub**: pointer position maps to a parameter (time, phase).
- **release / spring**: state returns elastically when pointer leaves.
- **stir**: pointer motion injects rotational energy.

## When the prompt is ambiguous

If the prompt names a vibe without renderer (e.g. "make something liquid and warm"), use this table to pick. Do not ask. The discovery question is reserved for prompts that don't even name a vibe.

## When the prompt contradicts

If the user says "liquid chrome" — both apply, blend: chrome material logic + liquid motion logic. Never pick one and drop the other.

## When the prompt is non-material

If the user names an emotion or scene rather than a material ("calm forest", "anxious city"), translate emotion to motion + palette before picking renderer:

- calm → slow + low contrast + minimal interaction
- anxious → fast + high contrast + reactive
- nostalgic → soft palette + slight grain + paper or tape
- energetic → saturated + pulse + bloom
- intimate → small subject + generous negative space + breath motion
