#!/usr/bin/env bash

# Enter the virtual environment
echo "CREATING VIRTUAL ENVIRONMENT"
python -m venv env
source env/bin/activate
exec "$@"

echo "INSTALLING REQUIRED PIP PACKAGES"

# Install required Python packages (via pip)
pip install -r requirements.txt

$SHELL