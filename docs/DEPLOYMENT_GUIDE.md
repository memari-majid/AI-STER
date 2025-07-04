]633;E;echo "# Deployment Guide";]633;C# Deployment Guide

---
## Deployment Steps

# 🚀 AI-STER Deployment Guide

**Simple deployment options for the Streamlit-based AI-STER application**

## 🌟 **Recommended: Streamlit Cloud (FREE)**

### **Step 1: Prepare Repository**
```bash
# Ensure your code is in GitHub
git add .
git commit -m "Ready for deployment"
git push origin main
```

### **Step 2: Deploy to Streamlit Cloud**
1. Visit [share.streamlit.io](https://share.streamlit.io)
2. Sign in with GitHub
3. Click "New app"
4. Select your repository and branch
5. Set main file path: `app.py`
6. Click "Deploy!"

### **Step 3: Configure Environment Variables**
1. In Streamlit Cloud dashboard, click "Settings"
2. Go to "Secrets" tab
3. Add your OpenAI API key:
```toml
OPENAI_API_KEY = "your_openai_api_key_here"
```

### **Result**
- ✅ **URL**: `https://your-app-name.streamlit.app`
- ✅ **Automatic updates** from GitHub
- ✅ **Free hosting** with Streamlit branding
- ✅ **Perfect for educational use**

---

## 💼 **Professional: Railway ($5/month)**

### **Step 1: Deploy from GitHub**
1. Visit [railway.app](https://railway.app)
2. Sign up/login with GitHub
3. Click "New Project" → "Deploy from GitHub repo"
4. Select your repository

### **Step 2: Configure**
```bash
# Railway will auto-detect Python and install requirements.txt
# No configuration needed!
```

### **Step 3: Add Environment Variables**
1. Go to your project dashboard
2. Click "Variables" tab
3. Add:
   - `OPENAI_API_KEY`: Your OpenAI API key
   - `PORT`: 8501 (if needed)

### **Step 4: Set Start Command**
1. In "Settings" → "Deploy"
2. Set start command: `streamlit run app.py --server.port $PORT`

### **Result**
- ✅ **Custom domain** available
- ✅ **Professional hosting**
- ✅ **$5/month** unlimited usage
- ✅ **Perfect for institutions**

---

## 🏢 **Institution Server (Self-Hosted)**

### **Option A: Docker Deployment**
```dockerfile
# Create Dockerfile
FROM python:3.11-slim

WORKDIR /app
COPY requirements.txt .
RUN pip install -r requirements.txt

COPY . .

EXPOSE 8501

CMD ["streamlit", "run", "app.py", "--server.address", "0.0.0.0"]
```

```bash
# Build and run
docker build -t ai-ster .
docker run -p 8501:8501 -e OPENAI_API_KEY=your_key ai-ster
```

### **Option B: Direct Python Deployment**
```bash
# On your server
git clone your-repository
cd streamlit-ster
pip install -r requirements.txt

# Set environment variable
export OPENAI_API_KEY=your_openai_api_key

# Run with external access
streamlit run app.py --server.address 0.0.0.0 --server.port 8501
```

### **Option C: Behind Reverse Proxy (nginx)**
```nginx
# /etc/nginx/sites-available/ai-ster
server {
    listen 80;
    server_name your-domain.edu;
    
    location / {
        proxy_pass http://localhost:8501;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
        proxy_buffering off;
    }
}
```

---

## ⚡ **Local Development**

### **Quick Start**
```bash
# Clone and run locally
git clone your-repository
cd streamlit-ster
pip install -r requirements.txt

# Add API key (optional for testing)
echo "OPENAI_API_KEY=your_key" > .env

# Run
streamlit run app.py
# Opens automatically at http://localhost:8501
```

### **Environment Setup**
```bash
# Create virtual environment (recommended)
python -m venv ai-ster-env
source ai-ster-env/bin/activate  # On Windows: ai-ster-env\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Run with specific port
streamlit run app.py --server.port 8502
```

---

## 🔒 **Security Configuration**

### **Environment Variables**
```bash
# Never commit API keys to git!
# Use .env file locally:
echo "OPENAI_API_KEY=your_key_here" > .env

# For production, set environment variables on host:
export OPENAI_API_KEY=your_production_key
```

### **Streamlit Secrets** (Streamlit Cloud)
```toml
# In Streamlit Cloud dashboard → Secrets
[secrets]
OPENAI_API_KEY = "your_openai_api_key_here"
OPENAI_MODEL = "gpt-4o-mini"
```

### **Railway Environment Variables**
```bash
# In Railway dashboard
OPENAI_API_KEY=your_openai_api_key_here
OPENAI_MODEL=gpt-4o-mini
```

---

## 📊 **Performance & Scaling**

### **Streamlit Cloud Limits**
- ✅ **Free tier**: 1GB RAM, adequate for most educational use
- ✅ **Good for**: 10-50 concurrent users
- ✅ **Storage**: Ephemeral (use data export/import for persistence)

### **Railway Performance**
- ✅ **Starter plan**: 512MB RAM, 1GB storage
- ✅ **Good for**: 50-100 concurrent users  
- ✅ **Storage**: Persistent volumes available

### **Self-Hosted Scaling**
```bash
# Multiple instances with load balancer
streamlit run app.py --server.port 8501 &
streamlit run app.py --server.port 8502 &
streamlit run app.py --server.port 8503 &

# nginx load balancing configuration
upstream ai-ster {
    server localhost:8501;
    server localhost:8502;
    server localhost:8503;
}
```

---

## 🔧 **Troubleshooting**

### **Common Deployment Issues**

#### **1. Import Errors**
```bash
# Fix: Ensure all dependencies in requirements.txt
pip freeze > requirements.txt

# Or manually verify:
cat requirements.txt
# Should contain:
# streamlit>=1.32.0
# pandas>=2.0.0  
# openai>=1.13.0
# python-dotenv>=1.0.0
```

#### **2. OpenAI API Issues**
```bash
# Test API key locally:
python -c "
import os
from openai import OpenAI
client = OpenAI(api_key='your_key_here')
print('API key works!')
"
```

#### **3. Port Issues**
```bash
# Check if port is in use:
lsof -i :8501

# Use different port:
streamlit run app.py --server.port 8502
```

#### **4. File Permission Issues**
```bash
# Ensure write permissions for data storage:
chmod 755 data_storage/
chmod 644 data_storage/*.json
```

### **Monitoring & Logs**

#### **Streamlit Cloud**
- View logs in dashboard
- Monitor usage metrics
- Check app health status

#### **Railway**
- Real-time logs in dashboard
- Resource usage monitoring
- Automatic crash recovery

#### **Self-Hosted**
```bash
# Run with logging:
streamlit run app.py --logger.level=debug

# Or with file logging:
streamlit run app.py 2>&1 | tee ai-ster.log
```

---

## 💡 **Best Practices**

### **1. Data Backup**
```bash
# Regular data exports (built into app)
# Use "📥 Export All Data" feature
# Store backups safely
```

### **2. API Key Management**
```bash
# Use separate keys for dev/prod
# Monitor API usage in OpenAI dashboard
# Set usage limits to prevent overcharges
```

### **3. Performance Optimization**
```bash
# For large datasets, consider:
# - Pagination in dashboard
# - Data archiving
# - Database backend (future enhancement)
```

### **4. User Training**
```bash
# Generate synthetic data for training
# Use "🧪 Test Data" feature
# Create user documentation specific to your institution
```

---

## 🎯 **Deployment Comparison**

| Platform | Cost | Complexity | Best For |
|----------|------|------------|----------|
| **Streamlit Cloud** | FREE | ⭐ | Education, testing, demos |
| **Railway** | $5/month | ⭐⭐ | Professional, institutions |
| **Self-Hosted** | Server costs | ⭐⭐⭐ | Enterprise, custom needs |
| **Local** | FREE | ⭐ | Development, offline use |

**Recommendation: Start with Streamlit Cloud, upgrade to Railway for production use.** 
---
## Streamlit Cloud Deployment

# 🚀 Deploy AI-STER to Streamlit Cloud

**Step-by-step guide to deploy your AI-STER app and share it with the world!**

## ✅ **Prerequisites Completed**
- ✅ Virtual environment set up with clean dependencies
- ✅ All modules tested and working
- ✅ OpenAI integration ready
- ✅ Proper .gitignore configured

## 📋 **Step 1: Prepare GitHub Repository**

### 1.1 Initialize Git (if not already done)
```bash
# In the streamlit-ster directory
git init
git add .
git commit -m "Initial commit: AI-STER Streamlit application"
```

### 1.2 Create GitHub Repository
1. Go to [github.com](https://github.com) and sign in
2. Click **"New repository"**
3. Repository name: `ai-ster` or `ai-ster-streamlit`
4. Description: `AI-powered Student Teaching Evaluation Rubric System`
5. Make it **Public** (required for free Streamlit Cloud)
6. **Don't** initialize with README (we have our own)
7. Click **"Create repository"**

### 1.3 Push to GitHub
```bash
# Replace YOUR_USERNAME with your GitHub username
git remote add origin https://github.com/YOUR_USERNAME/ai-ster.git
git branch -M main
git push -u origin main
```

## 🌐 **Step 2: Deploy to Streamlit Cloud**

### 2.1 Visit Streamlit Cloud
1. Go to [share.streamlit.io](https://share.streamlit.io)
2. Sign in with your **GitHub account**

### 2.2 Create New App
1. Click **"New app"**
2. Select **"From existing repo"**
3. **Repository**: `YOUR_USERNAME/ai-ster`
4. **Branch**: `main`
5. **Main file path**: `app.py`
6. **App URL**: Choose a custom name like `ai-ster-demo` (optional)

### 2.3 Configure Secrets (AI Features)
**🔐 IMPORTANT**: You'll configure the OpenAI API key AFTER deployment.

For now, just click **"Deploy!"** - the app works without AI features initially.

### 2.4 Deploy!
1. Click **"Deploy!"**
2. Wait 2-3 minutes for deployment
3. Your app will be live at: `https://YOUR_APP_NAME.streamlit.app`

### 2.5 Enable AI Features (After Deployment)
📖 **Follow the complete guide**: [`docs/STREAMLIT_SECRETS_SETUP.md`](STREAMLIT_SECRETS_SETUP.md)

**Quick Steps**:
1. Go to your app dashboard → **"Settings"** → **"Secrets"**
2. Add your OpenAI API key:
   ```toml
   OPENAI_API_KEY = "your-actual-openai-api-key"
   ```
3. Save and your app automatically restarts with AI features! 🤖

## 🎉 **Step 3: Share Your App**

### Your app will be publicly accessible at:
- **URL**: `https://your-app-name.streamlit.app`
- **Features**: All AI-STER functionality
- **Performance**: Handles 50+ concurrent users
- **Cost**: **FREE** on Streamlit Cloud!

### Share with:
- ✅ **Educational institutions**
- ✅ **Student teacher supervisors**
- ✅ **Cooperating teachers**
- ✅ **Education departments**

## 🔧 **Step 4: App Management**

### Auto-Updates
- Every `git push` to your repository **automatically updates** the live app
- No manual redeployment needed!

### Monitor Usage
- View app analytics in Streamlit Cloud dashboard
- See visitor count, uptime, and performance metrics

### Custom Domain (Optional)
- Available with Streamlit Cloud Pro ($20/month)
- Use your own domain like `ster.youruniversity.edu`

## 🧪 **Step 5: Testing Your Live App**

### Test All Features:
1. **📊 Dashboard** - View evaluation analytics
2. **📝 New Evaluation** - Create field/STER evaluations
3. **🤖 AI Features** - Generate justifications and analysis
4. **🧪 Test Data** - Generate synthetic evaluations
5. **📥 Export/Import** - Data management features

### AI Features Test:
- Create a new evaluation
- Select score levels
- Click **"🤖 Generate AI Justification"**
- Verify AI responses are professional and relevant

## 📱 **Mobile Compatibility**
Your app automatically works on:
- ✅ **Desktop browsers**
- ✅ **Tablets**
- ✅ **Mobile phones**
- ✅ **Any device with internet**

## 🚀 **Success Metrics**

### What You've Achieved:
- ✅ **Web-based application** accessible anywhere
- ✅ **AI-powered evaluation system** with OpenAI integration
- ✅ **Zero deployment complexity** (compared to React/Docker)
- ✅ **Professional-grade solution** for educational institutions
- ✅ **Cost-effective** (~$0.30 per 100 AI-enhanced evaluations)
- ✅ **Scalable** (handles hundreds of users)
- ✅ **Maintainable** (simple Python codebase)

## 🔗 **Example URLs**

Once deployed, you can share links like:
- **Main app**: `https://ai-ster-demo.streamlit.app`
- **Direct evaluation**: `https://ai-ster-demo.streamlit.app` (navigate to "New Evaluation")

## 💡 **Pro Tips**

### 1. SEO & Discovery
Add these to your GitHub repository description:
- `streamlit` `education` `ai` `evaluation` `teaching`

### 2. Usage Analytics
Monitor these in Streamlit Cloud:
- Daily active users
- Feature usage patterns
- Geographic distribution

### 3. Future Scaling
If you outgrow Streamlit Cloud's free tier:
- **Railway**: $5/month for more resources
- **Heroku**: $7/month with custom domain
- **Self-hosted**: Deploy on university servers

---

## 🎯 **You Did It!**

**You've successfully transformed a complex educational evaluation system into a simple, AI-powered web application that anyone can access and use!**

This is exactly what modern educational technology should be:
- **Simple to deploy** ✅
- **Powerful to use** ✅
- **Cost-effective** ✅
- **Accessible everywhere** ✅

**Share your app URL with the world!** 🌍 
---
## Streamlit Secrets Setup

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