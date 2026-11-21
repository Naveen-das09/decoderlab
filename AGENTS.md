# DecoderLab — Instructions for Codex and other development agents

This is an open-source research product, not a demo. Read this file first, then `docs/PRODUCT_PRD.md`, `docs/DESIGN_SYSTEM.md`, and `docs/DEVELOPMENT_WORKFLOW.md`.

## Mission
Build a reproducible, visualization-first QEC research workbench. Start with rotated-surface-code memory experiments using direct Stim + PyMatching; add Deltakit via a separately versioned adapter. Later support QLDPC, BP/OSD, GNNs, transformers and bring-your-own-compute. Do not claim future components are implemented.

## Repository reality
- PR #1 (`feat/initial-backend-baseline`) contains the first prototype backend and tests. Until merged, the default `main` branch is intentionally minimal.
- Inspect open PRs, GitHub issues and current branch before starting. Avoid duplicate work and don't overwrite uncommitted user changes.
- Scientific simulation dependencies have not yet been validated together on actual installed Stim/PyMatching. Mock-based tests alone are insufficient.

## Working principles
1. One small vertical slice per task. State user story, acceptance criteria, changes, evidence and remaining risks.
2. Prefer a short design note or ADR before cross-cutting architectural changes. Maintain typed APIs and isolated simulator/decoder adapters.
3. Every chart must display units, definitions, sample counts, confidence/uncertainty, and provenance (illustrative, user-supplied unverified, simulated, or hardware-measured).
4. Scientific correctness: don't invent benchmark results or treat illustrative data as measured. Confirm sampled logical observables are not leaked into the decoder input. Define the noise channels, circuit identity, seed, sample independence and reference baselines.
5. Design: precise layout, responsive behavior, keyboard access, contrast, screen-reader-equivalent data tables, zoom/export, reduced motion and polished loading/empty/error states. No decorative chart junk.
6. Tests: run appropriate unit/integration tests, static checks and a local UI preview when applicable. Never say checks passed unless they actually ran; identify blockers.
7. Security/privacy: never log secrets, add credentials to Git, use unrestricted shell/network access, upload private hardware calibration data, publish checkpoints, or provision cloud/GPU resources without approval.
8. Git: work on a feature branch or isolated worktree; open a draft PR with tests and scientific/design checklist. Never push directly to `main`, self-merge, enable auto-merge, modify GitHub settings, deploy, or incur paid services without explicit approval.
9. Keep commits reviewable, update documentation, record decisions and use conventional commit titles where practical.
10. If permissions or dependencies block a task, stop safely and report exact evidence and a minimal unblock step, not a speculative success.

## Priorities
1. Review PR #1 and run genuine Stim/PyMatching integration validation (zero-noise and nonzero-noise).
2. Next.js/TypeScript design system and polished experiment dashboard shell with honest illustrative mode.
3. Connect trustworthy experiment API output to logical-error-rate charts with uncertainty, provenance and downloadable tables.
4. Add bounded asynchronous jobs, database persistence, quotas and auth before public experiments.
5. Expand Deltakit, QLDPC and neural training only after core workflows are trustworthy.


## Current delivery focus — portfolio preview before v0.1
For early demo deliverables and the current visual reference, read `docs/PORTFOLIO_PREVIEW_ROADMAP.md` and `docs/DASHBOARD_VISUALIZATION_BRIEF.md`. These are **targets, not release claims**. Preserve scope of v0.1 issue #9 (two scientific presets) while prioritizing a polished truthful surface-code dashboard preview by December 7. First inspect existing dashboard PR #7 and backend scientific PR #6 to avoid duplication. All work still follows branch/PR/CI review gates.

## Daily completion report
- Issue/goal and user-visible change
- Branch, commit(s), draft PR URL (or explicit no-change reason)
- Checks executed and results; screenshots or plot evidence if UI changed
- Scientific provenance/assumptions and accessibility/security review
- Blockers and next small increment

See `automation/DAILY_SPRINT_PROMPT.md` for the repeatable daily task.