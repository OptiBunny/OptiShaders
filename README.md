# OptiShaders

CRT-style shader presets for ColecoVision in RetroArch using the **Gearcoleco** core. The **v10** pack includes 63 presets: nine looks across seven resolution and screen-shape folders.

[Download OptiShaders (v10)](downloads/OptiShaders-ColecoVision-Gearcoleco.zip?raw=true) · [Browse the presets](OptiShaders/) · [Pack guide](OptiShaders/README.md)

## Install

You need RetroArch, the Gearcoleco core, and RetroArch's Slang shader collection, including its shared Guest shaders and lookup images (LUTs).

1. Download and extract the ZIP.
2. Copy **OptiShaders** into `RetroArch/shaders/shaders_slang/`. Keep the folder structure and both files in `OptiShaders/shaders/` intact.
3. In Gearcoleco, set **Overscan: Top+Bottom** and **Aspect Ratio: 4:3 DAR**.
4. In RetroArch, select **Core Provided** aspect ratio and enable vertical/Y integer scaling.
5. Load a game, then choose a preset through **Quick Menu → Shaders → Load Shader Preset**.
6. To keep it for the core, load the supplied preset, make any parameter adjustments, enable **Simple Presets**, and choose **Save → Save Core Preset**. A saved game preset can override the core preset.

When updating, back up your edits and install the new **OptiShaders** folder. Load a renamed preset and resave any core or game presets: saved presets that point to an older folder or filename need their references updated before you remove that older installation. Keep the shared shader collection and saved presets together when moving or backing up your installation.

## Choose a preset

Choose the folder matching your output resolution and preferred screen shape:

| Output resolution | Folders |
| --- | --- |
| 720p | Steam Deck |
| 1080p | Flat, Curved |
| 1440p | Flat, Curved |
| 4K | Flat, Curved |

Each folder includes **Clean, Dirty, RGB, S-Video, Composite, RF, Badly Adjusted, RGB 100, and Composite 100**.

Preset filenames use `OptiShaders - ColecoVision - <look>.slangp`.

Signal effects target **NTSC**. RF adds filtering and delay; Badly Adjusted adds a slight static picture skew. RGB 100 and Composite 100 use alternate CRT profiles.

Keep **BFI** and **shader subframes** disabled for this setup. Set **Afterglow Strength** to zero to disable persistence. Appearance and performance can vary with the graphics backend, display, and hardware.

See the [pack guide](OptiShaders/README.md) for shader controls and setup details.

## Download checksum

SHA-256 for `OptiShaders-ColecoVision-Gearcoleco.zip`:

```text
56cd83fec03209be5be74be9d0d85724ba5b879ff198ea0e416cb4f928caf93d
```

## Credits and licenses

Presets are adapted from [RetroCrisis](https://github.com/RetroCrisis/Retro-Crisis-GDV-NTSC). Shared CRT shaders are by guest(r), Dr. Venom, and contributors, distributed through [libretro's Slang shaders](https://github.com/libretro/slang-shaders).

Keep the supplied license notices with the pack:

- [ColecoVision custom stages — MIT](OptiShaders/licenses/Coleco-NTSC-MIT.txt)
- [RetroCrisis — GPL-3.0](OptiShaders/licenses/RetroCrisis-GPL-3.0.txt)
- [Guest — GPL-2.0](OptiShaders/licenses/Guest-GPL-2.0.txt)
