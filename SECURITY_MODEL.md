# OptiShaders security model

Initial model reviewed against the public v10.2 pack, 2026-11-05. The dependency
inventory and integer-scaling safeguards below were updated for v10.5 on
2026-11-22. Curvature-domain safeguards were added for v10.6 on the same date;
the evidence limits still apply. Nonnegative bloom and positive-halation power
bases were added for v10.7 on 2026-11-23. The disabled-mask table index was
bounded for v10.8 on the same date. Animated-noise phase precision was corrected
for v10.9 on the same date. Humbar phase precision was corrected for v10.10
and enabled interlace field parity for v10.11 on the same date.

This model describes the distributed preset and shader files, their dependencies,
and release-review expectations. It is not a security certification or a claim
that all inputs, GPUs, and future dependency versions have been tested.

## Assets and security goals

| Asset | Protection sought |
| --- | --- |
| Supplied presets and shader source | Preserve intended paths, pass interfaces, finite calculations, and documented appearance. |
| Users' shader collections and saved presets | Limit installation and updates to the intended pack files; preserve user edits and unrelated content. |
| Host stability | Avoid accidental unbounded work and invalid resource use; investigate compiler, driver, and runtime failures. |
| Release files and attribution | Distribute the reviewed pack with its correct layout, checksum, source, and license notices. |
| Personal information and credentials | Exclude sensitive content from public files, archives, metadata, and publication history. |

## Scope and dependencies

The pack contains 63 `.slangp` presets, five `.slang` shader sources, a user
guide, and license texts. It contains no emulator executable, core, BIOS, game,
installer, background service, or network client. Installation is a file-copy
operation performed by the user or their chosen extraction tool.

The presets are adapted from RetroCrisis. A separate RetroCrisis installation
is not required. RetroArch, Gearcoleco, the BIOS, games, and the shared Slang
shader collection are installed separately. The pack expects shared Guest
stages and lookup images under `shaders_slang/crt/`, alongside `OptiShaders/`.
The final deconvergence stage is now bundled with the scanline stage so both
apply the same small-viewport integer-scaling safeguard. Its upstream revision
and modification notice are retained in the source.

RetroArch parses presets, resolves references, compiles shaders through its
graphics backend, and supplies textures and parameters for execution. The
graphics driver and operating system manage execution and resources. These are
external dependencies; OptiShaders adds no process isolation or permission
boundary around them.

## Threat model and assumptions

An attacker could alter a downloaded archive, contribute a malicious preset or
shader, change a dependency, or replace files in an installation they can write.
Review unexpected file references, hostile compiler input, excessive resource
demands, misleading instructions, and private data included in a release.

Using the pack assumes a trusted download source and a maintained RetroArch,
core, driver, and operating system. This model does not claim protection after
those components or the installed shader files have been compromised. Malicious
game or BIOS parsing belongs to the emulator/core boundary, not to this pack.

Ordinary shader execution processes supplied graphics data. The current sources
contain no host-file, network, or credential-handling implementation. This is a
description of the pack, not a guarantee against bugs in its native loaders,
compiler, driver, or image parsers.

## Data flow and review boundaries

1. **Download and extraction.** A release ZIP becomes files under the selected
   shader collection. Archive contents and paths must match the intended pack.
   Extraction and overwrite handling belong to the chosen tool; the pack cannot
   enforce where files are written or back up a user's edits automatically.
2. **Preset loading.** RetroArch resolves the selected preset's shader and lookup
   references. The documented sibling-folder layout is part of this interface.
   A local absolute path or extra directory level can select unintended files or
   break loading. Saved presets may continue referring to an older installation.
3. **Compilation and rendering.** Bundled and shared stages form one pipeline.
   Pass order, aliases, history, sampling, dimensions, and framebuffer formats
   affect output. Errors can appear only at particular parameter combinations,
   source sizes, or frame phases; final colour clamping can conceal nonfinite math.
4. **Saving and updating.** RetroArch writes the user's saved presets and config.
   The update guide asks users to back up edits, replace supplied pack files,
   reload a supplied preset, and verify new saves before removing older files.

## Repository invariants for review

Review package membership, dependency paths, corrected-stage references,
ZIP/source byte agreement, the published checksum and current release labels.
These checks complement shader, privacy and dependency review and runtime
validation. Development tooling is not part of this public product repository:

- Keep references within the documented pack and shared dependency tree. Resolve
  legitimate parent-relative paths fully and inspect every new loading surface.
- Preserve the bundled horizontal-filter zero-weight fallback and stable
  scanline normalization, including the earlier scanline-boundary behavior.
  Keep the scanline and deconvergence integer-scaling guards in agreement:
  floor modes use fractional fit when no positive integer scale fits, while
  valid integer scales and the interlace bypass keep their existing behavior.
  The two curvature functions replace only non-positive inverse-square-root
  radicands with a neutral factor. At the declared curvature-shape limits those
  coordinates are already outside the image; positive radicands and valid
  curvature calculations are preserved. Keep both stage guards in agreement.
  Brightness boost can extrapolate final bloom and positive-halation contributions
  below zero. Their power bases are lower-bounded at zero before fractional
  gamma conversion; nonnegative bases and the negative-halation branch retain
  their calculations. The mask-width lookup lower-bounds its index at zero for
  the disabled-mask sentinel; the original mask control and enabled indices
  0 through 14 are preserved. The optional animated-noise counter is reduced
  modulo 6001 as an unsigned integer before conversion to float. This preserves
  its intended phase when adjacent large counters would otherwise collapse to
  the same float; the fixed negative-noise seed and disabled branch are retained.
  The optional humbar reduces the unsigned counter using the exact binary32
  ratio of each supported speed from 5 through 200, preserving fractional saved
  settings. Its integer remainder uses at most 21 bounded doubling steps, with
  each intermediate below 2^25; integer speeds need no doubling steps. Only the
  bounded remainder is converted to float and scaled by a power of two. The
  intensity-zero bypass, speed-minus-one divisor and direction controls remain
  unchanged. Values outside the declared speed range retain their prior formula.
  Enabled interlace field parity is reduced as an unsigned integer before float
  conversion. The supplied presets set `frame_count_mod10` to 2 only for the
  shared linearizer at pass 10, whose counter is used only for field parity in
  the reviewed dependency. The bundled scanline stage at pass 16 reduces its
  own field parity while retaining the full counter for rolling scanlines.
  Preserve that pass mapping, the disabled defaults and the other pass counters;
  review the contract again if a shared dependency or custom chain changes.
  A correction for one arithmetic case is not proof that all arithmetic is safe.
- Preserve source attribution and the distinct MIT, GPL-3.0, and
  GPL-2.0-or-later notices supplied with the relevant components.
- Keep release membership explicit and verify ZIP bytes, metadata, and extraction
  layout. Do not infer correctness solely from a successful archive creation.
- Keep private evidence and personal data out of public artifacts and history.
  Ignore rules and scanners are supporting checks, not a confidentiality boundary.
- Keep these three review documents in the repository rather than the installable
  pack or Git source archives. User instructions and license texts remain supplied.

## Evidence limits and residual risks

Static path checks do not exercise the runtime loader. Compilation does not
establish correct texture bindings, pixels, or motion. An isolated shader check
does not establish full-chain behavior. A full-chain result covers the recorded
inputs and settings; it does not prove every parameter combination or future
dependency revision works.

Backend precision, intermediate texture formats, filtering, timing, and display
settings can change output. Software rendering does not establish physical-GPU
coverage or performance. Cross-backend differences require investigation rather
than an automatic claim that either image is correct.

Checksums detect changed bytes relative to a known reference. The published ZIP
checksum is not an independent signature, and replacing both the ZIP and its
checksum can defeat that comparison. Licensing and privacy checks likewise need
review of the actual outgoing files.

Use [AGENTS.md](AGENTS.md) for ordinary change review and
[SECURITY.md](SECURITY.md) for security findings and safe verification. Update
this model when the pack's loading paths, dependencies, or distribution change.
