import tempfile
import unittest
from pathlib import Path

import setup


class AgentTest(unittest.TestCase):
    def test_partial_reinstall_keeps_installed_profiles_in_sync(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            setup.apply(setup.build(root, ["python"], None, [], "github", agents=list(setup.AGENTS))[0])
            for rel in setup.AGENTS.values():
                path = root / rel
                path.write_text(f"before {rel}\n{setup.read(path)}after {rel}\n", encoding="utf-8")

            actions, _ = setup.build(root, ["react"], "web-frontend", [], "github", agents=["codex"],
                                     commit_lang="en", pr_lang="en")
            setup.apply(actions)
            rules = []
            for rel in setup.AGENTS.values():
                text = setup.read(root / rel)
                self.assertTrue(text.startswith(f"before {rel}\n"))
                self.assertTrue(text.endswith(f"after {rel}\n"))
                managed = text.split(setup.MD_MARKS[0])[1].split(setup.MD_MARKS[1])[0]
                rules.append(managed.replace("](../REVIEW.md)", "](REVIEW.md)"))
            self.assertEqual(len(set(rules)), 1)
            for fragment in ("## React", "## TypeScript", "## Area: Web frontend", "feat: add template",
                             "git reset --hard"):
                self.assertIn(fragment, rules[0])
            self.assertNotIn("## Python", rules[0])
            review = setup.read(root / "REVIEW.md")
            self.assertIn("## React", review)
            self.assertNotIn("## Python", review)

    def test_unselected_unmanaged_profile_is_untouched(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            path = root / "CLAUDE.md"
            path.write_bytes(b"User instructions\n")
            actions, _ = setup.build(root, ["python"], None, ["settings"], "github", agents=["codex"])
            setup.apply(actions)
            self.assertEqual(path.read_bytes(), b"User instructions\n")
            self.assertFalse((root / setup.AGENTS["copilot"]).exists())
            self.assertFalse((root / ".claude/settings.json").exists())

    def test_python_stack(self):
        with tempfile.TemporaryDirectory() as tmp:
            actions, _ = setup.build(Path(tmp), ["python", "react"], None,
                                     ["gitignore", "editorconfig"], "github")
            outputs = {p.name: s for p, s, _ in actions}
            self.assertIn("[*.py]", outputs[".editorconfig"])
            self.assertIn("__pycache__/", outputs[".gitignore"])
            self.assertIn("unittest", outputs["CLAUDE.md"])
            self.assertIn("Python", outputs["REVIEW.md"])

    def test_languages(self):
        with tempfile.TemporaryDirectory() as tmp:
            for commit in ("ru", "en"):
                for pr in ("ru", "en"):
                    actions, _ = setup.build(Path(tmp), ["react"], None, ["pr"], "both",
                                             commit_lang=commit, pr_lang=pr)
                    outputs = {p.name: s for p, s, _ in actions}
                    example = "feat: добавлен шаблон" if commit == "ru" else "feat: add template"
                    heading = "# Что сделано" if pr == "ru" else "# Summary"
                    self.assertIn(example, outputs["CLAUDE.md"])
                    for name in ("CLAUDE.md", "REVIEW.md", "pull_request_template.md"):
                        self.assertIn(heading, outputs[name])

    def test_output_paths(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            for agents in (["claude"], ["codex"], ["copilot"], list(setup.AGENTS)):
                actions, _ = setup.build(root, ["react"], None, ["settings"], "github", agents=agents)
                outputs = {p.relative_to(root).as_posix(): s for p, s, _ in actions}
                expected = {"REVIEW.md", *(setup.AGENTS[a] for a in agents)}
                if "claude" in agents:
                    expected.add(".claude/settings.json")
                self.assertEqual(set(outputs), expected)
                for a in agents:
                    link = "../REVIEW.md" if a == "copilot" else "REVIEW.md"
                    self.assertIn(f"]({link})", outputs[setup.AGENTS[a]])
