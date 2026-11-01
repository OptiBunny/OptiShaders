# OptiShaders

Custom RetroArch shader presets and their installable source. The current pack is **ColecoVision for Gearcoleco, v10**: nine looks across seven resolution/geometry folders, with 63 presets and two custom shader stages.

[Download the v10 installer ZIP](downloads/RetroCrisis-ColecoVision-Gearcoleco.zip?raw=true) · [Browse the shaders](retro%20crisis%20custom/)

This repository publishes the v10 pack, dated 30 September 2026. The public ZIP includes a documentation-only privacy edit; its presets and shader stages are unchanged from v10. This is not a new shader release.

## Install

1. Download the installer ZIP above and extract it.
2. Put its **retro crisis custom** folder inside `RetroArch/shaders/shaders_slang/`, beside `retro crisis` if that folder is present. Keep the internal folder names and layout intact.
3. Keep both included files in `retro crisis custom/shaders/`. The presets also require the normal shared Guest shaders and LUTs from RetroArch's Slang shader collection.
4. In Gearcoleco, set **Overscan: Top+Bottom** and **Aspect Ratio: 4:3 DAR**. In RetroArch, use **Core Provided** aspect ratio and vertical/Y integer scaling.
5. Load a game, then use **Quick Menu → Shaders → Load Shader Preset** to select a supplied preset.
6. To save it for the core, first load the original supplied preset, apply any personal parameter changes, enable **Simple Presets**, and use **Save → Save Core Preset**. A game preset can take precedence over the core preset.

Before replacing an older installation, back up personal edits. Replacing the old custom folder avoids leaving obsolete files behind. Keep the shader collection and saved core presets together when backing up or moving an installation; these presets reference shared dependencies.

The ZIP contains the same 69 installable files as the `retro crisis custom/` directory in this repository: 63 presets, two custom stages, one README and three license files.

**Installer SHA-256:**

```text
b4b74e4baa74b6bdcdb6a76bcda2f255c87dc2f713e7f71a03913f4e56f5721e
```

## Choose a look

Every folder provides **Clean, Dirty, RGB, S-Video, Composite, RF, Badly Adjusted, RGB 100, and Composite 100**.

| Output | Available folders |
| --- | --- |
| 720p | Steam Deck |
| 1080p | Flat, Curved |
| 1440p | Flat, Curved |
| 4K | Flat, Curved |

Signal simulations target **NTSC**. The two 100 variants preserve their distinct reference CRT profiles; their names do not certify measured ColecoVision or television matching. RF includes a restrained circuit-informed board-response approximation, and Badly Adjusted adds static picture skew. See the [included pack guide](retro%20crisis%20custom/COLECOVISION-README.md) for controls and setup details.

Keep BFI and shader subframes disabled for this setup. Set **Afterglow Strength** to zero if persistence is unwanted. Keep SDR/HDR mode and display settings fixed when comparing looks. Software screenshots cannot establish physical screen brightness or HDR accuracy.

## Limitations

Rendering can differ across graphics backends and hardware. Software checks do not establish calibrated ColecoVision/television colour matching, physical display brightness, HDR accuracy, real GPU performance, or viewing comfort. Commercial-game coverage and BIOS-dependent startup remain outside the recorded software checks.

## Credits and licenses

Presets adapt [RetroCrisis](https://github.com/RetroCrisis/Retro-Crisis-GDV-NTSC). Shared CRT shaders are by guest(r), Dr. Venom and contributors, distributed through [libretro's Slang shaders](https://github.com/libretro/slang-shaders). The two custom ColecoVision stages are included as source; RGB and RGB 100 bypass their encoding paths.

Keep the supplied notices with the pack. Licensing is recorded per component in [the licenses folder](retro%20crisis%20custom/licenses/):

- [ColecoVision custom stages — MIT](retro%20crisis%20custom/licenses/Coleco-NTSC-MIT.txt)
- [RetroCrisis — GPL-3.0](retro%20crisis%20custom/licenses/RetroCrisis-GPL-3.0.txt)
- [Guest — GPL-2.0](retro%20crisis%20custom/licenses/Guest-GPL-2.0.txt)

This public repository contains the installable pack and user documentation. Research, development tooling, and validation records are maintained in a separate private repository.
