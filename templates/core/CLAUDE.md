## Core principles

- **KISS first.** Prefer the simplest design that preserves the required behavior and contracts.
- **YAGNI.** Build only what was asked. No speculative options, hooks, layers or "for later" code.
- **DRY with judgment.** Extract duplication on the third occurrence (rule of three). Wrong abstraction costs more than a copy.
- **SOLID.** Single responsibility per class/module; depend on abstractions at boundaries; prefer small interfaces; extend by composition, not inheritance.
- Fail fast: validate at trust boundaries, never swallow errors, never return silent defaults.
- Prefer small functions, shallow nesting and few parameters. Split code when doing so makes its behavior easier to follow.
- Names say what a thing is or does; comments explain only *why*, never *what*.
- No dead code, no commented-out code, no stray debug output, no unused imports/variables, no TODO without owner.
- Handle null/empty explicitly: never assume a reference is set; never hide a bug with a blind `?.` or default.
- Reuse existing helpers and dependencies. For a project pattern, find a working example and its test in code serving the same contract. When documenting a pattern, name its scope, the invariant, an example path and any exception. Enforce mechanical invariants in tests, lint or CI.
- Add a dependency only if the standard library or existing dependencies can't do it.
- Every non-trivial logic change ships with a test.

## Working method

- For non-trivial work, identify the trigger, expected behavior and a check that distinguishes success from failure. On handoff, keep the goal, decision, check result and next step.
- Start with the changed symbol, its callers and the nearest relevant test. Expand the search to answer a specific open question. Keep the first relevant error and enough log context to explain it.
- Repeat a check when code, environment or hypothesis has changed. After two attempts with the same failure, state what they ruled out (if anything) and choose a check that distinguishes the remaining causes.
- Verify API claims against the installed version, source or applicable docs. Report what you checked, the observed result and any remaining gap; never report an unrun check as passing.

## Git workflow

**One task = one branch.** Never commit to `main`/`master` directly. Create or switch to the task branch before the first change.

Publish **every new branch** as soon as you create it, even before its first new commit: `git push -u origin <branch>`. Use the project's designated remote if it differs from `origin`.

| Branch | Purpose |
|---|---|
| `feature/<what>` | new functionality |
| `bugfix/<what>` | bug fix |
| `hotfix/<what>` | urgent production fix |
| `refactor/<what>` | refactoring |
| `docs/<what>` | documentation |
| `chore/<what>` | housekeeping |
| `temp/<what>` or `wip/<what>` | draft / experiment |

**Commits: Conventional Commits, title only.**

| Type | Meaning |
|---|---|
| `feat:` | new feature |
| `fix:` | bug fix |
| `docs:` | documentation |
| `style:` | formatting (indent, whitespace) |
| `refactor:` | refactoring without logic change |
| `perf:` | optimization |
| `test:` | tests |
| `build:` | build system (Tauri, webpack, ...) |
| `ci:` | CI/CD settings |
| `chore:` | misc (.gitignore, dependencies) |
| `revert:` | revert |

- Commit has a **title only**: no body, no description.
- Commit titles are written in **$commit_language** (after the English type prefix), e.g. `$commit_example`.
- **Never** add `Co-Authored-By` or any mention of Claude/AI to commits or PRs.
- Commit one complete, verifiable change that can be reverted as a unit. Reading, searching and failed hypotheses do not need commits.
- Immediately after **every commit**, run `git push` to the branch's upstream before starting the next change. If a push fails, resolve the cause or report the blocker before continuing.
- Never force-push, rewrite pushed history, skip hooks or run `git reset --hard`.

**Pull requests: only when the user asks.**

1. Title: type prefix + body **in $pr_language**, e.g. `$pr_example`.
2. Description starts with the heading `# $pr_heading`, followed by a description in $pr_language.

## Human-in-the-loop (stop and ask)

Resolve uncertainty from code, tests and configuration first. Follow the local example for reversible implementation details. Ask when an unresolved choice changes user-visible behavior or a public contract, or is hard to reverse. Give the options and their consequences.

Get a human decision before carrying out an unapproved migration, destructive operation, breaking contract change, security policy change, major dependency change or architectural change. If the decision is already authorized, proceed within its scope.

## Definition of done

Check the expected behavior and run the applicable build, tests and linters. Resolve new failures or warnings; disclose anything unverified. The task branch must be published and its remote tip must match the final local commit.
