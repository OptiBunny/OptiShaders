"""Exercise release checks with isolated copies of public package inputs.

These tests do not render shaders, use an installed RetroArch, or retain captures.
Run with --slang-root pointing to the pinned shared Slang checkout used by CI.
"""

from __future__ import annotations

import argparse
import copy
import hashlib
import io
import json
import os
from pathlib import Path
import re
import shutil
import stat
import struct
import tempfile
import unittest
import warnings
import zipfile

import validate_release


SOURCE_ROOT = Path(__file__).resolve().parents[1]
SHARED_ROOT: Path
ZIP_PATH = Path("downloads/OptiShaders-ColecoVision-Gearcoleco.zip")
PRESET_PATH = Path("OptiShaders/4K Flat/OptiShaders - ColecoVision - Composite 100.slangp")
STAGE_PATH = Path("OptiShaders/shaders/optishaders-guest-ntsc-pass1.slang")
SHARED_STAGE = Path("crt/shaders/guest/advanced/stock.slang")
SHARED_LUT = Path("crt/shaders/guest/advanced/lut/trinitron-lut.png")


class ReleaseMutationTests(unittest.TestCase):
    def setUp(self) -> None:
        self.temp = tempfile.TemporaryDirectory(prefix="optishaders-check-")
        self.addCleanup(self.temp.cleanup)
        base = Path(self.temp.name)
        self.root = base / "package"
        self.shared = base / "shared"
        self.root.mkdir()
        shutil.copytree(SOURCE_ROOT / "OptiShaders", self.root / "OptiShaders")
        shutil.copy2(SOURCE_ROOT / "README.md", self.root / "README.md")
        (self.root / "downloads").mkdir()
        shutil.copy2(SOURCE_ROOT / ZIP_PATH, self.root / ZIP_PATH)
        with zipfile.ZipFile(self.root / ZIP_PATH) as archive:
            self.member_count = len(archive.infolist())
        (self.root / "tools").mkdir()
        shutil.copy2(SOURCE_ROOT / "tools/release.json", self.root / "tools/release.json")
        self.release = json.loads((self.root / "tools/release.json").read_text(encoding="utf-8"))
        shutil.copytree(
            SHARED_ROOT / "crt/shaders/guest", self.shared / "crt/shaders/guest"
        )

    def check(self) -> dict:
        return validate_release.validate(self.root, self.shared)

    def reject(self, words: str) -> None:
        with self.assertRaisesRegex(validate_release.ValidationError, "(?i)" + words):
            self.check()

    def replace(self, path: Path, old: str, new: str) -> None:
        target = self.root / path
        data = target.read_bytes()
        self.assertIn(old.encode(), data)
        target.write_bytes(data.replace(old.encode(), new.encode(), 1))

    def preset_value(self, key: str, value: str) -> None:
        target = self.root / PRESET_PATH
        data = target.read_bytes()
        replacement = f'{key} = "{value}"'.encode()
        data, count = re.subn(rb"(?m)^" + key.encode() + rb" = [^\r\n]*", lambda _: replacement, data)
        self.assertEqual(count, 1)
        target.write_bytes(data)

    def refresh_checksum(self) -> None:
        target = self.root / "README.md"
        digest = hashlib.sha256((self.root / ZIP_PATH).read_bytes()).hexdigest()
        data, count = re.subn(rb"(?m)^[0-9a-f]{64}\r?$", digest.encode(), target.read_bytes())
        self.assertEqual(count, 1)
        target.write_bytes(data)

    @staticmethod
    def member_info(name: str) -> zipfile.ZipInfo:
        info = zipfile.ZipInfo(name, (2026, 1, 1, 0, 0, 0))
        # Keep deliberately malformed names verbatim, including on Windows.
        info.filename = name
        info.orig_filename = name
        info.create_system = 3
        info.external_attr = (stat.S_IFREG | 0o644) << 16
        info.compress_type = zipfile.ZIP_DEFLATED
        return info

    def sync_zip(self) -> None:
        """Keep changed fixture bytes and checksum in sync for non-ZIP tests."""
        with zipfile.ZipFile(self.root / ZIP_PATH, "w") as output:
            for path in sorted((self.root / "OptiShaders").rglob("*")):
                if path.is_file():
                    name = path.relative_to(self.root).as_posix()
                    output.writestr(self.member_info(name), path.read_bytes())
        self.refresh_checksum()

    def rewrite_zip(self, edit, comment: bytes = b"") -> None:
        """Mutate member records in memory; never extract untrusted ZIP entries."""
        target = self.root / ZIP_PATH
        with zipfile.ZipFile(target) as archive:
            members = [(copy.copy(info), archive.read(info)) for info in archive.infolist()]
        members = edit(members)
        with warnings.catch_warnings():
            warnings.simplefilter("ignore", UserWarning)  # Deliberate duplicate fixture.
            with zipfile.ZipFile(target, "w") as archive:
                archive.comment = comment
                for info, data in members:
                    archive.writestr(info, data)
        self.refresh_checksum()

    def zip_payload(self) -> dict[str, bytes]:
        with zipfile.ZipFile(self.root / ZIP_PATH) as archive:
            names = archive.namelist()
            self.assertEqual(len(names), self.member_count)
            self.assertEqual(len(set(names)), self.member_count)
            return {info.filename: archive.read(info) for info in archive.infolist()}

    def test_current_pack_and_historical_preset_headers_pass(self) -> None:
        self.assertIsInstance(self.check(), dict)
        target = self.root / PRESET_PATH
        target.write_bytes(b"# Historical profile note: v0.1.2.\n" + target.read_bytes())
        self.sync_zip()
        self.assertIsInstance(self.check(), dict)

    def test_rebuilt_archive_with_same_payload_passes(self) -> None:
        self.sync_zip()
        self.assertIsInstance(self.check(), dict)

    def test_missing_shared_stage(self) -> None:
        (self.shared / SHARED_STAGE).unlink()
        self.reject("missing|dependency|file")

    def test_missing_lookup_image(self) -> None:
        (self.shared / SHARED_LUT).unlink()
        self.reject("missing|dependency|file")

    def test_wrong_case_reference_even_on_windows(self) -> None:
        self.preset_value("shader0", "../../crt/shaders/guest/advanced/Stock.slang")
        self.sync_zip()
        self.reject("case|missing|path|dependency|file")

    def test_unsafe_shader_paths(self) -> None:
        for value in (
            "../../../outside.slang",
            "/outside.slang",
            "C:/outside.slang",
            "//server/share/outside.slang",
            "https://example.invalid/stage.slang",
        ):
            with self.subTest(path=value):
                self.preset_value("shader0", value)
                self.sync_zip()
                self.reject("unsafe|path|reference|outside|escape|absolute")

    def test_unsafe_texture_path(self) -> None:
        self.preset_value("SamplerLUT1", "../../../outside.png")
        self.sync_zip()
        self.reject("unsafe|path|reference|outside|escape")

    def test_missing_required_texture_list_entry(self) -> None:
        self.preset_value("textures", "SamplerLUT1;SamplerLUT2;SamplerLUT3")
        self.sync_zip()
        self.reject("texture.*binding")

    def test_missing_required_texture_path(self) -> None:
        target = self.root / PRESET_PATH
        data, count = re.subn(rb'(?m)^SamplerLUT4 = [^\r\n]*\r?\n', b"", target.read_bytes())
        self.assertEqual(count, 1)
        target.write_bytes(data)
        self.sync_zip()
        self.reject("missing texture path")

    def test_duplicate_assignment(self) -> None:
        with (self.root / PRESET_PATH).open("ab") as out:
            out.write(b'\nshader0 = "../../crt/shaders/guest/advanced/stock.slang"\n')
        self.sync_zip()
        self.reject("duplicate")

    def test_inherited_preset_is_not_silently_skipped(self) -> None:
        with (self.root / PRESET_PATH).open("ab") as out:
            out.write(b'\n#reference "other.slangp"\n')
        self.sync_zip()
        self.reject("reference|inherit|unsupported|directive")

    def test_missing_pass_assignment(self) -> None:
        target = self.root / PRESET_PATH
        data, count = re.subn(rb'(?m)^shader17 = [^\r\n]*\r?\n', b"", target.read_bytes())
        self.assertEqual(count, 1)
        target.write_bytes(data)
        self.sync_zip()
        self.reject("pass|shader|missing|stage")

    def test_inconsistent_pass_count(self) -> None:
        self.preset_value("shaders", "17")
        self.sync_zip()
        self.reject("pass|shader|count|stage")

    def test_corrected_stages_must_be_used(self) -> None:
        original = (self.root / PRESET_PATH).read_bytes()
        for index, filename in ((11, "ntsc-pass1.slang"), (16, "ntsc-pass2.slang")):
            with self.subTest(pass_index=index):
                (self.root / PRESET_PATH).write_bytes(original)
                self.preset_value(f"shader{index}", f"../../crt/shaders/guest/advanced/{filename}")
                self.sync_zip()
                self.reject("bundled|stage|shader|corrected")

    def test_missing_include_from_bundled_stage(self) -> None:
        with (self.root / STAGE_PATH).open("ab") as out:
            out.write(b'\n#include "absent.slang"\n')
        self.sync_zip()
        self.reject("include|missing|dependency|file")

    def test_nested_shared_include_must_resolve(self) -> None:
        helper = self.shared / SHARED_STAGE.parent / "test-include.slang"
        helper.write_bytes(b'#include "absent.slang"\n')
        with (self.shared / SHARED_STAGE).open("ab") as out:
            out.write(b'\n#include "test-include.slang"\n')
        self.reject("include|missing|dependency|file")

    def test_nested_shared_include_inside_tree_passes(self) -> None:
        helper = self.shared / SHARED_STAGE.parent / "test-include.slang"
        helper.write_bytes(b"// An inert test include.\n")
        with (self.shared / SHARED_STAGE).open("ab") as out:
            out.write(b'\n#include "test-include.slang"\n')
        self.assertIsInstance(self.check(), dict)

    def test_cyclic_shared_include_is_rejected(self) -> None:
        helper = self.shared / SHARED_STAGE.parent / "test-include.slang"
        helper.write_bytes(b'#include "stock.slang"\n')
        with (self.shared / SHARED_STAGE).open("ab") as out:
            out.write(b'\n#include "test-include.slang"\n')
        self.reject("cyclic.*include")

    def test_absolute_include_is_rejected(self) -> None:
        with (self.shared / SHARED_STAGE).open("ab") as out:
            out.write(b'\n#include "/outside.slang"\n')
        self.reject("include|unsafe|path|absolute")

    def test_unsupported_include_is_not_silently_skipped(self) -> None:
        with (self.shared / SHARED_STAGE).open("ab") as out:
            out.write(b"\n#include UNREVIEWED_INCLUDE\n")
        self.reject("include|unsupported|syntax")

    def make_symlink(self, link: Path, target: Path) -> None:
        try:
            os.symlink(target, link)
        except OSError as exc:
            if os.name == "nt" and getattr(exc, "winerror", None) == 1314:
                self.skipTest("Windows account cannot create symlinks; Linux CI covers this case")
            raise

    def test_bundled_stage_symlink_is_rejected(self) -> None:
        stage = self.root / STAGE_PATH
        outside = Path(self.temp.name) / "outside.slang"
        outside.write_bytes(stage.read_bytes())
        stage.unlink()
        self.make_symlink(stage, outside)
        self.reject("link|regular|unsafe|outside|path")

    def test_shared_dependency_symlink_is_rejected(self) -> None:
        stage = self.shared / SHARED_STAGE
        outside = Path(self.temp.name) / "outside.slang"
        outside.write_bytes(stage.read_bytes())
        stage.unlink()
        self.make_symlink(stage, outside)
        self.reject("link|regular|unsafe|outside|path")

    def test_unexpected_source_file_even_when_zipped(self) -> None:
        (self.root / "OptiShaders/private.log").write_bytes(b"synthetic extra payload\n")
        self.sync_zip()
        self.reject("unexpected|member|catalog|file|membership")

    def test_missing_bundled_stage(self) -> None:
        (self.root / STAGE_PATH).unlink()
        self.sync_zip()
        self.reject("missing|stage|catalog|file|membership")

    def test_missing_license(self) -> None:
        (self.root / "OptiShaders/licenses/Coleco-NTSC-MIT.txt").unlink()
        self.sync_zip()
        self.reject("missing|license|catalog|file|membership")

    def test_release_banner_versions_must_match(self) -> None:
        version = self.release["version"]
        different = "999.0" if version != "999.0" else "999.1"
        self.replace(Path("README.md"), f"**v{version}", f"**v{different}")
        self.reject("version|banner")

    def test_pack_version_must_match_manifest(self) -> None:
        version = self.release["version"]
        different = "999.0" if version != "999.0" else "999.1"
        self.replace(Path("OptiShaders/README.md"), f"**v{version}", f"**v{different}")
        self.sync_zip()
        self.reject("version|banner")

    def test_documented_preset_count_must_match(self) -> None:
        count = len(self.release["preset_folders"]) * len(self.release["looks"])
        self.replace(Path("README.md"), f"{count} presets", f"{count - 1} presets")
        self.reject("count|banner|preset")

    def test_stale_download_checksum(self) -> None:
        readme = self.root / "README.md"
        data, count = re.subn(rb"(?m)^[0-9a-f]{64}\r?$", b"0" * 64, readme.read_bytes())
        self.assertEqual(count, 1)
        readme.write_bytes(data)
        self.reject("checksum|sha")

    def test_source_change_without_rebuilt_zip(self) -> None:
        with (self.root / STAGE_PATH).open("ab") as out:
            out.write(b"\n// Synthetic stale-archive check.\n")
        self.reject("bytes|content|mismatch|differ|payload")

    def test_changed_zip_bytes_despite_updated_checksum(self) -> None:
        def edit(members):
            for index, (info, data) in enumerate(members):
                if info.filename == STAGE_PATH.as_posix():
                    members[index] = (info, data + b"\n// Synthetic stale-source check.\n")
                    break
            else:
                self.fail("Expected shader member missing from fixture")
            return members
        self.rewrite_zip(edit)
        self.reject("bytes|content|mismatch|differ|payload|size")

    def test_same_length_zip_change_despite_updated_checksum(self) -> None:
        def edit(members):
            for index, (info, data) in enumerate(members):
                if info.filename == STAGE_PATH.as_posix():
                    members[index] = (info, bytes([data[0] ^ 1]) + data[1:])
                    break
            else:
                self.fail("Expected shader member missing from fixture")
            return members
        self.rewrite_zip(edit)
        self.reject("bytes differ")

    def test_missing_zip_member(self) -> None:
        self.rewrite_zip(lambda members: members[1:])
        self.reject("missing|member|count|membership")

    def test_extra_zip_member(self) -> None:
        self.rewrite_zip(lambda members: members + [(self.member_info("OptiShaders/AGENTS.md"), b"extra\n")])
        self.reject("unexpected|member|count|membership")

    def test_duplicate_zip_member(self) -> None:
        self.rewrite_zip(lambda members: members[:-1] + [members[0]])
        self.reject("duplicate")

    def test_case_alias_zip_member(self) -> None:
        def edit(members):
            info = copy.copy(members[0][0])
            info.filename = info.filename.swapcase()
            return members[:-1] + [(info, members[0][1])]
        self.rewrite_zip(edit)
        self.reject("case.alias|duplicate")

    def test_unsafe_zip_paths(self) -> None:
        original = (self.root / ZIP_PATH).read_bytes()
        for name in ("../outside.txt", "/outside.txt", "C:/outside.txt", "OptiShaders\\README.md"):
            with self.subTest(name=name):
                (self.root / ZIP_PATH).write_bytes(original)
                self.rewrite_zip(lambda members: members[:-1] + [(self.member_info(name), b"x")])
                self.reject("unsafe.*path|member list|membership|duplicate|canonical|name")

    def test_noncanonical_zip_member_name(self) -> None:
        def edit(members):
            for info, _ in members:
                if info.filename == "OptiShaders/README.md":
                    info.filename = "OptiShaders\\README.md"
                    info.orig_filename = info.filename
                    break
            else:
                self.fail("Expected README member missing from fixture")
            return members
        self.rewrite_zip(edit)
        self.reject("unsafe|path|name|canonical|member")

    def test_hidden_local_record_before_zip(self) -> None:
        payload = self.zip_payload()
        prefix = io.BytesIO()
        with zipfile.ZipFile(prefix, "w") as archive:
            archive.writestr(self.member_info("unlisted.txt"), b"synthetic unlisted payload\n")
        with zipfile.ZipFile(prefix) as archive:
            local_record = prefix.getvalue()[:archive.start_dir]
        target = self.root / ZIP_PATH
        target.write_bytes(local_record + target.read_bytes())
        self.refresh_checksum()
        self.assertEqual(self.zip_payload(), payload)
        self.reject("layout|prefix|offset|unlisted|header|leading|unexpected")

    def test_local_only_extra_metadata(self) -> None:
        payload = self.zip_payload()
        target = self.root / ZIP_PATH
        with zipfile.ZipFile(target) as archive:
            local_offset = archive.infolist()[0].header_offset
            central_offset = archive.start_dir
        raw = bytearray(target.read_bytes())
        name_length, old_extra_length = struct.unpack_from("<HH", raw, local_offset + 26)
        insert_at = local_offset + 30 + name_length + old_extra_length
        extra = b"\xfe\xca\x04\x00test"
        raw[insert_at:insert_at] = extra
        struct.pack_into("<H", raw, local_offset + 28, old_extra_length + len(extra))
        position = central_offset + len(extra)
        entries = 0
        while raw[position:position + 4] == b"PK\x01\x02":
            name_length, extra_length, comment_length = struct.unpack_from("<HHH", raw, position + 28)
            offset = struct.unpack_from("<I", raw, position + 42)[0]
            if offset >= insert_at:
                struct.pack_into("<I", raw, position + 42, offset + len(extra))
            position += 46 + name_length + extra_length + comment_length
            entries += 1
        self.assertEqual(entries, self.member_count)
        self.assertEqual(raw[position:position + 4], b"PK\x05\x06")
        struct.pack_into("<I", raw, position + 16, central_offset + len(extra))
        target.write_bytes(raw)
        self.refresh_checksum()
        self.assertEqual(self.zip_payload(), payload)
        self.reject("layout|local|extra|metadata|header")

    def test_trailing_unlisted_bytes(self) -> None:
        payload = self.zip_payload()
        with (self.root / ZIP_PATH).open("ab") as out:
            out.write(b"synthetic unlisted trailing payload\n")
        self.refresh_checksum()
        self.assertEqual(self.zip_payload(), payload)
        self.reject("layout|trailing|end|unexpected")

    def test_unlisted_bytes_after_deflate_stream(self) -> None:
        payload = self.zip_payload()
        target = self.root / ZIP_PATH
        with zipfile.ZipFile(target) as archive:
            first = archive.infolist()[0]
            local_offset = first.header_offset
            central_offset = archive.start_dir
            compressed_size = first.compress_size
            self.assertEqual(first.compress_type, zipfile.ZIP_DEFLATED)
        raw = bytearray(target.read_bytes())
        name_length, extra_length = struct.unpack_from("<HH", raw, local_offset + 26)
        insert_at = local_offset + 30 + name_length + extra_length + compressed_size
        hidden = b"synthetic unlisted compressed trailing payload\n"
        raw[insert_at:insert_at] = hidden
        struct.pack_into("<I", raw, local_offset + 18, compressed_size + len(hidden))
        position = central_offset + len(hidden)
        entries = 0
        while raw[position:position + 4] == b"PK\x01\x02":
            name_length, extra_length, comment_length = struct.unpack_from("<HHH", raw, position + 28)
            offset = struct.unpack_from("<I", raw, position + 42)[0]
            if offset == local_offset:
                struct.pack_into("<I", raw, position + 20, compressed_size + len(hidden))
            elif offset >= insert_at:
                struct.pack_into("<I", raw, position + 42, offset + len(hidden))
            position += 46 + name_length + extra_length + comment_length
            entries += 1
        self.assertEqual(entries, self.member_count)
        self.assertEqual(raw[position:position + 4], b"PK\x05\x06")
        struct.pack_into("<I", raw, position + 16, central_offset + len(hidden))
        target.write_bytes(raw)
        self.refresh_checksum()
        self.assertEqual(self.zip_payload(), payload)
        self.reject("compressed|deflate|trailing|unused|stream")

    def test_zip_symlink(self) -> None:
        def edit(members):
            members[0][0].external_attr = (stat.S_IFLNK | 0o777) << 16
            return members
        self.rewrite_zip(edit)
        self.reject("link|regular|type|mode|metadata")

    def test_zip_archive_comment(self) -> None:
        self.rewrite_zip(lambda members: members, comment=b"synthetic metadata")
        self.reject("comment|metadata")

    def test_zip_member_comment(self) -> None:
        def edit(members):
            members[0][0].comment = b"synthetic metadata"
            return members
        self.rewrite_zip(edit)
        self.reject("comment|metadata")

    def test_zip_extra_metadata(self) -> None:
        def edit(members):
            members[0][0].extra = b"\xfe\xca\x00\x00"
            return members
        self.rewrite_zip(edit)
        self.reject("extra|metadata")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--slang-root", required=True, type=Path)
    args, unittest_args = parser.parse_known_args()
    SHARED_ROOT = args.slang_root.resolve()
    if not (SHARED_ROOT / SHARED_STAGE).is_file():
        parser.error("--slang-root must contain the checked-out shared Guest stages")
    unittest.main(argv=[__file__, *unittest_args], verbosity=2)
