# DecoderLab Experiment Command Center

The dashboard runs a fixed rotated surface-code simulation or reads a chart
JSON file on the local device. It supports the
`chart` field from FastAPI's `run-with-chart` response and standalone v1 charts.
Use **Load illustrative data** to inspect the workspace without the backend.
Imported source claims are labeled as unverified.

## Develop on a Mac

Use Node.js 24 or newer and run the following from this directory.

```bash
npm ci
npm run dev
```

Open [the local dashboard](http://127.0.0.1:3000). Select an observation with
the keyboard or point at a chart marker to inspect its counts and uncertainty.
Download SVG for the plot and CSV for the underlying observations.

To enable **Run surface-code preset**, run the backend in another terminal
from the repository root, using a Python 3.11+ virtual environment.

```bash
python -m pip install -e './backend[simulation]'
python -m uvicorn decoderlab.api:app --host 127.0.0.1 --port 8000
```

The frontend sends a fixed request through its own loopback server. The preset
runs 10,000 shots of distance-5, five-round rotated Z memory at seed 42 and
uses 0.005 per Stim circuit-level channel. PyMatching decodes the sampled
detectors. A shot fails if the predicted logical Z flip differs from the
sampled logical flip. **Export run JSON** saves the response with the request,
engine versions, and circuit hash. Replay by posting `experiment.manifest.spec`
to `/api/v1/experiments/run-with-chart` on FastAPI. For matching counts use the
same Stim version, platform/SIMD environment, and shot count.

To verify the production build and run Chromium browser checks:

```bash
npm run lint
npm run format:check
npm run typecheck
npm run build
npm exec -- playwright install chromium
npm test
```

With FastAPI running, use `DECODERLAB_LIVE_PRESET=1 npm test` to include
the real Stim/PyMatching browser round trip and verify the exported bundle.
