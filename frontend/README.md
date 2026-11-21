# DecoderLab Experiment Command Center

The dashboard reads a chart JSON file on the local device. It supports the
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

To verify the production build and run Chromium browser checks:

```bash
npm run lint
npm run format:check
npm run typecheck
npm run build
npm exec -- playwright install chromium
npm test
```

Direct API retrieval, experiment jobs and persistence are later work. This
slice begins [the dashboard issue](https://github.com/Naveen-das09/decoderlab/issues/4)
with a local import path that can be reviewed independently of deployment.
