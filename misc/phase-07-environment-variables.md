# Phase 7 Study Notes

## What We Built

We replaced the hardcoded backend URL in the frontend with an environment variable.

New files:

```text
frontend/
  .env.local
  .env.local.example
```

Updated file:

```text
frontend/app/page.tsx
```

## Why This Phase Exists

Hardcoding the backend URL in frontend code is okay for a quick demo, but it becomes a problem when:
- local development uses one URL
- production uses another URL

Environment variables solve that by moving deployment-specific values out of the app code.

## What Layer We Worked On

This phase is mostly in the `frontend/` layer.

The important idea is that configuration is not the same thing as business logic.

## Important File Roles

### `frontend/app/page.tsx`
Role:
- read the backend base URL from `NEXT_PUBLIC_API_BASE_URL`
- use that value when sending the `fetch` request

Inputs:
- browser form values
- environment variable value

Outputs:
- prediction request to the backend
- rendered response

Why separate:
- page logic should use configuration, not store configuration inline

### `frontend/.env.local`
Role:
- store your local frontend runtime configuration

Inputs:
- local development backend URL

Outputs:
- environment values injected into the Next.js app at startup

Why separate:
- local configuration changes often, but the code should not need to change

### `frontend/.env.local.example`
Role:
- show the expected environment variable format

Inputs:
- none

Outputs:
- a template for teammates or future setup

Why separate:
- example files can be committed safely, while real `.env.local` files usually should not be

## Exact Environment Variable

For this project, the frontend now uses:

```text
NEXT_PUBLIC_API_BASE_URL
```

Local value:

```text
NEXT_PUBLIC_API_BASE_URL=http://127.0.0.1:8000
```

## Why It Starts With `NEXT_PUBLIC_`

In Next.js, variables used in browser-side code must start with `NEXT_PUBLIC_`.

Why:
- this tells Next.js the value is allowed to be exposed to client-side JavaScript
- the browser cannot read server-only environment variables

## Local Development Vs Production

Local development:
- `NEXT_PUBLIC_API_BASE_URL` points to your local FastAPI backend
- example: `http://127.0.0.1:8000`

Production:
- the same variable would point to your deployed backend URL
- example: a Render, Railway, or other hosted backend URL

That means the frontend code stays the same.
Only the configuration changes.

## Commands For This Phase

From the `frontend/` directory, create the local env file:

```powershell
Copy-Item .env.local.example .env.local
```

Run the frontend:

```powershell
npm run dev
```

Important note:
- if you change `.env.local`, restart the Next.js dev server
- Next.js reads env vars when it starts

## Validation Performed

- updated the frontend code to read `NEXT_PUBLIC_API_BASE_URL`
- added `.env.local.example`
- added `.env.local` for local development
- confirmed the browser-to-backend flow still works after restarting the frontend with the env var in place

## How To Test This Phase Yourself

1. Make sure `frontend/.env.local` exists
2. Confirm it contains:

```text
NEXT_PUBLIC_API_BASE_URL=http://127.0.0.1:8000
```

3. Restart the frontend dev server
4. Open `http://localhost:3000`
5. Submit the prediction form
6. Confirm the prediction still works

## Git Commands For This Phase

Check changes:

```powershell
git status
```

Stage Phase 7 files:

```powershell
git add frontend/app/page.tsx frontend/.env.local.example frontend/README.md misc/phase-07-environment-variables.md
```

Suggested commit:

```powershell
git commit -m "Configure frontend backend URL with env vars"
```

Push decision:
- yes, this is a clean point to push
- the frontend is now easier to run locally and easier to deploy later

If you push:

```powershell
git push
```

## Commit Boundary Reason

This is a good commit boundary because it captures configuration cleanup separately from the original frontend feature work.

## Interview Talking Points

- I removed the hardcoded backend URL from the frontend and replaced it with a Next.js environment variable.
- I used a committed example env file so the setup is easy to understand without exposing local-only configuration.
- This lets the same frontend code run against different backend URLs in local development versus production.
- It also reinforces the separation between code and configuration, which is an important deployment concept.
