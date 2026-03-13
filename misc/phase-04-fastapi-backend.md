# Phase 4 Study Notes

## What We Built

We created the first version of the FastAPI backend:

```text
backend/
  app/
    __init__.py
    config.py
    schemas.py
    predictor.py
    main.py
  requirements.txt
```

## Why This Phase Exists

This phase creates the online inference layer.

The backend is different from the training layer:
- training reads historical CSVs and saves a model artifact offline
- backend loads the saved artifact and answers prediction requests online

This separation is one of the biggest architecture ideas to understand for interviews.

## Important File Roles

### `backend/app/config.py`
Layer:
- backend

Role:
- define where the backend should load the trained model from

Inputs:
- optional `MODEL_ARTIFACT_PATH` environment variable

Outputs:
- resolved path to `training/artifacts/model.joblib`

Why separate:
- path and environment config should not be mixed into route code

### `backend/app/schemas.py`
Role:
- define the request and response contracts for the API

Inputs:
- incoming JSON body from the frontend or curl/Postman

Outputs:
- validated request objects
- predictable response shapes

Why separate:
- API contracts are easier to reason about when they live in one file

### `backend/app/predictor.py`
Role:
- load the saved model
- convert raw request values into the feature format used during training
- call `model.predict(...)`

Inputs:
- saved model artifact
- validated request data

Outputs:
- numeric prediction
- feature values used for the prediction

Why separate:
- inference logic should not be tangled up with web-route definitions

### `backend/app/main.py`
Role:
- create the FastAPI app
- load the model at startup
- expose `/health` and `/predict`

Inputs:
- HTTP requests
- backend predictor functions

Outputs:
- JSON API responses

Why separate:
- this file owns the web/server layer

## What The API Endpoints Do

### `GET /health`
Purpose:
- quick status check

What it returns:
- whether the API is running
- whether the model loaded at startup

### `POST /predict`
Purpose:
- make one food distribution prediction

Raw inputs accepted:
- `month`
- `population`
- `snap_participants`
- `unemployed_people`
- `people_below_poverty`
- `previous_month_food_lbs`

Why these are the API inputs:
- they are easier for a frontend form to send
- they are more intuitive than raw model feature names

What the backend computes internally:
- `month`
- `snap_per_capita`
- `unemp_per_capita`
- `poverty_per_capita`
- `prev_food`

That is the key idea of inference:
- the backend receives request data
- reshapes it into the same feature format used during training
- feeds it into the saved model

## Request Flow

```mermaid
flowchart LR
    client[FrontendOrCurl] --> predictRoute["POST /predict"]
    predictRoute --> schema[PredictionRequest]
    schema --> featureStep[build_feature_payload]
    featureStep --> modelFrame[modelInputDataFrame]
    modelFrame --> modelPredict[model.predict]
    modelPredict --> response[PredictionResponseJson]
```

## Local Development Vs Production

Local development:
- you will run the backend with `uvicorn`
- the model path defaults to `training/artifacts/model.joblib`

Production:
- the backend would still load the same kind of saved artifact
- the model path would usually come from an environment variable or deployment config

## Commands For This Phase

Activate your virtual environment:

```powershell
.\.venv\Scripts\Activate.ps1
```

Install backend dependencies:

```powershell
pip install -r backend/requirements.txt
```

Run the backend locally:

```powershell
uvicorn backend.app.main:app --reload
```

## How To Test This Phase

This phase focuses on building the backend, not full API request testing yet.

Basic checks:
1. install dependencies with `pip install -r backend/requirements.txt`
2. run `uvicorn backend.app.main:app --reload`
3. open `http://127.0.0.1:8000/health`
4. confirm you get a JSON response with `status` and `model_loaded`

We will do full `/predict` request testing in the next phase.

## Validation Performed

- backend Python files passed `py_compile`
- backend files showed no linter errors

I did not run the live FastAPI server yet because Phase 5 is the dedicated local API testing phase.

## Git Commands For This Phase

Check changes:

```powershell
git status
```

Stage Phase 4 files:

```powershell
git add backend misc/phase-04-fastapi-backend.md
```

Suggested commit:

```powershell
git commit -m "Build FastAPI inference API"
```

Push decision:
- you can wait until after Phase 5 if you want the commit to include live request testing results

If you do push now:

```powershell
git push
```

## Commit Boundary Reason

This is a good commit boundary because it captures the backend service creation before local API testing and frontend integration.

## Interview Talking Points

- I built a separate FastAPI service that loads the trained model artifact instead of retraining on each request.
- I defined explicit request and response schemas so the API contract is clear and predictable.
- I kept inference logic separate from HTTP route code so the backend is easier to test and maintain.
- The backend accepts simple business inputs and converts them into the exact feature shape used during training.
- I added a health endpoint because real services need a lightweight way to confirm they started correctly and loaded dependencies.
