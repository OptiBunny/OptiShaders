# OptiShaders user guide

CRT-style shader presets for **ColecoVision in RetroArch**, using the **Gearcoleco** core.

**v10 · 63 presets · 9 looks · 720p to 4K**

[Download OptiShaders](https://github.com/OptiBunny/OptiShaders#readme)
· [Install](#install)
· [Choose a preset](#choose-a-preset)
· [Troubleshooting](#troubleshooting)

## Prerequisites

Before installing the pack, you need:

- **RetroArch** with a video driver that supports Slang shaders, such as **vulkan** or **glcore**.
- The **Gearcoleco** core, the **ColecoVision BIOS**, and a game.
- The **Slang shader collection**, installed through RetroArch's shader updater
  or downloaded manually.

These are installed separately. OptiShaders supplies complete presets adapted
from RetroCrisis and two custom shader stages; a separate RetroCrisis installation
is not required. The shared Guest shaders come from the Slang collection.

### Set the video driver

Open **Settings → Drivers → Video** and choose a Slang-compatible driver available
on your platform, such as **vulkan** or **glcore**. Fully restart RetroArch after
changing it.

The presets use `.slangp` files. They need a Slang-compatible driver to appear
and load correctly.

### Set up Gearcoleco

1. Install **Gearcoleco** through **Main Menu → Online Updater → Core Downloader**,
   or your platform's core-installation method.
2. Put **`colecovision.rom`** in the folder shown under
   **Settings → Directory → System/BIOS**. See the
   [Gearcoleco BIOS instructions](https://docs.libretro.com/library/gearcoleco/#bios).
3. Load a ColecoVision game with Gearcoleco and confirm it runs with shaders disabled.

### Install the shared shaders

Run **Main Menu → Online Updater → Update Slang Shaders** and let it finish.
This installs the shared Guest shaders and lookup images used by OptiShaders.

If the updater is unavailable, download the
[official Slang collection](https://github.com/libretro/slang-shaders) using
**Code → Download ZIP**. Extract its contents into your `shaders_slang/` directory.
The `crt/` folder must sit directly inside it, without an extra
`slang-shaders-master/` folder in between.

For more about RetroArch's shader setup, see the
[RetroArch shader guide](https://docs.libretro.com/guides/shaders/).

## Install

1. Download and extract **`OptiShaders-ColecoVision-Gearcoleco.zip`**.
2. Find your shader location under **Settings → Directory → Video Shader**.
   Open the Slang collection folder containing `crt/`, usually named `shaders_slang/`.
3. Copy the **`OptiShaders`** folder from the ZIP into that folder, alongside `crt/`.
   Keep all its subfolders together.

The installed layout should look like this:

```text
shaders_slang/
├── crt/                  # from the Slang shader collection
└── OptiShaders/           # copied from the OptiShaders ZIP
    ├── 720p Steam Deck/
    ├── 1080p Flat/
    ├── 1080p Curved/
    ├── 1440p Flat/
    ├── 1440p Curved/
    ├── 4K Flat/
    ├── 4K Curved/
    ├── shaders/
    ├── licenses/
    └── README.md
```

Use the **folder inside the download ZIP**. An extra level such as
`shaders_slang/OptiShaders/OptiShaders/` will break the shader paths.

## Set up the core and display

Start a game in Gearcoleco. Set **Overscan** and **Aspect Ratio** in its core
options, then apply the RetroArch video settings below.

| Setting | Value |
| --- | --- |
| Gearcoleco: Overscan | **Top+Bottom** |
| Gearcoleco: Aspect Ratio | **4:3 DAR** |
| RetroArch: Aspect Ratio | **Core Provided** |
| RetroArch: Integer Scale | **On** |
| RetroArch: Integer Scale Axis | **Y (vertical)** |
| Black Frame Insertion (BFI) | **Off** |
| Shader subframes | **Off** |

## Choose a preset

Choose the folder matching your **output resolution**, then **Flat** or
**Curved** where available.

| Output | Folder names |
| --- | --- |
| 720p | `720p Steam Deck` |
| 1080p | `1080p Flat` · `1080p Curved` |
| 1440p | `1440p Flat` · `1440p Curved` |
| 4K | `4K Flat` · `4K Curved` |

Every folder contains the same nine looks:

**Clean · Dirty · RGB · S-Video · Composite · RF · Badly Adjusted · RGB 100 · Composite 100**

- **RF** adds filtering and delay.
- **Badly Adjusted** adds a slight static picture skew.
- **RGB 100** and **Composite 100** use alternate CRT profiles.

Open **Quick Menu → Shaders**, turn **Video Shaders** on, and choose
**Load Shader Preset**. For example, the 1080p Flat Composite preset is:

```text
OptiShaders/1080p Flat/OptiShaders - ColecoVision - Composite.slangp
```

Signal effects target NTSC. Appearance and performance vary with the graphics
backend, display, and hardware. Keep SDR/HDR mode and display settings consistent
when comparing looks.

## Save your choice

After loading a preset, open **Quick Menu → Shaders**:

1. Make any changes under **Shader Parameters**.
2. Enable **Simple Presets**.
3. Choose **Save → Save Core Preset** to use this look with Gearcoleco.

For a different look in one game, load that game and the desired shader, then
choose **Save → Save Game Preset**. A game preset takes priority over the core preset.

Save again after making further parameter changes.

## Adjust the shader

Open **Quick Menu → Shaders → Shader Parameters** after loading a preset.
These controls adjust the custom signal effects and persistence:

| Control | Supplied setting | Adjustment |
| --- | --- | --- |
| **Coleco experimental board response** | RF: **0.5**; other encoded looks: **0** | Controls the added RF filtering and delay. Set to **0** to disable this effect. |
| **Coleco static picture skew (native pixels)** | Badly Adjusted: **0.5** | Set to **0** for straight picture geometry. |
| **Afterglow Strength** | Depends on the preset | Set to **0** to disable persistence. |

Leave **Coleco RGB geometry pass** at its supplied value: **0** for Clean/S-Video
and **1** for Badly Adjusted. It selects the operation rather than its strength.

[Save your preset](#save-your-choice) to keep the changes.

## Update an existing installation

1. Back up your own edits and saved core/game presets.
2. Install the new **`OptiShaders`** folder in your Slang shader directory.
3. Load a preset from the new folder, reapply your preferred settings, and save
   the core preset again. Repeat for any game presets.
4. Check that the new saves load correctly before removing an older installation.

Saved presets can refer to the original files by path. If you rename or move
the pack, load a preset from its new location and save it again.

When moving or backing up RetroArch, keep the pack, shared shader collection,
and saved presets together.

## Troubleshooting

| Problem | What to check |
| --- | --- |
| A `.slangp` preset is missing from the file picker | [Choose a Slang-compatible video driver](#set-the-video-driver), then restart RetroArch. |
| A preset reports a missing shader or lookup image (LUT) | [Update the shared Slang shaders](#install-the-shared-shaders) and check the [folder layout](#install). Keep both custom stages in `OptiShaders/shaders/`. |
| Gearcoleco will not start the game | Test with shaders disabled. Check `colecovision.rom` and the configured **System/BIOS** directory. |
| A saved preset fails after an update or move | Load a supplied preset from its new location and save it again. |
| One game uses the wrong look | Check its saved game preset; it takes priority over the core preset. |
| The picture is stretched or sized incorrectly | Check the [core and display settings](#set-up-the-core-and-display) and choose the folder matching your output resolution. |
| Moving objects leave an afterglow you want to turn off | Set **Afterglow Strength** to **0**, then save the preset. |

For missing-file errors, shared dependencies belong under
`crt/shaders/guest/advanced/` and `crt/shaders/guest/hd/`, with lookup images in
`advanced/lut/`. The included custom stages are
`OptiShaders/shaders/optishaders-colecovision-ntsc-pass1.slang` and
`OptiShaders/shaders/optishaders-colecovision-yc-pass1.slang`.

## Credits and licenses

Presets are adapted from
[RetroCrisis](https://github.com/RetroCrisis/Retro-Crisis-GDV-NTSC). Shared CRT
shaders are by guest(r), Dr. Venom, and contributors, distributed through
[libretro's Slang collection](https://github.com/libretro/slang-shaders).

Keep the supplied license notices with the pack:

[Custom stages — MIT](licenses/Coleco-NTSC-MIT.txt) ·
[RetroCrisis — GPL-3.0](licenses/RetroCrisis-GPL-3.0.txt) ·
[Guest — GPL-2.0](licenses/Guest-GPL-2.0.txt)
