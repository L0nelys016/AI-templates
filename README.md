# AI templates

[Русская версия](README.ru.md)

Install project instructions for Claude, Codex and GitHub Copilot in VS Code.

## Download the installer

Requires Python 3.9 or later.

| Platform | Download | How to start |
|---|---|---|
| macOS | [macOS.zip](https://github.com/L0nelys016/AI-templates/releases/latest/download/macOS.zip) | Extract the archive and double-click `Install.command` in Finder. |
| Windows | [Windows.zip](https://github.com/L0nelys016/AI-templates/releases/latest/download/Windows.zip) | Extract the archive and double-click `Install.cmd`. |
| Linux | [Linux.tar.gz](https://github.com/L0nelys016/AI-templates/releases/latest/download/Linux.tar.gz) | Extract the archive and run `./Install.sh` from the extracted folder. |

Stacks: **C#**, **Unity** (implies C#), **Python**, **Node.js**, **TypeScript**, **React** (implies TypeScript).
Areas: `backend-api`, `web-frontend`, `game`, `desktop-app`, `library-cli`.

## Usage

Requires Python 3.9+ (stdlib only).

```bash
python setup.py                       # interactive
python setup.py --target ../MyGame --stacks unity --area game --extras all --forge both --yes
python setup.py --target . --stacks react,nodejs --dry-run
```

| Flag | Meaning |
|---|---|
| `--agent` | `claude,codex,copilot`, `all`, `both` (Claude + Codex), default Claude |
| `--commit-lang` | Commit subject language (`ru` / `en`, default `ru`) |
| `--pr-lang` | PR title and description language (`ru` / `en`, default `ru`) |
| `--target` | project folder |
| `--stacks` | `csharp,unity,nodejs,typescript,react,python` |
| `--area` | one area or `none` |
| `--extras` | `settings,pr,commitlint,editorconfig,gitignore` / `all` / `none` |
| `--forge` | `github`, `gitea`, `both` (PR template folder) |
| `--dry-run` | show changes only |
| `--yes` | no prompts |
| `--force` | overwrite existing extras |

## What gets written

- `CLAUDE.md` (Claude), `AGENTS.md` (Codex), `.github/copilot-instructions.md` (Copilot), `REVIEW.md`: the rules are placed between `claude-templates:begin/end` markers. Re-running updates only that block; your own text is kept.
- `settings` (Claude): `.claude/settings.json` merged (no Claude co-author/attribution, deny force-push and `reset --hard`).
- `pr`: `pull_request_template.md` in `.github/` and/or `.gitea/`.
- `commitlint`: Node stacks get commitlint + husky; others get plain `.githooks/` (commit format, title only, no co-author, branch name).
- `editorconfig`, `gitignore`: per selected stack (gitignore is a marked block).

The script never runs `npm` or `git`; it prints the follow-up commands.

## macOS Finder

Double-click `Install.command` in the repository, or extract the `macOS.zip` release asset and double-click `Install.command` there. Select your project in the folder picker. The English-language wizard explains the choices and previews the files before asking for confirmation. Requires Python 3.9 or newer.

## macOS Terminal

From this repository, start the wizard or try the installation in a separate project. Requires Python 3.9+.

```bash
python3 setup.py
mkdir -p "../Demo Python"
python3 setup.py --target "../Demo Python" --stacks python --agent all --commit-lang ru --pr-lang en --extras all --yes --dry-run
python3 setup.py --target "../Demo Python" --stacks python --agent all --commit-lang ru --pr-lang en --extras all --yes
```

Build and run the standalone installer below. For a downloaded release asset, substitute its path.

```bash
python3 build.py
python3 dist/claude-templates.py
```

Codex reads project instructions from the repository root down to the working directory. In each directory a nonempty `AGENTS.override.md` takes precedence over `AGENTS.md`. More local rules win conflicts. The default combined project instruction budget is 32 KiB. [Codex](https://learn.chatgpt.com/docs/agent-configuration/agents-md)

CI checks PRs on macOS, Linux and Windows. Once the workflow is on the default branch, select Actions → CI → Run workflow to run just `macos-latest`.

## Adding a stack

Create `templates/stacks/<name>/CLAUDE.md` and `REVIEW.md`, add the name to `STACKS` (and `IMPLIES` if needed) in `setup.py`. Keep a fragment under ~60 lines.

## Tests

```bash
python -m unittest discover tests
```

## Download (no clone needed)

Extract the archive for your platform. On macOS open `Install.command` from `macOS.zip`. On Windows open `Install.cmd` from `Windows.zip`. On Linux extract `Linux.tar.gz` and run `./Install.sh` from its directory. Each archive includes the installer and requires Python 3.9 or later.

Take `claude-templates.py` from the [latest release](../../releases/latest) and run `python claude-templates.py`. It is a single file with all templates embedded. Build it yourself with `python build.py` (output: `dist/claude-templates.py`); pushing a `v*` tag publishes a release automatically.
