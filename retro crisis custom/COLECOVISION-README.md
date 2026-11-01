# ColecoVision shaders for Gearcoleco — v10

Nine NTSC looks across seven resolution and screen-shape folders, with 63 presets in total.

## Install

1. Copy **retro crisis custom** into `RetroArch/shaders/shaders_slang/`.
2. Keep both files in its **shaders** folder. The presets also need the shared Guest shaders and lookup images (LUTs) from RetroArch's Slang shader collection.
3. Load a game in Gearcoleco, then choose a preset through **Quick Menu → Shaders → Load Shader Preset**.
4. To save it for the core, load the supplied preset, adjust its parameters if needed, enable **Simple Presets**, and choose **Save → Save Core Preset**. A saved game preset can override the core preset.

When updating, back up your edits before replacing the previous custom folder. Load the supplied preset again before saving it. Keep shared shader dependencies with your installation when moving or backing it up.

## Core and display settings

- Gearcoleco: **Overscan: Top+Bottom** and **Aspect Ratio: 4:3 DAR**.
- RetroArch: **Core Provided** aspect ratio and vertical/Y integer scaling.
- Keep **BFI** and **shader subframes** disabled.
- Use the folder matching your output resolution. A 240-line input fits 4K at 9×; at 1080p, integer scaling uses a 960-line-high game viewport.

| Output resolution | Folders |
| --- | --- |
| 720p | Steam Deck |
| 1080p | Flat, Curved |
| 1440p | Flat, Curved |
| 4K | Flat, Curved |

## Looks and controls

Every folder includes **Clean, Dirty, RGB, S-Video, Composite, RF, Badly Adjusted, RGB 100, and Composite 100**. RGB 100 and Composite 100 use alternate CRT profiles.

RF adds filtering and delay. Badly Adjusted adds a small static picture skew while keeping the screen mask fixed.

| Shader control | Default | Adjustment |
| --- | --- | --- |
| Coleco experimental board response | RF: 0.5; other encoded looks: 0 | Set to 0 to disable this RF effect; increase for a stronger effect. |
| Coleco static picture skew (native pixels) | Badly Adjusted: 0.5 | Set to 0 for straight picture geometry. |
| Afterglow Strength | Preset-dependent | Set to 0 to disable persistence. |

Leave **Coleco RGB geometry pass** at its supplied value: Clean/S-Video use 0 and Badly Adjusted uses 1. It selects the operation rather than its strength.

Keep SDR/HDR mode and display settings consistent when comparing looks. Appearance and performance can vary with the graphics backend, display, and hardware.

## Credits and licenses

Presets are adapted from [RetroCrisis](https://github.com/RetroCrisis/Retro-Crisis-GDV-NTSC). Shared CRT shaders are by guest(r), Dr. Venom, and contributors, distributed through [libretro's Slang shaders](https://github.com/libretro/slang-shaders).

The pack includes 63 presets, two custom shader stages, this guide, and three license files. Keep the supplied notices:

- [ColecoVision custom stages — MIT](licenses/Coleco-NTSC-MIT.txt)
- [RetroCrisis — GPL-3.0](licenses/RetroCrisis-GPL-3.0.txt)
- [Guest — GPL-2.0](licenses/Guest-GPL-2.0.txt)
