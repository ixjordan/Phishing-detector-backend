#!/bin/bash
echo "🔧 Activating virtual environment..."
source venv/bin/activate

echo "🚀 Starting FastAPI server..."
uvicorn main:app --reload

# ./start.sh