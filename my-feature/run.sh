#!/bin/bash
# Clarivox - Run Script

# Activate virtual environment if it exists
if [ -d "venv" ]; then
    source venv/bin/activate
fi

# Run the FastAPI server
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
