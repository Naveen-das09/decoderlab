from fastapi.testclient import TestClient
from decoderlab.api import app

client = TestClient(app)

def test_health():
    assert client.get('/api/v1/health').json()['engine'] == 'not_configured'

def test_validate_default():
    r = client.post('/api/v1/experiments/validate', json={})
    assert r.status_code == 200
    assert r.json()['scientific_data'] is None

def test_validate_rejects_bad_distance():
    assert client.post('/api/v1/experiments/validate', json={'distance': 4}).status_code == 422

def test_validate_rejects_extra_fields():
    assert client.post('/api/v1/experiments/validate', json={'secret': 'ignored?'}).status_code == 422

def test_execution_does_not_fake_results():
    r = client.post('/api/v1/experiments', json={})
    assert r.status_code == 503
    assert 'logical_error_rate' not in r.text
