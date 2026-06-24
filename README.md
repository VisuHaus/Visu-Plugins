# Visu.Haus Plugins

Create interactive Visu.Haus visuals directly from your AI workspace.

This marketplace installs the Visu.Haus plugin and the `/visu:visu-haus`
skill. Use it to turn a prompt, image reference, brand direction, shader idea,
or motion concept into a polished `.visu` visual.

Choose whether to save new visus directly to **My Visus** through your
Visu.Haus connection, or create a local `.visu` file for manual upload.

## Install

Open your plugin settings, choose **Add marketplace**, and add:

```text
VisuHaus/Visu-Plugins
```

Then install and enable the **visu** plugin.

## Create A Visu

Start with:

```text
/visu:visu-haus
```

Then describe what you want to make:

```text
/visu:visu-haus
Create a slow liquid chrome flower with soft orbiting particles, pointer
interaction, and controls for bloom, density, color, and motion speed.
```

You can also attach images or describe a product, campaign, logo, texture,
gallery, video shader, audio-reactive visual, or typography system.

## What Happens Next

The plugin asks where to deliver the visu if your prompt does not make it clear.

If you choose your Visu.Haus account:

- your visu is created;
- the plugin checks your Visu.Haus connection;
- it is saved directly to **My Visus**;
- you receive a Visu.Haus link.

If you choose a local file:

- the plugin skips the connection;
- it creates a local `.visu` file in supported clients;
- upload that `.visu` file to Visu.Haus to edit, save, and share it.

## Good Prompts

Try describing subject, material, motion, interaction, and format:

```text
Create a 9:16 reactive poster for a perfume launch. It should feel like black
glass, silver mist, and slow magnetic particles. Add controls for intensity,
mist, palette, and motion speed.
```

```text
Create a video shader that turns an uploaded clip into liquid neon feedback
with a procedural fallback before a video is added.
```

```text
Create an interactive typography visu using the word AURA, with soft cloth
distortion, pointer pull, and a minimal editorial palette.
```

## Requirements

- A compatible plugin-enabled AI client.
- A Visu.Haus account to save directly to **My Visus**.
- Local file support only if you want `.visu` files.

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
See the plugin `NOTICE` file for scope and trademark notices.

## Included

- `visu` plugin
- `/visu:visu-haus` skill
- Visu.Haus connection configuration
- Local `.visu` builder for supported workflows

## Reviewer Notes

The plugin supports two delivery paths:

- **Local file:** creates a `.visu` file without using the Visu.Haus connection.
- **Account save:** uses the Visu.Haus connection to save directly to **My Visus**
  and return a saved link.

Only the account-save path requires signing in to Visu.Haus and authorizing the
connection. The local-file path can be tested without account authorization in
clients that allow local file creation.
