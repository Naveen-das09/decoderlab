# DecoderLab

**Open-source quantum error correction research, visualization, and AI decoder platform.**

> **Status: early research prototype.** The backend contract, statistical reporting,
> and direct Stim/PyMatching execution adapter exist. The dashboard, database and
> Deltakit integration are not yet implemented. No real-scientific-dependency
> integration benchmark is validated yet. **Do not deploy the synchronous simulation
> endpoints to an unrestricted public service.**

## Purpose

Build an accessible research workbench for reproducible QEC experiments, logical
error rate and decoder comparisons, and eventually GNN/transformer decoders,
BYOC/HPC training and evidence-based decoder recommendations.

## Backend quick start

Use Python 3.11+:

    cd backend
    python -m pip install -e '.[test]'
    python -m pytest -q
    uvicorn decoderlab.api:app --reload

Open http://localhost:8000/docs for interactive API documentation.

To run a real distance-5 Z-memory experiment, separately install the optional
simulation dependencies:

    python -m pip install -e '.[simulation,test]'

Example request body for POST /api/v1/experiments/run-with-chart:

    {"code_family":"rotated_surface","distance":5,
     "physical_error_probability":0.005,"rounds":5,
     "decoder":"pymatching","shots":10000,"seed":42}

The simulator applies the same p independently as a parameter to four explicitly
named Stim circuit-noise channels. This is not a calibrated hardware noise model.

## Prototype endpoints

| Route | Description |
| --- | --- |
| GET /api/v1/health | Service health (not simulation health) |
| POST /api/v1/experiments/validate | Input validation only |
| POST /api/v1/experiments | Local synchronous Stim/PyMatching run |
| POST /api/v1/experiments/run-with-chart | Local run and provenance-aware chart |
| POST /api/v1/charts/logical-error-rate/preview | User-supplied count preview, unverified |

All statistical intervals currently use two-sided 95% Wilson bounds under
independent shot sampling. Zero observed logical errors do **not** imply zero
logical error probability. Log-scale plots must not invent a positive floor.

## Architecture and roadmap

1. Verify real Stim/PyMatching integration using independent zero-noise and
   nonzero-noise scientific reference tests in CI.
2. Build visualization-first Next.js dashboard with responsive layouts,
   accessible plot data tables, uncertainty and provenance labels.
3. Add a resource-limited asynchronous job queue, persistence and authentication
   before enabling public experiment execution.
4. Add Deltakit and BP/OSD adapters; add QLDPC workflows.
5. Add neural GNN/transformer training and bring-your-own-compute workers.
6. Only then train an evidence-based intelligent decoder advisor.

See docs/ for science and design decisions. This repository is Apache-2.0
licensed. Contributions welcome after initial stabilization.
