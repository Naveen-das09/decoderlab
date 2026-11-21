# DecoderLab — Product requirements (initial, 2026-11-21)

**Stage:** Pre-alpha. Public repository: https://github.com/Naveen-das09/decoderlab

## Product promise
An open-source, local-first research workbench for configuring, executing, visualizing, comparing and reproducing quantum error correction experiments, later supporting decoder training and evidence-based selection.

**Primary users:** QEC graduate researchers, decoder developers, educators, experimental hardware teams.
**Not** a cloud QPU service or a validated real-time hardware controller.

## Core jobs to be done
- As a researcher, configure a rotated-surface-code memory experiment and understand exactly what noise, code, observable and decoder are used.
- As a researcher, inspect logical failure probabilities with uncertainty, shot counts and reproducibility metadata; export data and cite the experiment manifest.
- As a developer, benchmark two compatible decoders under the same reproducible workload and report accuracy, runtime and resource use without misleading comparisons.
- As a student, explore a code lattice and syndrome history, with accessible annotation and faithful semantics.
- As a future ML researcher, train a neural decoder using self-hosted compute and held-out noise/code configurations.

## Initial screens
1. **Overview / Command Center:** clear status of experiment jobs, latest trustworthy runs, quick-start configuration and failure/latency summaries. No fake live instrumentation.
2. **Experiment Builder:** code family, distance, rounds, basis, noise channel parameters, decoder, shots, seed and validation warnings; execution locked down until job queue exists.
3. **Experiment Detail:** result chart + data table, Wilson 95% intervals, sample count, code/circuit fingerprint, dependency versions, seed, reproducible manifest and export controls.
4. **Syndrome Explorer:** real detector geometry and time slices; accessible textual event listing and run/shot attribution.
5. **Decoder Comparison:** matched-noise comparisons with clear hardware and timing provenance, confidence intervals, and accuracy/latency Pareto views.
6. **Neural Studio / Advisor:** roadmap only; do not add placeholder fake results suggesting working models.

## Initial scientific contract
Reference: rotated surface-code Z-memory, distance 5, 5 rounds, Stim-generated circuit with four separate p=0.005 noise channels, PyMatching decoder, 10,000 shots. The noise model is *not* a physical QPU calibration. A logical failure means decoded logical observable prediction disagrees with sampled observable flip. Statistical intervals use Wilson score (independent shots); zero failures still have nonzero upper bound. Never equate classical matching baseline with neural decoder training.

## Release acceptance gates
- Reproducible Python and JS dependency installation and CI.
- Verified real Stim/PyMatching execution: noiseless, noisy, shape/observable and seed/metadata validation.
- A working UI, responsive at phone/tablet/desktop widths, with keyboard/screen-reader access and non-color-only encoding.
- Real data paths and visibly labeled **illustrative** mode; no mixing verified and unverified datasets within a chart without explicit grouping.
- No unrestricted synchronous compute endpoint exposed publicly; rate-limited worker execution, job cancellation and quotas are release blockers.
- Basic threat-model review, secure error states, and open-source license compliance.

## Out of scope for initial public MVP
Production hardware integration; FPGA/real-time deadlines; multi-tenant managed GPU training; validated QLDPC cross-family transfer; LLM-generated decoder superiority claims.

## Product success
A new user can clone the repo, run the system locally, reproduce a small experiment and explain every plotted point. A reviewer can verify code paths, statistical methods and recorded dependencies. A researcher can compare and export results without losing scientific meaning.