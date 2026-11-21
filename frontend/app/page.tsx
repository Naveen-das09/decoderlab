"use client";

import { useRef, useState, type ChangeEvent } from "react";
import {
  chartCsv,
  formatProbability,
  parseChartFile,
  provenanceLabel,
  type ChartPayload,
  type ChartSource,
} from "../lib/chart";
import example from "../lib/illustrative.json";
import { LerPlot } from "./ler-plot";

const count = new Intl.NumberFormat("en");
const maxFileSize = 1024 * 1024;

function saveFile(name: string, contents: string, type: string) {
  const url = URL.createObjectURL(new Blob([contents], { type }));
  const link = document.createElement("a");
  link.href = url;
  link.download = name;
  link.click();
  window.setTimeout(() => URL.revokeObjectURL(url), 1000);
}

export default function CommandCenter() {
  const [loaded, setLoaded] = useState<{
    chart: ChartPayload;
    source: ChartSource;
  } | null>(null);
  const [selected, setSelected] = useState(0);
  const [busy, setBusy] = useState(false);
  const [error, setError] = useState("");
  const input = useRef<HTMLInputElement>(null);
  const plot = useRef<SVGSVGElement>(null);
  const chart = loaded?.chart;
  const point = chart?.points[selected];

  function showChart(chart: ChartPayload, source: ChartSource) {
    setSelected(0);
    setError("");
    setLoaded({ chart, source });
  }

  async function importChart(event: ChangeEvent<HTMLInputElement>) {
    const file = event.target.files?.[0];
    event.target.value = "";
    if (!file) return;
    setBusy(true);
    setError("");
    try {
      if (file.size > maxFileSize)
        throw new Error("Choose a JSON file under 1 MB.");
      showChart(parseChartFile(await file.text()), "import");
    } catch (error) {
      setError(
        error instanceof Error ? error.message : "The chart could not be read.",
      );
    } finally {
      setBusy(false);
    }
  }

  return (
    <>
      <a className="skip-link" href="#main">
        Skip to experiment workspace
      </a>
      <header className="app-bar">
        <div className="wrap app-bar-inner">
          <span className="wordmark">
            <span className="mark" aria-hidden="true">
              <i />
              <i />
              <i />
              <i />
            </span>
            DecoderLab
          </span>
          <span className="workspace-label">Experiments</span>
        </div>
      </header>

      <main className="wrap workspace" id="main" tabIndex={-1}>
        <div className="page-header">
          <div>
            <h1>Experiment Command Center</h1>
            <p>
              Inspect logical error rates, statistical uncertainty and
              experiment provenance.
            </p>
          </div>
          <div className="actions">
            <button
              className="button secondary"
              type="button"
              disabled={busy}
              onClick={() =>
                showChart(parseChartFile(JSON.stringify(example)), "example")
              }
            >
              Load illustrative data
            </button>
            <button
              className="button primary"
              type="button"
              disabled={busy}
              onClick={() => input.current?.click()}
            >
              Import chart JSON
            </button>
            <input
              ref={input}
              type="file"
              accept=".json,application/json"
              aria-label="Chart JSON file"
              hidden
              onChange={importChart}
            />
          </div>
        </div>

        {busy && (
          <p role="status" className="state">
            Reading chart file…
          </p>
        )}
        {error && (
          <p role="alert" className="state error">
            {error}
          </p>
        )}

        <div className="grid grid-cols-1 gap-5 lg:grid-cols-[minmax(0,1fr)_310px]">
          <section
            className="panel chart-panel"
            aria-labelledby="chart-heading"
          >
            <div className="panel-header">
              <div>
                <h2 id="chart-heading">Logical error rate</h2>
                <p>Per-shot failure probability with a Wilson 95% interval</p>
              </div>
              {chart && (
                <button
                  className="button subtle"
                  type="button"
                  onClick={() => {
                    if (plot.current)
                      saveFile(
                        "decoderlab-logical-error-rate.svg",
                        new XMLSerializer().serializeToString(plot.current),
                        "image/svg+xml",
                      );
                  }}
                >
                  Export SVG
                </button>
              )}
            </div>
            {chart ? (
              <LerPlot
                chart={chart}
                selected={selected}
                onSelect={setSelected}
                plotRef={plot}
              />
            ) : (
              <div className="chart-empty">
                <div>
                  <strong>No experiment data loaded</strong>
                  <p>
                    Import a DecoderLab chart or run-with-chart JSON export. You
                    can also explore the chart with labeled illustrative data.
                  </p>
                </div>
              </div>
            )}
          </section>

          <section
            className="panel inspector"
            aria-labelledby="inspect-heading"
          >
            <div className="panel-header">
              <div>
                <h2 id="inspect-heading">Point details</h2>
                <p>Counts and source for the selected point</p>
              </div>
            </div>
            {chart && point ? (
              <>
                <div className="source-label" data-origin={chart.provenance}>
                  {provenanceLabel[chart.provenance]}
                </div>
                <p className="source-note">
                  {chart.provenance === "illustrative"
                    ? "Generated example data."
                    : "Source claims from the imported file are unverified."}
                </p>
                {loaded?.source === "import" && chart.source_description && (
                  <p className="source-note">{chart.source_description}</p>
                )}
                <dl className="metrics">
                  <div>
                    <dt>Physical error</dt>
                    <dd>
                      {formatProbability(point.physical_error_probability)}
                    </dd>
                  </div>
                  <div>
                    <dt>Logical failure</dt>
                    <dd>{formatProbability(point.logical_error_rate)}</dd>
                  </div>
                  <div>
                    <dt>Wilson 95%</dt>
                    <dd>
                      {formatProbability(point.ci95_lower)} –{" "}
                      {formatProbability(point.ci95_upper)}
                    </dd>
                  </div>
                  <div>
                    <dt>Failures / shots</dt>
                    <dd>
                      {count.format(point.logical_failures)} /{" "}
                      {count.format(point.shots)}
                    </dd>
                  </div>
                </dl>
                {chart.run_id && (
                  <p className="run-id">
                    <span>Run ID</span>
                    <code>{chart.run_id}</code>
                  </p>
                )}
              </>
            ) : (
              <p className="muted inspector-empty">
                Physical error, logical failures, shot count and source will
                appear once you load a chart.
              </p>
            )}
          </section>
        </div>

        {chart && (
          <section
            className="panel table-panel"
            aria-labelledby="table-heading"
          >
            <div className="panel-header">
              <div>
                <h2 id="table-heading">Observations</h2>
                <p>
                  {count.format(chart.points.length)}{" "}
                  {chart.points.length === 1 ? "point" : "points"} ·{" "}
                  {provenanceLabel[chart.provenance]}
                </p>
              </div>
              <button
                className="button subtle"
                type="button"
                onClick={() =>
                  saveFile(
                    "decoderlab-observations.csv",
                    chartCsv(chart),
                    "text/csv;charset=utf-8",
                  )
                }
              >
                Export CSV
              </button>
            </div>
            {/* biome-ignore lint/a11y/noNoninteractiveTabindex: Keyboard users need to scroll the table viewport. */}
            <section className="scroll" aria-label="Data table" tabIndex={0}>
              <table>
                <caption className="sr-only">
                  Logical error observations. Activate a physical error value to
                  inspect the point.
                </caption>
                <thead>
                  <tr>
                    <th scope="col">Physical error (%)</th>
                    <th scope="col">Logical failure (%)</th>
                    <th scope="col">Wilson 95% interval (%)</th>
                    <th scope="col">Failures</th>
                    <th scope="col">Shots</th>
                  </tr>
                </thead>
                <tbody>
                  {chart.points.map((point, index) => (
                    <tr
                      key={point.physical_error_probability}
                      data-selected={index === selected}
                    >
                      <th scope="row">
                        <button
                          type="button"
                          aria-pressed={index === selected}
                          onClick={() => setSelected(index)}
                        >
                          {formatProbability(point.physical_error_probability)}
                        </button>
                      </th>
                      <td>{formatProbability(point.logical_error_rate)}</td>
                      <td>
                        {formatProbability(point.ci95_lower)} –{" "}
                        {formatProbability(point.ci95_upper)}
                      </td>
                      <td>{count.format(point.logical_failures)}</td>
                      <td>{count.format(point.shots)}</td>
                    </tr>
                  ))}
                </tbody>
              </table>
            </section>
          </section>
        )}
      </main>
    </>
  );
}
