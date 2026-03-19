# INTERVIEW_WALKTHROUGH

This file is designed for one job: help you explain this app clearly, honestly, and confidently in a final-round software engineering interview.

Throughout this walkthrough, I use three labels:

- **Confirmed**: directly supported by the code or docs in this repo.
- **Inferred**: strongly suggested by the code, docs, and `misc/` notes, but not stated as a hard fact.
- **Unknown**: not clearly provable from the repo.

---

# 1. What This App Is

## Plain-English Summary

**Confirmed:** This is a small full-stack machine learning app that predicts monthly food distribution needs from a handful of socioeconomic inputs.

The app has three clean layers:

- `training/`: offline data prep and model training
- `backend/`: FastAPI inference service
- `frontend/`: Next.js browser UI

If you want a one-line description:

> "It is a simple production-shaped ML app where I train a model offline, serve it through a FastAPI API, and call that API from a Next.js frontend."

## Target User

**Confirmed:** The UI is a numeric input form for someone who wants a prediction.

**Inferred:** The target user is probably an analyst, operator, or planner trying to estimate how much food distribution will be needed in a month.

## Problem Solved

**Confirmed:** The app tries to estimate `food_distributed_pounds` using:

- month
- population
- SNAP participants
- unemployed people
- people below poverty
- previous month food distributed

**Inferred:** The real problem is not just prediction. It is also turning a messy notebook-style ML experiment into something you can explain as a real software system.

## Major Features

- **Confirmed:** Offline model training from CSV datasets
- **Confirmed:** Saved model artifact with `joblib`
- **Confirmed:** FastAPI `/health` endpoint
- **Confirmed:** FastAPI `/predict` endpoint
- **Confirmed:** Browser form that sends JSON to the backend
- **Confirmed:** Prediction result display
- **Confirmed:** Returned `features_used` object to make inference easier to inspect
- **Confirmed:** Config via environment variables for backend URL and allowed origins
- **Confirmed:** Deployment guidance for Render and Vercel

## Why This App Matters

**Confirmed:** The docs repeatedly emphasize clarity, separation of concerns, and interview-readiness.

This matters because the app gives you a credible story around:

- ML training vs online inference
- frontend/backend contracts
- deployment configuration
- real integration issues like CORS
- data cleaning from messy real CSVs

---

# 2. The Story of the App

## The Short Version

**Confirmed:** The app started from an original notebook-export style file named `ml4va.py`.

That original file mixed together:

- Colab-specific setup
- CSV loading
- cleaning
- county-level analysis
- plots
- a Random Forest experiment
- a Prophet experiment

The rebuild deliberately extracted the explainable, production-relevant path into a three-layer system.

## Reconstructed Timeline

### Phase 0: Analyze the legacy source

- **Confirmed:** `misc/food_forecast_rebuild_85bc3663.plan.md` analyzes `ml4va.py`
- **Confirmed:** the plan recommends keeping the Random Forest path first
- **Confirmed:** the plan recommends splitting responsibilities into `training/`, `backend/`, and `frontend/`
- **Confirmed:** the plan explicitly says the notebook is useful source material, not deployable app code

### Phase 1: Create a monorepo shape

- **Confirmed:** `training/`, `backend/`, `frontend/`, and `misc/` were created as separate layers
- **Confirmed:** raw datasets were moved under `training/data/raw`
- **Confirmed:** `ml4va.py` was intentionally kept as source material

### Phase 2: Extract reusable training code

- **Confirmed:** training logic was split into:
  - `config.py`
  - `data_loading.py`
  - `prepare_dataset.py`
  - `modeling.py`
- **Confirmed:** the messy SNAP multiline header was normalized
- **Confirmed:** date parsing was made explicit

### Phase 3: Save a real model artifact

- **Confirmed:** `train_model.py` was added
- **Confirmed:** outputs include:
  - `training/artifacts/model.joblib`
  - `training/artifacts/metrics.json`
  - `training/artifacts/feature_columns.json`
- **Confirmed:** metrics were recorded for a 12-row model dataframe

### Phase 4: Build the FastAPI inference service

- **Confirmed:** backend code was added with:
  - config
  - schemas
  - predictor
  - app entry point
- **Confirmed:** `/health` and `/predict` were introduced

### Phase 5: Prove the API works

- **Confirmed:** `misc/phase-05-local-api-testing.md` records actual local request and response examples
- **Confirmed:** `/health` returned `status: ok`
- **Confirmed:** `/predict` returned a numeric prediction and `features_used`

### Phase 6: Add the frontend

- **Confirmed:** a Next.js app was created
- **Confirmed:** it renders a single prediction form
- **Confirmed:** it calls the backend with `fetch`
- **Confirmed:** a real CORS issue was encountered and fixed

### Phase 7: Move URL config into env vars

- **Confirmed:** the frontend stopped hardcoding the backend URL
- **Confirmed:** it now reads `NEXT_PUBLIC_API_BASE_URL`

### Phase 8: Improve architecture docs

- **Confirmed:** the root `README.md` was expanded to explain the system end to end

### Phase 9: Prepare backend deployment

- **Confirmed:** backend deployment guidance targets Render
- **Confirmed:** `ALLOWED_ORIGINS` became configurable

### Phase 10: Prepare frontend deployment

- **Confirmed:** frontend deployment guidance targets Vercel
- **Confirmed:** docs reference a Render backend URL

### Phase 11: Create interview material

- **Confirmed:** `misc/phase-11-interview-walkthrough.md` contains a concise interview script

## The Design Journey You Can Retell

Here is the best speaking version:

> "The project originally lived in one Colab-style notebook export that mixed analysis, visualization, and modeling. I restructured it into three layers: offline training, online inference, and browser UI. That gave me a cleaner mental model, made deployment easier, and made the app much more explainable in interviews."

## What Changed Later, and Why

- **Confirmed:** hardcoded frontend configuration became env-driven
- **Confirmed:** backend CORS moved into config because the frontend/backend were on different origins
- **Confirmed:** deployment docs were added after the local stack worked
- **Inferred:** the project was intentionally optimized for clarity and interviewability over breadth of features

---

# 3. High-Level Architecture

## System Diagram In Words

```text
User -> Next.js Frontend -> FastAPI /predict -> Feature Transformation -> Trained Random Forest -> JSON Response -> Frontend UI
```

## Expanded Diagram

```text
Raw CSVs
  -> training/data_loading.py
  -> training/prepare_dataset.py
  -> training/modeling.py
  -> model.joblib + metrics.json + feature_columns.json

User in browser
  -> frontend/app/page.tsx
  -> fetch POST /predict
  -> backend/app/main.py
  -> backend/app/schemas.py validation
  -> backend/app/predictor.py feature conversion
  -> loaded model artifact
  -> prediction JSON
  -> rendered result
```

## Frontend

- **Confirmed:** Next.js 16 with App Router
- **Confirmed:** React 19
- **Confirmed:** single page under `frontend/app/page.tsx`
- **Confirmed:** local component state stores form values, error state, loading state, and result state
- **Confirmed:** frontend reads `NEXT_PUBLIC_API_BASE_URL`

## Backend

- **Confirmed:** FastAPI app in `backend/app/main.py`
- **Confirmed:** model loads during app lifespan startup
- **Confirmed:** request validation uses Pydantic models
- **Confirmed:** prediction logic is isolated in `backend/app/predictor.py`
- **Confirmed:** CORS middleware is configured at app startup

## Database / Storage

- **Confirmed:** there is no app database
- **Confirmed:** training uses raw CSV files
- **Confirmed:** runtime model storage is a file on disk: `training/artifacts/model.joblib`
- **Confirmed:** metadata is stored in JSON files

## APIs

- **Confirmed:** `GET /health`
- **Confirmed:** `POST /predict`
- **Confirmed:** frontend only needs the `/predict` contract

## Authentication

- **Confirmed:** none is present
- **Inferred:** this is intentional because the app is scoped as a simple demo/inference system

## External Services

- **Confirmed:** Render is the documented backend hosting target
- **Confirmed:** Vercel is the documented frontend hosting target
- **Confirmed:** the original notebook referenced a remote counties GeoJSON URL for plotting
- **Confirmed:** the rebuilt app no longer depends on that plotting path

## Deployment

- **Confirmed:** deployment is split by layer
- **Confirmed:** backend should run from repo root so it can access `training/artifacts/model.joblib`
- **Confirmed:** frontend is rooted at `frontend/` in Vercel
- **Confirmed:** CORS must be updated after frontend deployment

---

# 4. Folder and File Map

## Top-Level Folder Map

| Path | What it is | Interview priority |
| --- | --- | --- |
| `training/` | Offline data prep and model training | Must know deeply |
| `backend/` | FastAPI inference API | Must know deeply |
| `frontend/` | Next.js user interface | Must know deeply |
| `misc/` | Build phases, planning, design history, interview notes | Must know deeply |
| `ml4va.py` | Original notebook-export style source material | Know at medium level |
| `README.md` | Main system overview | Must know deeply |
| `pyrightconfig.json` | Editor/type-checking support | Can mention briefly |

## Important Files

| File | Why it matters | Priority |
| --- | --- | --- |
| `README.md` | Best high-level description of the whole system | Must know deeply |
| `training/src/food_forecast/prepare_dataset.py` | Core data cleaning and feature engineering | Must know deeply |
| `training/src/food_forecast/modeling.py` | Model training and evaluation logic | Must know deeply |
| `training/train_model.py` | End-to-end training entry point | Must know deeply |
| `backend/app/predictor.py` | Inference feature transformation and model call | Must know deeply |
| `backend/app/main.py` | FastAPI startup, CORS, routes | Must know deeply |
| `backend/app/schemas.py` | API contract | Must know deeply |
| `backend/app/config.py` | Model path and CORS config | Know at medium level |
| `frontend/app/page.tsx` | Form, API call, result rendering | Must know deeply |
| `frontend/app/layout.tsx` | App shell | Can mention briefly |
| `training/artifacts/metrics.json` | Honest record of model quality | Know at medium level |
| `training/artifacts/feature_columns.json` | Frozen feature order contract | Know at medium level |
| `misc/food_forecast_rebuild_85bc3663.plan.md` | Original rebuild reasoning | Must know deeply |
| `misc/phase-01` to `phase-11` | Sequential implementation story | Must know deeply |

## What You Can Safely De-Emphasize

- `frontend/app/globals.css`
- lockfiles
- generated `.next/` content
- minimal boilerplate files

---

# 5. End-to-End App Flow

## What Happens When a User Loads the App

1. **Confirmed:** Next.js serves the page defined in `frontend/app/page.tsx`.
2. **Confirmed:** the browser renders a form with default numeric values.
3. **Confirmed:** no initial backend fetch happens on page load.
4. **Confirmed:** the backend URL comes from `NEXT_PUBLIC_API_BASE_URL`.

## What Happens When the User Performs the Main Action

1. **Confirmed:** the user submits the form.
2. **Confirmed:** `handleSubmit` prevents default browser form submission.
3. **Confirmed:** the frontend clears old errors/results and sets `isSubmitting`.
4. **Confirmed:** the frontend sends JSON to `POST {BACKEND_URL}/predict`.
5. **Confirmed:** the backend validates the request using `PredictionRequest`.
6. **Confirmed:** the backend converts raw inputs into model features.
7. **Confirmed:** the backend builds a one-row pandas DataFrame.
8. **Confirmed:** the loaded model runs `predict`.
9. **Confirmed:** the backend returns:
   - `predicted_food_lbs`
   - `features_used`
10. **Confirmed:** the frontend renders the numeric result and the features list.

## Where Validation Happens

- **Confirmed:** browser input elements use HTML constraints like `min`, `max`, and `required`
- **Confirmed:** backend request validation is stronger and authoritative through Pydantic:
  - `month` must be `1-12`
  - `population` must be `> 0`
  - counts must be non-negative

## Where Data Is Transformed

- **Confirmed:** raw training data is transformed in `training/src/food_forecast/prepare_dataset.py`
- **Confirmed:** request-time feature transformation happens in `backend/app/predictor.py`

## Where State Changes Happen

- **Confirmed:** frontend local React state changes in `frontend/app/page.tsx`
- **Confirmed:** backend does not persist request state
- **Confirmed:** the only backend app state is the loaded model stored on `app.state.model`

## Where API Calls Happen

- **Confirmed:** the frontend performs the main API call via `fetch`
- **Confirmed:** there is no additional client data fetching layer

## Where Business Logic Lives

- **Confirmed:** training-side business logic for data prep lives in `prepare_dataset.py`
- **Confirmed:** runtime inference business logic lives in `predictor.py`
- **Confirmed:** route wiring lives in `main.py`
- **Confirmed:** frontend business logic is mostly submission state handling

## Where Failures Can Happen

- missing or invalid frontend env var
- invalid request payload
- missing model artifact
- dependency/environment issues in Python
- CORS misconfiguration between frontend and backend
- model/training contract drift if features change later

---

# 6. Core Features Breakdown

## Feature 1: Offline Model Training

### What it does

**Confirmed:** Reads raw CSVs, cleans them, builds a monthly model dataframe, trains a Random Forest, evaluates it, and saves artifacts.

### Main files

- `training/src/food_forecast/data_loading.py`
- `training/src/food_forecast/prepare_dataset.py`
- `training/src/food_forecast/modeling.py`
- `training/train_model.py`

### What data it needs

- `va_food_banks.csv`
- `HDPulse_data_export.csv`
- `Dec_2024_Participation_Report.csv`
- `bls_unemployment_by_month_county.csv`
- `2010_2024_population.csv`

### Code path

```text
load_raw_datasets
  -> prepare_datasets
  -> build_model_dataframe
  -> train_random_forest
  -> evaluate_model
  -> save model + metrics + feature columns
```

### How to explain it in an interview

> "I kept all historical data prep and model training offline. The training pipeline turns several raw public datasets into one clean model dataframe, trains a Random Forest, and saves a joblib artifact that the API can load later."

## Feature 2: API Inference

### What it does

**Confirmed:** Accepts raw numeric business inputs and returns a prediction.

### Main files

- `backend/app/schemas.py`
- `backend/app/predictor.py`
- `backend/app/main.py`

### What data it needs

- request JSON
- saved model artifact

### Code path

```text
POST /predict
  -> PredictionRequest validation
  -> build_feature_payload
  -> one-row DataFrame
  -> model.predict
  -> PredictionResponse
```

### How to explain it in an interview

> "The backend owns the prediction contract. It takes user-friendly inputs, transforms them into the exact feature shape the model expects, then runs inference using the saved artifact."

## Feature 3: Health Checking

### What it does

**Confirmed:** Exposes a simple route for service status.

### Main file

- `backend/app/main.py`

### Why it matters

**Confirmed:** the phase docs explicitly treat this as important operational behavior.

### How to explain it

> "I added a health endpoint because real services need a lightweight way to confirm startup and dependency loading before you debug actual business requests."

## Feature 4: Browser UI

### What it does

**Confirmed:** Renders a form, submits the request, shows loading/errors, and displays the prediction.

### Main files

- `frontend/app/page.tsx`
- `frontend/app/globals.css`

### What data it needs

- user input values
- backend base URL from env

### Code path

```text
form state
  -> handleSubmit
  -> fetch /predict
  -> response JSON
  -> result panel
```

### How to explain it

> "The frontend is intentionally thin. It does not know model internals; it just collects inputs, calls the API, and renders the result."

## Feature 5: Deployment Configuration

### What it does

**Confirmed:** Makes the app portable across local and deployed environments.

### Main files

- `backend/app/config.py`
- `frontend/.env.local.example`
- `frontend/.env.production.example`
- `backend/README.md`
- `frontend/README.md`

### How to explain it

> "I separated code from configuration. The frontend reads the backend URL from a browser-exposed Next.js env var, and the backend reads things like model path and allowed origins from environment variables."

---

# 7. Key Technologies and Why They Were Used

| Technology | What it is | Role here | Why it was likely chosen | Tradeoff |
| --- | --- | --- | --- | --- |
| Next.js | React framework | Frontend app shell and page routing | Popular, production-shaped, easy Vercel deployment | More framework than this tiny UI strictly needs |
| React | UI library | Form state and rendering | Standard for interactive web UIs | Could be overkill for a one-page form, but good interview signal |
| TypeScript | Typed JS | Safer frontend code | Better correctness and interview clarity | Slightly more setup |
| FastAPI | Python web framework | Backend inference API | Fast to build, clean request validation, good for ML APIs | Still requires Python runtime and dependency management |
| Pydantic | Validation layer | Request/response schemas | Clear API contract and runtime validation | Another abstraction layer to learn |
| pandas | Data manipulation library | CSV loading, cleaning, transforms | Standard for tabular ML pipelines | Type-checking and schema discipline are weaker than stricter systems |
| scikit-learn | ML library | Random Forest model | Simple, proven, easy to serialize | Limited production story compared with fuller MLOps setups |
| joblib | Serialization tool | Saves trained model artifact | Common and easy for scikit-learn artifacts | Tight coupling to Python/sklearn artifact format |
| Render | Hosting platform | Backend deployment target | Simple Python API hosting | Less control than more custom infra |
| Vercel | Hosting platform | Frontend deployment target | Great fit for Next.js | Build-time env handling can surprise beginners |

## Simple Way To Explain The Stack

> "I chose a lightweight but realistic stack: pandas and scikit-learn for offline training, FastAPI for serving predictions, and Next.js for the browser UI. That let me keep each layer simple but still talk about real API boundaries and deployment concerns."

---

# 8. Important Data Models / Schemas / API Contracts

## API Request Contract

**Confirmed:** `PredictionRequest` contains:

```json
{
  "month": 6,
  "population": 100000,
  "snap_participants": 12000,
  "unemployed_people": 4500,
  "people_below_poverty": 15000,
  "previous_month_food_lbs": 70000
}
```

## API Response Contract

**Confirmed:** `PredictionResponse` contains:

```json
{
  "predicted_food_lbs": 76964.97900675687,
  "features_used": {
    "month": 6.0,
    "snap_per_capita": 0.12,
    "unemp_per_capita": 0.045,
    "poverty_per_capita": 0.15,
    "prev_food": 70000.0
  }
}
```

## Internal Runtime Feature Contract

**Confirmed:** the trained model uses these features:

- `month`
- `snap_per_capita`
- `unemp_per_capita`
- `poverty_per_capita`
- `prev_food`

## Training Dataset Shape

**Confirmed:** the training code creates a monthly aggregated dataframe.

**Confirmed:** it computes:

- mean food distributed by month
- mean SNAP participants by month
- mean unemployment by month
- average population for 2024
- average poverty count
- lagged previous food value

**Important interview insight:** this means the final model is trained on a very small, aggregated table, not on a large row-per-county production dataset.

## Important Entities And Relationships

| Entity | Source | Role |
| --- | --- | --- |
| food bank data | `va_food_banks.csv` | target and historical food data |
| SNAP data | `Dec_2024_Participation_Report.csv` | social assistance input |
| unemployment data | `bls_unemployment_by_month_county.csv` | labor input |
| poverty data | `HDPulse_data_export.csv` | poverty input |
| population data | `2010_2024_population.csv` | normalization denominator |
| model artifact | `model.joblib` | runtime prediction engine |

## How Data Changes Across Layers

```text
Raw CSV rows
  -> cleaned pandas DataFrames
  -> monthly aggregated model dataframe
  -> trained Random Forest artifact
  -> backend receives raw user counts
  -> backend computes per-capita features
  -> model outputs predicted pounds
  -> frontend renders the result
```

## Certain vs Inferred vs Unknown

- **Confirmed:** the backend request contract is simpler than the actual model feature contract.
- **Confirmed:** the backend is responsible for the translation.
- **Inferred:** this design was chosen to make the frontend less ML-aware and easier to use.
- **Unknown:** whether a future version was meant to evolve into county-level predictions or richer forecasting workflows.

---

# 9. Important Code Snippets to Memorize

Pick a few. Do not try to memorize the entire codebase.

## Snippet 1: Backend startup loads the model once

```python
@asynccontextmanager
async def lifespan(app: FastAPI):
    app.state.model = load_model()
    yield
```

### What it does

Loads the trained model when the FastAPI app starts instead of reloading it on every request.

### Why it matters architecturally

This cleanly separates startup initialization from request handling and keeps inference fast.

### How to talk about it out loud

> "The backend loads the model once at startup and stores it in app state, which avoids repeated disk I/O and makes the request path simpler."

## Snippet 2: Request validation contract

```python
class PredictionRequest(BaseModel):
    month: int = Field(ge=1, le=12)
    population: float = Field(gt=0)
    snap_participants: float = Field(ge=0)
    unemployed_people: float = Field(ge=0)
    people_below_poverty: float = Field(ge=0)
    previous_month_food_lbs: float = Field(ge=0)
```

### What it does

Defines the shape and constraints of the incoming API body.

### Why it matters architecturally

It makes the API contract explicit and keeps invalid inputs out of the inference logic.

### How to talk about it out loud

> "I used schema validation at the API boundary so the backend can reject bad inputs before they reach the model logic."

## Snippet 3: Raw inputs become model features

```python
def build_feature_payload(request: PredictionRequest) -> FeaturePayload:
    population = request.population
    return FeaturePayload(
        month=float(request.month),
        snap_per_capita=request.snap_participants / population,
        unemp_per_capita=request.unemployed_people / population,
        poverty_per_capita=request.people_below_poverty / population,
        prev_food=float(request.previous_month_food_lbs),
    )
```

### What it does

Turns human-friendly API inputs into the model feature space.

### Why it matters architecturally

This is the key bridge between the frontend contract and the trained model contract.

### How to talk about it out loud

> "The backend acts as the translation layer. The frontend sends intuitive business values, and the backend computes the normalized features the model was trained on."

## Snippet 4: Frontend API call

```typescript
const response = await fetch(`${BACKEND_URL}/predict`, {
  method: "POST",
  headers: {
    "Content-Type": "application/json",
  },
  body: JSON.stringify({
    month: Number(form.month),
    population: Number(form.population),
    snap_participants: Number(form.snapParticipants),
    unemployed_people: Number(form.unemployedPeople),
    people_below_poverty: Number(form.peopleBelowPoverty),
    previous_month_food_lbs: Number(form.previousMonthFoodLbs),
  }),
});
```

### What it does

Sends the form state to the backend in the exact API format expected by FastAPI.

### Why it matters architecturally

It shows the frontend/backend contract in one place.

### How to talk about it out loud

> "The frontend is intentionally thin. Its main responsibility is packaging user inputs into the backend API contract and rendering the response."

## Snippet 5: Training and artifact handoff

```python
model = train_random_forest(model_df, n_estimators=100, random_state=42)
evaluation = evaluate_model(model, model_df)

joblib.dump(model, MODEL_ARTIFACT_PATH)
METRICS_PATH.write_text(json.dumps(metrics_payload, indent=2), encoding="utf-8")
FEATURE_COLUMNS_PATH.write_text(json.dumps(MODEL_FEATURES, indent=2), encoding="utf-8")
```

### What it does

Trains the model, evaluates it, and writes the artifact plus metadata to disk.

### Why it matters architecturally

This is the handoff point from offline training to online inference.

### How to talk about it out loud

> "I made the artifact and metadata explicit so the backend can serve predictions without retraining and so the training contract is inspectable."

## Snippet 6: Data prep builds the tiny monthly model table

```python
monthly_food = food_bank.groupby("month")["food_distributed_pounds"].mean().reset_index()
monthly_snap = snap.groupby("month")["persons_total"].mean().reset_index()
monthly_unemployment = unemployment.groupby("month")["unemployment"].mean().reset_index()

model_df["prev_food"] = model_df["food_distributed_pounds"].shift(1)
model_df["prev_food"] = model_df["prev_food"].fillna(
    model_df["food_distributed_pounds"].mean()
)
```

### What it does

Aggregates historical data into one row per month and adds a lag feature.

### Why it matters architecturally

It explains both the feature engineering and one of the biggest project limitations.

### How to talk about it out loud

> "The current model is intentionally simple. It collapses the historical data into 12 monthly rows and uses month-level averages plus a lag feature to make a prediction."

---

# 10. Design Decisions and Tradeoffs

## Why This Stack

**Confirmed:** the rebuild uses pandas + scikit-learn + FastAPI + Next.js.

Best interview explanation:

> "I wanted a stack that was easy to reason about, fast to implement, and still realistic enough to demonstrate clean separation between training, inference, and UI."

## Why This Folder Structure

**Confirmed:** the repo is split by responsibility, not by generic tech buckets.

Why that is a good answer:

- training concerns stay in `training/`
- online serving concerns stay in `backend/`
- browser concerns stay in `frontend/`
- design history stays in `misc/`

## Why This API Design

**Confirmed:** API inputs are business-style fields, not raw model features.

Tradeoff:

- Pro: easier frontend, clearer API
- Con: backend must own transformation logic and stay aligned with training

## Why This State Model

**Confirmed:** frontend uses local component state only.

Tradeoff:

- Pro: simplest possible solution for one page
- Con: not scalable to a large multi-page app with shared global state

## Why File-Based Persistence Instead of a DB

**Confirmed:** only artifacts and raw CSVs are stored

Tradeoff:

- Pro: simple and easy to explain
- Con: no request history, no audit trail, no user workflows

## Why Random Forest

**Confirmed:** the training code uses `RandomForestRegressor`

**Inferred:** it was chosen because it is easy to implement, explain, and serialize.

Tradeoff:

- Pro: simple, fast, familiar
- Con: not necessarily the strongest forecasting approach, especially with very small data

## Why Separate Deployment Targets

**Confirmed:** backend docs target Render, frontend docs target Vercel.

Tradeoff:

- Pro: aligns each layer with a platform that fits it well
- Con: introduces cross-origin config and multi-service deployment complexity

## Alternatives That Could Have Been Used

- Single Flask or FastAPI app serving both API and HTML
- Server-side rendered app with Python templates instead of Next.js
- A database for storing prediction history
- A more rigorous time-series pipeline
- Dockerized deployment
- Typed feature contract shared more explicitly between training and backend

## The Best Honest Framing

> "I optimized for clean architecture and explainability first, not full product maturity. That let me focus on the software boundaries that matter most in interviews."

---

# 11. Weak Spots / Risks / Things I Must Be Honest About

## ML / Data Risks

- **Confirmed:** the model is trained on only 12 rows
- **Confirmed:** evaluation is in-sample
- **Confirmed:** metrics therefore should not be oversold
- **Confirmed:** population and poverty become averaged/static values in the monthly training table
- **Inferred:** this makes the model more like a lightweight demo regressor than a production-grade forecasting engine

## Architecture Risks

- **Confirmed:** no database
- **Confirmed:** no authentication
- **Confirmed:** no authorization
- **Confirmed:** no rate limiting
- **Confirmed:** no background retraining pipeline
- **Confirmed:** no automated tests

## Contract Drift Risk

- **Confirmed:** `feature_columns.json` is saved during training
- **Confirmed:** backend predictor builds features by code, not by reading the JSON metadata
- **Inferred:** if training features changed later, backend and model could drift apart unless both were updated together

## Operational Risks

- **Confirmed:** the backend depends on the model artifact existing at startup
- **Confirmed:** a missing artifact raises a `FileNotFoundError`
- **Confirmed:** split frontend/backend deployment requires correct CORS configuration

## Product Risks

- **Confirmed:** the UI is minimal
- **Confirmed:** there is no saved history or user workflow
- **Confirmed:** it is not obvious that a non-technical end user would know what numeric values to enter without context

## How To Say This Well In An Interview

> "The main limitations are around ML rigor and product maturity, not system shape. The architecture is clean, but the current model is trained on a tiny aggregated dataset, evaluated in-sample, and wrapped in a deliberately simple API/UI."

---

# 12. Likely Final-Round Interview Questions

## Architecture

### Q: Why did you split the app into training, backend, and frontend?

**Model answer:**

> "Because those layers have different responsibilities and different runtime behavior. Training is offline and should not run on every request. The backend owns inference and API validation. The frontend owns user interaction. That separation made the system easier to reason about, easier to deploy, and much easier to explain."

### Q: Why not just keep everything in one Python app?

**Model answer:**

> "I could have, but I wanted a cleaner contract boundary. A separate frontend and API better reflects how production systems are often structured and forces me to define the request and response contract clearly."

## Data Flow

### Q: How does data flow through the system?

**Model answer:**

> "Historical CSVs are used offline to train a model and save an artifact. At runtime, the browser sends raw numeric inputs to the API. The API validates them, transforms them into the model feature format, runs inference using the saved artifact, and returns JSON that the frontend renders."

### Q: Where does inference happen?

**Model answer:**

> "Inference happens in the backend, specifically in the predictor layer after request validation. The frontend never touches the model directly."

## Design Choices

### Q: Why did you use FastAPI?

**Model answer:**

> "FastAPI is a strong fit for Python-based inference services because request validation is clear, route definitions are compact, and it is straightforward to expose prediction endpoints."

### Q: Why use a Random Forest?

**Model answer:**

> "For this rebuild I prioritized a model that was easy to train, explain, and serialize. The real engineering goal here was the system boundary between training and serving, not maximizing model sophistication."

## Debugging

### Q: What was the hardest integration issue?

**Model answer:**

> "CORS was the most real full-stack issue. The frontend and backend were on different origins, so even though the API worked directly, the browser blocked the request until I configured allowed origins in FastAPI."

### Q: Did you run into any messy data issues?

**Model answer:**

> "Yes. The SNAP CSV had a multiline header that normalized into an awkward column name, so I had to map it to a clean internal field. That was a good example of how real datasets are often messier than the modeling idea itself."

## Performance / Scaling

### Q: How would this scale?

**Model answer:**

> "The current request path is lightweight because it loads the model once and makes single-row predictions, so basic API scaling is fine. The bigger scaling gaps are around data volume, retraining workflows, monitoring, testing, and product features like persistence."

### Q: What would you change if request traffic grew?

**Model answer:**

> "I would add structured logging, metrics, rate limiting, and automated tests first. After that I would think about model versioning, more explicit feature contracts, and possibly a database if we needed request history or user workflows."

## Security

### Q: What security concerns exist here?

**Model answer:**

> "There is no auth or rate limiting, so I would not present this as production-secure. It is a clean demo architecture, not a hardened public service."

## Ownership / Collaboration

### Q: How would you explain your technical ownership here?

**Model answer:**

> "My ownership story is strongest around architecture and integration. I can explain how the original notebook logic was decomposed into training, serving, and frontend layers, how the API contract was designed, how deployment configuration works, and where the limitations are."

## Improvements

### Q: What would you improve next?

**Model answer:**

> "First, I would improve model evaluation with train/test or time-based validation. Second, I would add backend tests. Third, I would tighten the training-serving feature contract so the backend and training metadata stay in sync automatically. After that, I would consider persistence, logging, and a more product-friendly UI."

---

# 13. How To Talk About This App

## 30-Second Version

> "This is a full-stack ML app for predicting monthly food distribution needs. I split it into an offline training pipeline, a FastAPI backend for inference, and a Next.js frontend for user input and results. The main architectural goal was to separate training from serving so the system is easier to understand, deploy, and explain."

## 1-Minute Version

> "The project started as a notebook-style ML script that mixed data cleaning, analysis, and experiments. I restructured it into three layers. The training layer reads several CSV datasets, prepares a monthly model dataframe, trains a Random Forest, and saves a joblib artifact plus metadata. The backend loads that artifact at startup and exposes `/health` and `/predict`. The frontend is a thin Next.js app that collects raw business inputs, sends them to the backend, and renders the returned prediction. The biggest real integration issue I handled was CORS between the frontend and backend."

## 2-Minute Walkthrough

> "At a high level, this app predicts monthly food distribution needs from socioeconomic inputs like population, SNAP participation, unemployment, poverty, and previous food distributed. The project originally lived in a single Colab-style script, but I rebuilt it into a cleaner architecture with `training/`, `backend/`, and `frontend/`. In the training layer, I load five raw CSV datasets, normalize messy fields like FIPS and a multiline SNAP header, build a monthly aggregated dataframe, train a Random Forest, and save `model.joblib`, `metrics.json`, and `feature_columns.json`. In the backend, FastAPI loads the model once at startup and exposes `/predict`. That endpoint validates incoming JSON, converts raw business fields into the exact feature format used during training, runs inference, and returns the prediction plus the features used. In the frontend, a simple Next.js page manages form state, calls the backend with `fetch`, and shows the result. The main tradeoff is that the current model is intentionally simple: it is trained on only 12 monthly rows and evaluated in-sample, so I would describe it as a clean end-to-end architecture demo rather than a fully mature forecasting platform."

## "Tell Me About This Project" Answer

> "I worked on rebuilding a food insecurity forecasting project into a cleaner software architecture. The original version was a notebook-style ML script, so I pulled it apart into three responsibilities: offline training, online inference, and browser UI. That meant building a reusable training pipeline, saving a model artifact, serving predictions through FastAPI, and wiring a Next.js frontend to call the API. The most important thing I learned was how valuable it is to define a clear contract between layers instead of mixing data science code, request handling, and UI logic together."

## "What Was Technically Hardest?" Answer

> "The hardest part was not writing the individual pieces, it was preserving the original modeling logic while making the system cleaner. I had to understand what parts of the original notebook were essential for serving predictions and what parts were exploratory only. On top of that, I hit real integration details like a messy multiline SNAP header and CORS between frontend and backend."

## "What Would You Improve Next?" Answer

> "I would improve the ML rigor first by introducing stronger evaluation instead of in-sample scoring on 12 rows. Then I would add backend tests and make the training-serving feature contract more explicit so drift is less likely. After that I would consider persistence, better logging, and a more user-friendly frontend."

## "How Did Data Flow Through The System?" Answer

> "Offline, the system reads historical CSVs, prepares a model dataframe, trains a model, and saves an artifact. Online, the browser collects raw inputs and sends them to FastAPI. FastAPI validates the payload, computes the normalized features the model expects, runs prediction, and returns JSON that the frontend renders."

---

# 14. What I Absolutely Need To Understand

## Must Know Deeply

- why the system is split into `training/`, `backend/`, and `frontend/`
- the exact request and response shape of `/predict`
- the difference between raw API inputs and model features
- how `prepare_dataset.py` turns messy CSVs into a monthly model table
- how `predictor.py` transforms request data into model input
- how `train_model.py` creates the artifact handoff to the backend
- why the model evaluation is weak and how to discuss that honestly
- the CORS story
- the `ml4va.py` to monorepo rebuild story

## Should Know Reasonably Well

- Render and Vercel deployment setup
- environment variable behavior in Next.js and backend config
- where validation happens on the frontend vs backend
- why the backend loads the model at startup
- what each raw CSV contributes conceptually

## Can Discuss At High Level

- exact CSS/styling details
- boilerplate framework files
- pyright config details
- lockfiles and generated framework artifacts

---

# 15. Interview Cheat Sheet

## Top 10 Files

1. `README.md`
2. `training/src/food_forecast/prepare_dataset.py`
3. `training/src/food_forecast/modeling.py`
4. `training/train_model.py`
5. `backend/app/predictor.py`
6. `backend/app/main.py`
7. `backend/app/schemas.py`
8. `frontend/app/page.tsx`
9. `misc/food_forecast_rebuild_85bc3663.plan.md`
10. `misc/phase-11-interview-walkthrough.md`

## Top 10 Concepts

1. training vs serving
2. API contract
3. feature engineering
4. model artifact handoff
5. request validation
6. frontend/backend separation
7. environment-based configuration
8. CORS
9. data cleaning from messy real CSVs
10. honest discussion of model limitations

## Top 10 Phrases You Can Say

1. "I separated offline training from online inference."
2. "The backend owns the prediction contract."
3. "The frontend sends business-friendly inputs, not raw model features."
4. "The backend translates request data into the trained feature space."
5. "The model artifact is the handoff point between training and serving."
6. "I optimized for architecture clarity and explainability first."
7. "The original project started as a notebook-style script and I extracted the production-relevant path."
8. "CORS was a real integration issue once the frontend and backend lived on different origins."
9. "The current evaluation is intentionally simple and I would qualify it clearly."
10. "The codebase is small, but the system boundaries are real."

## Top 10 Risks To Be Ready For

1. only 12 training rows
2. in-sample evaluation
3. no tests
4. no auth
5. no rate limiting
6. no database or prediction history
7. feature drift risk between training and backend
8. simple UI with minimal product workflow
9. dependency/setup friction in Python environments
10. architecture is stronger than the ML rigor

---

# Fastest Study Plan

If you only have limited time, study in this order:

1. Read `README.md`
2. Read `backend/app/predictor.py`
3. Read `frontend/app/page.tsx`
4. Read `training/src/food_forecast/prepare_dataset.py`
5. Read `training/train_model.py`
6. Read `misc/food_forecast_rebuild_85bc3663.plan.md`
7. Read `misc/phase-05`, `phase-06`, `phase-09`, and `phase-11`

Then practice answering:

1. What does the app do?
2. Why is it split into three layers?
3. What happens when the user clicks submit?
4. Where does inference happen?
5. What are the main limitations?
6. What would you improve next?

If you can answer those smoothly, you can carry the interview conversation.
