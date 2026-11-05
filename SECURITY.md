# Security review guidance

OptiShaders distributes shader presets, shader source, licenses, and instructions.
RetroArch and its graphics stack load and execute the shaders. Use
[the security model](SECURITY_MODEL.md) for assets, trust boundaries, and limits,
and [AGENTS.md](AGENTS.md) for general review guidance.

## Scope and assumptions

Review contributed presets, shader source, lookup images, dependency changes,
and release archives as potentially untrusted inputs. A readable text file, a
successful compile, or a matching checksum does not establish benign behavior.

The selected RetroArch installation, core, graphics driver, operating system,
and extraction tools are separate platform inputs. This pack supplies no
sandbox, privileged installer, account system, or credential store. A review
must not attribute protection supplied by the host to the shader pack itself.

## Security review rules

1. **Trace file references.** Check shader and texture paths, nested includes,
   inherited presets, and any newly introduced file-loading mechanism. Resolve
   them against the documented installation layout. Reject unexpected absolute,
   network, device, or unrelated local targets. Intentional relative references
   into the shared Slang collection need to remain usable.
2. **Review executable shader input.** Follow parameter values and texture data
   into loops, indexing, arithmetic, texture operations, and framebuffer sizing.
   Check finite-input behavior, legal parameter combinations, startup geometry,
   and shader-stage interfaces. Separate image-quality defects from supported
   availability or security impacts; neither should be silently dismissed.
3. **Bound validation work.** Use disposable installations and configurations,
   known input content, and finite runtime/resource limits. A malformed shader
   can stress a compiler or driver. Do not test failure paths against a user's
   active configuration or treat a hung process as a passing visual check.
4. **Review dependency changes.** Identify the upstream revision and the exact
   files used. Preserve license and modification notices. Check the complete
   chain when a shared stage changes; successful testing against one installed
   collection does not establish compatibility with every later update.
5. **Inspect release contents.** Verify an explicit member list, extracted file
   bytes, paths, and required notices. Reject traversal, absolute archive paths,
   ambiguous duplicates, unexpected links, and unrelated executables or scripts.
   Keep the documented `OptiShaders/` layout and avoid including local tools or
   configurations. An extraction utility's own protections remain external.
6. **Protect publication privacy.** Review diffs, filenames, commit identities,
   relevant history, ZIP metadata, and embedded or nested content for personal
   information and credentials. Keep raw research and validation evidence out of
   the public payload. Scanner flags need contextual review; an exception must
   identify the specific benign content without suppressing new secrets.
7. **Keep claims tied to evidence.** Report exact inputs, runtime and dependency
   versions, and the boundary tested. Preserve failed checks and explain a
   changed expectation. A checksum proves byte identity against its reference;
   it does not authenticate an independently compromised download source.

## Findings and safe verification

For a security finding, identify the attacker-controlled input, required user
interaction, reachable code or loading path, violated property, and concrete
confidentiality, integrity, or availability impact. Explain which checks fail
to prevent it and whether the result was reproduced or established by inspection.

Distinguish a pack defect from a RetroArch, core, compiler, driver, or extraction
tool defect. An upstream location does not make a reachable problem irrelevant;
it changes the affected component and where the fix belongs.

Use a small shareable reproduction without copyrighted game/BIOS material,
credentials, personal paths, or unrelated files. Do not place sensitive payloads
or unsanitized logs in public issues. Describe the trigger and impact without
publishing confidential data.

Compilation, static checks, and a passing renderer case do not establish freedom
from driver vulnerabilities or universal GPU compatibility. Report unsupported
platforms, unavailable hardware, skipped checks, and incomplete coverage plainly.
Update the model when inputs, dependencies, distribution, or execution change.
