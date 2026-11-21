import { useEffect, useId, useRef, useState, type Ref } from "react";
import {
  formatProbability,
  provenanceLabel,
  type ChartPayload,
} from "../lib/chart";

const ticks = [0, 1, 2, 3, 4];

function axisMaximum(value: number) {
  const rawStep = Math.max(value, 0.000001) / 4;
  const magnitude = 10 ** Math.floor(Math.log10(rawStep));
  const step =
    [1, 2, 2.5, 5, 10].find((value) => value * magnitude >= rawStep) ?? 10;
  return Math.min(1, 4 * step * magnitude);
}

export function LerPlot({
  chart,
  selected,
  onSelect,
  plotRef,
}: {
  chart: ChartPayload;
  selected: number;
  onSelect: (index: number) => void;
  plotRef: Ref<SVGSVGElement>;
}) {
  const titleId = useId();
  const descriptionId = useId();
  const container = useRef<HTMLDivElement>(null);
  const [width, setWidth] = useState(720);
  useEffect(() => {
    const element = container.current;
    if (!element) return;
    const observer = new ResizeObserver(([entry]) => {
      setWidth(Math.max(240, Math.floor(entry.contentRect.width)));
    });
    observer.observe(element);
    return () => observer.disconnect();
  }, []);

  const narrow = width < 480;
  const height = narrow ? 300 : 350;
  const left = narrow ? 63 : 75;
  const right = width - (narrow ? 25 : 55);
  const top = 60;
  const bottom = height - 60;
  const xMax = axisMaximum(
    chart.points.at(-1)?.physical_error_probability || 0.01,
  );
  const yMax = axisMaximum(
    Math.max(...chart.points.map((point) => point.ci95_upper)) || 0.01,
  );
  const x = (value: number) => left + (value / xMax) * (right - left);
  const y = (value: number) => bottom - (value / yMax) * (bottom - top);

  const sourceLabel =
    provenanceLabel[chart.provenance] +
    (chart.provenance === "illustrative" ? "" : " · unverified import");

  return (
    <div ref={container}>
      <svg
        ref={plotRef}
        xmlns="http://www.w3.org/2000/svg"
        width={width}
        height={height}
        viewBox={[0, 0, width, height].join(" ")}
        role="img"
        aria-labelledby={titleId}
        aria-describedby={descriptionId}
        fontFamily="system-ui, sans-serif"
        fontSize={narrow ? 11 : 12}
      >
        <title id={titleId}>
          Logical error rate versus physical error probability
        </title>
        <desc id={descriptionId}>
          Linear axes in percent. The table gives each point and its Wilson 95%
          interval.
        </desc>
        <rect width={width} height={height} rx="12" fill="#0D1627" />
        <text x={left} y="24" fill="#F2F5FA">
          {sourceLabel}
        </text>
        <text x={left} y="42" fill="#A8B5CB">
          Wilson 95% intervals
        </text>
        {ticks.map((tick) => {
          const probability = (tick * yMax) / 4;
          return (
            <g key={tick}>
              <line
                x1={left}
                x2={right}
                y1={y(probability)}
                y2={y(probability)}
                stroke="#2B364D"
              />
              <text
                x={left - 10}
                y={y(probability)}
                textAnchor="end"
                dominantBaseline="middle"
                fill="#A8B5CB"
              >
                {formatProbability(probability)}
              </text>
            </g>
          );
        })}
        {ticks.map((tick) => {
          const probability = (tick * xMax) / 4;
          return (
            <g key={tick}>
              <line
                x1={x(probability)}
                x2={x(probability)}
                y1={top}
                y2={bottom}
                stroke="#22304A"
              />
              <text
                x={x(probability)}
                y={bottom + 20}
                textAnchor="middle"
                fill="#A8B5CB"
              >
                {formatProbability(probability)}
              </text>
            </g>
          );
        })}
        <text
          x={(left + right) / 2}
          y={height - 15}
          textAnchor="middle"
          fill="#F2F5FA"
        >
          Physical error probability (%)
        </text>
        <text
          transform={`translate(17 ${(top + bottom) / 2}) rotate(-90)`}
          textAnchor="middle"
          fill="#F2F5FA"
        >
          Logical failure probability (%)
        </text>
        {chart.points.map((point, index) => {
          const cx = x(point.physical_error_probability);
          const cy = y(point.logical_error_rate);
          const hi = y(point.ci95_upper);
          const lo = y(point.ci95_lower);
          const focused = selected === index;
          return (
            <g
              key={point.physical_error_probability}
              onPointerEnter={() => onSelect(index)}
            >
              <line
                x1={cx}
                x2={cx}
                y1={hi}
                y2={lo}
                stroke="#72D6DB"
                strokeWidth="2"
              />
              <line
                x1={cx - 5}
                x2={cx + 5}
                y1={hi}
                y2={hi}
                stroke="#72D6DB"
                strokeWidth="2"
              />
              <line
                x1={cx - 5}
                x2={cx + 5}
                y1={lo}
                y2={lo}
                stroke="#72D6DB"
                strokeWidth="2"
              />
              {focused && (
                <circle cx={cx} cy={cy} r="10" fill="none" stroke="#F2F5FA" />
              )}
              <circle cx={cx} cy={cy} r="5" fill="#72D6DB" />
              <circle cx={cx} cy={cy} r="13" fill="transparent" />
            </g>
          );
        })}
      </svg>
    </div>
  );
}
