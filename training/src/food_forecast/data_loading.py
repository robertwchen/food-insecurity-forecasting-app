from dataclasses import dataclass
from pathlib import Path

import pandas as pd

from food_forecast.config import DATASET_FILES, RAW_DATA_DIR


@dataclass
class RawDatasets:
    food_bank: pd.DataFrame
    poverty: pd.DataFrame
    snap: pd.DataFrame
    unemployment: pd.DataFrame
    population: pd.DataFrame


def _require_file(path: Path) -> Path:
    if not path.exists():
        raise FileNotFoundError(f"Missing required dataset: {path}")
    return path


def load_raw_datasets(raw_data_dir: Path = RAW_DATA_DIR) -> RawDatasets:
    return RawDatasets(
        food_bank=pd.read_csv(
            _require_file(raw_data_dir / DATASET_FILES["food_bank"]),
            dtype={"FIPS": str, "fips": str},
        ),
        poverty=pd.read_csv(_require_file(raw_data_dir / DATASET_FILES["poverty"])),
        snap=pd.read_csv(
            _require_file(raw_data_dir / DATASET_FILES["snap"]),
            dtype={"FIPS": str, "fips": str},
        ),
        unemployment=pd.read_csv(
            _require_file(raw_data_dir / DATASET_FILES["unemployment"])
        ),
        population=pd.read_csv(_require_file(raw_data_dir / DATASET_FILES["population"])),
    )
