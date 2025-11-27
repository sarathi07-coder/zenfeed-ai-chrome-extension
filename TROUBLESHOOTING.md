# 🔧 ZenFeed Troubleshooting Guide

## Problem: YouTube Not Changing

The backend is working (I can see it generating recommendations), but YouTube isn't being modified. This means the **Chrome extension isn't active**.

---

## ✅ Step-by-Step Fix

### **Step 1: Load the Chrome Extension**

1. **Open Chrome** and go to:
   ```
   chrome://extensions/
   ```

2. **Enable Developer Mode**
   - Look for toggle in **top-right corner**
   - Turn it **ON** (blue)

3. **Click "Load unpacked"**
   - Button appears after enabling Developer mode

4. **Select the extension folder:**
   ```
   /Users/sarathi/FeedZenAI/chrome_extension
   ```

5. **Verify it loaded:**
   - You should see **"ZenFeed"** in the list
   - Status should be **"Errors (0)"**
   - Icon: 🧘

---

### **Step 2: Check for Errors**

If you see **"Errors"** in red:

1. Click **"Errors"** button
2. Read the error message
3. Common issues:
   - **Manifest error:** Check `manifest.json`
   - **Script error:** Check `content.js` or `background.js`

**Fix:** Click **🔄 Reload** button after fixing errors

---

### **Step 3: Test on YouTube**

1. **Go to YouTube:**
   ```
   https://youtube.com
   ```

2. **Open DevTools:**
   - Press `F12` (Windows/Linux)
   - Press `Cmd+Option+I` (Mac)

3. **Go to Console tab**

4. **Look for ZenFeed logs:**
   ```
   [ZenFeed] 🚀 Smart Mode Initializing...
   [ZenFeed] 📊 Learning period: 3 minutes
   ```

5. **If you DON'T see logs:**
   - Extension is not loaded
   - Go back to Step 1

---

### **Step 4: Wait for Learning Mode**

**IMPORTANT:** The extension has a **3-minute learning period** before it starts blocking.

**What happens:**
- **0-3 minutes:** Just tracking (no blocking)
- **After 3 minutes:** Starts blocking addictive content

**Console will show:**
```
[ZenFeed] 🎓 Learning complete!
[ZenFeed] ✅ Blocked: "Funny Video" → "Python Tutorial"
```

---

### **Step 5: Verify Backend Connection**

In the **Console**, type:
```javascript
fetch('http://localhost:8000/health').then(r => r.json()).then(console.log)
```

**Expected output:**
```json
{
  "status": "healthy",
  "agents_registered": 6
}
```

**If you get an error:**
- Backend is not running
- Run: `./run_backend.sh`

---

## 🐛 Common Issues

### **Issue 1: Extension Not Showing**
**Solution:**
- Make sure you selected the **correct folder**
- Folder should be: `/Users/sarathi/FeedZenAI/chrome_extension`
- NOT the parent folder

### **Issue 2: No Console Logs**
**Solution:**
- Refresh YouTube page
- Click extension icon in toolbar
- Check if extension is enabled

### **Issue 3: CORS Error**
**Solution:**
- Backend should allow CORS (already configured)
- Check `.env` file: `CORS_ORIGINS=*`

### **Issue 4: Nothing Happens After 3 Minutes**
**Solution:**
- Check console for errors
- Verify backend is running: `curl http://localhost:8000/health`
- Reload extension: `chrome://extensions/` → 🔄 Reload

---

## 📊 How to Know It's Working

### **In Console:**
```
[ZenFeed] 🚀 Smart Mode Initializing...
[ZenFeed] 📊 Learning period: 3 minutes
[ZenFeed] 📝 Tracked: "Video Title"
... (wait 3 minutes) ...
[ZenFeed] 🎓 Learning complete!
[ZenFeed] ✅ Blocked: "Funny Shorts" → "Python Tutorial Tamil"
```

### **On YouTube Page:**
- Blurred thumbnails with 🚫
- Two buttons on thumbnail:
  - 📚 Watch Alternative (blue)
  - Continue Anyway (transparent)

### **In Backend Logs:**
```
INFO: Generating recommendations...
INFO: Generated dynamic queries: ['python tutorial', ...]
INFO: Found 25 results for: python tutorial
```

---

## 🎯 Quick Test Checklist

- [ ] Backend running: `curl http://localhost:8000/health`
- [ ] Extension loaded in `chrome://extensions/`
- [ ] Developer mode enabled
- [ ] No errors showing
- [ ] YouTube page open
- [ ] DevTools console open
- [ ] ZenFeed logs visible
- [ ] Waited 3+ minutes
- [ ] Videos being blocked

---

## 🆘 Still Not Working?

**Check these files:**

1. **Extension manifest:**
   ```bash
   cat /Users/sarathi/FeedZenAI/chrome_extension/manifest.json
   ```

2. **Content script:**
   ```bash
   ls /Users/sarathi/FeedZenAI/chrome_extension/js/content.js
   ```

3. **Backend health:**
   ```bash
   curl http://localhost:8000/health
   ```

**Send me:**
- Screenshot of `chrome://extensions/`
- Console logs from YouTube
- Any error messages

---

**💡 Tip:** The most common issue is forgetting to **reload the extension** after changes!
