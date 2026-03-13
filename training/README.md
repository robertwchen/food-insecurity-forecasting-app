# Training Layer

This folder is for offline machine learning work only.

## Structure

```text
training/
  artifacts/
  data/
    raw/
  src/
    food_forecast/
      config.py
      data_loading.py
      prepare_dataset.py
      modeling.py
  preview_training_data.py
  train_model.py
```

## File Roles

### `data/raw/`
Inputs:
- original CSV datasets

Outputs:
- none directly

Why separate:
- raw data should stay untouched and easy to locate

### `artifacts/`
Inputs:
- trained model object
- evaluation results
- feature column list

Outputs:
- `model.joblib`
- `metrics.json`
- `feature_columns.json`

Why separate:
- this folder is the handoff point from offline training to later backend inference

### `src/food_forecast/config.py`
Inputs:
- none

Outputs:
- shared paths, dataset names, artifact paths, and model feature names

Why separate:
- paths and feature lists should be defined once

### `src/food_forecast/data_loading.py`
Inputs:
- raw CSV files

Outputs:
- pandas DataFrames

Why separate:
- file reading should stay separate from cleaning logic

### `src/food_forecast/prepare_dataset.py`
Inputs:
- raw DataFrames

Outputs:
- cleaned tables
- final model dataset

Why separate:
- this file owns preprocessing and feature engineering

### `src/food_forecast/modeling.py`
Inputs:
- prepared model dataset

Outputs:
- trained model object
- evaluation metrics

Why separate:
- model code should not be mixed into raw data cleaning code

### `preview_training_data.py`
Inputs:
- all raw datasets

Outputs:
- terminal summary of prepared data

Why separate:
- this is a simple entry point for local development checks

### `train_model.py`
Inputs:
- all raw datasets
- training configuration from `src/food_forecast`

Outputs:
- trained `joblib` model artifact
- metrics JSON
- feature column list JSON

Why separate:
- this is the runnable training command, while `src/food_forecast` stays reusable library code

## Commands

Preview the prepared training dataset:

```powershell
python training/preview_training_data.py
```

Train the model and save artifacts:

```powershell
python training/train_model.py
```

## What Does Not Belong Here

- browser UI code
- FastAPI route handlers
- deployment-specific frontend logic
