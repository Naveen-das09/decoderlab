# DecoderLab development roadmap

## Next: verified simulator foundation
- Install Stim and PyMatching in a dedicated integration CI job.
- Validate zero-noise deterministic reference, nonzero-noise execution,
  detector/observable dimensions and decoder output.
- Fix scientific or API mismatches before charting actual runs.

## Visualization-first research dashboard
- Next.js + TypeScript app shell with clear product information architecture.
- Plotly/accessible charts for LER vs p, uncertainty bounds and comparative runs.
- Scalable syndrome spacetime explorer and lattice visualization.
- Responsive layouts, keyboard navigation, reduced motion, loading/empty/error
  states, CSV/SVG export and explicit data provenance.
- Demo datasets must always be visibly labeled illustrative.

## Safe hosted execution
- Job queue + worker with rate limits, quotas, cancellation and timeouts.
- PostgreSQL experiment manifest database and exportable run packages.
- Authentication and service security before public deployment.

## Expanded QEC/AI
- Deltakit backend integration and BB/QLDPC code families.
- BP/OSD, neural GNN, transformer and hybrid decoder plugins.
- Dataset provenance, held-out evaluation, user-owned GPUs and SLURM workers.
- Evidence-based decoder recommendation and hardware-aware benchmarks.
