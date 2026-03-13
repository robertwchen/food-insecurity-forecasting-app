from contextlib import asynccontextmanager

from fastapi import FastAPI

from backend.app.predictor import load_model, predict_food
from backend.app.schemas import HealthResponse, PredictionRequest, PredictionResponse


@asynccontextmanager
async def lifespan(app: FastAPI):
    app.state.model = load_model()
    yield


app = FastAPI(
    title="Food Forecast API",
    version="0.1.0",
    lifespan=lifespan,
)


@app.get("/health", response_model=HealthResponse)
def health_check() -> HealthResponse:
    return HealthResponse(status="ok", model_loaded=True)


@app.post("/predict", response_model=PredictionResponse)
def predict(request: PredictionRequest) -> PredictionResponse:
    prediction, features_used = predict_food(app.state.model, request)
    return PredictionResponse(
        predicted_food_lbs=prediction,
        features_used=features_used,
    )
