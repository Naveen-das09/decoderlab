# DecoderLab development roadmap

## Simulator foundation
- Review the backend and [reference suite](SCIENTIFIC_METHOD.md) with passing
  unit, scientific integration and dependency checks.
- Keep the adapter and chart contract stable while adding the first dashboard.

## Visualization-first research dashboard
- Start with an accessible Next.js and TypeScript Experiment Command Center
  and a typed adapter for the v1 logical-error-rate payload.
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
