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