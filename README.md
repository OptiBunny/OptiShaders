# OptiShaders

CRT-style shaders for **ColecoVision** in RetroArch using the **Gearcoleco** core.

**v10 · 63 presets · 9 looks · 720p to 4K**

**[Download OptiShaders](downloads/OptiShaders-ColecoVision-Gearcoleco.zip?raw=true)** · [Detailed pack guide](OptiShaders/README.md) · [Browse presets](OptiShaders/)

## Install

You need **RetroArch**, the **Gearcoleco** core, and RetroArch's **Slang shader collection**. The collection supplies the shared Guest shaders and lookup images (LUTs) used by this pack.

1. Download and extract `OptiShaders-ColecoVision-Gearcoleco.zip`.
2. Copy its **OptiShaders** folder into `RetroArch/shaders/shaders_slang/`.
3. Keep all supplied folders and both custom shader files together.
4. Load a game in Gearcoleco. Open **Quick Menu → Shaders → Load Shader Preset** and select a preset from the folder for your resolution.

The installed layout should look like this:

```text
shaders_slang/
├── crt/                  # shared RetroArch shaders and LUTs
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
| A preset will not load | Check the folder layout above. Keep both custom stages in `OptiShaders/shaders/` and make sure the shared Guest shaders and LUTs are present under `shaders_slang/crt/`. |
| An old save fails after an update | Load a renamed preset from the new pack and resave it. The saved reference may still point to an old path. |
| One game uses the wrong look | A game preset may be overriding the core preset. |
| The picture is stretched or sized incorrectly | Recheck the core/display settings and select the folder matching your output resolution. |
| You want to disable persistence | Set **Afterglow Strength** to **0**, then save your preset. |

For custom shader controls and a full file overview, see the [pack guide](OptiShaders/README.md).

## Download checksum

SHA-256 for `OptiShaders-ColecoVision-Gearcoleco.zip`:

```text
7b92c856c4674d01873891fa029b4a161999b49da5890877a088464efedf2409
```

## Credits and licenses

Presets are adapted from [RetroCrisis](https://github.com/RetroCrisis/Retro-Crisis-GDV-NTSC). Shared CRT shaders are by guest(r), Dr. Venom, and contributors, distributed through [libretro's Slang shaders](https://github.com/libretro/slang-shaders).

Keep the supplied license notices with the pack:

- [ColecoVision custom stages — MIT](OptiShaders/licenses/Coleco-NTSC-MIT.txt)
- [RetroCrisis — GPL-3.0](OptiShaders/licenses/RetroCrisis-GPL-3.0.txt)
- [Guest — GPL-2.0](OptiShaders/licenses/Guest-GPL-2.0.txt)
