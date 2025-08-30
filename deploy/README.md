# AI-STER Deployment Scripts

This directory contains scripts and configuration files for deploying AI-STER with ngrok.

## 📁 Directory Structure

```
deploy/
├── README.md                    # This file
├── quick_setup.sh              # Interactive setup wizard
├── install_ngrok.sh            # Ngrok installation script
├── start_with_ngrok.sh         # Start AI-STER with ngrok
├── stop_deployment.sh          # Stop running deployment
├── install_systemd_service.sh  # Install auto-start service
├── config/
│   └── ngrok.yml.template      # Ngrok configuration template
└── systemd/
    └── ai-ster-ngrok.service   # Systemd service file
```

## 🚀 Quick Start

### Option 1: Interactive Setup (Recommended)
```bash
./deploy/quick_setup.sh
```

This will guide you through:
- Installing dependencies
- Setting up ngrok
- Configuring the environment
- Starting the application

### Option 2: Manual Setup

1. **Install ngrok:**
   ```bash
   ./deploy/install_ngrok.sh
   ```

2. **Configure ngrok:**
   ```bash
   ~/.local/bin/ngrok config add-authtoken YOUR_AUTHTOKEN
   ```

3. **Start AI-STER:**
   ```bash
   # Foreground mode (see URL immediately)
   ./deploy/start_with_ngrok.sh
   
   # Background mode
   ./deploy/start_with_ngrok.sh --detached
   ```

## 📋 Script Descriptions

### `quick_setup.sh`
Interactive setup wizard that handles the complete installation and configuration process.

**Features:**
- Checks prerequisites
- Installs dependencies
- Configures ngrok
- Offers various deployment options

### `install_ngrok.sh`
Downloads and installs ngrok for your system architecture.

**Features:**
- Auto-detects system architecture
- Downloads appropriate ngrok binary
- Sets up PATH configuration
- Creates necessary directories

### `start_with_ngrok.sh`
Starts both Streamlit and ngrok, creating a public tunnel to your app.

**Options:**
- `-d, --detached`: Run in background mode
- `--domain DOMAIN`: Use custom domain (paid plan)
- `--region REGION`: Set ngrok region (us, eu, ap, au, sa, jp, in)

**Examples:**
```bash
# Basic start
./deploy/start_with_ngrok.sh

# Background with custom domain
./deploy/start_with_ngrok.sh --detached --domain myapp.ngrok.io

# Specific region
./deploy/start_with_ngrok.sh --region eu
```

### `stop_deployment.sh`
Stops any running AI-STER and ngrok processes.

**Usage:**
```bash
./deploy/stop_deployment.sh
```

### `install_systemd_service.sh`
Installs a systemd service for automatic startup on boot (Linux only).

**Usage:**
```bash
sudo ./deploy/install_systemd_service.sh
```

**Service Commands:**
```bash
# Start service
sudo systemctl start ai-ster-ngrok@username

# Stop service
sudo systemctl stop ai-ster-ngrok@username

# Check status
sudo systemctl status ai-ster-ngrok@username

# View logs
sudo journalctl -u ai-ster-ngrok@username -f
```

## 🔧 Configuration

### Ngrok Configuration
Copy and customize the ngrok configuration template:

```bash
cp deploy/config/ngrok.yml.template ~/.config/ngrok/ngrok.yml
```

Edit the file and add your authtoken and preferences.

### Environment Variables
Create a `.env` file in the project root:

```bash
cp docs/env_template.txt .env
```

Required variables:
- `OPENAI_API_KEY`: Your OpenAI API key for AI features

## 🌐 Accessing Your Deployment

After starting with ngrok, you'll receive a public URL like:
- Free plan: `https://random-id.ngrok.io`
- Paid plan: `https://your-domain.ngrok.io`

Share this URL with your users to access AI-STER.

## 🔍 Troubleshooting

### Port Already in Use
```bash
# Find process using port 8501
sudo lsof -i :8501

# Kill the process
sudo kill -9 PID
```

### Ngrok Not Starting
- Check if authtoken is configured
- Verify internet connection
- Check ngrok status: `~/.local/bin/ngrok diagnose`

### Can't Access the URL
- Ensure both Streamlit and ngrok are running
- Check firewall settings
- Verify ngrok tunnel status at http://localhost:4040

## 📚 More Information

For detailed deployment documentation, see:
- [Ngrok Deployment Guide](deploy/README.md)
- [General Deployment Guide](../docs/DEPLOYMENT_GUIDE.md)
- [AI-STER Documentation](../docs/README.md)

## 💡 Tips

1. **Development**: Use the free ngrok tier for testing
2. **Production**: Consider a paid plan for custom domains and better limits
3. **Security**: Always use the app's built-in authentication
4. **Monitoring**: Check logs regularly in `~/.ai-ster/`
5. **Updates**: Pull latest changes and restart the deployment

## 🆘 Support

- GitHub Issues: https://github.com/memari-majid/AI-STER/issues
- Documentation: https://github.com/memari-majid/AI-STER/docs
- Ngrok Support: https://ngrok.com/support
