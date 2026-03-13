from pydantic import BaseModel, Field


class PredictionRequest(BaseModel):
    month: int = Field(ge=1, le=12)
    population: float = Field(gt=0)
    snap_participants: float = Field(ge=0)
    unemployed_people: float = Field(ge=0)
    people_below_poverty: float = Field(ge=0)
    previous_month_food_lbs: float = Field(ge=0)


class PredictionResponse(BaseModel):
    predicted_food_lbs: float
    features_used: dict[str, float]


class HealthResponse(BaseModel):
    status: str
    model_loaded: bool
