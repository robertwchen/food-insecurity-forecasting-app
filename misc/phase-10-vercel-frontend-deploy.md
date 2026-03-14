# Phase 10 Study Notes

## What We Built

We prepared the Next.js frontend for Vercel deployment.

This phase focused on:
- documenting the exact Vercel UI settings
- making the production backend URL explicit
- clarifying how frontend deployment interacts with backend CORS settings

## Why This Phase Exists

By this point:
- the backend is deployed on Render
- the frontend works locally

Now we need the browser app to run from a real public URL.

Vercel is a strong fit for this phase because:
- it is designed for Next.js
- deployment is simple through the web UI
- environment variables are easy to configure

## What Layer We Worked On

This phase is in the `frontend/` layer.

But like Phase 9, the focus is deployment configuration rather than product behavior.

## Important File Roles

### `frontend/.env.production.example`
Role:
- show the production backend URL the frontend should use

Inputs:
- deployed backend URL

Outputs:
- an example production env file

Why separate:
- production configuration should be explicit and easy to reference

### `frontend/README.md`
Role:
- document the exact Vercel settings and frontend deployment flow

Inputs:
- actual deployment requirements

Outputs:
- copy/paste deployment instructions

Why separate:
- frontend deployment docs belong with the frontend layer

## Exact Production Backend URL

Deployed backend:

[`https://food-insecurity-forecasting-app.onrender.com/health`](https://food-insecurity-forecasting-app.onrender.com/health)

That means the frontend production env var should be:

```text
NEXT_PUBLIC_API_BASE_URL=https://food-insecurity-forecasting-app.onrender.com
```

## Exact Vercel UI Settings

When creating the Vercel project:

### Framework preset
- `Next.js`

### Root directory
- `frontend`

Why:
- the Next.js app lives in the `frontend/` subdirectory

### Build command
- leave the default Vercel Next.js build command

### Install command
- leave the default install command

### Environment variable

Add this before deploying:

```text
NEXT_PUBLIC_API_BASE_URL=https://food-insecurity-forecasting-app.onrender.com
```

## Important Next.js Deployment Detail

The frontend uses:

```text
NEXT_PUBLIC_API_BASE_URL
```

That matters because:
- `NEXT_PUBLIC_` variables are exposed to browser-side code
- Next.js inlines them at build time

So if you change the backend URL later:
- update the Vercel environment variable
- redeploy the frontend

## Very Important Follow-Up After Vercel Deploy

Once Vercel gives you the deployed frontend URL, go back to Render and update:

```text
ALLOWED_ORIGINS
```

It should include your real Vercel frontend origin.

Why:
- the browser will block cross-origin requests if the backend does not allow the deployed frontend domain

## How To Deploy In Vercel

You should do the deployment in the Vercel web UI yourself so you learn the platform flow.

That means:
- import the GitHub repo into Vercel
- set the root directory to `frontend`
- add `NEXT_PUBLIC_API_BASE_URL`
- deploy

## How To Test After Deploy

After Vercel gives you the frontend URL:

1. open the deployed frontend
2. submit the default prediction form
3. confirm a prediction appears
4. if you get a browser CORS error, update Render `ALLOWED_ORIGINS` and redeploy or restart the backend if needed

## Commands For This Phase

There are no new required local commands beyond the frontend build already tested.

Useful local reference:

```powershell
cd frontend
npm run build
```

## Git Commands For This Phase

Check changes:

```powershell
git status
```

Stage Phase 10 files:

```powershell
git add frontend/README.md frontend/.env.production.example misc/phase-10-vercel-frontend-deploy.md
```

Suggested commit:

```powershell
git commit -m "Prepare frontend for Vercel deployment"
```

Push decision:
- yes, push after this phase
- Vercel deploys from your GitHub repo, so these files should be committed first

Push command:

```powershell
git push
```

## Commit Boundary Reason

This is a good commit boundary because it captures frontend deployment preparation separately from the actual Vercel UI deployment action.

## Interview Talking Points

- I deployed the frontend separately from the backend, which reflects a common real-world architecture.
- I used a browser-exposed Next.js environment variable to point the frontend at the deployed backend API.
- I deployed the FastAPI backend and Next.js frontend on separate platforms and connected them through a clear HTTP API contract.
- I also accounted for cross-origin rules by planning to update the backend CORS settings with the deployed frontend origin.
