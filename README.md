# Visu.Haus Plugins

Create interactive Visu.Haus visuals directly from your AI workspace.

This marketplace installs the Visu.Haus plugin and the `/visu:create-visu`
skill. Use it to turn a prompt, image reference, brand direction, shader idea,
or motion concept into a polished `.visu` visual.

When your Visu.Haus connection is active, new visus are saved directly to
**My Visus** and you get a ready-to-open link. If the connection is not active
in the current client, supported local workflows can create a `.visu` file for
manual upload.

## Install

Open your plugin settings, choose **Add marketplace**, and add:

```text
Visu-Haus/Visu-Plugins
```

Then install and enable the **visu** plugin.

## Create A Visu

Start with:

```text
/visu:create-visu
```

Then describe what you want to make:

```text
/visu:create-visu
Create a slow liquid chrome flower with soft orbiting particles, pointer
interaction, and controls for bloom, density, color, and motion speed.
```

You can also attach images or describe a product, campaign, logo, texture,
gallery, video shader, audio-reactive visual, or typography system.

## What Happens Next

The plugin checks your Visu.Haus connection first.

If connected:

- your visu is created;
- it is saved directly to **My Visus**;
- you receive a Visu.Haus link.

If not connected:

- the plugin asks you to connect Visu.Haus before continuing;
- if connection is not available, it can create a local `.visu` file in
  supported clients;
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
- Local file support only if you want `.visu` fallback files.


