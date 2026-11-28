# OptiShaders

CRT-style shader presets for **ColecoVision in RetroArch**, using the **Gearcoleco** core.

**v0.9.2 · 63 presets · 9 looks · 720p to 4K**

Download the [v0.9.2 preset pack (ZIP)](https://github.com/OptiBunny/OptiShaders/releases/download/v0.9.2/OptiShaders-ColecoVision-Gearcoleco.zip), then follow the [installation guide](docs/USER_GUIDE.md#install).

## Changes since v0.9.1

- Fixed colour bleeding from **Bloom** into **Glow** when a colour-channel offset
  is active and **Deconvergence Strength** is below **1.0**.
- Fixed a thin processed strip at the right edge at high resolutions. **Show
  Original Image** at **1.0 (100%)** now shows the original image across the full
  width. Fractional settings retain their previous split position.

All 63 presets retain their supplied settings.

For an existing installation, follow the [update steps](docs/USER_GUIDE.md#update-an-existing-installation).

## Quick start

You need **RetroArch with a Slang-compatible video driver**, **Gearcoleco**,
the **ColecoVision BIOS**, a game, and **RetroArch's Slang shader collection**.
See [prerequisites and setup](docs/USER_GUIDE.md#prerequisites) if these are
not already installed.

1. Download and extract **`OptiShaders-ColecoVision-Gearcoleco.zip`**.
2. In RetroArch, run **Main Menu → Online Updater → Update Slang Shaders**.
   If the updater is unavailable, use the [manual installation steps](docs/USER_GUIDE.md#install-the-shared-shaders).
3. Copy the **`OptiShaders`** folder from the ZIP into `shaders_slang/`, alongside
   `crt/`. See [where to install it](docs/USER_GUIDE.md#install).
4. Start a ColecoVision game with Gearcoleco and apply the
   [core and display settings](docs/USER_GUIDE.md#set-up-the-core-and-display).
5. Open **Quick Menu → Shaders**, turn **Video Shaders** on, and choose
   **Load Preset**. Pick a preset from the folder matching your
   [output resolution](docs/USER_GUIDE.md#choose-a-preset).
6. Open **Manage Presets**, turn **Simple Presets** on, then choose **Save Core Preset**
   to use that look with Gearcoleco. See [saving and game overrides](docs/USER_GUIDE.md#save-your-choice).

## Choose your look

Each resolution folder includes **Clean, Dirty, RGB, S-Video, Composite, RF,
Badly Adjusted, RGB 100, and Composite 100**.

Choose from **720p**, **1080p**, **1440p**, or **4K** presets, with **Flat** and
**Curved** versions at 1080p and above. Signal effects target NTSC.

The [user guide](docs/USER_GUIDE.md) covers preset choices, shader adjustments,
updates, and troubleshooting.

## Credits and licenses

Presets are adapted from
[RetroCrisis](https://github.com/RetroCrisis/Retro-Crisis-GDV-NTSC), with shared
CRT shaders by guest(r), Dr. Venom, and contributors from
[libretro's Slang collection](https://github.com/libretro/slang-shaders).

OptiShaders includes its presets and five shader stages: two custom signal
stages and modified Guest horizontal-filter, scanline and deconvergence stages. RetroArch,
Gearcoleco, the BIOS, games, and the remaining shared Slang shaders are installed
separately.

Keep the supplied license notices with the pack:

[Custom signal stages — MIT](OptiShaders/licenses/Coleco-NTSC-MIT.txt) ·
[RetroCrisis — GPL-3.0](OptiShaders/licenses/RetroCrisis-GPL-3.0.txt) ·
[Guest stages — GPL-2.0-or-later](OptiShaders/licenses/Guest-GPL-2.0.txt)

## Download checksum

The release download and the [tagged repository copy](https://raw.githubusercontent.com/OptiBunny/OptiShaders/v0.9.2/downloads/OptiShaders-ColecoVision-Gearcoleco.zip) share this SHA-256:

```text
978e2199f99bdf912fccac6348395acfded11bdd54fb94b2c75b449e28451254
```
