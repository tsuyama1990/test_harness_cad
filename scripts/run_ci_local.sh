#!/bin/bash
# Local CI script to run checks sequentially.
# Exits immediately if any command fails.
set -e

echo "--- Running Format Check ---"
./.venv/bin/ruff format --check .
(cd frontend && npm run lint)

echo "--- Running Type Check ---"
./.venv/bin/mypy app

echo "--- Running Backend Tests ---"
./.venv/bin/pytest --cov=app

echo "--- Running Frontend Build Check ---"
(cd frontend && npm run build)

echo "--- All checks passed successfully! ---"
