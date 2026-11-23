# OptiShaders user guide

CRT-style shader presets for **ColecoVision in RetroArch**, using the **Gearcoleco** core.

**v10.9 · 63 presets · 9 looks · 720p to 4K**

[Download OptiShaders](https://github.com/OptiBunny/OptiShaders#readme)
· [Install](#install)
· [Choose a preset](#choose-a-preset)
· [Troubleshooting](#troubleshooting)

## What's new in v10.9

- Prevents repeated frames in animated **Add Noise** when the frame counter
  becomes large. This affects positive noise amounts in both **Colored** and
  **Luma** modes. Negative amounts keep their fixed pattern, and all supplied
  presets still leave this optional effect at **0**.

The pack also includes these earlier fixes:

- Keeps the mask-width table lookup in range when **CRT Mask** is disabled
  (value **-1**), including all nine supplied Steam Deck presets. The disabled
  mask control and all enabled mask selections retain their behavior.

- Keeps bloom and positive halation calculations defined at high custom
  **Bright Boost Dark Pixels** or **Bright Boost Bright Pixels** settings.
  Negative light contributions are bounded at zero before gamma conversion.
  The supplied presets and their default settings are unchanged.

- Prevents bright corner artefacts and undefined pixels when custom vertical
  shift or negative overscan settings move the picture away from the viewport
  edges. Supplied preset settings are unchanged.

- Keeps the complete image visible when shader **Integer Scaling** is **1** or
  **2** and the viewport becomes shorter than the game image. Both affected
  stages now use fractional scaling in that case, avoiding undefined sampling.
  All supplied presets use **0**, which is unchanged.

- Fixes horizontal cropping when **Speedup w. higher Internal Res.** is set to
  **2**, **3**, or **4** in the seven looks that use signal encoding. Previously,
  setting it to **2**, for example, stretched the left half across the screen.
  All supplied presets use **1**. The **RGB** and **RGB 100** looks bypass encoding.

This version includes the earlier corrections to scanline rendering and
horizontal filtering, including **Sharpness Definition** at **0**. For an
existing installation, follow the [update steps](#update-an-existing-installation).

## Prerequisites

Before installing the pack, you need:

- **RetroArch** with a video driver that supports Slang shaders, such as **vulkan** or **glcore**.
- The **Gearcoleco** core, the **ColecoVision BIOS**, and a game.
- The **Slang shader collection**, installed through RetroArch's shader updater
  or downloaded manually.

These are installed separately. OptiShaders supplies complete presets adapted
from RetroCrisis and five shader stages: two custom signal stages and modified
Guest horizontal-filter, scanline and deconvergence stages. A separate RetroCrisis installation
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

With the 240-line setup above, expect these 4:3 game viewports at each output size:

| Output | Folder names | Game viewport |
| --- | --- | --- |
| 720p | `720p Steam Deck` | 960 × 720 |
| 1080p | `1080p Flat` · `1080p Curved` | 1280 × 960 |
| 1440p | `1440p Flat` · `1440p Curved` | 1920 × 1440 |
| 4K (2160p) | `4K Flat` · `4K Curved` | 2880 × 2160 |

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
**Load Preset**. For example, the 1080p Flat Composite preset is:

```text
OptiShaders/1080p Flat/OptiShaders - ColecoVision - Composite.slangp
```

Signal effects target NTSC. Appearance and performance vary with the graphics
backend, display, and hardware. Keep SDR/HDR mode and display settings consistent
when comparing looks.

## Save your choice

After loading a preset, open **Quick Menu → Shaders**:

1. Make any changes under **Shader Parameters**.
2. Open **Manage Presets** and turn **Simple Presets** on.
3. Choose **Save Core Preset** to use this look with Gearcoleco.

For a different look in one game, load that game and the desired shader, then
choose **Manage Presets → Save Game Preset**.

Automatic presets load in this order of priority: **Game → Content Directory →
Core → Global**. If a game or folder keeps loading a different look, open **Manage
Presets** while that game is running. **Remove Game Preset** and **Remove Content
Directory Preset** appear when the corresponding override exists. Remove only
the override you no longer want.

RetroArch 1.21 uses separate **Save Preset** and **Remove Preset** menus for these
actions. RetroArch 1.22.2 groups them under **Manage Presets**.

Save again after making further parameter changes.

Simple Presets keep parameter changes while referencing the supplied preset.
Changing the shader chain makes RetroArch save a full preset even when **Simple
Presets** is on. Keep that full preset separately and review its stage references
when updating; reloading a supplied preset does not retain custom chain edits.
See [RetroArch's preset guidance](https://docs.libretro.com/guides/shaders/#simple-presets-vs-full-presets).

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

The shader's **Integer Scaling: Odd:Y, Even:'X'+Y** control is separate from
RetroArch's integer-scaling setting. Values **1** and **2** fit whole multiples
of the game's native height; when even one multiple is too tall, they use a
fractional fit to keep the complete picture. Values **3** and **4** keep their
overscale behavior and may crop. The supplied value of **0** disables this
additional shader scaling.

[Save your preset](#save-your-choice) to keep the changes.

## Update an existing installation

1. Back up your edited pack files and saved OptiShaders presets, including core,
   content-directory and game presets. Include a global preset if it uses OptiShaders.
2. Copy the new **`OptiShaders`** folder into the same Slang shader directory,
   replacing the supplied preset and shader files. Keep the included license notices.
3. For each saved OptiShaders look, load the matching preset from the new folder,
   reapply your parameter changes, turn **Simple Presets** on, and save at its
   original scope: **Core**, **Content Directory**, **Game** or **Global**.
   Review any [custom shader-chain edits](#save-your-choice) separately.
4. Reload the affected games and check that their saved looks load correctly
   before removing an older installation.

Automatic shader presets normally live in RetroArch's configuration directory.
Files saved with **Save Preset As** normally use the configured **Video
Shader** directory; include those in your backup if you use them. See
[RetroArch's preset storage guidance](https://docs.libretro.com/guides/shaders/#shader-presets).

The v10.6 update includes the earlier fixes and needs the supplied presets and
all five files in the bundled `shaders/` folder. Updating the shared Slang collection alone does not install
these fixes. Older full saved presets may still point to the shared horizontal
filter, scanline or deconvergence stage; reload a supplied preset, enable **Simple Presets**,
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
- `OptiShaders/shaders/optishaders-guest-deconvergence-ntsc.slang`

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

The three bundled Guest stages include OptiShaders changes for scanline
boundaries, extreme scanline settings, zero horizontal-filter weight sums,
**Sharpness Definition** set to **0**, integer scaling in small viewports,
bloom/halation power inputs at high brightness boosts, disabled-mask table
lookup bounds, and animated-noise phase precision at large frame counters.
They retain their upstream copyright notices and GPL-2.0-or-later license. The
two custom signal stages use the supplied MIT license.

Keep the supplied license notices with the pack:

[Custom signal stages — MIT](licenses/Coleco-NTSC-MIT.txt) ·
[RetroCrisis — GPL-3.0](licenses/RetroCrisis-GPL-3.0.txt) ·
[Guest stages — GPL-2.0-or-later](licenses/Guest-GPL-2.0.txt)
