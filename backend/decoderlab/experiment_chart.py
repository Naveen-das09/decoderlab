"""Build a single-run chart from the execution adapter, never from client counts."""
from __future__ import annotations
from hashlib import sha256
import json
from typing import Any

from .domain import ExperimentSpec
from .stim_engine import run_stim_pymatching
from .visualization import BinomialObservation, build_ler_chart


def execute_with_chart(spec: ExperimentSpec) -> dict[str, Any]:
    """Return a completed simulation and its derived, traceable chart.

    The deterministic identifier identifies result content, not a durable
    database record or independent scientific verification.
    """
    result = run_stim_pymatching(spec)
    if result.get('execution_status') != 'completed' or result.get('data_origin') != 'simulated':
        raise RuntimeError('Only completed simulated results may produce verified-origin charts')
    manifest = result.get('manifest')
    if not isinstance(manifest, dict) or not manifest.get('circuit_sha256'):
        raise RuntimeError('Simulation result lacks a circuit fingerprint')
    shots = result['shots']
    failures = result['logical_failures']
    if isinstance(shots, bool) or not isinstance(shots, int) or isinstance(failures, bool) or not isinstance(failures, int) or not 0 <= failures <= shots:
        raise RuntimeError('Simulation result has invalid counts')
    if shots != spec.shots or manifest.get('spec') != vars(spec):
        raise RuntimeError('Simulation manifest differs from requested experiment')
    digest = sha256(json.dumps({'manifest': manifest, 'shots': shots, 'logical_failures': failures}, sort_keys=True, separators=(',', ':')).encode()).hexdigest()
    run_id = 'sha256:' + digest
    chart = build_ler_chart([BinomialObservation(spec.physical_error_probability, shots, failures)], provenance='simulated', run_id=run_id, source_description='Stim + PyMatching execution; no hardware measurement')
    chart['verification'] = 'generated_from_completed_execution_adapter'
    chart['source_manifest_sha256'] = sha256(json.dumps(manifest, sort_keys=True, separators=(',', ':')).encode()).hexdigest()
    return {'run_id': run_id, 'experiment': result, 'chart': chart, 'persistence': 'not_persisted'}
