# OptiShaders security model

Reviewed against the public v10.2 pack, 2026-11-05.

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

The pack contains 63 `.slangp` presets, four `.slang` shader sources, a user
guide, and license texts. It contains no emulator executable, core, BIOS, game,
installer, background service, or network client. Installation is a file-copy
operation performed by the user or their chosen extraction tool.

The presets are adapted from RetroCrisis. A separate RetroCrisis installation
is not required. RetroArch, Gearcoleco, the BIOS, games, and the shared Slang
shader collection are installed separately. The pack expects shared Guest
stages and lookup images under `shaders_slang/crt/`, alongside `OptiShaders/`.

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

These remain review requirements. The [release checks](tools/README.md) automate
package membership, dependency paths, corrected-stage references, ZIP/source byte
agreement, the published checksum and current release labels on pull requests.
They do not replace shader, privacy or dependency review, or runtime validation:

- Keep references within the documented pack and shared dependency tree. Resolve
  legitimate parent-relative paths fully and inspect every new loading surface.
- Preserve the bundled horizontal-filter zero-weight fallback and stable
  scanline normalization, including the earlier scanline-boundary behavior.
  A fallback for one undefined case is not proof that all arithmetic is safe.
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
