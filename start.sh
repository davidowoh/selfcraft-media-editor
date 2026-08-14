#!/bin/bash
cd "$(dirname "$0")"
source .venv/bin/activate
echo "Starting SelfCraft Media Editor..."
echo "Open dashboard.html in your browser once the server is ready."
uvicorn app.core.main:app --reload