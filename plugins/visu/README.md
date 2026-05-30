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

## Connection

The plugin includes the Visu.Haus connection configuration:

```text
https://visu.haus/api/mcp
```

The plugin does not authenticate users itself. Visu.Haus handles account
authorization and plan access through the connected service.
