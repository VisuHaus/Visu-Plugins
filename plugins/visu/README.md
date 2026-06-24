# Visu.Haus Plugin

Create interactive Visu.Haus `.visu` visuals from a prompt, reference, or
creative direction.

The plugin can either save new visuals directly to **My Visus** through the
Visu.Haus connection, or create a local `.visu` file for manual upload.

## Start

```text
/visu:visu-haus
```

Example:

```text
/visu:visu-haus
Create a slow liquid chrome flower with soft orbiting particles, pointer
interaction, and controls for bloom, density, color, and motion speed.
```

This skill:

- creates polished interactive `.visu` visuals;
- asks whether to save to a Visu.Haus account or create a local `.visu` file
  when the destination is unclear;
- checks the Visu.Haus connection only for account saves;
- creates local `.visu` files without calling the connection;
- tells the user to upload local `.visu` files to Visu.Haus to edit, save, and
  share.

## Delivery Paths

### Local `.visu` file

Use this path when you want a portable file or when the Visu.Haus connection is
not active. The skill builds a local `.visu` file and does not call the remote
connection.

### Save to My Visus

Use this path when you want a saved Visu.Haus link. The skill checks the
Visu.Haus connection, saves the generated visual to the connected user's
**My Visus**, and returns the saved link.

## Connection

The plugin includes the Visu.Haus connection configuration:

```text
https://visu.haus/api/mcp
```

The plugin does not authenticate users itself. Visu.Haus handles account
authorization and plan access through the connected service.

## Public Links

- Plugin repository: <https://github.com/VisuHaus/Visu-Plugins>
- Visu.Haus: <https://visu.haus>
- Installation guide: <https://visu.haus/articles/how-to-install-visuhaus-mcp>
- Privacy policy: <https://visu.haus/privacy-policy>
- Support: <hello@visu.haus>

## License

The Claude plugin package is licensed under Apache-2.0. This license applies
only to the plugin package: manifests, skill files, local helper scripts,
references, examples, and plugin documentation.

The hosted Visu.Haus service, backend, editor, hosted APIs, databases,
infrastructure, account systems, billing systems, user data, private prompts,
saved visus, uploaded media, generated outputs stored in Visu.Haus accounts,
and Visu.Haus brand assets are not licensed under the plugin package license.
See `NOTICE` for scope and trademark notices.

## Reviewer Checklist

1. Install and enable the `visu` plugin.
2. Run `/visu:visu-haus`.
3. Ask for a simple local `.visu` file and confirm a file is created.
4. Connect a Visu.Haus account only when testing the **My Visus** save path.
5. Ask for an account save and confirm the response returns a saved Visu.Haus
   link.
