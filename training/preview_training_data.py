from pathlib import Path
import sys

TRAINING_DIR = Path(__file__).resolve().parent
SRC_DIR = TRAINING_DIR / "src"

if str(SRC_DIR) not in sys.path:
    sys.path.insert(0, str(SRC_DIR))

from food_forecast.config import MODEL_FEATURES  # noqa: E402
from food_forecast.data_loading import load_raw_datasets  # noqa: E402
from food_forecast.prepare_dataset import (  # noqa: E402
    build_model_dataframe,
    prepare_datasets,
)


def main() -> None:
    raw = load_raw_datasets()
    prepared = prepare_datasets(raw)
    model_df = build_model_dataframe(prepared)

    print("Prepared dataset counts:")
    print(f"- food_bank rows: {len(prepared.food_bank)}")
    print(f"- poverty rows: {len(prepared.poverty)}")
    print(f"- snap rows: {len(prepared.snap)}")
    print(f"- unemployment rows: {len(prepared.unemployment)}")
    print(f"- population_long rows: {len(prepared.population_long)}")

    print("\nModel dataframe columns:")
    print(list(model_df.columns))

    print("\nModel feature columns:")
    print(MODEL_FEATURES)

    print("\nModel dataframe preview:")
    print(model_df.head())


if __name__ == "__main__":
    main()
