import subprocess
import sys
import tarfile
import tempfile
import unittest
import zipfile
from pathlib import Path

HERE = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(HERE))
import build  # noqa: E402


class BuildTest(unittest.TestCase):
    def test_bundle_matches_setup_output(self):
        with tempfile.TemporaryDirectory() as tmp:
            tmp = Path(tmp)
            bundle = tmp / "claude-templates.py"
            bundle.write_bytes(build.bundle().encode("utf-8"))
            outs = []
            for script in (HERE / "setup.py", bundle):
                t = tmp / ("Проект с пробелом " + script.stem)
                t.mkdir()
                (t / "AGENTS.md").write_text("User instructions\n", encoding="utf-8")
                args = [sys.executable, "-I", str(script), "--target", str(t), "--stacks", "python,unity,react", "--agent", "all",
                        "--area", "game", "--extras", "all", "--forge", "both", "--yes"]
                result = subprocess.run(args, capture_output=True)
                self.assertEqual(result.returncode, 0, result.stderr)
                self.assertIn(str(t.resolve()), result.stdout.decode("utf-8"))
                first = (t / "AGENTS.md").read_bytes()
                result = subprocess.run(args, capture_output=True)
                self.assertEqual(result.returncode, 0, result.stderr)
                self.assertIn(str(t.resolve()), result.stdout.decode("utf-8"))
                self.assertTrue(first.startswith(b"User instructions"))
                self.assertEqual(first, (t / "AGENTS.md").read_bytes())
                outs.append({p.relative_to(t).as_posix(): p.read_bytes() for p in t.rglob("*") if p.is_file()})
            self.assertEqual(outs[0], outs[1])
            self.assertIn(".github/pull_request_template.md", outs[0])

    def test_bundle_has_no_templates_dir_dependency(self):
        with tempfile.TemporaryDirectory() as tmp:
            bundle = Path(tmp) / "c.py"
            bundle.write_bytes(build.bundle().encode("utf-8"))
            r = subprocess.run([sys.executable, "-I", str(bundle), "--version"], check=True, capture_output=True, text=True)
            self.assertEqual("claude-templates 0.3.0", r.stdout.strip())

    def test_localized_release_archives(self):
        with tempfile.TemporaryDirectory() as tmp:
            dist = Path(tmp) / "dist"
            build.build_release(dist)
            for lang, question in (("ru", "Записать перечисленные файлы?"), ("en", "Write the listed files?")):
                script = dist / f"claude-templates-{lang}.py"
                result = subprocess.run(
                    [sys.executable, "-I", str(script), "--target", tmp, "--stacks", "python",
                     "--area", "none", "--agent", "codex", "--extras", "none", "--commit-lang", "ru", "--pr-lang", "en"],
                    input=b"\n", capture_output=True, check=True)
                self.assertIn(question, result.stdout.decode("utf-8"))
                self.assertFalse((Path(tmp) / "AGENTS.md").exists())
                for os_name, launcher in (("Windows", "Install.cmd"), ("macOS", "Install.command")):
                    with zipfile.ZipFile(dist / f"{os_name}-{lang}.zip") as archive:
                        self.assertEqual(set(archive.namelist()), {launcher, "claude-templates.py"})
                        self.assertEqual(archive.read("claude-templates.py"), script.read_bytes())
                        self.assertEqual(build.launcher_bytes(launcher, lang), archive.read(launcher))
                        self.assertTrue(archive.getinfo(launcher).external_attr >> 16 & 0o111)
                with tarfile.open(dist / f"Linux-{lang}.tar.gz") as archive:
                    self.assertEqual(set(archive.getnames()), {"Install.sh", "claude-templates.py"})
                    self.assertEqual(archive.extractfile("claude-templates.py").read(), script.read_bytes())
                    self.assertTrue(archive.getmember("Install.sh").mode & 0o111)


if __name__ == "__main__":
    unittest.main()
