# ColecoVision custom shaders for Gearcoleco — v10

63 presets: nine looks in seven resolution folders.

## Version 10 — 30 September 2026

- **RF:** a restrained blend of separate brightness/colour filtering and delay, informed by the revision-F board schematic. This is a circuit-informed artistic approximation, not a measured complete RF modulator/tuner model.
- **Badly Adjusted:** a small static picture skew before the CRT stages, with no new animated wobble or frame insertion. The screen mask stays fixed.
- **Other seven looks:** appearance preserved after review. All nine receive native Gearcoleco pattern and motion checks. The existing v9 flat-colour ripple corrections remain in place.

| Optional shader control | Default | Effect |
| --- | --- | --- |
| Coleco experimental board response | RF 0.5; other encoded looks 0 | Set 0 to remove the new RF response. Larger values add more of the isolated board model. |
| Coleco static picture skew (native pixels) | Badly Adjusted 0.5 | Set 0 for straight picture geometry; occasional one-code downstream rounding differences remain compared with v9. |

Leave **Coleco RGB geometry pass** at the supplied value: Clean/S-Video 0, Badly Adjusted 1. It selects the operation, not its strength.

The 100 names retain RetroCrisis's reference intent and styling; they do not certify exact ColecoVision/Trinitron matching. No invented replacement palette or fixed HDR calibration is applied. Signal presets remain **NTSC**.

For picture comparisons, keep your SDR/HDR mode and display settings fixed. Check dark scenes, white lettering, green/blue scenery, large bright areas and scrolling from your normal seat. Software PNGs may precede HDR conversion and cannot measure physical TV luminance. Keep BFI and shader subframes disabled.

## Install

1. Place **retro crisis custom** beside **retro crisis**, inside `RetroArch/shaders/shaders_slang/`.
2. Keep its **shaders** folder: both included ColecoVision-specific files are required. Standard Guest shaders and lookup images come from RetroArch's installed Slang shader collection.
3. Load a game in Gearcoleco, then select your preset under **Quick Menu → Shaders → Load Shader Preset**.
4. Save it with **Save → Save Core Preset**. A saved game preset can override this choice.

For a clean update, replace the previous custom folder with this one, retaining any personal edits separately. Load the supplied preset again before saving it. Copying over an existing folder can leave older reports or an unused vendor folder behind.

## Core and display

- Gearcoleco: **Overscan: Top+Bottom** and **Aspect Ratio: 4:3 DAR**.
- RetroArch: **Core Provided** aspect ratio and vertical/Y integer scaling.
- Keep BFI and shader subframes disabled for this setup.
- Choose the folder matching your output resolution. A 240-line input fits 4K at 9×; a 1080p integer fit uses a 960-line-high game viewport.

Variants: **Clean, Dirty, RGB, S-Video, Composite, RF, Badly Adjusted, RGB 100, Composite 100**. The two 100 variants retain their distinct reference CRT profiles. Signal simulations target NTSC. Set **Afterglow Strength** to zero if you want to disable persistence.

## Limitations and credits

Rendering can vary across graphics backends and hardware. Software checks do not establish physical GPU/display performance, commercial-game coverage, or HDR/motion accuracy. Research and detailed validation records are maintained privately.

The install ZIP contains only 63 presets, two custom stages, this README and three licenses. Keep the two custom files; Guest dependencies continue to come from RetroArch's normal shared Slang collection. Presets adapted from RetroCrisis; shared CRT shaders by guest(r), Dr. Venom and contributors. Preserve supplied license notices.
