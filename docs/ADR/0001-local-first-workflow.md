# ADR 0001 — Local-first Codex development with GitHub review gates

**Status:** Proposed, 2026-11-21

## Context
DecoderLab has accumulated four backend sprint prototypes in ChatGPT outputs. The actual public repository and draft PR #1 now exist. The owner wants a visible local folder, daily progress, professional review, and no new Codex Cloud/API expense.

## Decision
- GitHub is the durable source of truth.
- Use a Mac-local clone in `~/Projects/decoderlab`, opened as a Codex project.
- Implement in isolated branches/worktrees; drafts and CI before reviewed merges.
- Prefer one existing daily scheduled task with a local project environment when the owner attaches it in the desktop app. A GitHub-only scheduled task may otherwise continue as review/coordinator but must avoid duplicate writes.
- ChatGPT handles product/research coordination; Codex local handles code/tests; the human owner approves merges and external cost.
- No unattended paid cloud/GPU infrastructure, API keys, production deployments or full computer privileges.

## Trade-offs
- Laptop must remain awake/app open for reliable unattended local runs.
- ChatGPT GitHub connector cannot independently mount or authorize an arbitrary Mac folder.
- The local project task requires a one-time desktop association by the owner.
- The plan's Codex usage allowance may cap automated agent work; stop rather than purchase credits.

## Consequences / verification
The workflow is complete only after (1) PR is reviewed/merged, (2) local folder opened, (3) Codex can inspect files and run tests in it, and (4) one local scheduled run creates a reviewable change. Merely committing instructions does not satisfy these runtime conditions.
