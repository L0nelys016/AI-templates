import os
import shutil
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

import build


@unittest.skipUnless(sys.platform == "darwin", "Finder launcher runs on macOS")
class MacLauncherTest(unittest.TestCase):
    def test_release_wizard_preview_and_install(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            launcher = root / "Install.command"
            shutil.copy2(build.HERE / launcher.name, launcher)
            (root / "claude-templates.py").write_text(build.bundle(), encoding="utf-8")
            project = root / "Мой проект"
            project.mkdir()
            # The automated runner supplies the folder normally selected in Finder.
            picker = root / "osascript"
            picker.write_text('#!/bin/sh\nprintf "%s\\n" "$PROJECT"\n')
            picker.chmod(0o755)
            env = dict(os.environ, PATH=str(root) + os.pathsep + os.environ["PATH"], PROJECT=str(project))
            for confirm in ("", "д"):
                result = subprocess.run([str(launcher)], input=f"6\n\n2\n1\n2\n\n{confirm}\n\n",
                                        text=True, capture_output=True, env=env, cwd=project)
                self.assertEqual(result.returncode, 0, result.stderr)
                self.assertIn("Записать перечисленные файлы?", result.stdout)
                self.assertEqual((project / "AGENTS.md").exists(), bool(confirm))
