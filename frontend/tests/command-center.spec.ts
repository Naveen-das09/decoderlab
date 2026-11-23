import { expect, test } from "@playwright/test";
import AxeBuilder from "@axe-core/playwright";
import illustrative from "../lib/illustrative.json";

test("shows an honest empty state and recovers from an invalid import", async ({
  page,
}) => {
  await page.goto("/");
  await expect(
    page.getByRole("heading", { name: "Experiment Command Center" }),
  ).toBeVisible();
  await expect(page.getByText("No experiment data loaded")).toBeVisible();
  await page.keyboard.press("Tab");
  const skipLink = page.getByRole("link", {
    name: "Skip to experiment workspace",
  });
  await expect(skipLink).toBeFocused();
  await page.keyboard.press("Enter");
  await expect(page.getByRole("main")).toBeFocused();
  await expect(page.getByRole("button", { name: "Export SVG" })).toHaveCount(0);

  await page.getByLabel("Chart JSON file").setInputFiles({
    name: "invalid.json",
    mimeType: "application/json",
    buffer: Buffer.from("{"),
  });
  await expect(page.getByRole("main").getByRole("alert")).toHaveText(
    "This file contains invalid JSON.",
  );

  await page.getByLabel("Chart JSON file").setInputFiles({
    name: "preview.json",
    mimeType: "application/json",
    buffer: Buffer.from(
      JSON.stringify({
        chart: { ...illustrative, provenance: "user_supplied" },
      }),
    ),
  });
  await expect(page.getByRole("main").getByRole("alert")).toHaveCount(0);
  await expect(
    page.getByText("Source claims from the imported file are unverified."),
  ).toBeVisible();
  await expect(
    page.getByRole("region", { name: "Data table" }).getByRole("row"),
  ).toHaveCount(7);
});

test("exposes point details to the keyboard and exports labeled data", async ({
  page,
}) => {
  await page.goto("/");
  await page.getByRole("button", { name: "Load illustrative data" }).click();
  await expect(page.getByText("Generated example data.")).toBeVisible();
  await expect(page.getByRole("img")).toHaveAccessibleName(
    "Logical error rate versus physical error probability",
  );

  const zero = page.getByRole("row", { name: /^0\.1% / });
  await expect(
    zero.getByRole("cell", { name: "0%", exact: true }),
  ).toBeVisible();
  await expect(zero.getByRole("cell", { name: /^0% – 0\./ })).toBeVisible();
  const point = page.getByRole("button", { name: "0.2%", exact: true });
  await point.focus();
  await page.keyboard.press("Enter");
  await expect(point).toHaveAttribute("aria-pressed", "true");
  await expect(
    page.getByRole("region", { name: "Point details" }),
  ).toContainText("3 / 2,000");

  const csvEvent = page.waitForEvent("download");
  await page.getByRole("button", { name: "Export CSV" }).click();
  const csv = await csvEvent;
  expect(csv.suggestedFilename()).toBe("decoderlab-observations.csv");
  const csvStream = await csv.createReadStream();
  const csvChunks = [];
  for await (const chunk of csvStream) csvChunks.push(chunk);
  expect(Buffer.concat(csvChunks).toString("utf-8")).toContain(
    "2000,3,illustrative",
  );

  const svgEvent = page.waitForEvent("download");
  await page.getByRole("button", { name: "Export SVG" }).click();
  const svg = await svgEvent;
  expect(svg.suggestedFilename()).toBe("decoderlab-logical-error-rate.svg");
  const svgStream = await svg.createReadStream();
  const svgChunks = [];
  for await (const chunk of svgStream) svgChunks.push(chunk);
  const svgText = Buffer.concat(svgChunks).toString("utf-8");
  expect(svgText).toContain("Illustrative data");
  expect(svgText).toContain("Logical failure probability (%)");
  expect((await new AxeBuilder({ page }).analyze()).violations).toEqual([]);

  const screenshotDir = process.env.DECODERLAB_SCREENSHOT_DIR;
  if (screenshotDir) {
    await page.evaluate(() => window.scrollTo(0, 0));
    await page.screenshot({
      path: `${screenshotDir}/decoderlab-desktop.png`,
      fullPage: true,
    });
  }
});

test("fits a narrow viewport with a responsive plot and scrollable table", async ({
  page,
}) => {
  await page.setViewportSize({ width: 390, height: 844 });
  await page.emulateMedia({ reducedMotion: "reduce" });
  await page.goto("/");
  await page.getByRole("button", { name: "Load illustrative data" }).click();
  const widths = await page.evaluate(() => ({
    document: document.documentElement.scrollWidth,
    viewport: window.innerWidth,
  }));
  expect(widths.document).toBe(widths.viewport);
  const plot = page.getByRole("img", {
    name: "Logical error rate versus physical error probability",
  });
  await expect(plot).toHaveAttribute("font-size", "11");
  const table = page.getByRole("region", { name: "Data table" });
  await table.focus();
  await page.keyboard.press("ArrowRight");
  await expect
    .poll(() => table.evaluate((element) => element.scrollLeft))
    .toBeGreaterThan(0);
  await table.evaluate((element) => {
    element.scrollLeft = 0;
  });
  await expect(page.getByRole("region", { name: "Data table" })).toBeVisible();
  await expect(
    page.getByRole("button", { name: "Import chart JSON" }),
  ).toBeVisible();
  expect((await new AxeBuilder({ page }).analyze()).violations).toEqual([]);

  const screenshotDir = process.env.DECODERLAB_SCREENSHOT_DIR;
  if (screenshotDir) {
    await page.evaluate(() => window.scrollTo(0, 0));
    await page.screenshot({
      path: `${screenshotDir}/decoderlab-mobile.png`,
      fullPage: true,
    });
  }
});

test("reports a failed local run and lets a researcher retry", async ({
  page,
}) => {
  let attempts = 0;
  await page.route("**/api/surface-preset", async (route) => {
    attempts++;
    await route.fulfill({
      status: 502,
      json: {
        error: "FastAPI did not respond. Check that it is running, then retry.",
      },
    });
  });
  await page.goto("/");
  const run = page.getByRole("button", { name: "Run surface-code preset" });
  await run.focus();
  await page.keyboard.press("Enter");
  await expect(page.getByRole("main").getByRole("alert")).toContainText(
    "FastAPI did not respond.",
  );
  await expect(run).toBeEnabled();
  await run.click();
  await expect.poll(() => attempts).toBe(2);
  await expect(page.getByText("No experiment data loaded")).toBeVisible();
});

test("rejects a preset request from a different origin", async ({
  request,
}) => {
  const response = await request.post("/api/surface-preset", {
    headers: { Origin: "http://example.test" },
  });
  expect(response.status()).toBe(403);
});

test("runs the real surface preset and exports the replayable response", async ({
  page,
}) => {
  test.skip(
    process.env.DECODERLAB_LIVE_PRESET !== "1",
    "Start the local FastAPI backend first.",
  );
  await page.setViewportSize({ width: 1440, height: 900 });
  await page.goto("/");
  const responseEvent = page.waitForResponse("**/api/surface-preset");
  await page.getByRole("button", { name: "Run surface-code preset" }).click();
  const response = await responseEvent;
  expect(response.ok()).toBe(true);
  const bundle = await response.json();
  await expect(page.getByRole("img")).toContainText("Local simulation");
  const details = page.getByRole("region", { name: "Point details" });
  await expect(details).toContainText(
    "Simulated locally with Stim and PyMatching.",
  );
  await expect(details).toContainText(bundle.run_id);
  await expect(details).toContainText(
    `${bundle.experiment.logical_failures.toLocaleString("en")} / 10,000`,
  );
  await expect(details.getByText("Wilson 95%", { exact: true })).toBeVisible();
  expect(bundle.experiment.manifest.spec.seed).toBe(42);
  expect(bundle.experiment.manifest.circuit_sha256).toMatch(/^[a-f0-9]{64}$/);

  const downloadEvent = page.waitForEvent("download");
  await page.getByRole("button", { name: "Export run JSON" }).click();
  const download = await downloadEvent;
  const chunks = [];
  for await (const chunk of await download.createReadStream())
    chunks.push(chunk);
  expect(JSON.parse(Buffer.concat(chunks).toString("utf-8"))).toEqual(bundle);

  const screenshotDir = process.env.DECODERLAB_SCREENSHOT_DIR;
  if (screenshotDir) {
    await page.screenshot({
      path: `${screenshotDir}/surface-desktop.png`,
      fullPage: true,
    });
  }
  await page.setViewportSize({ width: 390, height: 844 });
  expect(await page.evaluate(() => document.documentElement.scrollWidth)).toBe(
    390,
  );
  expect((await new AxeBuilder({ page }).analyze()).violations).toEqual([]);
  if (screenshotDir) {
    await page.screenshot({
      path: `${screenshotDir}/surface-mobile.png`,
      fullPage: true,
    });
    await download.saveAs(`${screenshotDir}/surface-run.json`);
  }
});
