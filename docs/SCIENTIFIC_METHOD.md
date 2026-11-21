# Rotated surface-code reference experiment

The baseline runs Stim's `surface_code:rotated_memory_z` task with distance 5,
five syndrome rounds, PyMatching minimum-weight perfect matching, 10,000
shots, and seed 42. Stim labels the single logical observable `L0`. It is the
logical Z readout parity relative to the noiseless reference. The run is a
simulation with four circuit-noise parameters set to the same value, 0.005:

| Stim parameter | Channel |
| --- | --- |
| `after_clifford_depolarization` | One- or two-qubit depolarization after the corresponding Clifford gate |
| `before_round_data_depolarization` | Single-qubit depolarization on each data qubit at the start of a syndrome round |
| `before_measure_flip_probability` | Basis-appropriate Pauli flip before measurement |
| `after_reset_flip_probability` | Basis-appropriate Pauli flip after reset |

The value of `p` is per configured channel application. The model describes
stochastic circuit faults. It has no hardware calibration input.

Stim supplies a graphlike detector error model through error decomposition.
The sampler produces one detector row and a separate logical-observable row
per shot. PyMatching receives only the detector row as input. A logical
failure occurs when the predicted `L0` flip differs from the sampled flip.
The per-experiment logical failure probability estimate equals failures
divided by shots. The two-sided 95% Wilson interval assumes independent
Bernoulli shots. Zero failures still have a positive upper confidence bound.

## Run the reference checks

From the repository root with Python 3.11 or newer:

```bash
python3 -m venv .venv
source .venv/bin/activate
python -m pip install -c backend/integration_tests/constraints.txt -e './backend[test,simulation]'
python -m pytest backend/tests backend/integration_tests -q
```

The noiseless references sample 256 shots each at distance 3 and distance 5,
five rounds and seed 42. They check for zero detector events, zero observable
flips and zero decoded failures. The noisy reference independently samples
the configured circuit, decodes the resulting syndromes one at a time, and
compares the failure count to the app's batch path through the chart API. It
also checks shapes, provenance, shot counts, the interval, and the circuit
fingerprint. The integration job requires both engines at collection time.

Record the returned experiment manifest, counts and interval with each
export. The manifest records the seed, circuit SHA-256, code task and Stim and
PyMatching versions. Record Python, NumPy, OS and CPU architecture when
comparing seeded runs across hosts. Stim may produce a different seeded shot
stream across versions, platforms or sampling batch shapes. CI compares counts
within a single environment. It uses the noiseless cases as fixed references.
A successful reference test validates the local computation path for these
cases. Hardware accuracy and decoder rankings require their own validation.

[Stim generator and noise reference](https://github.com/quantumlib/Stim/blob/main/doc/usage_command_line.md)

[PyMatching API reference](https://pymatching.readthedocs.io/en/stable/api.html)
