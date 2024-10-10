#!/usr/bin/env bash

set -e

HOST=${HOST:-0.0.0.0}
PORT=${PORT:-8000}
# Start Uvicorn with live reload
exec poetry run fastapi dev main.py --host $HOST --port $PORT
