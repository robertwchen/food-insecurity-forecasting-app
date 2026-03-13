from pathlib import Path

TRAINING_DIR = Path(__file__).resolve().parents[2]
RAW_DATA_DIR = TRAINING_DIR / "data" / "raw"

DATASET_FILES = {
    "food_bank": "va_food_banks.csv",
    "poverty": "HDPulse_data_export.csv",
    "snap": "Dec_2024_Participation_Report.csv",
    "unemployment": "bls_unemployment_by_month_county.csv",
    "population": "2010_2024_population.csv",
}

MODEL_FEATURES = [
    "month",
    "snap_per_capita",
    "unemp_per_capita",
    "poverty_per_capita",
    "prev_food",
]

TARGET_COLUMN = "food_distributed_pounds"
DEFAULT_POPULATION_YEAR = 2024
