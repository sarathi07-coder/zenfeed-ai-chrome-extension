# 🔍 YouTube Not Showing - Debug Checklist

## ❌ Problem: Extension not working on YouTube

Let's debug step by step:

---

## ✅ **Step 1: Is the Extension Loaded?**

1. Open Chrome: `chrome://extensions/`
2. Look for **"ZenFeed"**
3. Check:
   - [ ] Extension is in the list?
   - [ ] Toggle is **ON** (blue)?
   - [ ] Shows **"Errors (0)"** (not red)?
   - [ ] Has 🧘 icon?

**If NOT in list:**
- Click **"Load unpacked"**
- Select: `/Users/sarathi/FeedZenAI/chrome_extension`

**If shows errors:**
- Click "Errors" to see what's wrong
- Click 🔄 **Reload** after fixing

---

## ✅ **Step 2: Check Console on YouTube**

1. Go to `youtube.com`
2. Press `F12` (or `Cmd+Option+I` on Mac)
3. Click **"Console"** tab
4. Look for ZenFeed logs

**Expected logs:**
```
[ZenFeed] 🎯 Smart Content Script Loaded
[ZenFeed] 🚀 Smart Mode Initializing...
[ZenFeed] 📊 Learning period: 3 minutes
[ZenFeed] ✅ Preferences loaded
```

**If NO logs:**
- Extension is not loaded
- Go back to Step 1
- Make sure extension is enabled
- Refresh YouTube page

**If you see errors:**
- Take a screenshot
- Share the error message

---

## ✅ **Step 3: Wait for Learning Mode**

**IMPORTANT:** The extension has a **3-minute learning period** before it starts blocking.

**Timeline:**
- **0-3 minutes:** Just tracking (no blocking)
- **After 3 minutes:** Starts blocking

**Console will show:**
```
[ZenFeed] 🎓 Learning complete!
[ZenFeed] ✅ Blocked: "Video Title" → "Alternative"
```

---

## ✅ **Step 4: Check Backend Connection**

In the Console, type:
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

**If error:**
- Backend is not running
- Run: `./run_backend.sh`

---

## 🐛 **Common Issues**

### **Issue 1: Extension Not in List**
**Solution:**
```
1. chrome://extensions/
2. Enable "Developer mode" (top-right)
3. Click "Load unpacked"
4. Select: /Users/sarathi/FeedZenAI/chrome_extension
```

### **Issue 2: No Console Logs**
**Solution:**
- Extension not loaded or disabled
- Refresh YouTube: `Ctrl+R` (or `Cmd+R`)
- Check extension is enabled

### **Issue 3: "Extension context invalidated"**
**Solution:**
- This is normal when reloading extension
- Just refresh YouTube page
- Error is now handled gracefully

### **Issue 4: Nothing After 3 Minutes**
**Solution:**
- Check console for errors
- Verify backend: `./check_ai.sh`
- Reload extension: `chrome://extensions/` → 🔄

---

## 📸 **What to Check:**

1. **Screenshot of `chrome://extensions/`**
   - Is ZenFeed there?
   - Is it enabled?
   - Any errors?

2. **Screenshot of YouTube Console**
   - Any ZenFeed logs?
   - Any errors?

3. **Backend status:**
   ```bash
   ./check_ai.sh
   ```

---

## 🆘 **Still Not Working?**

**Send me:**
1. Screenshot of `chrome://extensions/` page
2. Screenshot of YouTube Console (F12)
3. Output of `./check_ai.sh`

**Most common issue:** Extension not loaded or disabled!

---

## ✅ **Quick Fix:**

```bash
# 1. Check backend
./check_ai.sh

# 2. Load extension
# chrome://extensions/ → Load unpacked → /Users/sarathi/FeedZenAI/chrome_extension

# 3. Go to YouTube
# youtube.com

# 4. Open Console
# F12 → Console tab

# 5. Look for logs
# [ZenFeed] 🚀 Smart Mode Initializing...

# 6. Wait 3 minutes
# [ZenFeed] 🎓 Learning complete!
```
