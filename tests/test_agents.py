import tempfile
import unittest
from pathlib import Path

import setup


class AgentTest(unittest.TestCase):
    def test_documented_markers_do_not_claim_or_replace_user_text(self):
        begin, end = setup.MD_MARKS
        example = f"Use {begin} and {end} as follows:\n\n```md\n{begin}\nmy example\n{end}\n```\n"
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            path = root / "CLAUDE.md"
            path.write_bytes(example.encode())
            setup.apply(setup.build(root, ["python"], None, [], "github", agents=["codex"])[0])
            self.assertEqual(path.read_bytes(), example.encode())
            setup.apply(setup.build(root, ["python"], None, [], "github", agents=["claude"])[0])
            setup.apply(setup.build(root, ["react"], None, [], "github", agents=["codex"])[0])
            content = setup.read(path)
            self.assertTrue(content.startswith(example))
            self.assertIn("## React", content)
            self.assertNotIn("## Python", content)

    def test_unselected_utf16_profile_does_not_block_install(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            path = root / "CLAUDE.md"
            original = "User instructions".encode("utf-16")
            path.write_bytes(original)
            setup.apply(setup.build(root, ["python"], None, [], "github", agents=["codex"])[0])
            self.assertEqual(path.read_bytes(), original)
            self.assertTrue((root / "AGENTS.md").is_file())

    def test_discovery_skips_links_outside_the_project(self):
        with tempfile.TemporaryDirectory() as tmp:
            base = Path(tmp)
            root = base / "project"
            root.mkdir()
            shared = base / "shared.md"
            original = "\n".join([setup.MD_MARKS[0], "shared rules", setup.MD_MARKS[1]]).encode()
            shared.write_bytes(original)
            try:
                (root / "CLAUDE.md").symlink_to(shared)
            except OSError as e:
                self.skipTest(f"symlink unavailable: {e}")
            setup.apply(setup.build(root, ["python"], None, [], "github", agents=["codex"])[0])
            self.assertEqual(shared.read_bytes(), original)

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
