# Backend Layer

This folder will contain the FastAPI application.

## Structure

```text
backend/
  app/
    config.py
    schemas.py
    predictor.py
    main.py
  requirements.txt
```

## Role In The App

- load the trained model artifact
- expose API endpoints like `/health` and `/predict`
- validate request data
- return prediction results as JSON

## File Roles

### `app/config.py`
Inputs:
- environment variable `MODEL_ARTIFACT_PATH` if provided

Outputs:
- the model artifact path the backend should load

Why separate:
- config should not be mixed into request handler code

### `app/schemas.py`
Inputs:
- incoming API JSON structure

Outputs:
- validated Python objects
- response shapes

Why separate:
- API contracts should be easy to read in one place

### `app/predictor.py`
Inputs:
- loaded model artifact
- validated request data

Outputs:
- model-ready feature frame
- prediction result

Why separate:
- inference logic should stay separate from HTTP route definitions

### `app/main.py`
Inputs:
- FastAPI app startup
- validated request objects

Outputs:
- `/health` response
- `/predict` response

Why separate:
- this file owns the web layer and route wiring

## Endpoints

### `GET /health`
Returns whether the API is up and whether the model loaded at startup.

### `POST /predict`
Accepts raw business inputs:
- `month`
- `population`
- `snap_participants`
- `unemployed_people`
- `people_below_poverty`
- `previous_month_food_lbs`

The backend converts those raw values into the training features:
- `month`
- `snap_per_capita`
- `unemp_per_capita`
- `poverty_per_capita`
- `prev_food`

## Local Commands

Install backend dependencies:

```powershell
pip install -r backend/requirements.txt
```

Run the backend locally:

```powershell
uvicorn backend.app.main:app --reload
```

Test the health endpoint:

```powershell
Invoke-RestMethod -Uri "http://127.0.0.1:8000/health" | ConvertTo-Json -Depth 4
```

Test the predict endpoint:

```powershell
$body = @{
  month = 6
  population = 100000
  snap_participants = 12000
  unemployed_people = 4500
  people_below_poverty = 15000
  previous_month_food_lbs = 70000
} | ConvertTo-Json

Invoke-RestMethod -Uri "http://127.0.0.1:8000/predict" -Method Post -ContentType "application/json" -Body $body | ConvertTo-Json -Depth 6
```

This layer should not retrain models or read the raw training CSVs.
