# Food Forecast App

This repository rebuilds the original food insecurity forecasting project into a simple, production-shaped architecture.

## Repository Structure

```text
food-insecurity-forecasting-app/
  training/
    data/
      raw/
  backend/
  frontend/
  README.md
```

## Layers

### `training/`
Offline machine learning work.

Inputs:
- raw CSV datasets

Outputs:
- cleaned features
- evaluation results
- saved model artifact

### `backend/`
FastAPI inference service.

Inputs:
- JSON requests from the frontend
- saved model artifact from training

Outputs:
- JSON predictions
- health check responses

### `frontend/`
Next.js user interface.

Inputs:
- user form values
- backend base URL from environment variables

Outputs:
- browser UI
- HTTP requests to the backend

## Phase 1 Goal

Set up the monorepo so each layer has a clear home before we refactor the ML code.
