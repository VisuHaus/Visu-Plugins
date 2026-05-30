# Visu.Haus Plugins

Claude plugin marketplace for creating interactive Visu.Haus visuals and tools.

## Install

In Claude, open **Customize -> Personal plugins -> Add marketplace**, then add:

```text
Visu-Haus/Visu-Plugins
```

Install and enable the **visu** plugin.

## Use

Run the create tool skill:

```text
/visu:create-visu
```

Some Claude surfaces may display the skill name as `create-visu`; plugin installs usually namespace skills with the plugin name, so the full command is `/visu:create-visu`.

## Connection Flow

The plugin tries the Visu.Haus connection first.

If the connection is active, Claude saves the result directly to **My Visus** and returns the saved link.

If the connection is not active, Claude should guide you through connecting the Visu.Haus MCP. If connection is unavailable in the current client, or you choose not to connect, supported local clients can create a `.visu` file instead.

Local `.visu` files must be uploaded to Visu.Haus to edit, save, and share them.

## Included Plugin

- `visu`: Visu.Haus MCP connection plus the `create-visu` skill.

## Requirements

- Claude with plugin support.
- A Visu.Haus account to save directly to My Visus.
- A Claude client with local file support for local `.visu` fallback.
