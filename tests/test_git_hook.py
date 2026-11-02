import os
import subprocess
import tempfile
import unittest
from pathlib import Path

import setup


@unittest.skipIf(os.name == "nt", "native POSIX Git hook integration")
class HookTest(unittest.TestCase):
    def test_git_executes_generated_hook(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            actions, _ = setup.build(root, ["python"], None, ["commitlint"], "github")
            setup.apply(actions)

            def git(*args, check=True):
                return subprocess.run(["git", *args], cwd=root, check=check, capture_output=True)

            git("init")
            git("config", "core.hooksPath", ".githooks")
            git("config", "user.name", "CI")
            git("config", "user.email", "ci@example.invalid")
            git("commit", "--allow-empty", "-m", "feat: добавлен шаблон")
            rejected = git("commit", "--allow-empty", "-m", "без типа", check=False)
            self.assertNotEqual(rejected.returncode, 0)
            self.assertIn(b"commit-msg:", rejected.stderr)
