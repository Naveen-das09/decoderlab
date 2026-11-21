import math
import pytest
from fastapi.testclient import TestClient
from decoderlab.api import app
from decoderlab.visualization import BinomialObservation, build_ler_chart


def obs(p, n, k):
    return BinomialObservation(p, n, k)


def test_sorted_points_and_wilson_intervals():
    chart = build_ler_chart([obs(.01, 100, 4), obs(.005, 100, 0)], provenance='illustrative')
    assert chart['schema_version'] == '1.0.0'
    assert chart['provenance'] == 'illustrative'
    assert [p['physical_error_probability'] for p in chart['points']] == [.005, .01]
    assert chart['points'][0]['logical_error_rate'] == 0
    assert chart['points'][0]['ci95_upper'] > 0
    assert chart['points'][0]['log_y_eligible'] is False
    assert chart['points'][1]['ci95_lower'] <= .04 <= chart['points'][1]['ci95_upper']

@pytest.mark.parametrize('items', [[], [obs(.01, 0, 0)], [obs(.01, 10, 11)], [obs(float('nan'), 10, 0)], [obs(.01, 10, 0), obs(.01, 20, 1)], [obs(True, 10, 0)]])
def test_reject_invalid_observations(items):
    with pytest.raises(ValueError):
        build_ler_chart(items, provenance='user_supplied')

@pytest.mark.parametrize('p', ['simulated', 'hardware_measured'])
def test_verified_provenance_requires_run_id(p):
    with pytest.raises(ValueError):
        build_ler_chart([obs(.005, 10, 1)], provenance=p)


def test_reject_run_id_on_unverified_data():
    with pytest.raises(ValueError):
        build_ler_chart([obs(.005, 10, 1)], provenance='user_supplied', run_id='run-1')


def test_preview_endpoint_marks_user_data_unverified():
    response = TestClient(app).post('/api/v1/charts/logical-error-rate/preview', json={'observations': [{'physical_error_probability': .005, 'shots': 100, 'logical_failures': 2}]})
    assert response.status_code == 200
    assert response.json()['provenance'] == 'user_supplied'
    assert response.json()['verification'] == 'not_verified_by_chart_builder'
    assert response.json()['run_id'] is None

@pytest.mark.parametrize('body', [
    {'observations': [{'physical_error_probability': .005, 'shots': 10, 'logical_failures': 11}]},
    {'observations': [{'physical_error_probability': .005, 'shots': 10, 'logical_failures': 0, 'extra': 1}]},
    {'observations': [{'physical_error_probability': .005, 'shots': 10, 'logical_failures': 0}], 'run_id': 'fake'},
    {'observations': []},
    {'observations': [{'physical_error_probability': .005, 'shots': True, 'logical_failures': 0}]},
])
def test_preview_rejects_invalid_payloads(body):
    assert TestClient(app).post('/api/v1/charts/logical-error-rate/preview', json=body).status_code == 422
