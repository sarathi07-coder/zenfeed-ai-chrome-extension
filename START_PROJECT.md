# 🚀 ZenFeed - Complete Startup Guide

## ✅ **Current Status: RUNNING**

Your ZenFeed AI backend is **already running** and working perfectly!

```
Backend: ✅ http://localhost:8000
Gemini AI: ✅ Active
Agents: ✅ 6 registered
```

---

## 🎯 **Quick Start (3 Steps)**

### **Step 1: Verify Backend (Already Done ✅)**
```bash
./check_ai.sh
```

### **Step 2: Load Chrome Extension**

1. Open Chrome: `chrome://extensions/`
2. Enable **Developer mode** (top-right)
3. Click **"Load unpacked"**
4. Select: `/Users/sarathi/FeedZenAI/chrome_extension`
5. Verify: ZenFeed appears with 🧘 icon

### **Step 3: Test on YouTube**

1. Go to: `youtube.com`
2. Open Console: `F12` (or `Cmd+Option+I`)
3. Look for:
   ```
   [ZenFeed] 🚀 Smart Mode Initializing...
   [ZenFeed] 📊 Learning period: 3 minutes
   ```
4. **Wait 3 minutes** (learning mode)
5. After 3 min:
   ```
   [ZenFeed] 🎓 Learning complete!
   [ZenFeed] ✅ Blocked: "Video" → "Python Tutorial"
   ```

---

## 🎨 **What You'll See**

### **Blocked Videos:**
- **Blurred thumbnail** (actual thumbnail, not replaced)
- **🚫 Icon** (32px)
- **"Blocked Content"** text
- **Two buttons:**
  - 📚 **Watch Alternative** (blue, pill-shaped)
  - **Continue Anyway** (transparent)
- **Alternative title** (small, below buttons)

### **Perfect UI:**
- ✅ Fits YouTube's exact dimensions
- ✅ Blurs actual thumbnail in place
- ✅ No layout shifts
- ✅ Native YouTube look

---

## 🧠 **AI Features**

### **Gemini AI Powers:**
1. **Content Classification** - Detects addictive content
2. **Smart Recommendations** - Generates productive alternatives

### **What Gets Blocked:**
- YouTube Shorts
- Funny/meme videos
- 18+ content
- Entertainment clips
- Gaming highlights
- Reaction videos

### **What You Get Instead:**
- Python tutorials (Tamil/English)
- Java, JavaScript, DSA
- Web development courses
- React, Node.js tutorials
- Study with me Pomodoro
- Meditation for focus
- Coding interview prep

---

## 📊 **Commands**

### **Check Status:**
```bash
./check_ai.sh
```

### **Start Backend:**
```bash
./run_backend.sh
```

### **Stop Backend:**
```bash
lsof -ti:8000 | xargs kill -9
```

---

## 🐛 **Troubleshooting**

### **Extension not working?**
1. `chrome://extensions/` → Find ZenFeed
2. Click 🔄 **Reload**
3. Refresh YouTube

### **No console logs?**
- Extension not loaded
- Check `chrome://extensions/`
- Make sure it's enabled

### **Backend not responding?**
```bash
lsof -ti:8000 | xargs kill -9
./run_backend.sh
```

---

## 📁 **Project Structure**

```
FeedZenAI/
├── backend/           # FastAPI backend
│   ├── api/          # API endpoints
│   └── services/     # LLM, YouTube API
├── agents/           # 6 AI agents
│   ├── classification/  # CCA (Gemini)
│   └── recommendation/  # ROA (Gemini)
├── chrome_extension/ # Chrome extension
│   ├── js/          # content.js (main logic)
│   └── manifest.json
└── .env             # API keys (Gemini, YouTube)
```

---

## 🔑 **API Keys (Already Configured ✅)**

- ✅ Gemini API Key
- ✅ OpenAI API Key
- ✅ Anthropic API Key
- ✅ YouTube Data API Key

---

## 🎯 **Next Steps**

1. ✅ Backend running
2. ⏳ Load extension in Chrome
3. ⏳ Test on YouTube
4. ⏳ Wait 3 minutes
5. ⏳ See blocking!

---

**Everything is ready! Just load the extension and test it! 🚀**
