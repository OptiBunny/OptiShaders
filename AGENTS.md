# OptiShaders repository guidance

OptiShaders is a ColecoVision shader preset pack for RetroArch with Gearcoleco.
The current v10.2 pack contains 63 presets and four bundled shader stages.
Use [the user guide](OptiShaders/README.md) for installation, prerequisites,
expected settings, updates, and troubleshooting.

For security-sensitive changes, read [SECURITY.md](SECURITY.md) and
[the security model](SECURITY_MODEL.md), then inspect the affected files.
These documents guide review; they do not establish that a change is correct.

## Review rules

### Preserve shader behavior and numerical validity

- Follow a changed value through the complete pass chain. Check source and
  viewport dimensions, sampler bindings, aliases, feedback/history inputs,
  filtering, wrapping, mipmaps, framebuffer formats, and colour-space handling.
  A compiling stage can still consume the wrong texture or produce wrong output.
- Review parameter combinations as well as individual slider endpoints. Check
  zero and near-zero divisors, signed filter weights, exponent overflow, invalid
  powers, array indices, and nonfinite intermediates. Final clamping can hide an
  invalid calculation; inspect the operation that produced it.
- Keep fallbacks narrowly tied to the invalid condition they repair. Check
  finite normal inputs and affected boundary cases independently. Preserve the
  scanline-boundary behavior and the horizontal-filter and normalization fixes
  when updating the bundled Guest stages.
- Treat shader parameter names and shared uniforms as interfaces. Keep declared
  ranges, defaults, preset values, and controls used across passes consistent.
  Changes to supplied looks should be deliberate and described to users.

### Preserve paths and dependencies

- Resolve shader, include, lookup-image, and preset references from the correct
  file location. Keep filenames, case, spaces, and directory structure consistent
  with the ZIP and installation examples. Check fresh extraction as well as an
  existing installation; a developer's extra files can hide a missing dependency.
- The pack installs as `shaders_slang/OptiShaders/`, alongside `crt/`. Relative
  references such as `../../crt/` are intentional. Review their resolved targets
  instead of rejecting all parent-directory references or accepting every path.
- RetroArch, Gearcoleco, BIOS, games, and the remaining Slang shaders are separate
  prerequisites. RetroCrisis is an upstream source of the presets; users do not
  need a separate RetroCrisis installation. Keep that distinction in the docs.
- Preserve the four bundled shader files and their preset references together.
  Updating the shared Slang collection does not replace these local stages.
  Saved full presets may retain old paths; check the documented update workflow.

### Keep releases public-facing

- Keep research, raw validation records, local configurations, logs, captures,
  machine paths, credentials, and unrelated material out of the public tree and
  release ZIP. Ignore rules alone do not establish that an artifact is safe.
- Review the exact outgoing files, commit metadata, archive members, archive
  metadata, and relevant Git history. Use an explicit release file list and
  verify extracted bytes against the reviewed pack. Update the published ZIP
  checksum whenever ZIP bytes change.
- Preserve upstream copyright, license texts, and modification notices. The
  custom signal stages, adapted presets, and modified Guest stages have distinct
  licensing notices; do not replace them with a blanket license assertion.
- Keep `AGENTS.md`, `SECURITY.md`, and `SECURITY_MODEL.md` repository-only.
  Exclude them from installable ZIPs and Git source archives while retaining the
  user guide, shader sources, presets, and required notices.
- Keep the root README concise and installation-oriented. Put detailed setup,
  parameter explanations, and troubleshooting in the user guide. Keep version,
  filenames, paths, prerequisites, and update instructions consistent.

## Pull request workflow

Use a focused `codex/...` branch and a pull request targeting `main` for changes.
Do not push changes directly to `main`. Validate the exact outgoing files before
opening the PR, summarize the behavior and relevant checks, and address review
findings with focused commits. Follow the repository's configured checks and
review process before merging; do not bypass branch protections.

Keep public changes and private development work in separate PRs. Public PR
descriptions, comments and attachments must follow the same privacy boundary as
the public files; do not include private evidence or links to private PRs.

## Findings and validation

Report a concrete trigger, affected file or pass, observed impact, and evidence.
Distinguish an introduced regression from an existing limitation or an upstream
dependency issue. Avoid style-only findings without a practical consequence.

Use an isolated installation and disposable configuration for runtime checks.
Preserve users' saved presets, game files, BIOS, and existing shader collection.
Use redistributable or synthetic content for shareable reproductions.

Record the RetroArch/core/dependency versions, backend, source dimensions,
viewport, parameter values, and input used. Separate source inspection, isolated
stage checks, full-chain RetroArch runs, and visual comparisons. A software
renderer result is not physical-GPU coverage; a successful load is not proof of
correct pixels, timing, or every parameter combination.

Compare regression output under matching conditions. Explain any permitted
difference before accepting it; do not loosen a criterion merely to pass.
Report failures, missing prerequisites, skips, and untested backends explicitly.

For documentation-only changes, check links, examples, and agreement with the
current files. Do not claim new runtime coverage. Preserve existing file bytes
and line endings; `.gitattributes` disables automatic text conversion.
