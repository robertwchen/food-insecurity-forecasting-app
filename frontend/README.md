# Frontend Layer

This folder will contain the Next.js and TypeScript application.

## Structure

```text
frontend/
  .env.local.example
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

This layer should not contain Python training code or direct model files.
