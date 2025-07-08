# 🔐 Streamlit Cloud API Key Setup Guide

**Complete guide to securely configure your OpenAI API key for AI-STER on Streamlit Cloud**

---

## 🚨 **SECURITY FIRST: Never Commit API Keys!**

### ❌ **NEVER Do This:**
```python
# DON'T: Hard-code API keys in your code
OPENAI_API_KEY = "sk-proj-abc123..."  # ❌ EXPOSED!

# DON'T: Commit .env files with real keys
# .env file with real API key pushed to GitHub ❌
```

### ✅ **ALWAYS Do This:**
- Use **Streamlit Secrets** for cloud deployment
- Use **local .env files** for development (excluded from Git)
- Keep API keys separate from your codebase

---

## 🔑 **Step 1: Get Your OpenAI API Key**

### 1.1 Create OpenAI Account
1. Visit [platform.openai.com](https://platform.openai.com)
2. Sign up or log in to your account
3. Go to **API Keys** section

### 1.2 Generate API Key
1. Click **"Create new secret key"**
2. Name it: `AI-STER-Production`
3. **Copy the key immediately** (you won't see it again!)
4. Store it securely (password manager recommended)

### 1.3 Add Billing (Required)
- Add a payment method to enable API usage
- Set usage limits to control costs
- Recommended limit: $10/month for small-scale use

---

## 🌐 **Step 2: Configure Streamlit Cloud Secrets**

### 2.1 Deploy Your App First
1. Go to [share.streamlit.io](https://share.streamlit.io)
2. Connect your GitHub repository: `https://github.com/yourusername/AI-STER`
3. Set **Main file**: `app.py`
4. Click **"Deploy"** (it will work without API key, just no AI features)

### 2.2 Access Secrets Management
1. Once deployed, go to your app dashboard
2. Click **"⚙️ Settings"** → **"Secrets"**
3. You'll see a text editor for TOML format

### 2.3 Add Your API Key
**Copy and paste this format:**
```toml
# AI-STER Secrets Configuration
OPENAI_API_KEY = "your-actual-api-key-here"

# Optional: Add other secrets for future features
# DATABASE_URL = "your-database-url"
# SMTP_PASSWORD = "your-email-password"
```

**Replace `your-actual-api-key-here` with your real OpenAI API key**

### 2.4 Save and Restart
1. Click **"Save"**
2. Your app will automatically restart
3. AI features will now work! 🤖

---

## 🧪 **Step 3: Test AI Features**

### 3.1 Verify Setup
1. Go to your live Streamlit app
2. Create a new evaluation
3. Select some scores
4. Click **"🤖 Generate AI Justification"**
5. If you see AI-generated text → **Success!** ✅

### 3.2 Troubleshooting
If AI features don't work:

1. **Check API Key Format:**
   ```toml
   # ✅ Correct format
   OPENAI_API_KEY = "sk-proj-..."
   
   # ❌ Wrong formats
   OPENAI_API_KEY = sk-proj-...    # Missing quotes
   OpenAI_API_KEY = "sk-proj-..."  # Wrong case
   ```

2. **Check Streamlit Logs:**
   - Go to app dashboard → **"Manage app"** → **"Logs"**
   - Look for OpenAI-related error messages

3. **Verify API Key:**
   - Test your key at [platform.openai.com/playground](https://platform.openai.com/playground)
   - Check if you have API credits/billing set up

---

## 💻 **Step 4: Local Development Setup**

### 4.1 Create Local .env File
```bash
# In your AI-STER directory
cp .env.example .env
```

### 4.2 Edit .env File
```bash
# Edit the .env file (not committed to Git)
OPENAI_API_KEY=your-actual-api-key-here
```

### 4.3 Test Locally
```bash
# Activate virtual environment
source ai-ster-env/bin/activate  # Linux/Mac
# or
ai-ster-env\Scripts\activate     # Windows

# Run app
streamlit run app.py
```

---

## 🔄 **How It Works: Priority Order**

The AI-STER app checks for your API key in this order:

1. **Streamlit Secrets** (Production - Streamlit Cloud)
   ```python
   st.secrets['OPENAI_API_KEY']
   ```

2. **Environment Variable** (Development - Local)
   ```python
   os.getenv('OPENAI_API_KEY')
   ```

This ensures:
- ✅ **Cloud deployment** uses secure Streamlit secrets
- ✅ **Local development** uses your .env file
- ✅ **No API keys** ever get committed to GitHub

---

## 💰 **Cost Management**

### Typical Usage Costs:
- **GPT-4o-mini** (recommended): ~$0.003 per AI justification
- **100 AI-enhanced evaluations**: ~$0.30
- **1000 AI-enhanced evaluations**: ~$3.00

### Cost Control:
1. **Set OpenAI usage limits** in your OpenAI dashboard
2. **Monitor usage** monthly
3. **Use GPT-4o-mini** (10x cheaper than GPT-4)

---

## 🛡️ **Security Best Practices**

### ✅ **Do:**
- Use unique API keys for each project
- Set reasonable usage limits
- Rotate API keys every 90 days
- Monitor usage for unexpected spikes

### ❌ **Don't:**
- Share API keys in emails/chat
- Use the same key for multiple projects
- Store keys in plaintext files
- Commit keys to version control

---

## 🆘 **Common Issues & Solutions**

### Issue: "OpenAI service is not configured"
**Solution:** Check API key format in Streamlit secrets

### Issue: "API key is invalid"
**Solution:** Regenerate API key at platform.openai.com

### Issue: "Rate limit exceeded"
**Solution:** Wait or upgrade OpenAI plan

### Issue: "Insufficient quota"
**Solution:** Add billing to OpenAI account

---

## 🎉 **Success Checklist**

Once setup is complete, you should have:

- ✅ OpenAI API key generated and secured
- ✅ Streamlit Cloud secrets configured
- ✅ AI features working in live app
- ✅ Local development environment setup
- ✅ Cost controls in place
- ✅ No API keys in your GitHub repository

**🚀 Your AI-STER app is now fully powered with artificial intelligence!**

---

## 📞 **Need Help?**

- **OpenAI Issues**: [help.openai.com](https://help.openai.com)
- **Streamlit Issues**: [docs.streamlit.io](https://docs.streamlit.io)
- **AI-STER GitHub**: Create an issue in your repository 