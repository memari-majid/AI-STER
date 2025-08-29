# 🚀 AI-STER Ngrok Deployment - Quick Start Guide

Deploy your AI-STER Streamlit app with ngrok in minutes!

## ⚡ Prerequisites

1. **Sign up for ngrok** (free): https://ngrok.com
2. **Get your authtoken**: https://dashboard.ngrok.com/auth

## 🎯 One-Line Quick Start

```bash
./deploy/quick_setup.sh
```

This interactive wizard will handle everything for you!

## 📝 Manual Steps (if preferred)

### 1️⃣ Install ngrok
```bash
./deploy/install_ngrok.sh
```

### 2️⃣ Configure ngrok
```bash
~/.local/bin/ngrok config add-authtoken YOUR_AUTHTOKEN_HERE
```

### 3️⃣ Create Virtual Environment (if needed)
```bash
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

### 4️⃣ Configure Environment
```bash
# Copy template if .env doesn't exist
cp docs/env_template.txt .env

# Edit .env and add your OpenAI API key
nano .env
```

### 5️⃣ Start AI-STER with ngrok

**Option A: Foreground Mode** (see URL immediately)
```bash
./deploy/start_with_ngrok.sh
```

**Option B: Background Mode** (detached)
```bash
./deploy/start_with_ngrok.sh --detached

# Check the URL
cat ~/.ai-ster/current_url.txt

# Stop when needed
./deploy/stop_deployment.sh
```

## 🌐 Accessing Your App

After starting, you'll get a public URL like:
- Free: `https://abc123.ngrok.io`
- Paid: `https://your-domain.ngrok.io`

Share this URL with your users!

## 🔧 Advanced Options

### Custom Domain (Paid Plans)
```bash
./deploy/start_with_ngrok.sh --domain your-app.ngrok.io
```

### Different Region
```bash
./deploy/start_with_ngrok.sh --region eu  # Options: us, eu, ap, au, sa, jp, in
```

### Auto-Start on Boot
```bash
sudo ./deploy/install_systemd_service.sh
```

## 📊 Ngrok Dashboard

Monitor your tunnel at: http://localhost:4040

## 💡 Pro Tips

1. **Free Plan Limits**: 
   - URL changes on restart
   - 40 connections/minute
   - 1 tunnel at a time

2. **For Production**:
   - Get a paid plan for persistent URLs
   - Use systemd service for auto-restart
   - Configure IP restrictions for security

3. **Troubleshooting**:
   ```bash
   # Check if services are running
   ps aux | grep -E "(streamlit|ngrok)"
   
   # View logs
   tail -f ~/.ai-ster/*.log
   
   # Restart everything
   ./deploy/stop_deployment.sh
   ./deploy/start_with_ngrok.sh
   ```

## 📚 Full Documentation

- [Detailed Ngrok Deployment Guide](docs/NGROK_DEPLOYMENT_GUIDE.md)
- [Deployment Scripts README](deploy/README.md)
- [AI-STER Documentation](docs/README.md)

## 🆘 Need Help?

1. Run `./deploy/quick_setup.sh` for interactive help
2. Check [Troubleshooting](docs/NGROK_DEPLOYMENT_GUIDE.md#troubleshooting)
3. Open an [issue](https://github.com/memari-majid/AI-STER/issues)

---

**Ready to deploy?** Run `./deploy/quick_setup.sh` and follow the prompts! 🎉
