# Frontend Layer

This folder will contain the Next.js and TypeScript application.

## Structure

```text
frontend/
  .env.local.example
  .env.production.example
  app/
    globals.css
    layout.tsx
    page.tsx
  next-env.d.ts
  next.config.ts
  package.json
  tsconfig.json
```

## Role In The App

- render the form users fill out
- send requests to the backend with `fetch`
- show prediction results in the browser

## File Roles

### `app/layout.tsx`
Inputs:
- page children

Outputs:
- shared HTML document shell

Why separate:
- layout concerns should stay outside page-specific logic

### `app/page.tsx`
Inputs:
- user form values from the browser

Outputs:
- fetch request to the backend
- rendered prediction result

Why separate:
- this file owns the page-level UI and request flow

### `app/globals.css`
Inputs:
- none

Outputs:
- app-wide styling

Why separate:
- presentation should stay separate from React logic

### `.env.local`
Inputs:
- local frontend configuration values

Outputs:
- runtime environment values available in the browser app

Why separate:
- URLs and environment-specific settings should not be hardcoded in React code

## Local Commands

Install frontend dependencies:

```powershell
npm install
```

Run the frontend locally:

```powershell
npm run dev
```

Create your local environment file:

```powershell
Copy-Item .env.local.example .env.local
```

Open the app:

```text
http://localhost:3000
```

## Current Backend Connection

The frontend reads the backend base URL from:

```text
NEXT_PUBLIC_API_BASE_URL
```

For local development, `.env.local` should contain:

```text
NEXT_PUBLIC_API_BASE_URL=http://127.0.0.1:8000
```

For deployment, the production value should point to the deployed backend:

```text
NEXT_PUBLIC_API_BASE_URL=https://food-insecurity-forecasting-app.onrender.com
```

## Vercel Deployment

Recommended approach:
- create the frontend deployment through the Vercel web UI
- set the project root directory to `frontend`

### Vercel UI Settings

Framework preset:
- `Next.js`

Root directory:
- `frontend`

Build command:
- leave the default Vercel Next.js build command

Install command:
- leave the default Vercel install command

### Vercel Environment Variable

Set this in the Vercel project settings before deploying:

```text
NEXT_PUBLIC_API_BASE_URL=https://food-insecurity-forecasting-app.onrender.com
```

Important:
- `NEXT_PUBLIC_` variables are exposed to the browser
- Next.js inlines them at build time, so if you change the value later you need to redeploy

### After Frontend Deployment

Once Vercel gives you the frontend URL, go back to Render and update the backend `ALLOWED_ORIGINS` value to include that deployed frontend origin.

This layer should not contain Python training code or direct model files.
