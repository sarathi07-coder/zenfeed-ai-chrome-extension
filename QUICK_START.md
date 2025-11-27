# 🚀 ZenFeed Quick Start Guide

## ✅ Prerequisites Check

Your system is ready! All API keys are configured:
- ✅ Gemini API Key
- ✅ OpenAI API Key  
- ✅ Anthropic API Key
- ✅ YouTube Data API Key

---

## 🎯 Step 1: Start the Backend

The backend is **already running** on `http://localhost:8000`

To restart it manually:
```bash
cd /Users/sarathi/FeedZenAI
./run_backend.sh
```

**Verify it's working:**
```bash
curl http://localhost:8000/health
```

You should see: `{"status":"healthy"}`

---

## 🔌 Step 2: Load the Chrome Extension

1. **Open Chrome** and go to: `chrome://extensions/`

2. **Enable Developer Mode** (toggle in top-right corner)

3. **Click "Load unpacked"**

4. **Select the folder:**
   ```
   /Users/sarathi/FeedZenAI/chrome_extension
   ```

5. **You should see:**
   - 🧘 **ZenFeed** extension loaded
   - Icon appears in your toolbar

---

## 🧪 Step 3: Test on YouTube

1. **Go to YouTube:** `https://youtube.com`

2. **Open DevTools:** Press `F12` or `Cmd+Option+I`

3. **Go to Console tab**

4. **Watch for logs:**
   ```
   [ZenFeed] 🚀 Smart Mode Initializing...
   [ZenFeed] 📊 Learning period: 3 minutes
   ```

5. **Wait 3 minutes** for learning mode to complete

6. **After 3 minutes, you'll see:**
   ```
   [ZenFeed] 🎓 Learning complete!
   [ZenFeed] ✅ Blocked: "Funny Video" → "Python Tutorial"
   ```

---

## 🎨 What You'll See

### Blocked Content:
- **Blurred thumbnail** with 🚫 icon
- **Two buttons:**
  - 📚 **Watch Alternative** (blue)
  - **Continue Anyway** (transparent)
- **Alternative title** below buttons

### Alternatives (AI-Powered):
- Python tutorials (Tamil/English)
- Java, JavaScript, DSA
- Web development courses
- Study with me Pomodoro
- Meditation for focus
- Coding interview prep

---

## 🔧 Troubleshooting

### Backend not responding?
```bash
lsof -ti:8000 | xargs kill -9
./run_backend.sh
```

### Extension not working?
1. Go to `chrome://extensions/`
2. Find ZenFeed
3. Click 🔄 **Reload**
4. Refresh YouTube

### No alternatives showing?
- Check backend logs for errors
- Verify API keys in `.env`
- Check console for errors (F12)

---

## 📊 Monitor Activity

### Backend Logs:
The terminal running `./run_backend.sh` shows:
- API requests
- LLM calls (Gemini)
- YouTube searches
- Errors/warnings

### Extension Console:
Open DevTools on YouTube to see:
- Videos scanned
- Interventions applied
- Alternatives fetched
- Smart mode status

---

## 🎯 Next Steps

1. **Test for 10 minutes** on YouTube
2. **Check if blocking works** for:
   - YouTube Shorts
   - Funny videos
   - 18+ content
   - Entertainment
3. **Verify alternatives** are relevant
4. **Report any issues**

---

## 🛑 Stop the Project

**Stop Backend:**
```bash
lsof -ti:8000 | xargs kill -9
```

**Disable Extension:**
1. Go to `chrome://extensions/`
2. Toggle off ZenFeed

---

## 📝 Important Notes

- **Learning Period:** First 3 minutes = no blocking (just tracking)
- **Smart Mode:** Analyzes your watch history for better alternatives
- **18+ Detection:** Instant block with max score (10/10)
- **Already Watched:** Completely removes from feed

---

**🎉 You're all set! Enjoy a more productive YouTube experience!**
