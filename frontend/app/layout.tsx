import type { Metadata } from "next";
import "./globals.css";

export const metadata: Metadata = {
  title: "Experiment Command Center | DecoderLab",
  description:
    "Inspect logical error rates, uncertainty and experiment provenance.",
};

export default function RootLayout({
  children,
}: Readonly<{ children: React.ReactNode }>) {
  return (
    <html lang="en">
      <body>{children}</body>
    </html>
  );
}
