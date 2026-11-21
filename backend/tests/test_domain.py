import math
import pytest
from decoderlab.domain import ExperimentSpec, wilson_interval, summarize


def test_default_spec():
    ExperimentSpec().validate()

@pytest.mark.parametrize('kwargs', [
    {'distance': 4}, {'distance': 1}, {'distance': True},
    {'physical_error_probability': -0.1}, {'physical_error_probability': math.nan},
    {'physical_error_probability': math.inf}, {'shots': 0}, {'shots': True},
    {'decoder': 'imaginary'}, {'rounds': 0}, {'seed': -1},
])
def test_invalid_spec(kwargs):
    with pytest.raises(ValueError):
        ExperimentSpec(**kwargs).validate()

@pytest.mark.parametrize('failures,shots', [(0,100), (1,100), (50,100), (100,100)])
def test_wilson_properties(failures, shots):
    lo, hi = wilson_interval(failures, shots)
    assert 0 <= lo <= failures/shots <= hi <= 1

def test_wilson_reference():
    lo, hi = wilson_interval(5, 100)
    assert lo == pytest.approx(0.02154, abs=0.0001)
    assert hi == pytest.approx(0.11175, abs=0.0001)

def test_summary_provenance():
    r = summarize(0, 100)
    assert r['logical_error_rate'] == 0
    assert r['confidence_interval_95']['upper'] > 0
    assert r['data_origin'] == 'measured'

@pytest.mark.parametrize('failures,shots', [(-1,10), (11,10), (0,0), (1,True)])
def test_invalid_counts(failures,shots):
    with pytest.raises(ValueError):
        wilson_interval(failures,shots)
