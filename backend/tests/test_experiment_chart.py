from dataclasses import asdict
import pytest
from fastapi.testclient import TestClient
from decoderlab.domain import ExperimentSpec
from decoderlab import experiment_chart
from decoderlab.api import app
from decoderlab.stim_engine import EngineUnavailable


def fake_run(spec):
    return {'execution_status':'completed','data_origin':'simulated','shots':spec.shots,
            'logical_failures':0,'manifest':{'spec':asdict(spec),'circuit_sha256':'a'*64,
            'library_versions':{'stim':'fixture','pymatching':'fixture'}}}


def test_chart_is_derived_from_execution_not_request_counts(monkeypatch):
    monkeypatch.setattr(experiment_chart, 'run_stim_pymatching', fake_run)
    payload = experiment_chart.execute_with_chart(ExperimentSpec())
    assert payload['chart']['provenance'] == 'simulated'
    assert payload['chart']['points'][0]['logical_failures'] == 0
    assert payload['chart']['points'][0]['ci95_upper'] > 0
    assert payload['chart']['points'][0]['log_y_eligible'] is False
    assert payload['persistence'] == 'not_persisted'
    assert payload['run_id'].startswith('sha256:')
    assert payload['chart']['run_id'] == payload['run_id']
    assert payload['chart']['verification'] == 'generated_from_completed_execution_adapter'


def test_content_id_stable_for_same_manifest_and_counts(monkeypatch):
    monkeypatch.setattr(experiment_chart, 'run_stim_pymatching', fake_run)
    assert experiment_chart.execute_with_chart(ExperimentSpec())['run_id'] == experiment_chart.execute_with_chart(ExperimentSpec())['run_id']

@pytest.mark.parametrize('mutation', [
    lambda r: r.update(execution_status='not_started'),
    lambda r: r.update(data_origin='user_supplied'),
    lambda r: r.update(shots=999),
    lambda r: r.update(logical_failures=10001),
    lambda r: r['manifest'].update(spec={'wrong':'spec'}),
    lambda r: r['manifest'].pop('circuit_sha256'),
])
def test_rejects_invalid_execution_claims(monkeypatch, mutation):
    def bad(spec):
        result = fake_run(spec)
        mutation(result)
        return result
    monkeypatch.setattr(experiment_chart, 'run_stim_pymatching', bad)
    with pytest.raises(RuntimeError):
        experiment_chart.execute_with_chart(ExperimentSpec())


def test_api_chart_route_with_fixture(monkeypatch):
    monkeypatch.setattr(experiment_chart, 'run_stim_pymatching', fake_run)
    response = TestClient(app).post('/api/v1/experiments/run-with-chart', json={})
    assert response.status_code == 200
    assert response.json()['chart']['points'][0]['shots'] == 10000


def test_api_missing_simulator_returns_503(monkeypatch):
    def unavailable(spec):
        raise EngineUnavailable('scientific dependencies not installed')
    monkeypatch.setattr(experiment_chart, 'run_stim_pymatching', unavailable)
    response = TestClient(app).post('/api/v1/experiments/run-with-chart', json={})
    assert response.status_code == 503
    assert 'not installed' in response.json()['detail']


def test_api_rejects_invalid_request():
    response = TestClient(app).post('/api/v1/experiments/run-with-chart', json={'distance':4})
    assert response.status_code == 422
