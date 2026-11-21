# DecoderLab — local-first professional engineering workflow

## Source of truth
GitHub `Naveen-das09/decoderlab` stores issues, acceptance criteria, source, design/architecture notes, PRs, CI and releases. Do not treat chat messages or generated ZIPs as canonical after code is imported.

## Responsibilities
- **ChatGPT:** product scope, QEC research/design reviews, backlog curation and daily GitHub status reports.
- **Codex in local desktop app:** actual code changes and tests on the selected `decoderlab` local folder; attach the project before scheduling local work.
- **GitHub:** branches, immutable reviews, checks, decisions and history.
- **Human owner:** approve scientific claims, repository merging, spending, external secrets and deployments.

## One-time local setup
Follow `docs/LOCAL_SETUP_MAC.md`. Only after the local clone is opened as a project in the desktop app does local Codex have a visible workspace. A GitHub connection does not mount a laptop folder.

## Repeatable task lifecycle
1. Inspect `main`, open PRs, CI, recent commits, worktree and issue backlog.
2. Choose the smallest high-priority unblocked issue and write acceptance criteria.
3. Create a branch or isolated worktree (feature/, fix/, docs/, chore/).
4. Implement one coherent vertical slice plus tests, documentation and data provenance.
5. Run targeted tests, lint/typecheck and browser UI verification where relevant.
6. Push authorized changes and open **draft** PR; include screenshots/graphs for UI, results/assumptions for QEC.
7. GitHub CI runs, then human reviews and authorizes merge.
8. Daily status references actual links, files and checks—not aspirational features.

## Automation policy
A daily ChatGPT scheduled task already exists, approximately 08:00 IST. It can inspect and act through GitHub. To make a scheduled task operate on the **local Mac**, attach the `decoderlab` project directory as its environment in the desktop app; use an isolated Git worktree. If the app does not support changing the existing task's environment, create a *local Codex* task using `automation/DAILY_SPRINT_PROMPT.md`, and then pause the old code-writing task or change it to reporting only to avoid parallel agents conflicting.

Keep the Mac awake, logged in and the desktop app running for unattended local work. A sleeping, powered-off or disconnected Mac cannot serve as a reliable 24/7 coding host. Sandbox mode should be workspace-write with minimal necessary permissions, not full access. Never turn on auto-merge.

## Cost policy
Use local compute and existing ChatGPT Codex plan allowance. Never use API keys, paid inference endpoints, managed GPUs, cloud hosting, purchased credits or billable runners without separate consent. Stop when plan allowance is exhausted.

## Definition of Done
Acceptance criteria satisfied; actual tests run and results linked; screenshots and accessible table for visual changes; scientific assumptions/units/provenance documented; no new security or billing risks; PR reviewed. Branch creation or a speculative README is not feature completion.

## First two work items
1. Finish scientific integration validation for draft PR #1 and review its CI before merging.
2. Deliver a premium but honest Next.js dashboard shell: real typed contracts, prominent illustrative-data labeling, accessibility and responsive layout. No pretend real QPU feed.
