# OptiShaders

CRT-style shader presets for **ColecoVision in RetroArch**, using the **Gearcoleco** core.

**v10.1 · 63 presets · 9 looks · 720p to 4K**

[**Download OptiShaders**](downloads/OptiShaders-ColecoVision-Gearcoleco.zip?raw=true)
· [**User guide**](OptiShaders/README.md)

This update reduces isolated bright artifacts at scanline boundaries.
For an existing installation, follow the [update steps](OptiShaders/README.md#update-an-existing-installation).

## Quick start

You need **RetroArch with a Slang-compatible video driver**, **Gearcoleco**,
the **ColecoVision BIOS**, a game, and **RetroArch's Slang shader collection**.
See [prerequisites and setup](OptiShaders/README.md#prerequisites) if these are
not already installed.

1. Download and extract **`OptiShaders-ColecoVision-Gearcoleco.zip`**.
2. In RetroArch, run **Main Menu → Online Updater → Update Slang Shaders**.
   If the updater is unavailable, use the [manual installation steps](OptiShaders/README.md#install-the-shared-shaders).
3. Copy the **`OptiShaders`** folder from the ZIP into `shaders_slang/`, alongside
   `crt/`. See [where to install it](OptiShaders/README.md#install).
4. Start a ColecoVision game with Gearcoleco and apply the
   [core and display settings](OptiShaders/README.md#set-up-the-core-and-display).
5. Open **Quick Menu → Shaders**, turn **Video Shaders** on, and choose
   **Load Shader Preset**. Pick a preset from the folder matching your
   [output resolution](OptiShaders/README.md#choose-a-preset).
6. Open **Save**, turn **Simple Presets** on, then choose **Save Core Preset**
   to use that look with Gearcoleco. See [saving and game overrides](OptiShaders/README.md#save-your-choice).

## Choose your look

Each resolution folder includes **Clean, Dirty, RGB, S-Video, Composite, RF,
Badly Adjusted, RGB 100, and Composite 100**.

Choose from **720p**, **1080p**, **1440p**, or **4K** presets, with **Flat** and
**Curved** versions at 1080p and above. Signal effects target NTSC.

The [user guide](OptiShaders/README.md) covers preset choices, shader adjustments,
updates, and troubleshooting.

## Credits and licenses

Presets are adapted from
[RetroCrisis](https://github.com/RetroCrisis/Retro-Crisis-GDV-NTSC), with shared
CRT shaders by guest(r), Dr. Venom, and contributors from
[libretro's Slang collection](https://github.com/libretro/slang-shaders).

OptiShaders includes its presets, two custom signal stages, and a modified Guest
scanline stage. RetroArch, Gearcoleco, the BIOS, games, and the remaining shared
Slang shaders are installed separately.

Keep the supplied license notices with the pack:

[Custom signal stages — MIT](OptiShaders/licenses/Coleco-NTSC-MIT.txt) ·
[RetroCrisis — GPL-3.0](OptiShaders/licenses/RetroCrisis-GPL-3.0.txt) ·
[Guest scanline stage — GPL-2.0-or-later](OptiShaders/licenses/Guest-GPL-2.0.txt)

## Download checksum

SHA-256 for `OptiShaders-ColecoVision-Gearcoleco.zip`:

```text
ea2622ecb2d23f301f0cfec303817b26a9844d93f8ebbcdb9147bf5e4a115895
```
