import { defineConfig } from "@playwright/test";

export default defineConfig({
  testDir: "./tests",
  use: {
    baseURL: "http://127.0.0.1:3024",
    browserName: "chromium",
    channel: process.env.DECODERLAB_BROWSER_CHANNEL || undefined,
  },
  webServer: {
    command: "npm run start -- --port 3024",
    url: "http://127.0.0.1:3024",
    timeout: 30_000,
  },
});
