"""Real Stim and PyMatching references, separate from dependency-free engine fixtures."""

from dataclasses import asdict
from hashlib import sha256

import numpy as np
import pymatching
import pytest
import stim
from fastapi.testclient import TestClient

from decoderlab.api import app
from decoderlab.domain import ExperimentSpec
from decoderlab.stim_engine import run_stim_pymatching


def reference_circuit(distance: int, probability: float) -> stim.Circuit:
    return stim.Circuit.generated(
        "surface_code:rotated_memory_z",
        distance=distance,
        rounds=5,
        after_clifford_depolarization=probability,
        before_round_data_depolarization=probability,
        before_measure_flip_probability=probability,
        after_reset_flip_probability=probability,
    )


@pytest.mark.parametrize(("distance", "detector_count"), [(3, 40), (5, 120)])
def test_noiseless_reference(distance: int, detector_count: int) -> None:
    spec = ExperimentSpec(distance=distance, physical_error_probability=0.0, shots=256)
    circuit = reference_circuit(distance, 0.0)
    detectors, observables = circuit.compile_detector_sampler(seed=spec.seed).sample(
        shots=spec.shots, separate_observables=True
    )
    assert detectors.shape == (spec.shots, detector_count)
    assert observables.shape == (spec.shots, 1)
    assert not detectors.any()
    assert not observables.any()

    result = run_stim_pymatching(spec)
    assert result["shots"] == spec.shots
    assert result["logical_failures"] == 0
    assert result["logical_error_rate"] == 0
    assert result["confidence_interval_95"]["lower"] == 0
    assert result["confidence_interval_95"]["upper"] == pytest.approx(0.0147838564)
    assert (
        result["manifest"]["circuit_sha256"]
        == sha256(str(circuit).encode()).hexdigest()
    )


def test_noisy_reference_through_api() -> None:
    spec = ExperimentSpec()
    circuit = reference_circuit(5, 0.005)
    detectors, observables = circuit.compile_detector_sampler(seed=spec.seed).sample(
        shots=spec.shots, separate_observables=True
    )
    assert detectors.shape == (10_000, 120)
    assert observables.shape == (10_000, 1)
    assert detectors.any()
    assert observables.any()

    matcher = pymatching.Matching.from_detector_error_model(
        circuit.detector_error_model(decompose_errors=True)
    )
    assert matcher.num_detectors == detectors.shape[1]
    assert matcher.num_fault_ids == observables.shape[1]
    predictions = np.stack([matcher.decode(syndrome) for syndrome in detectors])
    assert predictions.shape == observables.shape
    expected_failures = np.count_nonzero(predictions[:, 0] != observables[:, 0])

    response = TestClient(app).post(
        "/api/v1/experiments/run-with-chart", json=asdict(spec)
    )
    assert response.status_code == 200
    payload = response.json()
    result, chart = payload["experiment"], payload["chart"]
    assert result["execution_status"] == "completed"
    assert result["data_origin"] == chart["provenance"] == "simulated"
    assert result["shots"] == spec.shots
    assert result["logical_failures"] == expected_failures
    assert result["logical_error_rate"] == expected_failures / spec.shots
    assert result["manifest"]["code_task"] == "surface_code:rotated_memory_z"
    assert result["manifest"]["spec"] == asdict(spec)
    assert (
        result["manifest"]["circuit_sha256"]
        == sha256(str(circuit).encode()).hexdigest()
    )
    assert result["manifest"]["library_versions"] == {
        "stim": stim.__version__,
        "pymatching": pymatching.__version__,
    }

    (point,) = chart["points"]
    assert chart["run_id"] == payload["run_id"]
    assert point["physical_error_probability"] == spec.physical_error_probability
    assert point["shots"] == spec.shots
    assert point["logical_failures"] == expected_failures
    assert point["logical_error_rate"] == result["logical_error_rate"]
    assert (
        0
        <= point["ci95_lower"]
        == result["confidence_interval_95"]["lower"]
        < point["logical_error_rate"]
        < point["ci95_upper"]
        == result["confidence_interval_95"]["upper"]
        <= 1
    )
