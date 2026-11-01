# OptiShaders

CRT-style shaders for **ColecoVision** in RetroArch using the **Gearcoleco** core.

**v10 · 63 presets · 9 looks · 720p to 4K**

**[Download OptiShaders](downloads/OptiShaders-ColecoVision-Gearcoleco.zip?raw=true)** · [Detailed pack guide](OptiShaders/README.md) · [Browse presets](OptiShaders/)

## Prerequisites

**A separate RetroCrisis installation is not required.** OptiShaders includes complete presets adapted from RetroCrisis. They use two custom stages included in this ZIP and shared Guest shaders from RetroArch's Slang collection.

Set up these three requirements first:

1. **RetroArch with a Slang-compatible video driver.** Under **Settings → Drivers → Video**, select a supported driver such as **vulkan** or **glcore**, then fully restart RetroArch after changing it. These presets use `.slangp`; a GLSL-only driver cannot load them. Driver availability depends on your platform.
2. **Gearcoleco, its BIOS and a game.** Install the **Gearcoleco** core through **Main Menu → Online Updater → Core Downloader**, or your platform's core-installation method. Put `colecovision.rom` in the folder shown under **Settings → Directory → System/BIOS**. Confirm that a ColecoVision game runs with shaders disabled before continuing. See the [Gearcoleco BIOS instructions](https://docs.libretro.com/library/gearcoleco/#bios). The core, BIOS and games are not included in OptiShaders.
3. **RetroArch's shared Slang shaders.** Run **Main Menu → Online Updater → Update Slang Shaders** and let it finish. This supplies the Guest Advanced/HD shader files and lookup images (LUTs) referenced by the presets. They are not included in the OptiShaders ZIP. See [RetroArch's shader guide](https://docs.libretro.com/guides/shaders/).

If **Update Slang Shaders** is unavailable, download the [official Slang collection](https://github.com/libretro/slang-shaders) using **Code → Download ZIP**. Extract its contents into your `shaders_slang` directory so `crt/` sits directly inside it; do not leave an extra `slang-shaders-master/` folder between them.

## Install

Find your shader location under **Settings → Directory → Video Shader**. The examples below use `RetroArch/shaders/shaders_slang/`; the actual location can differ by installation. Use the Slang collection folder containing `crt/` as the destination.

1. Download and extract `OptiShaders-ColecoVision-Gearcoleco.zip`.
2. Copy its **OptiShaders** folder into that `shaders_slang/` directory, alongside `crt/`.
3. Keep all supplied folders and both custom shader files together.
4. Load a game in Gearcoleco. Open **Quick Menu → Shaders**, turn **Video Shaders** on, then choose **Load Shader Preset** and select a preset from the folder for your resolution.

The installed layout should look like this:

```text
shaders_slang/
├── crt/                  # installed by Update Slang Shaders
│   └── shaders/guest/     # advanced/, hd/ and LUT files
└── OptiShaders/
    ├── 1080p Flat/        # one of the seven preset folders
    ├── ...
    ├── shaders/          # both included custom stages
    └── licenses/
```

Copy the folder **inside the ZIP**, rather than the entire repository. Avoid nesting it as `OptiShaders/OptiShaders/` inside `shaders_slang/`.

## Set up the core and display

| Setting | Value |
| --- | --- |
| Gearcoleco: Overscan | **Top+Bottom** |
| Gearcoleco: Aspect Ratio | **4:3 DAR** |
| RetroArch: Aspect Ratio | **Core Provided** |
| RetroArch: Integer Scale | **On** |
| RetroArch: Integer Scale Axis | **Y (vertical)** |
| BFI | **Off** |
| Shader subframes | **Off** |

## Choose a preset

First choose your **output resolution**, then **Flat** or **Curved** where available.

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

Preset names follow `OptiShaders - ColecoVision - <look>.slangp`. For example, the 1080p Flat Composite preset is:

```text
OptiShaders/1080p Flat/OptiShaders - ColecoVision - Composite.slangp
```

Signal effects target NTSC. Appearance and performance can vary with the graphics backend, display, and hardware.

## Save your choice

1. Load the supplied preset you want to use.
2. Make any changes under **Shader Parameters**.
3. Enable **Simple Presets**.
4. Choose **Save → Save Core Preset** to use it with Gearcoleco.

A saved game preset can override the core preset. If one game keeps loading a different look, check its saved preset too.

## Update an existing installation

1. Back up your own edits and saved core/game presets.
2. Install the new **OptiShaders** folder.
3. Load a preset from that folder, reapply your preferred settings, and save the core preset again. Repeat for any game-specific presets.
4. Check that the new saves load correctly before removing an older installation.

**Renaming a folder does not update saved preset references.**

When moving or backing up RetroArch, keep the pack, shared shader collection, and saved presets together.

## Troubleshooting

| Problem | What to check |
| --- | --- |
| A `.slangp` preset is missing from the file picker | Check the video driver. Choose a supported Slang driver such as **vulkan** or **glcore**, then restart RetroArch. |
| A preset reports a missing shader or LUT | Run **Update Slang Shaders** and check the layout above. Keep both included custom stages in `OptiShaders/shaders/`. Shared dependencies belong in `crt/shaders/guest/advanced/` and `crt/shaders/guest/hd/`, including the `advanced/lut/` images. |
| Gearcoleco will not start the game | Test with shaders disabled and check the required BIOS filename and **System/BIOS** directory. Shader files cannot replace the core or BIOS. |
| An old save fails after an update | Load a renamed preset from the new pack and resave it. The saved reference may still point to an old path. |
| One game uses the wrong look | A game preset may be overriding the core preset. |
| The picture is stretched or sized incorrectly | Recheck the core/display settings and select the folder matching your output resolution. |
| You want to disable persistence | Set **Afterglow Strength** to **0**, then save your preset. |

For custom shader controls and a full file overview, see the [pack guide](OptiShaders/README.md).

## Download checksum

SHA-256 for `OptiShaders-ColecoVision-Gearcoleco.zip`:

```text
012389ef8a22a44a6878eb5935cddba23b6b1c617b4fbf49757f532f8796e59c
```

## Credits and licenses

Presets are adapted from [RetroCrisis](https://github.com/RetroCrisis/Retro-Crisis-GDV-NTSC). Shared CRT shaders are by guest(r), Dr. Venom, and contributors, distributed through [libretro's Slang shaders](https://github.com/libretro/slang-shaders).

Keep the supplied license notices with the pack:

- [ColecoVision custom stages — MIT](OptiShaders/licenses/Coleco-NTSC-MIT.txt)
- [RetroCrisis — GPL-3.0](OptiShaders/licenses/RetroCrisis-GPL-3.0.txt)
- [Guest — GPL-2.0](OptiShaders/licenses/Guest-GPL-2.0.txt)
