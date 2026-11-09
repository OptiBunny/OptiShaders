# Release checks

These repository tools check the installable OptiShaders package without running
RetroArch or changing an installation. They use Python 3.12's standard library
and Git; there are no Python package dependencies.

The **Release checks** workflow runs on every pull request, pushes to `main`, and
manual dispatch. It checks out only this public repository and a pinned revision
of the public Slang collection. It has read-only repository permissions, does not
retain checkout credentials, and uploads no artifacts.

## What is checked

- The release has the expected 63 presets: nine looks in each of seven folders.
- All four bundled stages, the user guide and three license files are present.
- Preset shader and texture paths resolve with exact filename case within the
  documented `shaders_slang/OptiShaders/` and sibling `crt/` layout. Referenced
  shader includes are checked too.
- Every preset keeps the bundled corrected Guest horizontal-filter and scanline
  stage references. Having the corrected files on disk is not enough if a preset
  still points at the shared versions.
- The download ZIP contains exactly the 71 selected package files, with matching
  file bytes and safe, unambiguous member paths and file types.
- The ZIP SHA-256 matches the root README, and the root and packaged user-guide
  release banners agree with `release.json`. Historical `v10` preset comments
  are not current release labels.

The companion test script changes disposable package copies to verify that
broken paths, missing or unexpected files, stale checksums and other invalid
packages are rejected. It does not alter the release files being checked.

## Run locally

From this repository, create a separate dependency checkout. Choose a new sibling
folder; do not reuse your RetroArch installation or shader directory.

```sh
git clone --filter=blob:none --no-checkout https://github.com/libretro/slang-shaders.git ../OptiShaders-slang-check
git -C ../OptiShaders-slang-check sparse-checkout set crt/shaders/guest
git -C ../OptiShaders-slang-check checkout --detach 2345ee91602a7404d3a1a6a5df6108d7305fdad4
python -B tools/validate_release.py --slang-root ../OptiShaders-slang-check
python -B tools/test_validate_release.py --slang-root ../OptiShaders-slang-check
```

The commit above is the `shared_revision` in `release.json`. Use the manifest's
current value if it changes. The validator checks the dependency checkout's
actual Git revision and requires the selected files to be available. The pin is
a repeatable compatibility baseline, not a claim about every later Slang update.

## Deliberate release changes

Review changes to `release.json` alongside the package changes they describe.
When changing the release version, folder/look inventory, bundled stage list or
shared dependency revision, update the corresponding manifest fields and check
the new inputs. Do not change expected values just to silence an unexplained
failure.

When package bytes change, rebuild the download ZIP from the selected public
files and update its documented checksum. Keep the user-facing version labels,
paths and notices consistent. The checker validates an existing ZIP; it does
not build, overwrite, publish or install one.

These are static packaging and dependency checks. Passing does not demonstrate
shader compilation, correct rendered pixels, physical-GPU performance, historical
display accuracy, or freedom from personal information or credentials. Continue
to review outgoing content and run relevant rendering or security checks for
changes that need them. Keep detailed research, runtime validation records and
recovery material private.

This tooling and the workflow are repository-only and are excluded from the
installable package and Git source archives.
