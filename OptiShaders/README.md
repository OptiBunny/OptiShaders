# OptiShaders — ColecoVision pack guide

**v10 · 63 presets · 9 looks · 7 resolution folders**

This pack is for the **Gearcoleco** core in RetroArch. It provides nine CRT looks, with NTSC signal effects.

[Project and downloads](https://github.com/OptiBunny/OptiShaders#readme)

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

## Adjust the shader

Open **Quick Menu → Shaders → Shader Parameters** after loading a preset. Save the preset again when you want to keep a change.

| Control | Supplied setting | What it does |
| --- | --- | --- |
| **Coleco experimental board response** | RF: **0.5**; other encoded looks: **0** | Controls the added RF filtering/delay effect. Set it to 0 to disable that effect. |
| **Coleco static picture skew (native pixels)** | Badly Adjusted: **0.5** | Controls picture skew. Set it to 0 for straight picture geometry. |
| **Afterglow Strength** | Depends on the preset | Set it to 0 to disable persistence. |

Leave **Coleco RGB geometry pass** at its supplied value: **0** for Clean/S-Video and **1** for Badly Adjusted. It selects the operation rather than its strength.

Keep SDR/HDR mode and display settings consistent when comparing looks.

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

## Included files

The ZIP contains **69 files**: 63 presets, two custom shader stages, this guide, and three licenses.

Keep both custom stages in `OptiShaders/shaders/`:

- `optishaders-colecovision-ntsc-pass1.slang`
- `optishaders-colecovision-yc-pass1.slang`

The shared Guest shaders and LUTs come from RetroArch's Slang shader collection; they are not bundled in this ZIP.

## Credits and licenses

Presets are adapted from [RetroCrisis](https://github.com/RetroCrisis/Retro-Crisis-GDV-NTSC). Shared CRT shaders are by guest(r), Dr. Venom, and contributors, distributed through [libretro's Slang shaders](https://github.com/libretro/slang-shaders).

Keep the supplied license notices with the pack:

- [ColecoVision custom stages — MIT](licenses/Coleco-NTSC-MIT.txt)
- [RetroCrisis — GPL-3.0](licenses/RetroCrisis-GPL-3.0.txt)
- [Guest — GPL-2.0](licenses/Guest-GPL-2.0.txt)
