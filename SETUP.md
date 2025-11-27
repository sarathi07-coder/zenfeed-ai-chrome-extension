# ZenFeed Setup & Testing Guide

## Quick Start (5 Minutes)

### 1. Install Dependencies

```bash
# Make start script executable
chmod +x start.sh

# Run quick start (sets up everything)
./start.sh
```

The script will:
- Create virtual environment
- Install all dependencies
- Create `.env` file from template
- Start the backend server

### 2. Configure API Keys (Optional)

Edit `.env` file and add your API keys:

```bash
# For LLM-powered classification (optional - works without)
GEMINI_API_KEY=your_gemini_key_here

# For YouTube alternative recommendations (optional - has mock fallback)
YOUTUBE_API_KEY=your_youtube_key_here
```

**Note:** The system works in "mock mode" without API keys for testing!

### 3. Load Chrome Extension

1. Open Chrome and go to `chrome://extensions/`
2. Enable "Developer mode" (toggle in top right)
3. Click "Load unpacked"
4. Select the `chrome_extension/` folder
5. Extension is now active! 🎉

### 4. Test the System

Visit YouTube and watch ZenFeed in action:
- High-risk videos will be blurred
- Alternatives will be suggested
- Click the extension icon to see statistics

---

## Manual Setup (Detailed)

### Prerequisites

- Python 3.10 or higher
- Node.js 16+ (optional, for extension development)
- Google Chrome browser
- Git

### Step-by-Step Installation

#### 1. Clone Repository

```bash
git clone https://github.com/FEEDX-Team/ZenFeed.git
cd ZenFeed
```

#### 2. Python Environment

```bash
# Create virtual environment
python3 -m venv venv

# Activate (macOS/Linux)
source venv/bin/activate

# Activate (Windows)
venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt
```

#### 3. Environment Configuration

```bash
# Copy template
cp .env.example .env

# Edit .env and add your keys
nano .env  # or use your preferred editor
```

#### 4. Run Backend

```bash
cd backend
uvicorn api.main:app --reload --port 8000
```

Backend will be available at:
- API: http://localhost:8000
- Docs: http://localhost:8000/docs
- Health: http://localhost:8000/health

#### 5. Load Extension

See Quick Start Step 3 above.

---

## Testing the Multi-Agent System

### Test Individual Agents

Each agent can be tested independently:

```bash
# Test Feed Ingestion Agent
python agents/feed_ingestion/fia.py

# Test Content Classification Agent
python agents/classification/cca.py

# Test Addiction Scoring Agent
python agents/addiction_scoring/asa.py

# Test Recommendation Optimizer
python agents/recommendation/roa.py

# Test Behavior Monitor
python agents/behaviour_monitor/bma.py

# Test Extension Control Agent
python agents/extension_control/ceca.py
```

### Test Orchestrator Pipeline

```bash
# Run orchestrator demo
python agents/orchestrator/orchestrator.py
```

### Test Backend API

```bash
# Using curl
curl -X POST http://localhost:8000/analyze \
  -H "Content-Type: application/json" \
  -d '{
    "title": "Try Not To Laugh - Funny Memes Compilation",
    "duration_sec": 45,
    "channel": "MemeWorld"
  }'

# Or visit http://localhost:8000/docs for interactive API testing
```

### Test Chrome Extension

1. Visit YouTube.com
2. Open DevTools (F12) → Console
3. Look for `[ZenFeed]` log messages
4. Navigate to a video with "meme" or "compilation" in title
5. Watch the intervention appear!

---

## Project Structure

```
ZenFeed/
├── agents/                      # Multi-agent system
│   ├── base_agent.py           # Base class
│   ├── orchestrator/           # Orchestrator
│   ├── feed_ingestion/         # FIA
│   ├── classification/         # CCA (LLM-powered)
│   ├── addiction_scoring/      # ASA
│   ├── recommendation/         # ROA
│   ├── behaviour_monitor/      # BMA
│   └── extension_control/      # CECA
│
├── backend/                    # FastAPI backend
│   ├── api/
│   │   └── main.py            # API endpoints
│   ├── core/
│   │   └── prompts.py         # LLM prompts
│   └── services/
│       ├── llm_client.py      # LLM integration
│       └── youtube_service.py # YouTube API
│
├── chrome_extension/           # Browser extension
│   ├── manifest.json
│   ├── js/
│   │   ├── content.js         # Feed manipulation
│   │   └── background.js
│   ├── popup/
│   │   ├── popup.html
│   │   └── popup.js
│   └── styles/
│       └── interventions.css
│
├── ml_models/                  # ML models
├── data/                       # Data storage
├── docs/                       # Documentation
├── tests/                      # Tests
│
├── requirements.txt
├── Dockerfile
├── .env.example
├── start.sh                    # Quick start script
└── README.md
```

---

## Common Issues & Solutions

### Issue: "No module named 'agents'"

**Solution:** Make sure you're running from the project root directory.

```bash
cd /path/to/ZenFeed
python agents/orchestrator/orchestrator.py
```

### Issue: "LLM client failed to initialize"

**Solution:** This is expected if you don't have API keys. The system will use mock mode.

To fix: Add your API key to `.env`:
```
GEMINI_API_KEY=your_actual_key_here
```

### Issue: Extension not detecting videos

**Solution:** 
1. Check DevTools console for errors
2. Reload the extension (chrome://extensions → reload button)
3. Refresh the YouTube page

### Issue: Backend won't start

**Solution:**
```bash
# Check if port 8000 is already in use
lsof -i :8000

# Kill existing process
kill -9 <PID>

# Or use a different port
uvicorn api.main:app --port 8001
```

---

## Development Workflow

### 1. Make Changes to Agents

Edit agent files in `agents/` directory. Each agent is self-contained.

### 2. Test Changes

```bash
# Test individual agent
python agents/classification/cca.py

# Test full pipeline
python agents/orchestrator/orchestrator.py
```

### 3. Update Extension

If you modify the extension:
1. Save your changes
2. Go to `chrome://extensions/`
3. Click reload button on ZenFeed extension
4. Refresh YouTube page

### 4. Restart Backend

If you modify backend code:
- If using `--reload` flag, it auto-restarts
- Otherwise, stop (Ctrl+C) and restart

---

## Deployment

### Deploy to Google Cloud Run

```bash
# Build Docker image
docker build -t gcr.io/YOUR_PROJECT_ID/zenfeed-backend .

# Push to registry
docker push gcr.io/YOUR_PROJECT_ID/zenfeed-backend

# Deploy
gcloud run deploy zenfeed-backend \
  --image gcr.io/YOUR_PROJECT_ID/zenfeed-backend \
  --platform managed \
  --region us-central1 \
  --allow-unauthenticated \
  --set-env-vars GEMINI_API_KEY=$GEMINI_API_KEY,YOUTUBE_API_KEY=$YOUTUBE_API_KEY
```

### Update Extension Backend URL

Edit `chrome_extension/js/content.js`:

```javascript
const CONFIG = {
  BACKEND_URL: 'https://your-cloud-run-url.run.app',
  // ...
};
```

---

## Next Steps

1. **Add your API keys** to `.env` for full functionality
2. **Test on real YouTube videos** to see interventions
3. **Review the code** in `agents/` to understand the system
4. **Customize interventions** in `agents/extension_control/ceca.py`
5. **Deploy to Cloud Run** for production use
6. **Create evaluation dataset** for testing accuracy
7. **Prepare Kaggle submission** using the implementation plan

---

## Getting Help

- **Documentation:** See `docs/` folder
- **API Docs:** http://localhost:8000/docs
- **Issues:** Check console logs and error messages
- **Architecture:** See `implementation_plan.md`

---

## Kaggle Submission Checklist

- [x] Multi-agent system (7 agents)
- [x] Tools integration (YouTube API, LLM)
- [x] Memory & state management
- [x] Observability (logging)
- [x] Chrome extension (real-world deployment)
- [x] FastAPI backend
- [x] Comprehensive documentation
- [ ] Evaluation results
- [ ] 3-minute demo video
- [ ] Cloud deployment (optional for bonus)

---

**Built with ❤️ by Team FEEDX for Kaggle Agents Intensive Capstone Project**
