# 🔑 How to Get API Keys for ZenFeed

To make ZenFeed smart (using AI), you need an API key. **Google Gemini is recommended** because it has a generous free tier.

---

## 1. Google Gemini (Recommended & Free) 🌟
Best for this project. Fast and free to start.

1. Go to **[Google AI Studio](https://aistudio.google.com/app/apikey)**.
2. Click the blue **"Create API key"** button.
3. Select a project (or create a new one).
4. Copy the key that starts with `AIza...`.
5. Paste it into your `.env` file:
   ```bash
   GEMINI_API_KEY=AIzaSy...
   ```

---

## 2. OpenAI (ChatGPT) 🤖
Good alternative, but requires a paid account (credits).

1. Go to **[OpenAI API Keys](https://platform.openai.com/api-keys)**.
2. Log in or sign up.
3. Click **"Create new secret key"**.
4. Name it "ZenFeed" and copy the key (`sk-...`).
5. Paste it into your `.env` file:
   ```bash
   OPENAI_API_KEY=sk-...
   ```

---

## 3. Anthropic (Claude) 🧠
Another powerful option, also paid.

1. Go to **[Anthropic Console](https://console.anthropic.com/settings/keys)**.
2. Log in or sign up.
3. Click **"Create Key"**.
4. Name it "ZenFeed" and copy the key (`sk-ant-...`).
5. Paste it into your `.env` file:
   ```bash
   ANTHROPIC_API_KEY=sk-ant-...
   ```

---

## ⚠️ Important Security Tips
- **NEVER share your keys** or commit them to GitHub.
- If you accidentally share a key, delete it immediately and create a new one.
- ZenFeed uses the `.env` file which is ignored by Git, so your keys stay safe on your computer.
