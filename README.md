# OptiShaders

CRT-style shader presets for ColecoVision in RetroArch using the **Gearcoleco** core. The **v10** pack includes 63 presets: nine looks across seven resolution and screen-shape folders.

[Download the v10 ZIP](downloads/RetroCrisis-ColecoVision-Gearcoleco.zip?raw=true) · [Browse the presets](retro%20crisis%20custom/) · [Pack guide](retro%20crisis%20custom/COLECOVISION-README.md)

## Install

You need RetroArch, the Gearcoleco core, and RetroArch's Slang shader collection, including its shared Guest shaders and lookup images (LUTs).

1. Download and extract the ZIP.
2. Copy **retro crisis custom** into `RetroArch/shaders/shaders_slang/`. Keep the folder structure and both files in `retro crisis custom/shaders/` intact.
3. In Gearcoleco, set **Overscan: Top+Bottom** and **Aspect Ratio: 4:3 DAR**.
4. In RetroArch, select **Core Provided** aspect ratio and enable vertical/Y integer scaling.
5. Load a game, then choose a preset through **Quick Menu → Shaders → Load Shader Preset**.
6. To keep it for the core, load the supplied preset, make any parameter adjustments, enable **Simple Presets**, and choose **Save → Save Core Preset**. A saved game preset can override the core preset.

When updating, back up your own edits before replacing the old custom folder. Keep the shared shader collection and saved presets together when moving or backing up your installation.

## Choose a preset

Choose the folder matching your output resolution and preferred screen shape:

| Output resolution | Folders |
| --- | --- |
| 720p | Steam Deck |
| 1080p | Flat, Curved |
| 1440p | Flat, Curved |
| 4K | Flat, Curved |

Each folder includes **Clean, Dirty, RGB, S-Video, Composite, RF, Badly Adjusted, RGB 100, and Composite 100**.

Signal effects target **NTSC**. RF adds filtering and delay; Badly Adjusted adds a slight static picture skew. RGB 100 and Composite 100 use alternate CRT profiles.

Keep **BFI** and **shader subframes** disabled for this setup. Set **Afterglow Strength** to zero to disable persistence. Appearance and performance can vary with the graphics backend, display, and hardware.

See the [pack guide](retro%20crisis%20custom/COLECOVISION-README.md) for shader controls and setup details.

## Download checksum

SHA-256 for `RetroCrisis-ColecoVision-Gearcoleco.zip`:

```text
a05562c6073e815311b81a9ad6e6828f588fc49c6da56d1518ecce9e65679d0b
```

## Credits and licenses

Presets are adapted from [RetroCrisis](https://github.com/RetroCrisis/Retro-Crisis-GDV-NTSC). Shared CRT shaders are by guest(r), Dr. Venom, and contributors, distributed through [libretro's Slang shaders](https://github.com/libretro/slang-shaders).

Keep the supplied license notices with the pack:

- [ColecoVision custom stages — MIT](retro%20crisis%20custom/licenses/Coleco-NTSC-MIT.txt)
- [RetroCrisis — GPL-3.0](retro%20crisis%20custom/licenses/RetroCrisis-GPL-3.0.txt)
- [Guest — GPL-2.0](retro%20crisis%20custom/licenses/Guest-GPL-2.0.txt)
