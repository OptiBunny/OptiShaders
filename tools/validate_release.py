#!/usr/bin/env python3
"""Read-only checks for the public OptiShaders package; Python standard library only."""

import argparse
import hashlib
import json
import re
import stat
import struct
import subprocess
import sys
import zipfile
import zlib
from pathlib import Path, PurePosixPath


class ValidationError(Exception):
    """A release invariant was not satisfied."""


PACK = "OptiShaders"
ZIP = "downloads/OptiShaders-ColecoVision-Gearcoleco.zip"
MAX_FILE = 2 * 1024 * 1024
MAX_ZIP = 16 * 1024 * 1024
BUNDLED = {
    "optishaders-colecovision-ntsc-pass1.slang",
    "optishaders-colecovision-yc-pass1.slang",
    "optishaders-guest-ntsc-pass1.slang",
    "optishaders-guest-ntsc-pass2.slang",
}
LICENSES = {"Coleco-NTSC-MIT.txt", "RetroCrisis-GPL-3.0.txt", "Guest-GPL-2.0.txt"}
KEY = r"[A-Za-z_][A-Za-z_0-9]*"


def require(condition, message):
    if not condition:
        raise ValidationError(message)


def regular(path):
    info = path.lstat()
    require(not stat.S_ISLNK(info.st_mode) and not (
        getattr(info, "st_file_attributes", 0) & 0x400
    ), f"Unsafe link/reparse path: {path.name}")
    return info


def safe_parts(name):
    require(isinstance(name, str) and bool(name), "Empty or invalid path")
    require(not any(ord(c) < 32 for c in name) and not any(c in name for c in "\\:"),
            "Unsafe path characters")
    parts = name.split("/")
    require(all(p and p not in (".", "..") for p in parts), f"Unsafe path: {name}")
    return parts


def file_at(base, name):
    """Resolve exact case on Windows too; reject links along the entire path."""
    current = base
    require(stat.S_ISDIR(regular(current).st_mode), "Invalid root directory")
    for part in safe_parts(name):
        require(current.is_dir(), f"Missing directory in path: {name}")
        require(part in {p.name for p in current.iterdir()},
                f"Missing file or wrong-case path: {name}")
        current = current / part
        regular(current)
    require(current.is_file(), f"Expected a regular file: {name}")
    return current


def read_bytes(base, name, limit=MAX_FILE):
    path = file_at(base, name)
    require(path.stat().st_size <= limit, f"File exceeds size limit: {name}")
    return path.read_bytes()


def text(data, label):
    try:
        result = data.decode("utf-8")
    except UnicodeDecodeError as exc:
        raise ValidationError(f"Invalid UTF-8: {label}") from exc
    require("\0" not in result, f"NUL in text: {label}")
    return result


def manifest(root):
    def unique_pairs(pairs):
        result = {}
        for key, value in pairs:
            require(key not in result, f"Duplicate manifest key: {key}")
            result[key] = value
        return result

    try:
        data = json.loads(read_bytes(root, "tools/release.json"), object_pairs_hook=unique_pairs)
    except (ValueError, UnicodeDecodeError) as exc:
        raise ValidationError("Invalid release manifest JSON") from exc
    require(isinstance(data, dict), "Invalid release manifest")
    require(set(data) == {"version", "shared_revision", "preset_folders", "looks",
                          "bundled_shaders", "licenses"}, "Unexpected manifest fields")
    require(isinstance(data["version"], str) and
            re.fullmatch(r"\d+\.\d+(?:\.\d+)?", data["version"]), "Invalid release version")
    require(isinstance(data["shared_revision"], str) and
            re.fullmatch(r"[0-9a-f]{40}", data["shared_revision"]), "Invalid shared revision")
    for key in ("preset_folders", "looks", "bundled_shaders", "licenses"):
        values = data[key]
        require(isinstance(values, list) and 0 < len(values) <= 100, f"Invalid manifest {key}")
        require(all(isinstance(v, str) and re.fullmatch(r"[A-Za-z0-9 .-]+", v)
                    and v.strip() == v and v not in (".", "..") for v in values),
                f"Unsafe manifest names: {key}")
        require(len(values) == len({v.casefold() for v in values}), f"Duplicate manifest {key}")
    require(set(data["bundled_shaders"]) == BUNDLED, "Bundled stage catalog must contain the four stages")
    require(set(data["licenses"]) == LICENSES, "License catalog must retain all three notices")
    return data


def catalog(data):
    presets = {
        f"{PACK}/{folder}/OptiShaders - ColecoVision - {look}.slangp"
        for folder in data["preset_folders"] for look in data["looks"]
    }
    members = presets | {f"{PACK}/shaders/{name}" for name in data["bundled_shaders"]}
    members |= {f"{PACK}/licenses/{name}" for name in data["licenses"]}
    members.add(f"{PACK}/README.md")
    return presets, members


def source_catalog(root, expected):
    """Walk without following links, rejecting even extra empty directories."""
    allowed_dirs = {str(parent) for member in expected
                    for parent in PurePosixPath(member).parents if str(parent) != "."}
    actual = set()

    def walk(directory, logical):
        require(logical in allowed_dirs, f"Unexpected source directory: {logical}")
        require(stat.S_ISDIR(regular(directory).st_mode), f"Invalid source directory: {logical}")
        for child in directory.iterdir():
            name = f"{logical}/{child.name}"
            info = regular(child)
            if stat.S_ISDIR(info.st_mode):
                walk(child, name)
            else:
                require(stat.S_ISREG(info.st_mode), f"Non-regular source file: {name}")
                actual.add(name)

    require((root / PACK).is_dir(), "Missing OptiShaders source directory")
    walk(root / PACK, PACK)
    require(actual == expected,
            f"Source member mismatch; missing={sorted(expected - actual)}, extra={sorted(actual - expected)}")


def release_banner(source, label, data, preset_count):
    banners = re.findall(r"^\*\*v([^\r\n]+)\*\*\s*$", source, re.MULTILINE)
    expected = f"{data['version']} · {preset_count} presets · {len(data['looks'])} looks · 720p to 4K"
    require(banners == [expected], f"Release version/count banner mismatch: {label}")
    headings = re.findall(r"^## What's new in v([^\r\n]+)\s*$", source, re.MULTILINE)
    require(all(h.strip() == data["version"] for h in headings), f"Release version heading mismatch: {label}")


def parse_preset(source, label):
    settings = {}
    for number, raw in enumerate(source.splitlines(), 1):
        line = raw.strip()
        require(not re.match(r"#\s*(reference|include)\b", line, re.IGNORECASE),
                f"Unsupported preset inheritance/include: {label}:{number}")
        if not line or line.startswith("#"):
            continue
        match = re.fullmatch(rf'({KEY})\s*=\s*"([^"\r\n]*)"\s*(?:#.*)?', line)
        require(match is not None, f"Unsupported preset syntax: {label}:{number}")
        key, value = match.groups()
        require(key not in settings, f"Duplicate preset key: {label}:{key}")
        settings[key] = value
    return settings


def resolve_reference(parent, reference):
    require(isinstance(reference, str) and reference and not reference.startswith(("/", "~")),
            "Unsafe absolute or empty reference path")
    require(not any(ord(c) < 32 for c in reference) and not any(c in reference for c in "\\:"),
            "Unsafe reference path characters")
    parts = list(PurePosixPath(parent).parts)
    for part in reference.split("/"):
        require(bool(part), "Unsafe empty reference path component")
        if part == "..":
            require(bool(parts), "Reference path escapes the shader installation")
            parts.pop()
        elif part != ".":
            parts.append(part)
    require(parts and (parts[0] == PACK or parts[:3] == ["crt", "shaders", "guest"]),
            "Reference path outside the pack/shared Guest tree")
    return "/".join(parts)


def check_dependencies(root, slang_root, payload, presets):
    visited = set()
    active = set()
    dependencies = set()

    def contents(logical):
        if logical.startswith(PACK + "/"):
            require(logical in payload, f"Missing bundled dependency: {logical}")
            return payload[logical]
        dependencies.add(logical)
        return read_bytes(slang_root, logical)

    def shader(logical, depth=0):
        require(logical.endswith(".slang") or logical.endswith(".h") or logical.endswith(".inc"),
                f"Unsupported shader/include file: {logical}")
        require(depth < 32, "Shader include depth exceeded")
        require(logical not in active, f"Cyclic shader include: {logical}")
        if logical in visited:
            return
        require(len(visited) < 512, "Too many shader includes")
        visited.add(logical)
        active.add(logical)
        source = text(contents(logical), logical)
        # Includes in comments are not loading directives. Macro includes fail closed.
        source = re.sub(r"/\*.*?\*/", "", source, flags=re.DOTALL)
        source = re.sub(r"//[^\n]*", "", source)
        for line in source.splitlines():
            if re.match(r"\s*#\s*(include|include_next)\b", line):
                match = re.fullmatch(r'\s*#\s*include\s+"([^"\r\n]+)"\s*', line)
                require(match is not None, f"Unsupported include syntax: {logical}")
                target = resolve_reference(str(PurePosixPath(logical).parent), match[1])
                shader(target, depth + 1)
        active.remove(logical)

    for name in sorted(presets):
        settings = parse_preset(text(payload[name], name), name)
        require(settings.get("shaders") == "18", f"Expected 18 shader passes: {name}")
        shader_keys = {key for key in settings if re.fullmatch(r"shader\d+", key)}
        require(shader_keys == {f"shader{i}" for i in range(18)}, f"Missing/extra shader pass: {name}")
        parent = str(PurePosixPath(name).parent)
        for index in range(18):
            target = resolve_reference(parent, settings[f"shader{index}"])
            if index in (11, 16):
                stage = 1 if index == 11 else 2
                require(target == f"{PACK}/shaders/optishaders-guest-ntsc-pass{stage}.slang",
                        f"Corrected bundled Guest stage {index} not selected: {name}")
            shader(target)
        textures = settings.get("textures", "").split(";")
        require(all(re.fullmatch(KEY, key) for key in textures) and len(set(textures)) == len(textures),
                f"Invalid or duplicate textures list: {name}")
        require(set(textures) == {f"SamplerLUT{i}" for i in range(1, 5)},
                f"Missing or unexpected texture binding: {name}")
        for key in textures:
            require(key in settings, f"Missing texture path: {name}:{key}")
            target = resolve_reference(parent, settings[key])
            require(target.endswith(".png"), f"Unsupported texture file: {name}:{key}")
            contents(target)
        for key, value in settings.items():
            if key not in shader_keys and key not in textures:
                require(not re.search(r"\.(?:slangp?|png|jpe?g|tga|h|inc)$", value, re.IGNORECASE),
                        f"Unrecognized file reference: {name}:{key}")
    # Also check the bundled files even when no selected preset consumes a stage.
    for name in sorted(BUNDLED):
        shader(f"{PACK}/shaders/{name}")
    return dependencies


def check_zip_layout(raw, entries):
    """Require a complete ordinary ZIP layout, including non-indexed metadata.

    ZipFile primarily exposes the central directory and permits archive prefixes.
    Check local records too so unlisted records, gaps or local-only extra fields
    cannot disappear behind an otherwise correct member list and checksum.
    """
    end = len(raw) - 22

    def unpack(fmt, offset, boundary):
        size = struct.calcsize(fmt)
        require(0 <= offset <= boundary <= len(raw) and offset + size <= boundary,
                "Truncated ZIP structure")
        return struct.unpack_from(fmt, raw, offset)

    eocd = unpack("<4s4H2IH", end, len(raw))
    signature, disk, central_disk, disk_count, count, central_size, central_offset, comment = eocd
    require(signature == b"PK\x05\x06" and disk == central_disk == 0
            and disk_count == count == len(entries) and count < 0xffff and comment == 0,
            "Unsupported ZIP end record or multiple disks")
    require(central_offset < 0xffffffff and central_size < 0xffffffff
            and central_offset + central_size == end,
            "Unexpected ZIP central-directory bounds")

    local_records = []
    position = central_offset
    for info in entries:
        fields = unpack("<4s6H3I5H2I", position, end)
        (signature, made_by, needed, flags, method, time, date, crc, compressed,
         uncompressed, name_size, extra_size, comment_size, start_disk,
         internal, external, local_offset) = fields
        require(signature == b"PK\x01\x02", "Unexpected ZIP central-directory record")
        require(needed <= 20 and flags & ~0x800 == 0 and start_disk == 0
                and compressed < 0xffffffff and uncompressed < 0xffffffff
                and local_offset < 0xffffffff,
                "Unsupported ZIP flags, ZIP64 or multiple disks")
        require(extra_size == comment_size == 0, "Unexpected ZIP central metadata")
        next_position = position + 46 + name_size
        require(next_position <= end, "Truncated ZIP central filename")
        name = raw[position + 46:next_position]
        # Catalog members are ASCII. Comparing the raw names also rejects NUL
        # truncation and names normalized by a host's ZipInfo implementation.
        require(name == info.filename.encode("utf-8"), "Noncanonical ZIP central filename")
        require((made_by, needed, flags, method, crc, compressed, uncompressed,
                 internal, external, local_offset) ==
                ((info.create_system << 8) | info.create_version,
                 (info.reserved << 8) | info.extract_version, info.flag_bits,
                 info.compress_type, info.CRC, info.compress_size, info.file_size,
                 info.internal_attr, info.external_attr, info.header_offset),
                "ZIP central metadata/offset disagreement")
        local_records.append((local_offset, needed, flags, method, time, date,
                              crc, compressed, uncompressed, name))
        position = next_position
    require(position == end, "Unexpected bytes after ZIP central records")

    expected_offset = 0
    for record in sorted(local_records):
        (offset, needed, flags, method, time, date, crc, compressed,
         uncompressed, name) = record
        require(offset == expected_offset, "Unlisted ZIP prefix, record, gap or overlap")
        fields = unpack("<4s5H3I2H", offset, central_offset)
        (signature, local_needed, local_flags, local_method, local_time,
         local_date, local_crc, local_compressed, local_uncompressed,
         local_name_size, local_extra_size) = fields
        require(signature == b"PK\x03\x04", "Unexpected ZIP local record")
        require(local_extra_size == 0, "Unexpected ZIP local metadata")
        require((local_needed, local_flags, local_method, local_time, local_date,
                 local_crc, local_compressed, local_uncompressed) ==
                (needed, flags, method, time, date, crc, compressed, uncompressed),
                "ZIP local/central header disagreement")
        name_end = offset + 30 + local_name_size
        require(name_end <= central_offset, "Truncated ZIP local filename")
        require(raw[offset + 30:name_end] == name, "ZIP local/central filename disagreement")
        expected_offset = name_end + compressed
        require(expected_offset <= central_offset, "ZIP member overlaps the central directory")
    require(expected_offset == central_offset, "Unlisted bytes before ZIP central directory")


def check_zip(root, payload, root_readme):
    raw = read_bytes(root, ZIP, MAX_ZIP)
    checksum = hashlib.sha256(raw).hexdigest()
    section = re.search(r"^## Download checksum\s*\n(.*?)(?=^## |\Z)", root_readme,
                        re.MULTILINE | re.DOTALL)
    require(section is not None, "Missing README download checksum section")
    hashes = re.findall(r"(?<![0-9a-f])[0-9a-f]{64}(?![0-9a-f])", section[1])
    require(hashes == [checksum], "README ZIP checksum mismatch")
    require(ZIP in root_readme, "Missing README ZIP download path")
    # The release format uses ordinary ZIP without a prefix, suffix or archive comment.
    require(raw.startswith(b"PK\x03\x04") and raw[-22:-18] == b"PK\x05\x06",
            "Unexpected ZIP envelope/metadata")
    try:
        with zipfile.ZipFile(file_at(root, ZIP)) as archive:
            require(not archive.comment, "Unexpected ZIP comment metadata")
            entries = archive.infolist()
            require(len(entries) == len(payload), "ZIP member count mismatch")
            names = [info.filename for info in entries]
            require(len({n.casefold() for n in names}) == len(names), "Duplicate or case-alias ZIP member")
            require(set(names) == set(payload), "ZIP member list mismatch")
            check_zip_layout(raw, entries)
            for info in entries:
                safe_parts(info.orig_filename)
                mode = info.external_attr >> 16
                require(not info.is_dir() and stat.S_IFMT(mode) in (0, stat.S_IFREG)
                        and not mode & 0o111, f"Unsafe ZIP member type/mode: {info.filename}")
                require(not info.comment and not info.extra, f"Unexpected ZIP member metadata: {info.filename}")
                require(not info.flag_bits & 1 and info.compress_type in (zipfile.ZIP_STORED, zipfile.ZIP_DEFLATED),
                        f"Unsupported ZIP member encoding: {info.filename}")
                expected = payload[info.filename]
                require(info.file_size == len(expected), f"ZIP member size differs from source: {info.filename}")
                if info.compress_type == zipfile.ZIP_DEFLATED:
                    # The layout check established identical ASCII local names
                    # and no local extra fields. ZipFile otherwise permits bytes
                    # after the deflate endpoint inside a declared compressed span.
                    start = info.header_offset + 30 + len(info.filename.encode("utf-8"))
                    compressed = raw[start:start + info.compress_size]
                    decoder = zlib.decompressobj(-15)
                    decoded = decoder.decompress(compressed, len(expected) + 1)
                    require(decoder.eof and not decoder.unused_data and not decoder.unconsumed_tail
                            and len(decoded) == len(expected),
                            f"Invalid ZIP deflate stream or trailing data: {info.filename}")
                else:
                    require(info.compress_size == info.file_size,
                            f"Invalid stored ZIP member size: {info.filename}")
                require(archive.read(info) == expected, f"ZIP member bytes differ from source: {info.filename}")
    except (zipfile.BadZipFile, RuntimeError, NotImplementedError, zlib.error) as exc:
        raise ValidationError("Invalid or unreadable ZIP member") from exc
    return checksum


def validate(root, slang_root):
    """Validate supplied trees offline; CLI additionally verifies dependency Git identity."""
    data = manifest(root)
    presets, members = catalog(data)
    source_catalog(root, members)
    payload = {name: read_bytes(root, name) for name in sorted(members)}
    root_readme = text(read_bytes(root, "README.md"), "README.md")
    release_banner(root_readme, "README.md", data, len(presets))
    release_banner(text(payload[f"{PACK}/README.md"], f"{PACK}/README.md"),
                   f"{PACK}/README.md", data, len(presets))
    dependencies = check_dependencies(root, slang_root, payload, presets)
    checksum = check_zip(root, payload, root_readme)
    return {"version": data["version"], "presets": len(presets), "bundled_stages": len(BUNDLED),
            "zip_members": len(members), "shared_files": len(dependencies), "zip_sha256": checksum}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--root", type=Path, default=Path(__file__).resolve().parents[1])
    parser.add_argument("--slang-root", type=Path, required=True,
                        help="Clean checkout of libretro/slang-shaders at the manifest revision")
    args = parser.parse_args()
    try:
        data = manifest(args.root)
        revision = subprocess.run(["git", "-C", str(args.slang_root), "rev-parse", "HEAD"],
                                  capture_output=True, text=True, check=True, timeout=20).stdout.strip()
        require(revision == data["shared_revision"], "Shared shader Git revision mismatch")
        dirty = subprocess.run(["git", "-C", str(args.slang_root), "status", "--porcelain", "--untracked-files=all"],
                               capture_output=True, text=True, check=True, timeout=20).stdout
        require(not dirty, "Shared shader checkout has local changes")
        print(json.dumps({"passed": True, **validate(args.root, args.slang_root)}, sort_keys=True))
        return 0
    except (ValidationError, OSError, subprocess.SubprocessError) as exc:
        # Avoid runner-specific absolute paths or subprocess output in public CI logs.
        message = str(exc) if isinstance(exc, ValidationError) else type(exc).__name__
        print(f"Release check failed: {message}", file=sys.stderr)
        return 1


if __name__ == "__main__":
    sys.exit(main())
