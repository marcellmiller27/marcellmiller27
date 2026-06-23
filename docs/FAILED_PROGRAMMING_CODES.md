# Failed Programming Codes and Fixes

## Purpose

This file records the failed programming commands, error messages, and fixes encountered while building the John Henry Investments platform application.

Use this as a troubleshooting reference if future agents or developers encounter the same issues.

## Current final status

The platform currently verifies successfully with:

```bash
python3 -m compileall backend/app backend/tests
python3 -m pytest backend/tests
python3 -m ruff check backend
npm run typecheck
npm run lint
npm run build
npm audit --audit-level=moderate
```

Latest successful backend test count at the time this file was created:

```text
20 passed
```

## Failure 1 - JSX lint failure from unescaped quotes

### Failed command

```bash
npm run typecheck && npm run lint && npm run build && npm audit --audit-level=moderate
```

### Error

```text
/workspace/src/app/page.tsx
154:38  error  `"` can be escaped with `&quot;`, `&ldquo;`, `&#34;`, `&rdquo;`  react/no-unescaped-entities
154:52  error  `"` can be escaped with `&quot;`, `&ldquo;`, `&#34;`, `&rdquo;`  react/no-unescaped-entities
155:83  error  `"` can be escaped with `&quot;`, `&ldquo;`, `&#34;`, `&rdquo;`  react/no-unescaped-entities
```

### Cause

The JSX copy used literal double quotes around example AI assistant prompts.

### Fix applied

Changed the sentence from quoted examples to plain text examples.

```tsx
Answers questions like Analyze Tesla, Evaluate this business, Compare SBA loans,
Build a dividend portfolio, and Analyze the Bitcoin cycle.
```

## Failure 2 - npm audit failure from nested PostCSS dependency

### Failed command

```bash
npm audit --audit-level=moderate
```

### Error

```text
postcss  <8.5.10
Severity: moderate
PostCSS has XSS via Unescaped </style> in its CSS Stringify Output
fix available via `npm audit fix --force`
Will install next@9.3.3, which is a breaking change
```

### Cause

The installed Next.js dependency tree included a vulnerable nested PostCSS version.

### Fix applied

Added an npm override in `package.json`:

```json
{
  "overrides": {
    "postcss": "^8.5.15"
  }
}
```

Then ran:

```bash
npm install
```

Final result:

```text
found 0 vulnerabilities
```

## Failure 3 - ESLint peer dependency conflict

### Command that produced warnings

```bash
npm install --package-lock-only
```

### Warning

```text
npm warn ERESOLVE overriding peer dependency
peer eslint@"^2 || ^3 || ^4 || ^5 || ^6 || ^7.2.0 || ^8 || ^9"
```

### Cause

The latest ESLint major version installed initially was ahead of the supported peer range for the Next.js ESLint config dependency tree.

### Fix applied

Installed the latest compatible ESLint major:

```bash
npm install --save-dev eslint@9
```

## Failure 4 - Backend command failed because `python` was unavailable

### Failed command

```bash
python --version && python -m pip install -e "backend[dev]"
```

### Error

```text
--: line 1: python: command not found
```

### Cause

The environment exposes Python as `python3`, not `python`.

### Fix applied

Used `python3` consistently:

```bash
python3 --version
python3 -m pip install -e "backend[dev]"
python3 -m compileall backend/app backend/tests
python3 -m pytest backend/tests
python3 -m ruff check backend
```

Documentation was updated to use `python3 -m ...` commands.

## Failure 5 - Ruff lint failure from unused import

### Failed command

```bash
python3 -m ruff check backend
```

### Error

```text
F401 `app.models.JournalEntry` imported but unused
--> backend/app/services.py:13:5
```

### Cause

`JournalEntry` was imported in `backend/app/services.py` but was not used.

### Fix applied

Removed the unused import from `backend/app/services.py`.

## Failure 6 - FastAPI route tests required `httpx2`

### Failed command

```bash
python3 -m pytest backend/tests
```

### Error

```text
RuntimeError: The starlette.testclient module requires the httpx2 package to be installed.
You can install this with:
    $ pip install httpx2
```

### Cause

The FastAPI/Starlette test client required the `httpx2` testing dependency.

### Fix applied

Added `httpx2` to backend development dependencies in `backend/pyproject.toml`:

```toml
[project.optional-dependencies]
dev = [
  "httpx2",
  "pytest",
  "ruff"
]
```

Then reinstalled backend dev dependencies:

```bash
python3 -m pip install -e "backend[dev]"
```

## Failure 7 - Generated Python cache and egg-info files appeared during tests

### Observed files

```text
backend/.pytest_cache/
backend/.ruff_cache/
backend/john_henry_investments_backend.egg-info/
```

### Cause

Python test, lint, and editable install workflows generated local metadata/cache files.

### Fix applied

Updated `.gitignore`:

```gitignore
__pycache__
*.py[cod]
.pytest_cache
.ruff_cache
.venv
*.egg-info
*.db
*.sqlite
*.sqlite3
```

## Failure 8 - Next.js generated TypeScript route types changed config expectations

### Observed behavior

During `next build`, Next.js updated TypeScript-related generated references and route types.

### Fix applied

Updated the typecheck script to generate Next.js route types before running TypeScript:

```json
{
  "scripts": {
    "typecheck": "next typegen && tsc --noEmit"
  }
}
```

## Failure 9 - Patch context mismatch while updating documentation

### Error

```text
Error: Failed to find context
```

### Cause

The target documentation section had changed after previous edits, so the patch context no longer matched exactly.

### Fix applied

Read the current file section, then applied the patch with the exact updated context.

## Final verification command

Use this complete verification command after future programming changes:

```bash
python3 -m compileall backend/app backend/tests && \
python3 -m pytest backend/tests && \
python3 -m ruff check backend && \
npm run typecheck && \
npm run lint && \
npm run build && \
npm audit --audit-level=moderate
```

## Current known status

No known failing programming commands remain at the time this file was created.
