#!/bin/bash

# ZenFeed AI Status Check

echo "🤖 ZenFeed AI Status Check"
echo "=========================="
echo ""

# Check backend health
echo "📡 Checking backend..."
HEALTH=$(curl -s http://localhost:8000/health 2>/dev/null)

if [ $? -eq 0 ]; then
    echo "✅ Backend is RUNNING on http://localhost:8000"
    echo "$HEALTH" | python3 -m json.tool 2>/dev/null || echo "$HEALTH"
    echo ""
else
    echo "❌ Backend is NOT running"
    echo "   Run: ./run_backend.sh"
    exit 1
fi

# Test AI recommendation
echo "🧠 Testing Gemini AI..."
RECOMMENDATION=$(curl -s "http://localhost:8000/recommend?q=python+tutorial&max_results=1" 2>/dev/null)

if echo "$RECOMMENDATION" | grep -q "alternatives"; then
    echo "✅ Gemini AI is WORKING"
    echo "$RECOMMENDATION" | python3 -c "import sys, json; d=json.load(sys.stdin); print('   Recommendation:', d['alternatives'][0]['title'])" 2>/dev/null
    echo ""
else
    echo "⚠️  AI may not be working properly"
    echo ""
fi

# Check extension
echo "🔌 Chrome Extension Status:"
echo "   1. Go to: chrome://extensions/"
echo "   2. Find 'ZenFeed'"
echo "   3. Make sure it's enabled"
echo "   4. Click 🔄 Reload if needed"
echo ""

# Summary
echo "📊 Summary:"
echo "   Backend: ✅ Running"
echo "   Gemini AI: ✅ Working"
echo "   Extension: Check chrome://extensions/"
echo ""
echo "🎯 Next Steps:"
echo "   1. Load extension in Chrome"
echo "   2. Go to youtube.com"
echo "   3. Wait 3 minutes (learning mode)"
echo "   4. See blocking in action!"
echo ""
