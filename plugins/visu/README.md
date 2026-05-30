# Visu Plugin

Create interactive Visu.Haus `.visu` visuals from a prompt, reference, or
creative direction.

When connected to Visu.Haus, this plugin saves new visuals directly to
**My Visus** and returns a ready link. When not connected, it can guide the user
through connection first, then fall back to a local `.visu` file only when the
current client supports it.

## Skill

```text
/visu:create-visu
```

This skill:

- creates polished interactive `.visu` visuals;
- uses the Visu.Haus connection first;
- saves directly to My Visus when connected;
- asks the user to connect before falling back;
- creates a local `.visu` file only when connection is unavailable, declined,
  or repeatedly fails;
- tells the user to upload local `.visu` files to Visu.Haus to edit, save, and
  share.

## 3D Skill

```text
/visu:3d-visu
```

Use this skill for the fast, high-fidelity 3D rendering route proven by
**Liquid Violet Metaballs**. It reuses the technology path, not the look:
Babylon.js, fullscreen WebGL, custom fragment shaders, SDF/raymarching or
equivalent procedural GPU fields, procedural lighting/reflections, and compact
uniform-driven motion. It also reuses the render direction that made that visu
work: procedural environment light, studio highlights, rim/Fresnel edges, soft
occlusion, tone mapping, bloom, FXAA, and material recipes for chrome, glass,
gel, liquid, mineral, energy, and product-like surfaces.

Requests can be broad - objects, spaces, portals, terrain, typography-inspired
forms, liquid, crystal, chrome, glass, or abstract scenes - while staying on the
same performance-oriented rendering path and lighting/material quality bar.

This route is intentionally exclusive for `/3D-Visu` style requests, so it
avoids mesh-heavy scenes, imported models, DOM animation, Canvas 2D, p5.js, and
Three.js for the core visual.

## Connection

The plugin includes the Visu.Haus connection configuration:

```text
https://visu.haus/api/mcp
```

The plugin does not authenticate users itself. Visu.Haus handles account
authorization and plan access through the connected service.
