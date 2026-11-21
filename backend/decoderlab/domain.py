"""Experiment contracts and statistically honest result summaries."""
from __future__ import annotations
from dataclasses import dataclass
from math import sqrt, isfinite


@dataclass(frozen=True)
class ExperimentSpec:
    code_family: str = 'rotated_surface'
    distance: int = 5
    physical_error_probability: float = 0.005
    rounds: int = 5
    decoder: str = 'pymatching'
    shots: int = 10_000
    seed: int = 42

    def validate(self) -> None:
        if self.code_family != 'rotated_surface':
            raise ValueError('Only rotated_surface is supported by the initial contract')
        if isinstance(self.distance, bool) or not isinstance(self.distance, int) or self.distance < 3 or self.distance % 2 != 1 or self.distance > 31:
            raise ValueError('distance must be odd, between 3 and 31')
        if not isinstance(self.physical_error_probability, (int, float)) or not isfinite(self.physical_error_probability) or not 0 <= self.physical_error_probability <= 1:
            raise ValueError('physical_error_probability must be finite and in [0, 1]')
        if isinstance(self.rounds, bool) or not isinstance(self.rounds, int) or not 1 <= self.rounds <= 1000:
            raise ValueError('rounds must be in [1, 1000]')
        if self.decoder != 'pymatching':
            raise ValueError('Only pymatching is supported by the initial contract')
        if isinstance(self.shots, bool) or not isinstance(self.shots, int) or not 1 <= self.shots <= 1_000_000:
            raise ValueError('shots must be in [1, 1000000]')
        if isinstance(self.seed, bool) or not isinstance(self.seed, int) or not 0 <= self.seed < 2**64:
            raise ValueError('seed must be an unsigned 64-bit integer')


def wilson_interval(failures: int, shots: int, z: float = 1.959963984540054) -> tuple[float, float]:
    """Two-sided 95% Wilson score interval for a binomial failure proportion."""
    if isinstance(shots, bool) or not isinstance(shots, int) or shots <= 0:
        raise ValueError('shots must be a positive integer')
    if isinstance(failures, bool) or not isinstance(failures, int) or not 0 <= failures <= shots:
        raise ValueError('failures must be an integer between zero and shots')
    p = failures / shots
    denom = 1 + z*z/shots
    center = (p + z*z/(2*shots))/denom
    half = z*sqrt((p*(1-p) + z*z/(4*shots))/shots)/denom
    return max(0.0, min(p, center-half)), min(1.0, max(p, center+half))


def summarize(failures: int, shots: int) -> dict:
    lower, upper = wilson_interval(failures, shots)
    return {'shots': shots, 'logical_failures': failures,
            'logical_error_rate': failures / shots,
            'confidence_interval_95': {'lower': lower, 'upper': upper},
            'interval_method': 'Wilson score, two-sided 95%',
            'data_origin': 'measured'}
