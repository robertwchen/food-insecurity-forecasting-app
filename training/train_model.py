from pathlib import Path
import json
import sys

import joblib

TRAINING_DIR = Path(__file__).resolve().parent
SRC_DIR = TRAINING_DIR / "src"

if str(SRC_DIR) not in sys.path:
    sys.path.insert(0, str(SRC_DIR))

from food_forecast.config import (  # noqa: E402
    ARTIFACTS_DIR,
    FEATURE_COLUMNS_PATH,
    METRICS_PATH,
    MODEL_ARTIFACT_PATH,
    MODEL_FEATURES,
    RANDOM_FOREST_N_ESTIMATORS,
    RANDOM_FOREST_RANDOM_STATE,
)
from food_forecast.data_loading import load_raw_datasets  # noqa: E402
from food_forecast.modeling import evaluate_model, train_random_forest  # noqa: E402
from food_forecast.prepare_dataset import (  # noqa: E402
    build_model_dataframe,
    prepare_datasets,
)


def main() -> None:
    raw = load_raw_datasets()
    prepared = prepare_datasets(raw)
    model_df = build_model_dataframe(prepared)

    model = train_random_forest(
        model_df,
        n_estimators=RANDOM_FOREST_N_ESTIMATORS,
        random_state=RANDOM_FOREST_RANDOM_STATE,
    )
    evaluation = evaluate_model(model, model_df)

    ARTIFACTS_DIR.mkdir(parents=True, exist_ok=True)
    joblib.dump(model, MODEL_ARTIFACT_PATH)

    metrics_payload = evaluation.to_dict()
    metrics_payload["n_estimators"] = RANDOM_FOREST_N_ESTIMATORS
    metrics_payload["random_state"] = RANDOM_FOREST_RANDOM_STATE
    metrics_payload["evaluation_scope"] = "training_data"

    METRICS_PATH.write_text(json.dumps(metrics_payload, indent=2), encoding="utf-8")
    FEATURE_COLUMNS_PATH.write_text(
        json.dumps(MODEL_FEATURES, indent=2), encoding="utf-8"
    )

    print("Training complete.")
    print(f"- model rows: {len(model_df)}")
    print(f"- r2: {evaluation.r2:.4f}")
    print(f"- rmse: {evaluation.rmse:,.2f} lbs")
    print(f"- model saved to: {MODEL_ARTIFACT_PATH}")
    print(f"- metrics saved to: {METRICS_PATH}")
    print(f"- feature list saved to: {FEATURE_COLUMNS_PATH}")


if __name__ == "__main__":
    main()
