import tempfile
import unittest
from pathlib import Path

import setup


class AgentTest(unittest.TestCase):
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
