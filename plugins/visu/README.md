# Visu Plugin

Create interactive Visu.Haus `.visu` visuals from a prompt, reference, or
creative direction.

The plugin can either save new visuals directly to **My Visus** through the
Visu.Haus connection, or create a local `.visu` file for manual upload.

## Skill

```text
/visu:create-visu
```

This skill:

- creates polished interactive `.visu` visuals;
- asks whether to save to a Visu.Haus account or create a local `.visu` file
  when the destination is unclear;
- checks the Visu.Haus connection only for account saves;
- creates local `.visu` files without calling the connection;
- tells the user to upload local `.visu` files to Visu.Haus to edit, save, and
  share.

## Connection

The plugin includes the Visu.Haus connection configuration:

```text
https://visu.haus/api/mcp
```

The plugin does not authenticate users itself. Visu.Haus handles account
authorization and plan access through the connected service.
