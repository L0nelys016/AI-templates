#!/usr/bin/env python3
"""Build localized standalone installers and platform archives for GitHub Releases."""
import io
import json
import sys
import tarfile
import zipfile
from pathlib import Path

HERE = Path(__file__).resolve().parent
ROOT_LINE = 'ROOT = Path(__file__).resolve().parent / "templates"  # build.py swaps this line in the bundle'
MESSAGES_LINE = "MESSAGES = {}  # build.py embeds the installer translations here"

SHIM = '''import atexit as _atexit, json as _json, shutil as _shutil, tempfile as _tempfile

_DATA = _json.loads(%r)


def _materialize():
    d = _tempfile.mkdtemp(prefix="claude-templates-")
    _atexit.register(_shutil.rmtree, d, ignore_errors=True)
    for rel, text in _DATA.items():
        p = Path(d) / rel
        p.parent.mkdir(parents=True, exist_ok=True)
        p.write_bytes(text.encode("utf-8"))
    return Path(d)


ROOT = _materialize()
'''


def bundle(lang="en"):
    data = {
        p.relative_to(HERE / "templates").as_posix(): p.read_bytes().decode("utf-8").replace("\r\n", "\n")
        for p in sorted((HERE / "templates").rglob("*")) if p.is_file()
    }
    src = (HERE / "setup.py").read_text(encoding="utf-8")
    if ROOT_LINE not in src:
        sys.exit("error: ROOT line in setup.py changed; update ROOT_LINE in build.py")
    if lang == "ru":
        if MESSAGES_LINE not in src:
            sys.exit("error: missing translations marker in setup.py")
        messages = json.loads((HERE / "locales/ru.json").read_text(encoding="utf-8"))
        src = src.replace(MESSAGES_LINE, f"MESSAGES = {messages!r}")
    return src.replace(ROOT_LINE, SHIM % json.dumps(data, ensure_ascii=False))


def launcher_bytes(name, lang):
    script = (HERE / name).read_text(encoding="utf-8")
    if lang == "ru":
        messages = json.loads((HERE / "locales/launchers.ru.json").read_text(encoding="utf-8"))
        for english, russian in messages[name].items():
            if english not in script:
                raise ValueError(f"Missing message in {name}: {english}")
            script = script.replace(english, russian)
        if name == "Install.cmd":
            script = script.replace("setlocal\n", "setlocal\nchcp 65001 >nul\n")
    if name == "Install.cmd":
        script = script.replace("\n", "\r\n")
    return script.encode("utf-8")


def build_release(dist):
    dist.mkdir(exist_ok=True)
    for lang in ("ru", "en"):
        installer = bundle(lang).encode("utf-8")
        (dist / f"claude-templates-{lang}.py").write_bytes(installer)
        for platform, launcher in (("macOS", "Install.command"), ("Windows", "Install.cmd"), ("Linux", "Install.sh")):
            files = {launcher: launcher_bytes(launcher, lang), "claude-templates.py": installer}
            if platform == "Linux":
                with tarfile.open(dist / f"Linux-{lang}.tar.gz", "w:gz") as archive:
                    for name, data in files.items():
                        entry = tarfile.TarInfo(name)
                        entry.mode = 0o755 if name == launcher else 0o644
                        entry.size = len(data)
                        archive.addfile(entry, io.BytesIO(data))
            else:
                with zipfile.ZipFile(dist / f"{platform}-{lang}.zip", "w") as archive:
                    for name, data in files.items():
                        entry = zipfile.ZipInfo(name)
                        entry.create_system = 3
                        entry.external_attr = (0o100755 if name == launcher else 0o100644) << 16
                        archive.writestr(entry, data, compress_type=zipfile.ZIP_DEFLATED)


if __name__ == "__main__":
    dist = HERE / "dist"
    build_release(dist)
    print(f"Built Russian and English installers in {dist}")
