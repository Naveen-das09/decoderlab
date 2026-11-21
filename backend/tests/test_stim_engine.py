import hashlib
from types import SimpleNamespace

import numpy as np
import pytest
from fastapi.testclient import TestClient

from decoderlab.api import app
from decoderlab.domain import ExperimentSpec
from decoderlab import stim_engine


class FakeCircuit:
    def __str__(self):
        return 'STIM REFERENCE CIRCUIT'

    def detector_error_model(self, decompose_errors):
        assert decompose_errors is True
        return 'DEM'

    def compile_detector_sampler(self, seed):
        assert seed == 42
        return self

    def sample(self, shots, separate_observables):
        assert separate_observables is True
        assert shots == 4
        return np.array([[0], [1], [0], [1]], dtype=np.uint8), np.array([[0], [1], [1], [0]], dtype=np.uint8)


class FakeMatching:
    @staticmethod
    def from_detector_error_model(dem):
        assert dem == 'DEM'
        return FakeMatching()

    def decode_batch(self, detectors):
        return np.array([[0], [1], [0], [0]], dtype=np.uint8)


def fake_engines():
    def generate(task, **kwargs):
        assert task == 'surface_code:rotated_memory_z'
        assert kwargs == dict(distance=5, rounds=5, after_clifford_depolarization=.005,
                              before_round_data_depolarization=.005,
                              before_measure_flip_probability=.005, after_reset_flip_probability=.005)
        return FakeCircuit()
    return SimpleNamespace(Circuit=SimpleNamespace(generated=generate), __version__='fake'), SimpleNamespace(Matching=FakeMatching, __version__='fake')


def test_adapter_counts_failures_and_provenance(monkeypatch):
    monkeypatch.setattr(stim_engine, '_load_engines', fake_engines)
    result = stim_engine.run_stim_pymatching(ExperimentSpec(shots=4))
    assert result['logical_failures'] == 1
    assert result['logical_error_rate'] == .25
    assert result['data_origin'] == 'simulated'
    assert result['manifest']['circuit_sha256'] == hashlib.sha256(b'STIM REFERENCE CIRCUIT').hexdigest()
    assert result['manifest']['spec']['seed'] == 42
    assert result['confidence_interval_95']['lower'] < .25 < result['confidence_interval_95']['upper']


def test_api_returns_simulated_result_from_adapter(monkeypatch):
    monkeypatch.setattr(stim_engine, '_load_engines', fake_engines)
    response = TestClient(app).post('/api/v1/experiments', json={'shots': 4})
    assert response.status_code == 200
    assert response.json()['logical_failures'] == 1


def test_rejects_wrong_observable_shape(monkeypatch):
    class BadCircuit(FakeCircuit):
        def sample(self, shots, separate_observables):
            return np.zeros((shots, 1)), np.zeros((shots, 2))
    stim, matching = fake_engines()
    stim.Circuit.generated = lambda *args, **kwargs: BadCircuit()
    monkeypatch.setattr(stim_engine, '_load_engines', lambda: (stim, matching))
    with pytest.raises(RuntimeError, match='exactly one'):
        stim_engine.run_stim_pymatching(ExperimentSpec(shots=4))


def test_rejects_bad_decoder_output_shape(monkeypatch):
    class BadMatching(FakeMatching):
        def decode_batch(self, detectors):
            return np.zeros((4, 2))
    stim, matching = fake_engines()
    matching.Matching = SimpleNamespace(from_detector_error_model=lambda dem: BadMatching())
    monkeypatch.setattr(stim_engine, '_load_engines', lambda: (stim, matching))
    with pytest.raises(RuntimeError, match='shape'):
        stim_engine.run_stim_pymatching(ExperimentSpec(shots=4))


def test_dependency_failure_is_explicit(monkeypatch):
    monkeypatch.setattr(stim_engine, '_load_engines', lambda: (_ for _ in ()).throw(stim_engine.EngineUnavailable('missing dependencies')))
    response = TestClient(app).post('/api/v1/experiments', json={})
    assert response.status_code == 503
    assert 'missing dependencies' in response.json()['detail']
    assert 'logical_error_rate' not in response.text


def test_invalid_spec_rejected_before_loading_dependencies(monkeypatch):
    monkeypatch.setattr(stim_engine, '_load_engines', lambda: pytest.fail('should not import engines'))
    with pytest.raises(ValueError):
        stim_engine.run_stim_pymatching(ExperimentSpec(distance=4))
