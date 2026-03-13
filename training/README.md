# Training Layer

This folder is for offline machine learning work only.

## Structure

```text
training/
  data/
    raw/
  src/
    food_forecast/
      config.py
      data_loading.py
      prepare_dataset.py
      modeling.py
  preview_training_data.py
```

## File Roles

### `data/raw/`
Inputs:
- original CSV datasets

Outputs:
- none directly

Why separate:
- raw data should stay untouched and easy to locate

### `src/food_forecast/config.py`
Inputs:
- none

Outputs:
- shared paths, dataset names, and model feature names

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

## What Does Not Belong Here

- browser UI code
- FastAPI route handlers
- deployment-specific frontend logic
