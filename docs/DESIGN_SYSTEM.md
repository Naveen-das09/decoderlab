# DecoderLab visual design system — v0

## Design goals
Professional scientific workstation: quiet, crisp and information-dense without feeling crowded. Visual quality is a functional requirement. Original data, uncertainty and provenance are more important than animation.

## Navigation and layout
Desktop: persistent left sidebar (Overview, Experiments, Code Explorer, Benchmarks, Models [planned], Advisor [planned]), compact top context bar and a consistent 12-column grid. Mobile: collapsible sidebar, card stacking and horizontal overflow only for inherently wide scientific data. Prefer sticky filters on long analysis pages.

## Initial tokens (proposal, not implemented)
- Dark canvas `#0B1020`; panel `#121A2C`; raised panel `#1A2438`; separator `#2B364D`.
- Primary text `#F2F5FA`; secondary `#A8B5CB`; interactive accent `#72D6DB`.
- Semantic error `#FB7185`, warning `#FBBF24`, success `#4ADE80`. Never rely on hue alone.
- Use a variable sans-serif family with tabular numeric variants; mathematical symbols must remain legible.
- Rounded corners ~12px, restrained shadows, spacious 8px rhythm, target minimum 44px hit areas on touch.

## Chart standards
- Each chart shows a research question in its title, with labelled axes, units, legend, explicit data origin and observation count.
- LER vs physical error p: show Wilson 95% intervals and failure/shot counts on inspection. Never replace zero with an arbitrary positive plotting floor.
- A log axis may only display positive values; if zero observations are present, provide an explicit omission note plus accessible linear/table alternative.
- Tooltips, keyboard focus and data table must agree. Users can export underlying CSV/JSON and high-quality SVG/PNG without altering provenance.
- Distinguish unverified user input, illustrative fixtures, simulation and hardware measurement with labels and shapes/patterns, not color alone.
- Decode/latency comparisons must state host device, per-shot vs end-to-end wall time, batch size and units.
- Layouts must handle one point, dozens of points, extreme confidence intervals, missing data and failed jobs honestly.

## Interaction states
Every page and visualization needs loading, empty, validation-error, engine-unavailable and retry states. No animated fake progress. Default reduced-motion support; never auto-play particle lattices in the background.

## Review checklist
- Is the chart scientifically valid?
- Can a keyboard-only or screen reader user reach equivalent information?
- Can a reviewer reproduce the data?
- Does the UI adapt to a narrow viewport?
- Are demo data impossible to confuse with actual results?

Design implementation begins after backend scientific verification and PR #1 review. The palette and navigation are proposals requiring a real browser review.