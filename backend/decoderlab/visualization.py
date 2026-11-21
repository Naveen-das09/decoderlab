"""Versioned, provenance-aware chart payloads for binomial QEC benchmarks.

These utilities do not generate or certify quantum experiment data.
"""
from __future__ import annotations
from dataclasses import dataclass
from math import isfinite
from typing import Literal
from .domain import wilson_interval


@dataclass(frozen=True)
class BinomialObservation:
    physical_error_probability: float
    shots: int
    logical_failures: int

    def validate(self) -> None:
        if isinstance(self.physical_error_probability, bool) or not isinstance(self.physical_error_probability, (float, int)) or not isfinite(self.physical_error_probability) or not 0 <= self.physical_error_probability <= 1:
            raise ValueError('physical_error_probability must be finite and in [0,1]')
        wilson_interval(self.logical_failures, self.shots)


def build_ler_chart(
    observations: list[BinomialObservation], *,
    provenance: Literal['user_supplied', 'illustrative', 'simulated', 'hardware_measured'],
    run_id: str | None = None,
    source_description: str | None = None,
) -> dict:
    """Build chart points with Wilson intervals and explicit provenance.

    'simulated' and 'hardware_measured' require an immutable run identifier;
    this function does not verify the provenance claim itself.
    """
    if not observations:
        raise ValueError('at least one observation is required')
    if len(observations) > 500:
        raise ValueError('maximum 500 observations per chart')
    if provenance not in ('user_supplied', 'illustrative', 'simulated', 'hardware_measured'):
        raise ValueError('unsupported provenance')
    if provenance in ('simulated', 'hardware_measured') and (not run_id or not run_id.strip()):
        raise ValueError('simulated and hardware_measured data require a run_id')
    if provenance in ('user_supplied', 'illustrative') and run_id is not None:
        raise ValueError('unverified data cannot be associated with a verified run_id')
    if source_description is not None and len(source_description) > 500:
        raise ValueError('source_description exceeds 500 characters')
    for obs in observations:
        obs.validate()
    probabilities = [float(o.physical_error_probability) for o in observations]
    if len(set(probabilities)) != len(probabilities):
        raise ValueError('duplicate physical error probabilities are ambiguous')
    points = []
    for obs in sorted(observations, key=lambda o: o.physical_error_probability):
        lo, hi = wilson_interval(obs.logical_failures, obs.shots)
        rate = obs.logical_failures / obs.shots
        points.append({
            'physical_error_probability': float(obs.physical_error_probability),
            'logical_error_rate': rate,
            'ci95_lower': lo,
            'ci95_upper': hi,
            'shots': obs.shots,
            'logical_failures': obs.logical_failures,
            'log_y_eligible': rate > 0 and lo > 0,
        })
    return {
        'schema_version': '1.0.0',
        'chart_type': 'logical_error_rate_vs_physical_error_probability',
        'provenance': provenance,
        'verification': 'not_verified_by_chart_builder',
        'run_id': run_id,
        'source_description': source_description,
        'confidence_interval': {'method': 'Wilson score', 'level': 0.95, 'assumption': 'independent Bernoulli shots'},
        'axes': {'x': {'label': 'Physical error probability', 'scale': 'linear'},
                 'y': {'label': 'Logical failure probability', 'scale': 'linear', 'optional_log_scale': True}},
        'points': points,
    }
