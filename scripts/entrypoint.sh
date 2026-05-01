#!/bin/bash

# Start the Go Ingestor worker in the background
echo "Starting Aegis Ingestor Worker..."
./ingestor &

# Start the FastAPI Engine
echo "Starting Aegis Engine on port ${PORT:-7860}..."
python -m uvicorn main:app --host 0.0.0.0 --port ${PORT:-7860}
