# DecoderLab — dashboard visualization and portfolio showcase brief

**Audience:** researchers, PhD supervisors, QEC developers. **Status:** actionable design direction, not a screenshot or claim that these UI elements already exist.

## Creative direction: a premium scientific workstation

Imagine a blend of:
1. **Observability console** — tight navigation, status chip and well-structured analytical panels (not fake infrastructure telemetry).
2. **Modern scientific data explorer** — generous chart space, restrained gridlines, annotated uncertainty, responsive hover/focus inspection and accessible data tables.
3. **Quantum-code workbench** — precise Tanner/lattice geometry and syndrome events in time, with visible shot/run identity; not decorative quantum particles.

These are *visual reference descriptions*, not copied images or assets. Derive an original UI from the existing design tokens in `docs/DESIGN_SYSTEM.md`, then verify in a real browser.

Avoid generic SaaS landing hero gradients, giant vanity numbers, neon-glow-heavy dark themes, fake model accuracy and unexplained decorative visualizations.

## Screen 1 — Experiment Command Center (portfolio hero)

### Layout sketch (concept, not current implementation)

```text
┌────────────────────────────────────────────────────────────────────────────────────┐
│ DecoderLab   /   Experiments                        LOCAL RESEARCH   ● SIMULATED    │
├──────────────┬─────────────────────────────────────────────────────────────────────┤
│ Overview     │  Rotated surface-code memory           [Run / Import]  [Export ▾]    │
│ Experiments  │  d = 5 · rounds = 5 · Z-memory · PyMatching · seed = 42              │
│ Code Explorer│  circuit-level Stim noise · p = 0.005 · 10,000 shots                 │
│ Benchmarks   ├─────────────────────────────────────────────────────────────────────┤
│ Models       │  Logical failure rate   Failures / shots   Wilson 95% CI   Run state │
│  (planned)   │  ACTUAL DATA ONLY       ACTUAL COUNTS      ACTUAL BOUNDS  Completed │
│ Advisor      ├─────────────────────────────────────────┬───────────────────────────┤
│  (planned)   │  LOGICAL FAILURE ESTIMATE               │  CIRCUIT & REPRODUCIBILITY │
│              │  one point + 95% Wilson bounds           │  manifest · package vers. │
│              │  or an honest histogram for 1 run        │  circuit SHA · seed        │
│              │  No fake multi-p line from one point     │  Noise channel definitions│
│              ├─────────────────────────────────────────┴───────────────────────────┤
│              │  Accessible data table  ·  failures/shots  ·  CSV/SVG/JSON exports  │
└──────────────┴─────────────────────────────────────────────────────────────────────┘
```

The placeholder words `ACTUAL DATA ONLY` are instructions: populate only from a verified result. If none is present, render a branded, accessible empty state: "No verified run selected". If `illustrative`, prominently mark each panel "ILLUSTRATIVE — NOT A SIMULATION RESULT".

### Primary components

- Sidebar: Overview / Experiments / Code Explorer / Benchmarks, with Models and Advisor marked **planned**, not misleading active capabilities.
- Top bar: local-only engine badge, selected experiment + scientific status, accessible run/import/export actions.
- Configuration rail: selected preset, code family and distance, rounds, logical basis, noise model, decoder, shot limit and random seed.
- Four compact scientific KPI panels: logical failure estimate; **logical failures / shots**; **95% Wilson interval**; execution status or *measured* runtime if captured (never invented).
- Main visualization: one experimental observation as a point with confidence interval, or an interval plot/accurate binomial-count presentation. **No fake line chart from a single p value.**
- Provenance panel: `source=simulated`, engine versions, run id/manifest SHA, Stim circuit hash and exact noise-channel mapping.
- Accessible results table: same data as graph, keyboard focus, sortable/exportable where appropriate.
- Footer: explicit `Preview` status and last code/data build context.

## Chart concepts to implement incrementally

### A. Logical-error rate with confidence interval (showcase P0)
A clearly labelled point estimate for single preset p=0.005, with a vertical error bar for Wilson 95% bounds and a tooltip showing k failures / n shots. On log y, never replace zero observations with an arbitrary positive floor; show upper-bound annotation and allow linear/table mode. Plot labels `Physical error probability p` and `Logical failure probability`. **Sweep line charts are not part of v0.1 (#11).**

For two presets later, use separate panels and prominent noise-model labels; surface circuit-level LER and BB code-capacity block failure have different denominators/assumptions and **must not be directly ranked**.

### B. Interactive syndrome spacetime explorer (later unless minimally reproducible)
Use authentic detector metadata, actual detector `(x,y,t)` coordinates and a specific shot/syndrome identifier. 2D detector-layer playback with step slider, hover/focus description and event legend first; Three.js only where scientifically helpful. Never fabricate detector geometry or imply animated events came from the stored result without per-shot metadata.

### C. Code connectivity / Tanner graph (after verified matrices)
For surface code: stabilizer/detector graph from actual Stim reference. For BB: bipartite graph based on verified binary `H_X,H_Z` matrices, optional logical operator overlays, cycle/highlight inspection. Warn when projection is not geometrically physical. Avoid generic decorative node networks.

### D. Decoder comparison and training (post-preview)
Aligned experiments on the **same** code/noise/shots and hardware; plot logical failure with confidence bounds against measured latency and resources. Use Pareto view only when timing methodology is recorded. No neural benchmark cards until training and held-out evaluation actually exist.

### E. Export and reproducibility lane (showcase P0 / alpha P0)
User actions: download CSV with raw counts/CI/units, JSON run manifest with seed/versions/code/noise/basis/fingerprint/failure definition, and vector SVG. Data table and export must agree. Re-import/export must preserve identity and provenance.

## Interaction design requirements

- Actual plot hover + keyboard tooltip/focus inspection; table row and plot point share values.
- Main controls visible on small screens; chart is touch-scroll/resize safe, labels stay legible.
- Info button for each noise model and logical failure definition; no ambiguous shorthand without context.
- A "source" chip always visible: `Simulated`, `Illustrative`, `User-supplied — unverified`, or `Hardware-measured` (only if genuine).
- Loading skeleton, no-results state, invalid manifest recovery, backend offline, dependency missing and run failed/cancelled states.
- Minimum 44px touch targets, strong visible focus, screen-reader summaries and data-equivalent table. Respect reduced-motion.
- Performance budget: avoid WebGL for static single-point charts; lazy-load complex explorers; use existing library rather than adding a second charting stack without reason.
- Security: never automatically upload local manifest contents or expose unrestricted compute endpoints.

## Quality bar for the portfolio demo

1. Actual desktop screenshot at 1440×900; actual mobile screenshot near 390×844, showing polished responsive hierarchy.
2. Working keyboard navigation from preset selection to plot/table and export.
3. One clear authentic experiment story (config, sample count, failure definition, uncertainty, provenance, export/replay).
4. Browser test verifies that the displayed and exported raw numbers equal API response values. No screenshot-only mockups presented as deployed software.
5. A 60–90 second screen-recorded flow with title card, shot count, Wilson interval and simulation/noise model explanation. Avoid an inaccurate "world's best decoder" claim.
6. Use images in design discussions only as **inspiration**. The existing PR #7 running UI and its screenshot/test evidence are the baseline; improve that code rather than restarting it.

## Immediate Codex design assignment

Read PR #7 and `frontend/app/page.tsx`, `frontend/app/ler-plot.tsx`, `frontend/lib/chart.ts` before making changes. Compare against the sketch above, identify the biggest trustworthy UI/UX gap, and implement **one** small P0 fix with Playwright screenshots. Don't replace the working stack, rename branches, or expand scope into v0.1 BB simulation in this design task.

Related: `docs/PORTFOLIO_PREVIEW_ROADMAP.md`, issue #4, issue #9, issue #10, and the workflow PR #2.