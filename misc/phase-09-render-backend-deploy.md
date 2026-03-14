# Phase 9 Study Notes

## What We Built

We prepared the FastAPI backend for Render deployment.

This phase did two things:
- made backend CORS configurable with an environment variable
- documented the exact Render UI settings needed to deploy the API

## Why This Phase Exists

Local development and deployment are different.

Locally:
- you start the backend yourself with `uvicorn`
- the frontend usually runs at `localhost:3000`

In deployment:
- Render starts the backend for you
- Render assigns the backend a public URL
- the backend must listen on the `PORT` value Render provides
- the backend must allow requests from the deployed frontend origin later

## What Layer We Worked On

This phase is still in the `backend/` layer.

But the focus changed from app logic to deployment configuration.

## Important File Roles

### `backend/app/config.py`
Role:
- read deployment-time environment variables

Inputs:
- `MODEL_ARTIFACT_PATH`
- `ALLOWED_ORIGINS`

Outputs:
- resolved model path
- allowed CORS origin list

Why separate:
- deployment configuration should live in backend config, not route handlers

### `backend/app/main.py`
Role:
- apply CORS middleware using the configured origins

Inputs:
- backend CORS settings from config

Outputs:
- HTTP responses with the correct CORS behavior

Why separate:
- CORS is web-server behavior, so it belongs in the app startup layer

### `backend/README.md`
Role:
- document the exact Render UI settings and commands

Inputs:
- actual backend deployment requirements

Outputs:
- copy/paste deployment instructions

Why separate:
- deployment docs should live with the backend layer they describe

## Render Recommendation

For this project, Render is a good fit because:
- it is beginner-friendly
- FastAPI deployment is straightforward
- logs and service settings are easy to inspect
- you do not need Docker for this app

## Exact Render UI Settings

When creating the Render backend service:

### Service type
- `Web Service`

### Runtime
- `Python 3`

### Root directory
- leave it at the repo root

Why:
- the backend needs access to `training/artifacts/model.joblib`
- if you set the root directory to `backend/`, the backend would not naturally see the training artifact path

### Build command

```text
pip install -r backend/requirements.txt
```

### Start command

```text
uvicorn backend.app.main:app --host 0.0.0.0 --port $PORT
```

Why this matters:
- `0.0.0.0` allows external traffic into the container
- `$PORT` is injected by Render

## Environment Variables

### Optional model path

```text
MODEL_ARTIFACT_PATH=training/artifacts/model.joblib
```

You may not strictly need this because the backend already defaults to that path, but it can make the deployment settings more explicit.

### CORS setting

For now:

```text
ALLOWED_ORIGINS=http://localhost:3000,http://127.0.0.1:3000
```

Later, after frontend deployment, update it to include the real frontend URL.

## How To Deploy In Render

You should do the actual deployment through the Render UI so you learn the flow.

That means:
- connect your GitHub repo in Render
- create a new web service
- paste in the build/start commands above
- set the environment variables
- click deploy

My role here is to prepare the repo side and give you exact values, not hide the deployment steps from you.

## How To Test This Phase

After Render finishes deploying:

1. copy the public backend URL from Render
2. open:

```text
https://your-render-url/health
```

3. confirm you get a JSON response like:

```json
{
  "status": "ok",
  "model_loaded": true
}
```

4. optionally test `/predict` with Postman or curl

## Commands For This Phase

No new local install command is required for the backend code change itself.

Useful local check:

```powershell
python -m py_compile backend/app/config.py backend/app/main.py
```

## Git Commands For This Phase

Check changes:

```powershell
git status
```

Stage Phase 9 files:

```powershell
git add backend/app/config.py backend/app/main.py backend/README.md misc/phase-09-render-backend-deploy.md
```

Suggested commit:

```powershell
git commit -m "Prepare backend for Render deployment"
```

Push decision:
- yes, push after this phase
- Render deploys from your GitHub repo, so the deployment platform needs these files committed first

Push command:

```powershell
git push
```

## Commit Boundary Reason

This is a good commit boundary because it captures deployment preparation separately from the actual Render UI deployment action.

## Interview Talking Points

- I deployed the backend separately from the frontend, which mirrors how many real production systems are structured.
- I configured the backend to read deployment-specific settings like CORS origins from environment variables instead of hardcoding them.
- I used Render for the FastAPI service because it is a simple platform for hosting a Python web API without introducing Docker complexity.
- I kept the saved model artifact as the handoff point between offline training and deployed inference.
