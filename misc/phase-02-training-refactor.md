# Phase 2 Study Notes

## What We Built

We refactored the useful training logic from `ml4va.py` into small, focused files under `training/src/food_forecast/`.

## Why This Phase Exists

The original file mixed many responsibilities together:
- raw CSV loading
- preprocessing
- feature engineering
- model code
- plotting and notebook experiments

This phase separates the reusable training logic from the notebook-style script.

## New Training File Structure

```text
training/
  data/
    raw/
  src/
    food_forecast/
      __init__.py
      config.py
      data_loading.py
      prepare_dataset.py
      modeling.py
  preview_training_data.py
  requirements.txt
```

## File Roles

### `config.py`
Role:
- stores shared paths, dataset names, and model feature names

Inputs:
- none

Outputs:
- constants used by other training files

Why separate:
- shared configuration should live in one place

### `data_loading.py`
Role:
- reads the five raw CSV files

Inputs:
- files from `training/data/raw`

Outputs:
- raw pandas DataFrames

Why separate:
- reading files is different from cleaning or modeling

### `prepare_dataset.py`
Role:
- cleans each dataset
- standardizes FIPS values
- builds the final monthly model dataframe

Inputs:
- raw DataFrames

Outputs:
- cleaned tables
- model-ready dataframe

Why separate:
- preprocessing and feature engineering are the heart of the training pipeline

### `modeling.py`
Role:
- defines the Random Forest training and evaluation functions

Inputs:
- prepared model dataframe

Outputs:
- trained model object
- evaluation metrics

Why separate:
- model code should be independent from raw data cleaning code

### `preview_training_data.py`
Role:
- simple local entry point to test the training prep pipeline

Inputs:
- real CSVs

Outputs:
- terminal summary of cleaned data and model columns

Why separate:
- gives you a beginner-friendly way to inspect the pipeline without starting the backend

## What We Kept From `ml4va.py`

- the same five input datasets
- the same monthly aggregation idea
- the same core feature set:
  - `month`
  - `snap_per_capita`
  - `unemp_per_capita`
  - `poverty_per_capita`
  - `prev_food`
- the same Random Forest path

## Real Data Wrinkle We Found

The SNAP CSV has a multiline header for total persons:

- raw header text: `PERSONS\\n (TOTAL)`

After normalization, that became `persons__total`, not `persons_total`.

We fixed the training pipeline to map that messy real header to the clean internal column name `persons_total`.

We also made the SNAP date parsing explicit with the format `%m/%d/%y` so pandas does not need to guess.

Why this matters:
- real datasets often have annoying formatting details
- clean internal names make the rest of the pipeline easier to reason about
- this is a normal part of production data engineering, not a sign that the project is broken

## What We Did Not Carry Over Yet

- plotting
- correlation visualizations
- choropleth mapping
- Prophet forecasting
- commented neural-network experiments
- notebook-only `display(...)` calls

## Commands For This Phase

Create a virtual environment if you do not already have one:

```powershell
python -m venv .venv
```

Activate it in PowerShell:

```powershell
.\.venv\Scripts\Activate.ps1
```

Install training dependencies:

```powershell
pip install -r training/requirements.txt
```

Preview the prepared training dataset:

```powershell
python training/preview_training_data.py
```

## Local Development Note

We added `pyrightconfig.json` at the repo root so the editor knows to resolve Python imports from `.venv`.

Why this matters:
- this is only a local development/editor concern
- it does not change production behavior
- it helps Cursor and basedpyright understand installed packages like `pandas`
- we set type checking to `basic` so pandas-heavy code does not produce a wall of noisy static-analysis errors

For `prepare_dataset.py`, we also added a file-level pyright directive to suppress noisy pandas-specific static-analysis errors.

Why that is acceptable here:
- the file is runtime-validated with the real CSVs
- pandas code is often harder for static type checkers to understand
- the goal is to keep useful warnings without burying you in false positives

## What Happened During Validation

When the preview script was run, the current Python interpreter did not have `pandas` installed yet. That is an environment setup issue, not a code-structure issue.

A syntax-only validation did pass:

```powershell
python -m py_compile training/preview_training_data.py training/src/food_forecast/config.py training/src/food_forecast/data_loading.py training/src/food_forecast/prepare_dataset.py training/src/food_forecast/modeling.py
```

## Git Commands For This Phase

```powershell
git status
git add training misc
git commit -m "Refactor ML script into training pipeline modules"
```

You can usually wait to push until after Phase 3 if you want a slightly more useful checkpoint with the saved model artifact.

## Interview Talking Points

- I split the original notebook-style ML script into dedicated modules for config, data loading, preprocessing, and modeling.
- I kept training logic separate from backend and frontend concerns so the model pipeline can evolve independently.
- I created a simple preview script to inspect the cleaned dataset before training or deployment.
- I preserved the real feature engineering ideas from the original project instead of replacing them with a generic sample pipeline.
