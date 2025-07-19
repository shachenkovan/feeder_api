#!/bin/bash

cd "$(dirname "$0")"

if [ ! -d "venv" ]; then
  python3 -m venv venv
fi

if [ -z "$VIRTUAL_ENV" ]; then
  source venv/bin/activate
fi

uvicorn api.service:app --host 127.0.0.1 --port 8000 --reload
