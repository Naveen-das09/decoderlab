import { surfacePreset } from "../../../lib/surface-preset";

export async function POST(request: Request) {
  const host = request.headers.get("host");
  if (
    !host ||
    !/^(127\.0\.0\.1|localhost)(:\d+)?$/.test(host) ||
    request.headers.get("origin") !== `http://${host}`
  ) {
    return Response.json(
      { error: "Open the loopback dashboard to run this preset." },
      { status: 403 },
    );
  }

  let response: Response;
  try {
    response = await fetch(
      "http://127.0.0.1:8000/api/v1/experiments/run-with-chart",
      {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify(surfacePreset),
        redirect: "error",
        signal: AbortSignal.timeout(30_000),
      },
    );
  } catch {
    return Response.json(
      {
        error:
          "FastAPI did not respond. Check that it is running at 127.0.0.1:8000, then retry.",
      },
      { status: 502 },
    );
  }

  if (!response.ok) {
    return Response.json(
      {
        error:
          response.status === 503
            ? "Stim or PyMatching is unavailable. Install the backend simulation extras, then retry."
            : "FastAPI could not complete the preset. Check the server output, then retry.",
      },
      { status: 502 },
    );
  }

  return new Response(response.body, {
    headers: {
      "Content-Type": "application/json",
      "Cache-Control": "no-store",
    },
  });
}
