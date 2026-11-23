import { z } from "zod";
import { surfacePreset } from "./surface-preset";

const probability = z.number().min(0).max(1);

const pointSchema = z
  .object({
    physical_error_probability: probability,
    logical_error_rate: probability,
    ci95_lower: probability,
    ci95_upper: probability,
    shots: z.int().positive(),
    logical_failures: z.int().nonnegative(),
    log_y_eligible: z.boolean(),
  })
  .refine(
    (point) =>
      point.logical_failures <= point.shots &&
      point.logical_error_rate === point.logical_failures / point.shots &&
      point.ci95_lower <= point.logical_error_rate &&
      point.logical_error_rate <= point.ci95_upper &&
      point.log_y_eligible ===
        (point.logical_error_rate > 0 && point.ci95_lower > 0),
    "Counts, rates or interval bounds are inconsistent",
  );

const chartSchema = z
  .object({
    schema_version: z.literal("1.0.0"),
    chart_type: z.literal("logical_error_rate_vs_physical_error_probability"),
    provenance: z.enum([
      "illustrative",
      "user_supplied",
      "simulated",
      "hardware_measured",
    ]),
    verification: z.string(),
    run_id: z.string().min(1).max(256).nullable(),
    source_description: z.string().max(500).nullable(),
    confidence_interval: z.object({
      method: z.literal("Wilson score"),
      level: z.literal(0.95),
      assumption: z.literal("independent Bernoulli shots"),
    }),
    axes: z.object({
      x: z.object({
        label: z.literal("Physical error probability"),
        scale: z.literal("linear"),
      }),
      y: z.object({
        label: z.literal("Logical failure probability"),
        scale: z.literal("linear"),
        optional_log_scale: z.literal(true),
      }),
    }),
    points: z.array(pointSchema).min(1).max(500),
  })
  .refine(
    ({ points }) =>
      points.every(
        (point, i) =>
          i === 0 ||
          points[i - 1].physical_error_probability <
            point.physical_error_probability,
      ),
    "Physical error probabilities must be unique and sorted",
  )
  .refine(
    ({ provenance, run_id }) =>
      (provenance === "simulated" || provenance === "hardware_measured") ===
      Boolean(run_id),
    "The run identifier does not match the declared provenance",
  );

const bundleSchema = z.object({ chart: chartSchema });
const importSchema = z.union([chartSchema, bundleSchema]);

export type ChartPayload = z.infer<typeof chartSchema>;
export type ChartPoint = z.infer<typeof pointSchema>;
export type ChartSource = "example" | "import" | "local";

const fingerprint = z.string().regex(/^[a-f0-9]{64}$/);
const surfaceRunSchema = z
  .object({
    run_id: z.string().regex(/^sha256:[a-f0-9]{64}$/),
    chart: chartSchema,
    experiment: z.object({
      shots: z.literal(surfacePreset.shots),
      logical_failures: z.int().nonnegative(),
      data_origin: z.literal("simulated"),
      execution_status: z.literal("completed"),
      manifest: z.object({
        schema_version: z.literal("decoderlab.simulation.v1"),
        simulator: z.literal("stim"),
        decoder: z.literal(surfacePreset.decoder),
        code_task: z.literal("surface_code:rotated_memory_z"),
        circuit_noise_model: z.literal(
          "stim_generated_circuit_level_4_channels_equal_p",
        ),
        circuit_sha256: fingerprint,
        spec: z.object({
          code_family: z.literal(surfacePreset.code_family),
          distance: z.literal(surfacePreset.distance),
          physical_error_probability: z.literal(
            surfacePreset.physical_error_probability,
          ),
          rounds: z.literal(surfacePreset.rounds),
          decoder: z.literal(surfacePreset.decoder),
          shots: z.literal(surfacePreset.shots),
          seed: z.literal(surfacePreset.seed),
        }),
        library_versions: z.object({
          stim: z.string(),
          pymatching: z.string(),
        }),
      }),
    }),
  })
  .refine(({ chart, run_id, experiment }) => {
    const point = chart.points[0];
    return (
      chart.provenance === "simulated" &&
      chart.run_id === run_id &&
      chart.points.length === 1 &&
      point.physical_error_probability ===
        surfacePreset.physical_error_probability &&
      point.shots === experiment.shots &&
      point.logical_failures === experiment.logical_failures
    );
  });

export function parseSurfaceRun(input: unknown) {
  const result = surfaceRunSchema.safeParse(input);
  if (!result.success) {
    throw new Error(
      "FastAPI returned an invalid surface-code result. Check the backend version, then retry.",
    );
  }
  return result.data;
}

export function parseChartFile(input: string): ChartPayload {
  let data: unknown;
  try {
    data = JSON.parse(input);
  } catch {
    throw new Error("This file contains invalid JSON.");
  }

  const outcome = importSchema.safeParse(data);
  if (!outcome.success) {
    throw new Error(
      "Choose a DecoderLab v1 chart or run-with-chart JSON export with valid counts and intervals.",
    );
  }
  return "chart" in outcome.data ? outcome.data.chart : outcome.data;
}

const percent = new Intl.NumberFormat("en", {
  style: "percent",
  maximumSignificantDigits: 5,
});

export function formatProbability(value: number) {
  return value > 0 && value < 0.000001
    ? `${(value * 100).toExponential(2)}%`
    : percent.format(value);
}

export const provenanceLabel: Record<ChartPayload["provenance"], string> = {
  illustrative: "Illustrative data",
  user_supplied: "User-supplied data",
  simulated: "Simulation",
  hardware_measured: "Hardware measurement",
};

export function chartCsv(
  chart: ChartPayload,
  source: ChartSource = "import",
): string {
  const headings = [
    "physical_error_probability",
    "logical_error_rate",
    "wilson_95_lower",
    "wilson_95_upper",
    "shots",
    "logical_failures",
    "provenance",
    "source_verification",
    "run_id",
  ];
  const id = chart.run_id ?? "";
  const safeId =
    /^[=+@-]/.test(id.trimStart()) || id !== id.trim() ? `'${id}` : id;
  const csvId = `"${safeId.replaceAll('"', '""')}"`;
  return `${[
    headings.join(","),
    ...chart.points.map((point) =>
      [
        point.physical_error_probability,
        point.logical_error_rate,
        point.ci95_lower,
        point.ci95_upper,
        point.shots,
        point.logical_failures,
        chart.provenance,
        chart.provenance === "illustrative"
          ? "illustrative"
          : source === "local"
            ? "local_simulation"
            : "unverified_import",
        csvId,
      ].join(","),
    ),
  ].join("\r\n")}\r\n`;
}
