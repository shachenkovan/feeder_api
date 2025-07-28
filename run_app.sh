#!/bin/bash

cd "$(dirname "$0")"

if [ ! -d "venv" ]; then
  python3 -m venv venv
fi

source venv/bin/activate

pip install --upgrade pip
pip install -r requirements.txt

uvicorn api.service:app --host 127.0.0.1 --port 8000 --reload
