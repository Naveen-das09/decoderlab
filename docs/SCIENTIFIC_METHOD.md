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

## Bivariate bicycle parity-check reference

The `[[72,12,6]]` construction uses the `(6,6)` torus and polynomials
`A = x^3 + y + y^2` and `B = y^3 + x + x^2` from [Bravyi et al., Table 3](https://arxiv.org/html/2308.07915v2#S4.T3).
The constructor returns `H_X = [A | B]` and `H_Z = [B^T | A^T]`. Both
matrices have 36 rows and 72 columns, row weight six and binary rank 30.
They commute over GF(2), giving `72 - 30 - 30 = 12` logical qubits.
The paper reports distance six.

Each block uses monomial order `6*i + j` for `x^i y^j`. A shift moves a
column's 1 to the row for the translated monomial. The reference hashes
use the raw row-major bytes with one unsigned byte per binary entry.

| Matrix | SHA-256 |
| --- | --- |
| `H_X` | `5ba3e05b4407c4584fd585cd52b714a1a432dc08ec7d1a3d243ffb66b8458838` |
| `H_Z` | `ffc3405373dc5afa63f51be84d8c7f1d31a973e4334a8d60dd70fb2e5368d63b` |

For the planned code-capacity model, each data qubit receives an
independent X error with probability `p`, and the syndrome is measured
perfectly as `H_Z e` over GF(2). A shot fails if the residual after
decoding has a nonzero syndrome or represents a nontrivial logical X
even though its syndrome is zero.

The deterministic checks use zero-based qubit and check indices. With
an X error at qubit 0, checks 3, 24 and 30 fire. At qubit 36, checks 4,
5 and 18 fire. The X operator on qubits 0, 3, 6, 15, 24 and 30 has zero
syndrome and increases the X-stabilizer rank by one when appended as a
row. It is a weight-six logical X witness. Run the reference tests
with `python -m pytest backend/tests/test_bivariate_bicycle.py -q` after
installing the test dependencies above. These are exact algebraic
checks with no random seed, decoder, simulated shots or confidence
intervals.
