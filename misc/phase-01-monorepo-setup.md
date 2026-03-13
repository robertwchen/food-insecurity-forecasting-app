# Phase 1 Study Notes

## What We Built

We created the project skeleton for the rebuild:

```text
food-insecurity-forecasting-app/
  backend/
  frontend/
  training/
    data/
      raw/
  README.md
```

## Why This Phase Exists

This phase answers a simple but important architecture question:

Where does each kind of code live?

- `training/` is for offline ML work
- `backend/` is for the FastAPI inference API
- `frontend/` is for the Next.js browser app

## Important File Roles

### `training/`
Inputs:
- raw CSV files

Outputs:
- cleaned datasets
- trained model artifacts later

Why separate:
- training should stay offline and should not run inside the API server

### `backend/`
Inputs:
- JSON requests
- saved model artifact later

Outputs:
- JSON responses

Why separate:
- the backend owns inference and API contracts

### `frontend/`
Inputs:
- user form values
- backend URL later

Outputs:
- browser UI
- HTTP requests to the backend

Why separate:
- the frontend should focus on user interaction, not Python ML code

## Commands Used In This Phase

```powershell
git status
ls
ls training
ls training/data/raw
```

## Git Commands For This Phase

```powershell
git add .gitignore README.md ml4va.py training backend frontend misc
git commit -m "Set up monorepo structure for food forecast app"
```

If `origin` is set correctly:

```powershell
git push -u origin main
```

## Interview Talking Points

- I separated the project into training, backend, and frontend so each layer has one responsibility.
- I moved raw datasets under `training/data/raw` because only the training layer should read historical CSV data.
- I added documentation early so the architecture is easy to understand before implementation details grow.
- I kept the original `ml4va.py` file in the repo as source material for the refactor instead of replacing it with a generic demo.
