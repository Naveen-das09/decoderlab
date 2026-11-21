# DecoderLab architecture and scientific release policy

**Stage:** Research prototype, backend baseline from sprints 01–04.

## Components

- A Next.js/TypeScript scientific dashboard is planned, not yet implemented.
- The FastAPI backend validates experiments, formats logical-failure charts,
  and exposes a developer-only synchronous Stim/PyMatching simulator adapter.
- Direct Stim/PyMatching and future Deltakit adapters must share a stable
  experiment schema. Future BP/OSD and neural decoders must be plugins.
- PostgreSQL persistence, bounded worker execution, and bring-your-own-compute
  agents remain roadmap items, not implemented capabilities.

## Scientific contract

The current baseline uses rotated Z-memory surface-code tasks with d=5,
five rounds, and physical error probability 0.005 as defaults. Each of four
Stim-generated noise channels receives p separately. This is **not** a
calibrated QPU noise model. Logical failures are mismatches between predicted
and actual logical observable flips. Simulation output carries circuit hash,
dependency versions, seed, task, code parameters and shot counts.
See the [scientific method](SCIENTIFIC_METHOD.md) for the four channel
definitions, reference cases, validation commands and reproducibility limits.

Wilson score 95% intervals are appropriate only for the independent Bernoulli
shots baseline. Error bars must show zero-failure upper confidence bounds.
Chart payloads generated from user-provided counts must be marked
user_supplied and unverified. A content-addressed run_id is not a persistent
database identifier or a scientific certification.

## Definition of Done

1. Acceptance criteria and reproducibility details documented.
2. Unit tests run locally; GitHub CI independently green before merge.
3. Real Stim/PyMatching integration checks at p=0 and a nonzero p pass.
4. Scientific plots present confidence intervals, sample size, provenance,
   axes and accessible tabular equivalents.
5. Public execution requires authentication, quotas, bounded jobs, cancellation,
   safe storage and clear cost controls.
6. Do not mark Deltakit, Next.js dashboard or AI training as implemented
   before real code and integration tests exist.

## Development

Development happens on feature branches, through draft pull requests, and
with explicit review before merging to main. Never commit raw calibration
secrets, research datasets or trained checkpoints by default.
