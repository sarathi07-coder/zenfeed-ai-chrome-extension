#!/bin/bash

# Simple ZenFeed Backend Starter

echo "🚀 Starting ZenFeed Backend..."
echo ""

cd /Users/sarathi/FeedZenAI
source venv/bin/activate

echo "✓ Virtual environment activated"
echo "✓ Starting server on http://localhost:8000"
echo ""
echo "Press Ctrl+C to stop"
echo ""

# Run from project root so imports work
uvicorn backend.api.main:app --reload --port 8000
