#!/usr/bin/env bash
set -euo pipefail

if [[ ! -f requirements.txt ]]; then
  echo "requirements.txt not found. Run this script from the project root."
  exit 1
fi

python3 -m venv .venv
source .venv/bin/activate
python -m pip install --upgrade pip
pip install -r requirements.txt

echo "\nCreated virtual environment in .venv and installed packages."

if [[ ! -f .env ]]; then
  cp .env.example .env
  echo "Created .env from .env.example. Edit .env with your OpenAI and Weaviate settings."
else
  echo ".env already exists. Verify your API keys and settings in .env."
fi

echo "\nActivate the environment with: source .venv/bin/activate"
