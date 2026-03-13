from dataclasses import dataclass

import pandas as pd
from sklearn.ensemble import RandomForestRegressor
from sklearn.metrics import mean_squared_error, r2_score

from food_forecast.config import MODEL_FEATURES, TARGET_COLUMN


@dataclass
class ModelEvaluation:
    r2: float
    rmse: float
    row_count: int


def build_features_and_target(
    model_df: pd.DataFrame,
) -> tuple[pd.DataFrame, pd.Series]:
    features = model_df[MODEL_FEATURES].copy()
    target = model_df[TARGET_COLUMN].copy()
    return features, target


def train_random_forest(
    model_df: pd.DataFrame,
    n_estimators: int = 100,
    random_state: int = 42,
) -> RandomForestRegressor:
    features, target = build_features_and_target(model_df)
    model = RandomForestRegressor(
        n_estimators=n_estimators,
        random_state=random_state,
    )
    model.fit(features, target)
    return model


def evaluate_model(
    model: RandomForestRegressor, model_df: pd.DataFrame
) -> ModelEvaluation:
    features, target = build_features_and_target(model_df)
    predictions = model.predict(features)
    return ModelEvaluation(
        r2=r2_score(target, predictions),
        rmse=mean_squared_error(target, predictions, squared=False),
        row_count=len(model_df),
    )
