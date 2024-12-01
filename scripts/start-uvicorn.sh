#!/usr/bin/env bash

set -e

HOST=${HOST:-0.0.0.0}
PORT=${PORT:-8000}
# Start Uvicorn
poetry run uvicorn main:app --host $HOST --port $PORT --workers 4
