"""Direct Stim + PyMatching adapter for circuit-level surface-code memory experiments.

Requires the optional 'simulation' dependency group. This module never substitutes
synthetic observations for simulator output.
"""
from __future__ import annotations

from dataclasses import asdict, dataclass
from hashlib import sha256
import importlib
from typing import Any

from .domain import ExperimentSpec, summarize


class EngineUnavailable(RuntimeError):
    """Optional scientific simulation dependencies are not installed."""


@dataclass(frozen=True)
class SimulationManifest:
    schema_version: str
    simulator: str
    decoder: str
    code_task: str
    circuit_noise_model: str
    circuit_sha256: str
    spec: dict[str, Any]
    library_versions: dict[str, str]


def _load_engines():
    try:
        stim = importlib.import_module('stim')
        pymatching = importlib.import_module('pymatching')
    except ImportError as exc:
        raise EngineUnavailable('Install decoderlab-api[simulation] to run Stim + PyMatching experiments') from exc
    return stim, pymatching


def run_stim_pymatching(spec: ExperimentSpec) -> dict[str, Any]:
    """Run a noisy rotated surface-code Z-memory experiment and return counts.

    The physical error probability applies to each of four explicitly defined
    Stim circuit-level channels. This does not model a particular hardware device.
    """
    spec.validate()
    stim, pymatching = _load_engines()
    p = spec.physical_error_probability
    circuit = stim.Circuit.generated(
        'surface_code:rotated_memory_z',
        distance=spec.distance,
        rounds=spec.rounds,
        after_clifford_depolarization=p,
        before_round_data_depolarization=p,
        before_measure_flip_probability=p,
        after_reset_flip_probability=p,
    )
    detector_model = circuit.detector_error_model(decompose_errors=True)
    matcher = pymatching.Matching.from_detector_error_model(detector_model)
    detector_samples, observable_samples = circuit.compile_detector_sampler(
        seed=spec.seed
    ).sample(shots=spec.shots, separate_observables=True)
    if observable_samples.ndim != 2 or observable_samples.shape != (spec.shots, 1):
        raise RuntimeError('Expected exactly one logical observable per shot')
    predictions = matcher.decode_batch(detector_samples)
    if predictions.shape != observable_samples.shape:
        raise RuntimeError('Decoder output shape does not match logical observables')
    failures = int((predictions != observable_samples).any(axis=1).sum())
    if not 0 <= failures <= spec.shots:
        raise RuntimeError('Invalid failure count from decoder')
    manifest = SimulationManifest(
        schema_version='decoderlab.simulation.v1',
        simulator='stim', decoder='pymatching',
        code_task='surface_code:rotated_memory_z',
        circuit_noise_model='stim_generated_circuit_level_4_channels_equal_p',
        circuit_sha256=sha256(str(circuit).encode('utf-8')).hexdigest(),
        spec=asdict(spec),
        library_versions={
            'stim': str(getattr(stim, '__version__', 'unknown')),
            'pymatching': str(getattr(pymatching, '__version__', 'unknown')),
        },
    )
    return {
        **summarize(failures, spec.shots),
        'data_origin': 'simulated',
        'execution_status': 'completed',
        'manifest': asdict(manifest),
        'statistical_assumption': 'independent sampled shots; Wilson binomial interval',
    }
