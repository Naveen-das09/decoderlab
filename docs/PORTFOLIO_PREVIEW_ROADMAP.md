# DecoderLab — early portfolio preview and alpha milestones

**Proposed planning targets as of 2026-11-21.** These dates are goals, **not guaranteed delivery commitments or claims of deployed functionality**.

## Three separate deliverables

| Target | Milestone | What must actually work | Public description |
| --- | --- | --- | --- |
| Now, 2026-11-21 | Honest portfolio WIP | Public GitHub repository with explicit link to current PRs, actual tests and limitations | "Open-source QEC research platform — in active development" |
| 2026-11-30 through 2026-12-07 | **Portfolio showcase / preview** | Visually strong, reproducible **rotated-surface-code** Command Center; real local Stim/PyMatching reference results imported from verifiable API/manifest, or labelled fixture mode; an interactive and accessible plot, shot counts, confidence interval, provenance, controls, screenshots and 60–90s demo video | "Interactive scientific dashboard preview" — not a released two-code research product |
| 2026-12-10 through 2026-12-20 | **Small runnable local alpha** | Fresh-clone instructions; bounded local surface-code run initiated from UI via typed loopback-only API; coherent empty/loading/error/cancel states; replayable JSON/CSV/SVG exports; one-click preset with seed/noise/decoder/versions shown; smoke/browser/scientific tests | "Local alpha — validated surface-code preset" |
| 2027-01-21 | **Full v0.1 research release** | Issue #9's TWO working local dashboard presets: validated rotated surface code circuit-level Stim/PyMatching **and** published BB `[[72,12,6]]` code-capacity X noise, perfect syndrome measurements, validated BP+OSD (#10). Independent researcher replay tests and release docs | "DecoderLab v0.1" only after approval and passing gates |

**Scope guard:** Surface-code physical-error sweeps (#11), BB circuit-level simulation, QLDPC families beyond the published reference, model training, advisor, Deltakit adapters, hosted SaaS and paid compute are **post-v0.1**. Do not block the December portfolio preview on the BB implementation; do not silently remove BB from January v0.1.

## The dependency-aware order for Codex

1. **Review existing work, don't regenerate it.** Dashboard draft PR #7 builds on workflow PR #2; validated surface-code scientific PR #6 builds on backend PR #1. Establish merge strategy with human review; do not auto-merge.
2. **Portfolio showcase vertical slice:** polish PR #7 Command Center; render scientifically honest *one-point* real surface-code result and uncertainty, source/status metadata and accessible table. A single physical-error setting is **not a p-sweep curve**. Use a well-marked illustrative/fixture mode for no-engine scenarios.
3. **Actual local run loop:** typed frontend → loopback-only FastAPI → bounded Stim/PyMatching job → result/manifest → dashboard → replayable export. Test server unavailable, timeouts, invalid request, excessive shot counts and malformed import; don't publicly expose synchronous compute.
4. **Parallel BB validation task (#10):** verify published matrices and logical operators, GF(2) commutation, logical count and deterministic cases before integrating BP+OSD. Surface-code circuit-level and BB code-capacity error rates are **not comparable on identical noise footing**.
5. **Pre-release quality:** use at least three independent researcher fresh-clone/replay checks for both presets before the January release (#9).

## Showcase review gates

- Screenshot at 1440x900 desktop and 390x844 mobile from the **actual** app; include keyboard/focus flow and readable panel hierarchies.
- At least one real Stim/PyMatching reference run from the validated scientific integration path, with true shot counts, logical failures, Wilson interval and circuit hash, and no fabricated live metrics.
- A compact research story: **configure → execute/import → inspect → verify uncertainty/provenance → export/replay**.
- Clear version/status: "Preview", "Local simulation", "Illustrative" when applicable. No made-up QPU telemetry, models or graph curves.
- Browser smoke tests for export, malformed/unavailable data and responsive/keyboard states; CI evidence on draft PR; screen capture of a reproducible demo.
- No paid service required. A public URL is optional: portfolio may link GitHub plus an annotated demo video/screenshot. Hosting/deployment only with owner approval.

## Suggested sprint for the next local Codex execution

**User story:** As a prospective research supervisor visiting my portfolio, I can understand an actual QEC experiment's outcome and trust the evidence within the first screen.

**Small vertical slice:** Improve the existing PR #7 first-screen information architecture and experiment provenance rail while preserving the running frontend. Show code and noise definition, decoder, seed, shots/failures, Wilson 95% bounds and engine status from verified contracts; make illustrative mode unmissable; do not add unrelated routes.

**Acceptance:** one responsive browser-verified screen, passing Playwright + types/lint/build, a table equivalent for all chart numbers, actual screenshots and draft PR commentary. If CI or scientific blockers prevent this, document them without inventing success.

## Portfolio wording

**Now:** "DecoderLab — open-source QEC research platform (in development). Building reproducible Stim/PyMatching simulation, confidence-aware logical failure analysis and a Next.js experiment dashboard."

**After preview is demonstrated:** "Built an interactive QEC experiment dashboard with a validated rotated-surface-code reference, uncertainty visualization, provenance and reproducible exports." Only use clauses that are independently verifiable in code/run artifacts.

Owner approves merging, release labels, deployment and paid resources.