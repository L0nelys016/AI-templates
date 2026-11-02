## Review levels

Review the diff against the intended behavior. For each finding, identify the changed line, a reachable condition, the violated expectation and its consequence. Check the caller, contract or test when the conclusion depends on it. Report one finding per root cause, highest impact first:

`[L3] path/file:line — when <condition>, <actual> instead of <expected>; <impact>. Fix: <action>.`

| Level | Name | Meaning | Action |
|---|---|---|---|
| L1 | Nit | local clarity issue with a specific improvement | optional, never block |
| L2 | Low | minor defect with limited impact | recommend a fix |
| L3 | Medium | material correctness or maintenance issue | fix before merge |
| L4 | High | serious regression on a reachable path | block merge |
| L5 | Critical | credible path to data loss, security compromise or severe contract break | stop; describe options for human decision |

Use the checklist and stack-specific levels below to guide inspection. Assign final severity by demonstrated impact. A migration, dependency, auth or architecture change listed under L5 is a prompt to check its consequences; required sign-off alone is not a defect.

Keep unresolved questions and pending approvals separate from findings. If no defects were found, say so. End with `needs human` for a critical finding or outstanding required decision, `changes requested` for other blocking findings, or `approve` otherwise.

## General checklist (all stacks)

**Junk and noise**
- dead code, unreachable branches, unused imports/variables/parameters/files
- commented-out code, stray logs/prints, debug leftovers, TODO without owner
- empty `catch`, empty methods/classes kept "for later"

**Null and empty references**
- unchecked null/undefined/None, missing guard on optional input
- blind `?.`/`??`/default that hides a bug instead of handling it
- empty collections/strings assumed non-empty; off-by-one on first/last element

**Simplicity**
- Flag complexity when you can identify what it makes unsafe or hard to change. A shorter alternative or a size threshold alone does not block a change.
- interface/abstract/factory/wrapper with a single implementation and no real need
- speculative generality: options, flags, hooks, generics nobody uses
- nesting deeper than 3, functions over ~30 lines, more than 4 parameters
- clever one-liner that needs decoding; cleverness must come from simplicity, not density

**Principles**
- DRY: copy-paste beyond the third occurrence; but also wrong early abstractions
- SOLID: class doing several jobs, dependency on concretions at boundaries, fat interfaces, inheritance where composition fits
- naming: vague (`data`, `manager`, `helper`), misleading, inconsistent with the codebase

**Correctness and safety**
- error handling: swallowed errors, lost context, exceptions used as flow control
- security: secrets in code, injection, missing authn/authz, unvalidated input → L4/L5
- concurrency: races, blocking calls in async paths, unawaited work
- resources: unreleased handles/subscriptions/listeners
- performance: allocations or I/O in hot paths, N+1, needless work in loops

**Tests**
- new logic without a test; tests asserting nothing; tests coupled to implementation

**Git hygiene**
- every new branch is pushed on creation and every commit is pushed immediately. Verify that the remote tip matches the local tip. A matching tip alone does not establish when earlier pushes happened.
- branch name matches `feature|bugfix|hotfix|refactor|docs|chore|temp|wip/<what>`
- every commit is Conventional Commits, title only, $commit_language text, **no co-author / no Claude mention**
- one task per branch, no unrelated changes mixed in
- PR: title with prefix and $pr_language text; description starts with `# $pr_heading` in $pr_language

When changing a review rule, try it on a known violation, a safe exception and an unrelated diff. Compare detected defects, false positives and token use on the same model. Narrow or drop rules that only add noise.
