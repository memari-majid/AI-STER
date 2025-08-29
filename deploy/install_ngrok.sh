#!/bin/bash

# AI-STER Ngrok Installation Script
# This script installs ngrok and sets up the environment for deployment

set -e  # Exit on error

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# Function to print colored output
print_status() {
    echo -e "${GREEN}[✓]${NC} $1"
}

print_error() {
    echo -e "${RED}[✗]${NC} $1"
}

print_warning() {
    echo -e "${YELLOW}[!]${NC} $1"
}

# Check if running on Linux
if [[ "$OSTYPE" != "linux-gnu"* ]]; then
    print_error "This script is designed for Linux. Please install ngrok manually for your OS."
    echo "Visit: https://ngrok.com/download"
    exit 1
fi

# Detect system architecture
ARCH=$(uname -m)
NGROK_URL=""

case $ARCH in
    x86_64)
        NGROK_URL="https://bin.equinox.io/c/bNyj1mQVY4c/ngrok-v3-stable-linux-amd64.tgz"
        ;;
    aarch64|arm64)
        NGROK_URL="https://bin.equinox.io/c/bNyj1mQVY4c/ngrok-v3-stable-linux-arm64.tgz"
        ;;
    armv7l|armhf)
        NGROK_URL="https://bin.equinox.io/c/bNyj1mQVY4c/ngrok-v3-stable-linux-arm.tgz"
        ;;
    *)
        print_error "Unsupported architecture: $ARCH"
        exit 1
        ;;
esac

# Create deployment directory
DEPLOY_DIR="$HOME/.ai-ster"
mkdir -p "$DEPLOY_DIR"

print_status "Installing ngrok for $ARCH architecture..."

# Download ngrok
cd /tmp
wget -q --show-progress "$NGROK_URL" -O ngrok.tgz

# Extract ngrok
tar -xzf ngrok.tgz

# Move ngrok to local bin
mkdir -p "$HOME/.local/bin"
mv ngrok "$HOME/.local/bin/"
chmod +x "$HOME/.local/bin/ngrok"

# Clean up
rm -f ngrok.tgz

print_status "Ngrok installed successfully!"

# Add to PATH if not already present
if ! echo "$PATH" | grep -q "$HOME/.local/bin"; then
    print_warning "Adding $HOME/.local/bin to PATH..."
    echo 'export PATH="$HOME/.local/bin:$PATH"' >> "$HOME/.bashrc"
    print_warning "Please run 'source ~/.bashrc' or restart your terminal"
fi

# Check if ngrok authtoken is set
print_status "Checking ngrok configuration..."
if [ ! -f "$HOME/.config/ngrok/ngrok.yml" ]; then
    print_warning "Ngrok is not configured with an authtoken."
    echo ""
    echo "To use ngrok, you need to:"
    echo "1. Sign up for a free account at https://ngrok.com"
    echo "2. Get your authtoken from https://dashboard.ngrok.com/auth"
    echo "3. Run: $HOME/.local/bin/ngrok config add-authtoken YOUR_AUTH_TOKEN"
    echo ""
    echo "For persistent URLs (recommended for production):"
    echo "- Upgrade to a paid plan at https://ngrok.com/pricing"
    echo "- Configure a custom domain in your ngrok dashboard"
else
    print_status "Ngrok configuration found!"
fi

# Create deployment configuration directory
mkdir -p "$DEPLOY_DIR/config"

print_status "Installation complete!"
echo ""
echo "Next steps:"
echo "1. Configure ngrok with your authtoken (if not already done)"
echo "2. Run ./deploy/start_with_ngrok.sh to start AI-STER with ngrok"
echo "3. For production deployment, consider using the systemd service"
