#!/bin/bash

# AI-STER Systemd Service Installation Script
# This script installs the systemd service for automatic startup

set -e  # Exit on error

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
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

print_info() {
    echo -e "${BLUE}[i]${NC} $1"
}

# Check if running with sudo
if [ "$EUID" -ne 0 ]; then 
    print_error "This script must be run with sudo"
    echo "Usage: sudo $0"
    exit 1
fi

# Get the actual user (not root)
ACTUAL_USER=${SUDO_USER:-$USER}
if [ "$ACTUAL_USER" = "root" ]; then
    print_error "Please run this script as a regular user with sudo"
    exit 1
fi

# Paths
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
SERVICE_FILE="$SCRIPT_DIR/systemd/ai-ster-ngrok.service"
SYSTEMD_DIR="/etc/systemd/system"
PROJECT_ROOT="$(cd "$SCRIPT_DIR/.." && pwd)"

print_info "Installing AI-STER systemd service for user: $ACTUAL_USER"

# Check prerequisites
print_status "Checking prerequisites..."

# Get the actual AI-STER directory
AI_STER_DIR="$(cd "$SCRIPT_DIR/.." && pwd)"

# Check if AI-STER directory exists
if [ ! -d "$AI_STER_DIR" ]; then
    print_error "AI-STER directory not found"
    exit 1
fi

# Check if virtual environment exists
if [ ! -f "$AI_STER_DIR/venv/bin/activate" ]; then
    print_warning "Virtual environment not found. Creating it..."
    sudo -u $ACTUAL_USER bash -c "cd $AI_STER_DIR && python3 -m venv venv && source venv/bin/activate && pip install -r requirements.txt"
fi

# Check if ngrok is installed (either system-wide or local)
if ! command -v ngrok &> /dev/null && [ ! -f "/home/$ACTUAL_USER/.local/bin/ngrok" ]; then
    print_error "Ngrok not installed"
    print_info "Please install ngrok first"
    exit 1
fi

# Check if .env file exists
if [ ! -f "$AI_STER_DIR/.env" ]; then
    print_warning "No .env file found. Creating from template..."
    sudo -u $ACTUAL_USER cp "$AI_STER_DIR/docs/env_template.txt" "$AI_STER_DIR/.env"
    print_warning "Please edit $AI_STER_DIR/.env and add your API keys"
fi

# Copy service file
print_status "Installing systemd service..."
cp "$SERVICE_FILE" "$SYSTEMD_DIR/ai-ster-ngrok@.service"

# Create instance for the user
print_status "Creating service instance for user: $ACTUAL_USER"

# Reload systemd
systemctl daemon-reload

# Enable the service
print_status "Enabling AI-STER service..."
systemctl enable "ai-ster-ngrok@$ACTUAL_USER.service"

print_status "Installation complete!"
echo ""
print_info "Service Management Commands:"
echo "  Start:   sudo systemctl start ai-ster-ngrok@$ACTUAL_USER"
echo "  Stop:    sudo systemctl stop ai-ster-ngrok@$ACTUAL_USER"
echo "  Status:  sudo systemctl status ai-ster-ngrok@$ACTUAL_USER"
echo "  Logs:    sudo journalctl -u ai-ster-ngrok@$ACTUAL_USER -f"
echo "  Disable: sudo systemctl disable ai-ster-ngrok@$ACTUAL_USER"
echo ""
print_info "The service will start automatically on system boot"
print_warning "Remember to configure your ngrok authtoken if not already done:"
echo "  /home/$ACTUAL_USER/.local/bin/ngrok config add-authtoken YOUR_TOKEN"
echo ""
read -p "Would you like to start the service now? (y/n) " -n 1 -r
echo
if [[ $REPLY =~ ^[Yy]$ ]]; then
    systemctl start "ai-ster-ngrok@$ACTUAL_USER.service"
    sleep 3
    systemctl status "ai-ster-ngrok@$ACTUAL_USER.service" --no-pager
    
    # Try to get the URL
    if [ -f "/home/$ACTUAL_USER/.ai-ster/current_url.txt" ]; then
        echo ""
        print_status "AI-STER is accessible at: $(cat /home/$ACTUAL_USER/.ai-ster/current_url.txt)"
    fi
fi
