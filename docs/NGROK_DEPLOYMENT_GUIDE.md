# AI-STER Ngrok Deployment Guide

Complete guide for deploying AI-STER using ngrok for public access without a static IP

## 📋 Table of Contents

1. [Overview](#overview)
2. [Prerequisites](#prerequisites)
3. [Quick Start](#quick-start)
4. [Detailed Setup](#detailed-setup)
5. [Configuration Options](#configuration-options)
6. [Production Deployment](#production-deployment)
7. [Security Considerations](#security-considerations)
8. [Troubleshooting](#troubleshooting)
9. [Cost Analysis](#cost-analysis)

## 🌐 Overview

Ngrok provides a secure tunnel to expose your local AI-STER instance to the internet without requiring:
- Static IP address
- Port forwarding configuration
- Complex firewall rules
- Domain name (optional with paid plans)

### Benefits
- ✅ **Zero Network Configuration**: Works behind firewalls, NAT, and corporate networks
- ✅ **Instant Public URLs**: Get a public URL in seconds
- ✅ **HTTPS by Default**: Automatic SSL/TLS encryption
- ✅ **Real-time Inspection**: Web interface to inspect traffic
- ✅ **Custom Domains**: Use your own domain (paid plans)

## 📦 Prerequisites

- Linux server (Ubuntu 20.04+ recommended)
- Python 3.8 or higher
- Git installed
- Internet connection
- Free ngrok account (sign up at [ngrok.com](https://ngrok.com))

## 🚀 Quick Start

### 1. Clone and Setup AI-STER
```bash
# Clone the repository
git clone https://github.com/memari-majid/AI-STER.git
cd AI-STER

# Make deployment scripts executable
chmod +x deploy/*.sh
```

### 2. Install Ngrok
```bash
./deploy/install_ngrok.sh
```

### 3. Configure Ngrok
```bash
# Sign up at https://ngrok.com and get your authtoken
# Configure ngrok with your authtoken
~/.local/bin/ngrok config add-authtoken YOUR_AUTH_TOKEN_HERE
```

### 4. Start AI-STER with Ngrok
```bash
# Start in foreground (see the URL immediately)
./deploy/start_with_ngrok.sh

# OR start in background
./deploy/start_with_ngrok.sh --detached
```

### 5. Access Your App
- Look for the ngrok URL in the output (e.g., `https://abc123.ngrok.io`)
- Share this URL with your users
- Access ngrok dashboard at `http://localhost:4040`

## 🔧 Detailed Setup

### Step 1: Environment Preparation

```bash
# Update system
sudo apt update && sudo apt upgrade -y

# Install Python and pip
sudo apt install python3 python3-pip python3-venv -y

# Clone AI-STER
git clone https://github.com/memari-majid/AI-STER.git
cd AI-STER
```

### Step 2: Configure AI-STER

```bash
# Create virtual environment
python3 -m venv venv
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt

# Copy and configure environment variables
cp docs/env_template.txt .env
nano .env  # Add your OpenAI API key
```

### Step 3: Install and Configure Ngrok

```bash
# Run the installation script
chmod +x deploy/install_ngrok.sh
./deploy/install_ngrok.sh

# Add ngrok to PATH (if not done automatically)
export PATH="$HOME/.local/bin:$PATH"
echo 'export PATH="$HOME/.local/bin:$PATH"' >> ~/.bashrc

# Configure ngrok authtoken
~/.local/bin/ngrok config add-authtoken YOUR_AUTH_TOKEN
```

### Step 4: Test the Deployment

```bash
# Start AI-STER with ngrok
./deploy/start_with_ngrok.sh

# You should see output like:
# [✓] Starting Streamlit app on port 8501...
# [✓] Streamlit is running!
# [✓] Starting ngrok tunnel...
# 
# Session Status                online
# Account                       your-email@example.com (Plan: Free)
# Version                       3.5.0
# Region                        United States (us)
# Latency                       32ms
# Web Interface                 http://127.0.0.1:4040
# Forwarding                    https://abc123.ngrok.io -> http://localhost:8501
```

## ⚙️ Configuration Options

### Start Script Options

```bash
# Basic start
./deploy/start_with_ngrok.sh

# Run in background
./deploy/start_with_ngrok.sh --detached

# Use custom domain (requires paid plan)
./deploy/start_with_ngrok.sh --domain your-domain.ngrok.io

# Specify region for better latency
./deploy/start_with_ngrok.sh --region eu  # Options: us, eu, ap, au, sa, jp, in

# Combine options
./deploy/start_with_ngrok.sh --detached --domain ai-ster.ngrok.io --region us
```

### Ngrok Configuration File

Create a custom ngrok configuration file at `~/.config/ngrok/ngrok.yml`:

```yaml
version: "2"
authtoken: YOUR_AUTH_TOKEN
tunnels:
  ai-ster:
    proto: http
    addr: 8501
    inspect: true
    # For paid plans:
    # domain: your-custom-domain.ngrok.io
    # ip_restriction:
    #   allow_cidrs:
    #     - 1.2.3.4/32
    #   deny_cidrs:
    #     - 0.0.0.0/0
```

### Environment Variables

Configure AI-STER settings in `.env`:

```bash
# Required for AI features
OPENAI_API_KEY=sk-your-openai-api-key

# Optional: Streamlit configuration
STREAMLIT_SERVER_PORT=8501
STREAMLIT_SERVER_HEADLESS=true
STREAMLIT_SERVER_ENABLE_CORS=false
STREAMLIT_SERVER_MAX_UPLOAD_SIZE=200
```

## 🏭 Production Deployment

### Systemd Service Setup

For production environments, use systemd for automatic startup and management:

```bash
# Create systemd service file
sudo nano /etc/systemd/system/ai-ster-ngrok.service
```

Add the following content:

```ini
[Unit]
Description=AI-STER with Ngrok
After=network.target

[Service]
Type=simple
User=YOUR_USERNAME
WorkingDirectory=/home/YOUR_USERNAME/AI-STER
Environment="PATH=/home/YOUR_USERNAME/.local/bin:/usr/local/bin:/usr/bin:/bin"
ExecStart=/home/YOUR_USERNAME/AI-STER/deploy/start_with_ngrok.sh --detached
ExecStop=/home/YOUR_USERNAME/AI-STER/deploy/stop_deployment.sh
Restart=always
RestartSec=10

[Install]
WantedBy=multi-user.target
```

Enable and start the service:

```bash
# Reload systemd
sudo systemctl daemon-reload

# Enable auto-start on boot
sudo systemctl enable ai-ster-ngrok

# Start the service
sudo systemctl start ai-ster-ngrok

# Check status
sudo systemctl status ai-ster-ngrok

# View logs
sudo journalctl -u ai-ster-ngrok -f
```

### Monitoring and Logging

Set up monitoring for production:

```bash
# Create log directory
mkdir -p ~/.ai-ster/logs

# Monitor logs
tail -f ~/.ai-ster/*.log

# Check current URL
cat ~/.ai-ster/current_url.txt

# Monitor system resources
htop
```

### Backup and Recovery

```bash
# Backup evaluation data
tar -czf ai-ster-backup-$(date +%Y%m%d).tar.gz data_storage/

# Restore from backup
tar -xzf ai-ster-backup-20240115.tar.gz
```

## 🔒 Security Considerations

### 1. Authentication
- Always use the app's built-in authentication
- Set strong passwords in `.env` file
- Consider IP whitelisting (paid ngrok plans)

### 2. HTTPS/TLS
- Ngrok provides automatic HTTPS encryption
- All traffic is encrypted end-to-end
- SSL certificates are managed by ngrok

### 3. Access Control
For paid ngrok plans, configure IP restrictions:

```bash
# Whitelist specific IPs
ngrok http 8501 --ip-restriction-allow 1.2.3.4/32,5.6.7.8/32

# Or use configuration file
```

### 4. Rate Limiting
- Free plan: 40 connections/minute
- Paid plans: Higher limits available
- Implement app-level rate limiting if needed

### 5. Data Protection
- Store sensitive data locally, not in ngrok
- Use environment variables for secrets
- Regular backups of evaluation data

## 🛠️ Troubleshooting

### Common Issues and Solutions

#### Ngrok Not Starting
```bash
# Check if port 8501 is already in use
sudo lsof -i :8501

# Kill existing process
sudo kill -9 $(sudo lsof -t -i:8501)

# Restart
./deploy/start_with_ngrok.sh
```

#### Cannot Access Ngrok URL
```bash
# Check if both services are running
ps aux | grep -E "(streamlit|ngrok)"

# Check ngrok status
curl http://localhost:4040/api/tunnels

# Restart services
./deploy/stop_deployment.sh
./deploy/start_with_ngrok.sh
```

#### Streamlit Import Errors
```bash
# Activate virtual environment
source venv/bin/activate

# Reinstall dependencies
pip install -r requirements.txt --upgrade

# Check Python version
python --version  # Should be 3.8+
```

#### Ngrok Session Expired
```bash
# Re-authenticate ngrok
~/.local/bin/ngrok config add-authtoken YOUR_TOKEN

# For paid plans, check subscription status
```

### Debug Mode

Enable verbose logging:

```bash
# Start with debug output
STREAMLIT_LOG_LEVEL=debug ./deploy/start_with_ngrok.sh

# Check logs
tail -f ~/.ai-ster/*.log
```

## 💰 Cost Analysis

### Ngrok Pricing Tiers

| Feature | Free | Basic ($8/mo) | Pro ($20/mo) | Business |
|---------|------|---------------|--------------|----------|
| **Connections** | 40/min | 60/min | 120/min | Unlimited |
| **Tunnels** | 1 | 1 | 2 | Unlimited |
| **Custom Domains** | ❌ | 1 | 2 | Unlimited |
| **Reserved TCP** | ❌ | ❌ | ✅ | ✅ |
| **IP Whitelisting** | ❌ | ❌ | ✅ | ✅ |
| **Team Members** | 1 | 1 | 5 | Unlimited |

### Cost Comparison

| Deployment Method | Monthly Cost | Setup Time | Maintenance |
|-------------------|--------------|------------|-------------|
| **Ngrok Free** | $0 | 5 minutes | Low |
| **Ngrok Basic** | $8 | 5 minutes | Low |
| **Static IP + Domain** | $15-50 | 2-4 hours | Medium |
| **Cloud Hosting** | $20-100 | 1-2 hours | Medium |

### Recommendations

- **Development/Testing**: Free tier is sufficient
- **Small Teams**: Basic plan with custom domain
- **Production**: Pro plan with IP restrictions
- **Enterprise**: Business plan with SLA

## 📚 Additional Resources

- [Ngrok Documentation](https://ngrok.com/docs)
- [Streamlit Deployment Guide](https://docs.streamlit.io/library/advanced-features/configuration)
- [AI-STER Main Documentation](./README.md)
- [Security Best Practices](https://ngrok.com/docs/guides/security/)

## 🤝 Support

- **Ngrok Issues**: [Ngrok Support](https://ngrok.com/support)
- **AI-STER Issues**: [GitHub Issues](https://github.com/memari-majid/AI-STER/issues)
- **Community**: [Discussions](https://github.com/memari-majid/AI-STER/discussions)

---

*Last Updated: January 2025*
*Compatible with AI-STER v1.0.0 and ngrok v3.x*
