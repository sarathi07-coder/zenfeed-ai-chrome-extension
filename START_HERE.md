# 🚀 ZenFeed - Complete Step-by-Step Guide

## 📍 **START HERE - Complete Setup from Scratch**

Follow these steps **exactly** in order. Copy and paste each command.

---

## **PART 1: Start the Backend Server**

### Step 1: Open Terminal

Open a new Terminal window (Command + Space → type "Terminal")

### Step 2: Navigate to Project

```bash
cd /Users/sarathi/FeedZenAI
```

### Step 3: Run the Quick Start Script

```bash
./start.sh
```

**What you'll see:**
```
🚀 ZenFeed Quick Start
======================
📌 Checking Python version...
✓ Virtual environment already exists
🔧 Activating virtual environment...
📥 Installing dependencies...
🎯 Starting ZenFeed backend...
   Backend will be available at: http://localhost:8000
   API docs: http://localhost:8000/docs
```

**✅ SUCCESS:** When you see "Uvicorn running on http://0.0.0.0:8000", the backend is ready!

**⚠️ IMPORTANT:** Keep this terminal window open! Don't close it.

---

## **PART 2: Test the Backend**

### Step 4: Open Your Browser

Open **Google Chrome** (or any browser)

### Step 5: Visit the API Documentation

Go to: **http://localhost:8000/docs**

**✅ SUCCESS:** You should see a page titled "ZenFeed API" with a list of endpoints!

### Step 6: Test the Health Check

Go to: **http://localhost:8000/health**

**✅ SUCCESS:** You should see JSON like:
```json
{
  "status": "healthy",
  "agents_registered": 6,
  "metrics": {...}
}
```

---

## **PART 3: Load the Chrome Extension**

### Step 7: Open Chrome Extensions Page

In Chrome, go to: **chrome://extensions/**

Or: Menu (⋮) → Extensions → Manage Extensions

### Step 8: Enable Developer Mode

Look at the **top-right corner** of the page.

Find the toggle switch that says **"Developer mode"**

**Click it to turn it ON** (it should turn blue)

### Step 9: Load the Extension

1. Click the **"Load unpacked"** button (top-left area)

2. A file browser will open

3. Navigate to: `/Users/sarathi/FeedZenAI/chrome_extension/`

4. Click **"Select"** or **"Open"**

**✅ SUCCESS:** You should see a new card appear with:
- **Name:** ZenFeed - AI Social Media Detox
- **Icon:** 🧘
- **Status:** Enabled (blue toggle)

### Step 10: Pin the Extension (Optional)

1. Click the **puzzle piece icon** (🧩) in Chrome toolbar
2. Find "ZenFeed"
3. Click the **pin icon** to keep it visible

---

## **PART 4: Test on YouTube**

### Step 11: Open YouTube

Go to: **https://www.youtube.com**

### Step 12: Open Developer Console

Press: **F12** (or **Cmd + Option + I** on Mac)

Click the **"Console"** tab

**✅ SUCCESS:** You should see messages like:
```
[ZenFeed] Content script loaded
[ZenFeed] Initializing...
[ZenFeed] Starting feed scanner...
```

### Step 13: Search for Addictive Content

In YouTube search, type: **"funny memes compilation"**

Or: **"try not to laugh"**

### Step 14: Watch the Magic! ✨

**You should see:**
- Some videos get **blurred** with an overlay
- A message: "High-Risk Content Detected ⚠️"
- Buttons: "Show Alternatives" and "Reveal"

**✅ SUCCESS:** ZenFeed is working!

### Step 15: Test Alternatives

1. Click **"Show Alternatives"** on a blurred video
2. A popup appears with **3 productive alternatives**
3. These are **real YouTube videos** fetched from the API!

### Step 16: Check Statistics

1. Click the **ZenFeed icon** (🧘) in Chrome toolbar
2. A popup opens showing:
   - Items Scanned Today
   - Interventions Applied
   - Alternatives Shown

---

## **PART 5: Test the API (Optional)**

### Step 17: Open a New Terminal

**Don't close the first terminal!** Open a **second** terminal window.

### Step 18: Test Content Analysis

Copy and paste this command:

```bash
curl -X POST http://localhost:8000/analyze \
  -H "Content-Type: application/json" \
  -d '{
    "title": "Try Not To Laugh - Funny Memes Compilation",
    "duration_sec": 45,
    "channel": "MemeWorld",
    "platform": "youtube"
  }'
```

**✅ SUCCESS:** You get a JSON response with:
- Classification (category: "addictive")
- Addiction score
- Risk level
- Recommended intervention

### Step 19: Test Recommendations

```bash
curl "http://localhost:8000/recommend?q=study+with+me+pomodoro&max_results=3"
```

**✅ SUCCESS:** You get 3 real YouTube videos as alternatives!

---

## **PART 6: Verify Everything Works**

### ✅ Checklist

- [ ] Backend running at http://localhost:8000
- [ ] API docs visible at http://localhost:8000/docs
- [ ] Chrome extension loaded and enabled
- [ ] Extension icon visible in Chrome toolbar
- [ ] Console shows `[ZenFeed]` messages on YouTube
- [ ] Videos get blurred on YouTube
- [ ] "Show Alternatives" button works
- [ ] Alternatives popup shows real videos
- [ ] Extension popup shows statistics

**If all checked:** 🎉 **ZenFeed is fully operational!**

---

## **🐛 Troubleshooting**

### Problem: Backend won't start

**Solution:**
```bash
# Check if port 8000 is already in use
lsof -i :8000

# If something is using it, kill it:
kill -9 <PID>

# Then restart:
./start.sh
```

### Problem: Extension not loading

**Solution:**
1. Make sure you selected the **folder** `/Users/sarathi/FeedZenAI/chrome_extension/`
2. Not a file inside it, but the folder itself
3. Try clicking "Reload" button on the extension card

### Problem: No interventions on YouTube

**Solution:**
1. Refresh the YouTube page
2. Check DevTools console for errors
3. Make sure extension is **enabled** (blue toggle)
4. Try videos with "meme" or "compilation" in title

### Problem: "Module not found" errors

**Solution:**
```bash
cd /Users/sarathi/FeedZenAI
source venv/bin/activate
pip install -r requirements.txt
```

---

## **📊 What Each Part Does**

### Backend (Terminal 1)
- Runs the FastAPI server
- Hosts 7 AI agents
- Provides API endpoints
- Fetches YouTube alternatives

### Chrome Extension
- Watches YouTube feed
- Extracts video metadata
- Runs on-device classification
- Applies interventions (blur/nudge)
- Shows alternatives

### API Endpoints
- `/analyze` - Analyze content
- `/recommend` - Get alternatives
- `/health` - Check status
- `/stats` - View statistics

---

## **🎬 Demo for Kaggle**

### Recording Your Demo Video:

1. **Start screen recording**
2. **Show the problem:** Scroll YouTube without extension
3. **Enable extension:** Show it in chrome://extensions
4. **Live demo:** Visit YouTube, show interventions
5. **Show alternatives:** Click button, show real videos
6. **Show backend:** Visit /docs, test API
7. **Show stats:** Click extension icon

**Duration:** 3 minutes max

---

## **📁 Important Files**

- **Backend code:** `/Users/sarathi/FeedZenAI/backend/`
- **Agents:** `/Users/sarathi/FeedZenAI/agents/`
- **Extension:** `/Users/sarathi/FeedZenAI/chrome_extension/`
- **Docs:** `/Users/sarathi/FeedZenAI/README.md`

---

## **🎯 Quick Commands Reference**

```bash
# Start backend
cd /Users/sarathi/FeedZenAI
./start.sh

# Stop backend
# Press Ctrl+C in the terminal

# Test API
curl http://localhost:8000/health

# Activate virtual environment (if needed)
source venv/bin/activate

# Install dependencies (if needed)
pip install -r requirements.txt
```

---

## **✅ You're Done!**

Your ZenFeed system is now:
- ✅ Running locally
- ✅ Connected to YouTube API
- ✅ Working on live YouTube
- ✅ Ready for demo
- ✅ Ready for Kaggle submission

**Next:** Record your demo video and write your Kaggle submission!

---

**Questions? Check these files:**
- `README.md` - Project overview
- `SETUP.md` - Detailed setup
- `NEXT_STEPS.md` - What to do next
- `PROJECT_STATUS.md` - Current status

**Good luck! 🚀**
