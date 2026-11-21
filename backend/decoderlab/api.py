"""Research-only API: synchronous simulation endpoints are not suitable for public deployment."""
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, Field, ConfigDict
from .domain import ExperimentSpec
from .stim_engine import EngineUnavailable, run_stim_pymatching

app = FastAPI(title='DecoderLab API', version='0.1.0')

class ExperimentRequest(BaseModel):
    model_config = ConfigDict(extra='forbid')
    code_family: str = 'rotated_surface'
    distance: int = 5
    physical_error_probability: float = 0.005
    rounds: int = 5
    decoder: str = 'pymatching'
    shots: int = 10_000
    seed: int = Field(default=42, ge=0, lt=2**64)

@app.get('/api/v1/health')
def health():
    return {'status': 'ok', 'engine': 'not_configured'}

@app.post('/api/v1/experiments/validate')
def validate_experiment(request: ExperimentRequest):
    try:
        ExperimentSpec(**request.model_dump()).validate()
    except ValueError as exc:
        raise HTTPException(status_code=422, detail=str(exc)) from exc
    return {'valid': True, 'specification': request.model_dump(),
            'execution_status': 'not_started', 'scientific_data': None}

@app.post('/api/v1/experiments')
def create_experiment(request: ExperimentRequest):
    try:
        ExperimentSpec(**request.model_dump()).validate()
    except ValueError as exc:
        raise HTTPException(status_code=422, detail=str(exc)) from exc
    try:
        return run_stim_pymatching(ExperimentSpec(**request.model_dump()))
    except EngineUnavailable as exc:
        raise HTTPException(status_code=503, detail=str(exc)) from exc

from .visualization import BinomialObservation, build_ler_chart

class ChartObservation(BaseModel):
    model_config = ConfigDict(extra='forbid', allow_inf_nan=False, strict=True)
    physical_error_probability: float
    shots: int
    logical_failures: int

class ChartPreviewRequest(BaseModel):
    model_config = ConfigDict(extra='forbid')
    observations: list[ChartObservation] = Field(min_length=1, max_length=500)
    source_description: str | None = Field(default=None, max_length=500)

@app.post('/api/v1/charts/logical-error-rate/preview')
def chart_preview(request: ChartPreviewRequest):
    try:
        return build_ler_chart(
            [BinomialObservation(**obs.model_dump()) for obs in request.observations],
            provenance='user_supplied', source_description=request.source_description,
        )
    except ValueError as exc:
        raise HTTPException(status_code=422, detail=str(exc)) from exc

from .experiment_chart import execute_with_chart

@app.post('/api/v1/experiments/run-with-chart')
def run_experiment_with_chart(request: ExperimentRequest):
    try:
        spec = ExperimentSpec(**request.model_dump())
        spec.validate()
    except ValueError as exc:
        raise HTTPException(status_code=422, detail=str(exc)) from exc
    try:
        return execute_with_chart(spec)
    except EngineUnavailable as exc:
        raise HTTPException(status_code=503, detail=str(exc)) from exc
