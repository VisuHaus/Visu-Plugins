# Visu Plugin

Create interactive Visu.Haus `.visu` tools from Claude.

## Skill

```text
/visu:create-visu
```

This skill:

- checks the Visu.Haus connection first;
- saves directly to My Visus when connected;
- asks the user to connect before falling back;
- creates a local `.visu` file only when connection is unavailable, declined, or repeatedly fails;
- tells the user to upload local `.visu` files to Visu.Haus to edit, save, and share.

## MCP

The plugin includes a remote MCP server configuration:

```text
https://visu.haus/api/mcp
```

The plugin does not authenticate users itself. The Visu.Haus MCP handles account authorization and plan access.
