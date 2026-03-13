from dataclasses import dataclass

import joblib
import pandas as pd

from backend.app.config import MODEL_ARTIFACT_PATH
from backend.app.schemas import PredictionRequest


@dataclass
class FeaturePayload:
    month: float
    snap_per_capita: float
    unemp_per_capita: float
    poverty_per_capita: float
    prev_food: float

    def to_model_frame(self) -> pd.DataFrame:
        return pd.DataFrame(
            [
                {
                    "month": self.month,
                    "snap_per_capita": self.snap_per_capita,
                    "unemp_per_capita": self.unemp_per_capita,
                    "poverty_per_capita": self.poverty_per_capita,
                    "prev_food": self.prev_food,
                }
            ]
        )

    def to_dict(self) -> dict[str, float]:
        return {
            "month": self.month,
            "snap_per_capita": self.snap_per_capita,
            "unemp_per_capita": self.unemp_per_capita,
            "poverty_per_capita": self.poverty_per_capita,
            "prev_food": self.prev_food,
        }


def load_model():
    if not MODEL_ARTIFACT_PATH.exists():
        raise FileNotFoundError(
            f"Model artifact not found at {MODEL_ARTIFACT_PATH}. Run training first."
        )
    return joblib.load(MODEL_ARTIFACT_PATH)


def build_feature_payload(request: PredictionRequest) -> FeaturePayload:
    population = request.population
    return FeaturePayload(
        month=float(request.month),
        snap_per_capita=request.snap_participants / population,
        unemp_per_capita=request.unemployed_people / population,
        poverty_per_capita=request.people_below_poverty / population,
        prev_food=float(request.previous_month_food_lbs),
    )


def predict_food(model, request: PredictionRequest) -> tuple[float, dict[str, float]]:
    features = build_feature_payload(request)
    model_input = features.to_model_frame()
    prediction = float(model.predict(model_input)[0])
    return prediction, features.to_dict()
