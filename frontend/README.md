# Frontend Layer

This folder will contain the Next.js and TypeScript application.

## Structure

```text
frontend/
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

## Local Commands

Install frontend dependencies:

```powershell
npm install
```

Run the frontend locally:

```powershell
npm run dev
```

Open the app:

```text
http://localhost:3000
```

## Current Backend Connection

Right now the frontend calls:

```text
http://127.0.0.1:8000
```

directly inside `app/page.tsx`.

That is fine for Phase 6 so you can clearly see the request flow.
In the next phase, we will move that URL into an environment variable.

This layer should not contain Python training code or direct model files.
