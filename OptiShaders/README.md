# OptiShaders user guide

CRT-style shader presets for **ColecoVision in RetroArch**, using the **Gearcoleco** core.

**v10.2 · 63 presets · 9 looks · 720p to 4K**

[Download OptiShaders](https://github.com/OptiBunny/OptiShaders#readme)
· [Install](#install)
· [Choose a preset](#choose-a-preset)
· [Troubleshooting](#troubleshooting)

## What's new in v10.2

- Prevents washed-out output from extreme scanline adjustments.
- Prevents dark vertical lines from certain horizontal-filter adjustments.

The supplied preset settings are unchanged, and the earlier scanline-boundary
fix is retained. For an existing installation, follow the
[update steps](#update-an-existing-installation).

## Prerequisites

Before installing the pack, you need:

- **RetroArch** with a video driver that supports Slang shaders, such as **vulkan** or **glcore**.
- The **Gearcoleco** core, the **ColecoVision BIOS**, and a game.
- The **Slang shader collection**, installed through RetroArch's shader updater
  or downloaded manually.

These are installed separately. OptiShaders supplies complete presets adapted
from RetroCrisis and four shader stages: two custom signal stages and modified
Guest horizontal-filter and scanline stages. A separate RetroCrisis installation
is not required. The remaining shared Guest shaders and lookup images come from
the Slang collection.

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

These settings target standard NTSC ColecoVision video in Gearcoleco. Start a
game and open **Quick Menu → Core Options** for the Gearcoleco settings below;
some core versions group them under **System** and **Video**.

Open **Settings → Video → Scaling** for RetroArch's aspect ratio and integer
scaling. **Black Frame Insertion** and **Shader Sub-frames** are under
**Settings → Video → Synchronization**.

| Setting | Value |
| --- | --- |
| Gearcoleco: Refresh Rate (restart) | **NTSC (60 Hz)** |
| Gearcoleco: Video Chip (restart), if available | **TMS9918A** |
| Gearcoleco: Overscan | **Top+Bottom** |
| Gearcoleco: Aspect Ratio | **4:3 DAR** |
| RetroArch: Aspect Ratio | **Core Provided** |
| RetroArch: Integer Scale | **On** |
| RetroArch: Integer Scale Axis | **Y (vertical)** |
| RetroArch: Integer Scale Scaling | **Underscale** |
| Black Frame Insertion (BFI) | **Off** |
| Shader Sub-frames | **Off** |

Close and reload the game after changing a setting marked **(restart)**.
For games that require PAL timing or F18A, keep the settings they need; the
240-line setup below describes Gearcoleco's NTSC/TMS output.

Use the core's native output without an additional software video filter. If one
is selected, choose **Settings → Video → Remove Video Filter**.

With NTSC timing, the **TMS9918A** core option, and **Top+Bottom** overscan,
Gearcoleco outputs 240 lines. **Underscale** fits whole multiples of those lines
inside the display without cropping. At 1080p,
this gives a **1280 × 960** game viewport, so borders are expected. Use the
**1080p** preset folder even though the game viewport is 960 pixels high.

## Choose a preset

Choose the folder matching **RetroArch's output resolution**, then **Flat** or
**Curved** where available. The output resolution can differ from your display's
native resolution.

| Output | Folder names |
| --- | --- |
| 720p | `720p Steam Deck` |
| 1080p | `1080p Flat` · `1080p Curved` |
| 1440p | `1440p Flat` · `1440p Curved` |
| 4K | `4K Flat` · `4K Curved` |

On Steam Deck's built-in **1280 × 800** screen, use **`720p Steam Deck`**.
With the core and display settings above, the game viewport is **960 × 720**,
so borders are expected.

Every folder contains the same nine looks:

| Look | What to expect |
| --- | --- |
| **Clean** | Light filtering with clear detail and separated colour edges. |
| **Dirty** | More analogue texture and colour fringing than Clean. |
| **RGB** | Bypasses NTSC signal filtering while retaining CRT effects. |
| **S-Video** | Separates brightness and colour, with softer colour detail than RGB. |
| **Composite** | Colour bleed, fringing, and moderate softness. |
| **RF** | Extra filtering and delay, with subtle signal noise. |
| **Badly Adjusted** | Stronger colour artifacts, a warmer picture, and slight static skew. |
| **RGB 100** | RGB signal treatment with a distinct RetroCrisis 100 CRT profile. |
| **Composite 100** | Composite signal treatment with a distinct RetroCrisis 100 CRT profile. |

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
2. Open **Save** and turn **Simple Presets** on.
3. Choose **Save Core Preset** to use this look with Gearcoleco.

For a different look in one game, load that game and the desired shader, then
choose **Save → Save Game Preset**.

Automatic presets load in this order of priority: **Game → Content Directory →
Core → Global**. If a game or folder keeps loading a different look, open **Save**
and check **Remove Game Preset** or **Remove Content Directory Preset**. Remove
only the saved override you no longer want.

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
2. Copy the new **`OptiShaders`** folder into the same Slang shader directory,
   replacing the supplied preset and shader files. Keep the included license notices.
3. Load a preset from the new folder, reapply your preferred settings, and save
   the core preset again. Repeat for any game presets.
4. Check that the new saves load correctly before removing an older installation.

The v10.2 fixes need the new presets and all four files in the bundled
`shaders/` folder. Updating the shared Slang collection alone does not install
these fixes. Older full saved presets may still point to the shared horizontal
filter or scanline stage; reload a supplied preset, enable **Simple Presets**,
and save it again.

Saved presets can refer to the original files by path. If you rename or move
the pack, load a preset from its new location and save it again.

When moving or backing up RetroArch, keep the pack, shared shader collection,
and saved presets together.

## Troubleshooting

| Problem | What to check |
| --- | --- |
| A `.slangp` preset is missing from the file picker | [Choose a Slang-compatible video driver](#set-the-video-driver), then restart RetroArch. |
| A preset reports a missing shader or lookup image (LUT) | [Update the shared Slang shaders](#install-the-shared-shaders) and check the [folder layout](#install). Keep all files in `OptiShaders/shaders/` together. |
| Gearcoleco will not start the game | Test with shaders disabled. Check `colecovision.rom` and the configured **System/BIOS** directory. |
| A saved preset fails after an update or move | Load a supplied preset from its new location and save it again. |
| A saved preset stalls when a game starts, but loads manually | Try an [automatic shader delay](#saved-preset-stalls-at-startup). |
| One game or folder uses the wrong look | Check its saved game or content-directory preset; either can override the core preset. See [saving and overrides](#save-your-choice). |
| The picture is stretched or sized incorrectly | Check the [core and display settings](#set-up-the-core-and-display) and choose the folder matching your output resolution. |
| There are borders above and below the image at 1080p | This is expected with the recommended **Underscale** setting: the 240-line source fits at 960 pixels high. |
| Moving objects leave an afterglow you want to turn off | Set **Afterglow Strength** to **0**, then save the preset. |

For missing-file errors, shared dependencies belong under
`crt/shaders/guest/advanced/` and `crt/shaders/guest/hd/`, with lookup images in
`advanced/lut/`. The included stages are:

- `OptiShaders/shaders/optishaders-colecovision-ntsc-pass1.slang`
- `OptiShaders/shaders/optishaders-colecovision-yc-pass1.slang`
- `OptiShaders/shaders/optishaders-guest-ntsc-pass1.slang`
- `OptiShaders/shaders/optishaders-guest-ntsc-pass2.slang`

### Saved preset stalls at startup

If a preset works when loaded after the game starts but stalls when loaded
automatically, try a short delay:

1. Start RetroArch without loading a game.
2. Enable **Settings → User Interface → Show Advanced Settings**.
3. Set **Settings → Video → Auto-Shader Delay** to **100 ms**.
4. Load the game again. Save your RetroArch configuration to keep the setting.

This can give the core time to initialize before RetroArch applies the saved shader.

## Credits and licenses

Presets are adapted from
[RetroCrisis](https://github.com/RetroCrisis/Retro-Crisis-GDV-NTSC). Shared CRT
shaders are by guest(r), Dr. Venom, and contributors, distributed through
[libretro's Slang collection](https://github.com/libretro/slang-shaders).

The two bundled Guest stages include OptiShaders changes for scanline
boundaries, extreme scanline settings, and zero horizontal-filter weight sums.
They retain their upstream copyright notices and GPL-2.0-or-later license. The
two custom signal stages use the supplied MIT license.

Keep the supplied license notices with the pack:

[Custom signal stages — MIT](licenses/Coleco-NTSC-MIT.txt) ·
[RetroCrisis — GPL-3.0](licenses/RetroCrisis-GPL-3.0.txt) ·
[Guest stages — GPL-2.0-or-later](licenses/Guest-GPL-2.0.txt)
