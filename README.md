# SRE Reliability Lab

A small Python/FastAPI project for learning the software development lifecycle through an SRE reliability-monitoring API.

Currently, `GET /health` returns HTTP 200 with `{"status": "healthy"}`. An API test checks this contract. Availability calculations, persistence, CI, and observability are planned learning exercises, not implemented features.

## Run locally (Windows PowerShell)

Use Python 3.13 (the version used in the current development environment).

```powershell
python -m venv .venv
.\.venv\Scripts\python.exe -m pip install -r requirements-dev.txt
.\.venv\Scripts\python.exe -m uvicorn main:app --reload
```

Open http://127.0.0.1:8000/health or the interactive API documentation at http://127.0.0.1:8000/docs. Stop the server with Ctrl+C.

## Run tests

```powershell
.\.venv\Scripts\python.exe -m pytest -q
```

The requirements files pin direct dependencies to the versions installed for this project; transitive dependencies are not locked.

## Project files

- `main.py`: FastAPI application and health endpoint.
- `tests/test_health.py`: health endpoint contract test.
- `requirements.txt`: application dependencies.
- `requirements-dev.txt`: application and test dependencies.

Commit source code, tests, documentation, and dependency declarations. `.gitignore` excludes virtual environments, generated caches, local runtime data, and common secret files. Recreate `.venv` by installing dependencies rather than uploading it.

## Everyday Git workflow

From the project directory, review changes and explicitly stage the files intended for the commit:

```powershell
git status
git diff
git add main.py tests/test_health.py
git diff --cached
git commit -m "Describe the change"
git push
```

Adjust the paths in `git add` to match the files changed. `.gitignore` applies to untracked files; it does not remove files already tracked by Git. Always review the staged diff before committing.
