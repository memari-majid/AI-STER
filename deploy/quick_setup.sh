#!/bin/bash

# AI-STER Quick Setup Script with Ngrok
# This script provides an interactive setup for AI-STER deployment

set -e  # Exit on error

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
PURPLE='\033[0;35m'
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

print_header() {
    echo -e "\n${PURPLE}=== $1 ===${NC}\n"
}

# Banner
clear
echo -e "${PURPLE}"
echo "    _    ___     ____ _____ _____ ____  "
echo "   / \  |_ _|   / ___|_   _| ____|  _ \ "
echo "  / _ \  | |____\___ \ | | |  _| | |_) |"
echo " / ___ \ | |_____|__) || | | |___|  _ < "
echo "/_/   \_\___|   |____/ |_| |_____|_| \_\\"
echo -e "${NC}"
echo -e "${BLUE}AI-Powered Student Teaching Evaluation System${NC}"
echo -e "${GREEN}Quick Setup with Ngrok Deployment${NC}\n"

# Check prerequisites
print_header "Checking Prerequisites"

# Check Python
if ! command -v python3 &> /dev/null; then
    print_error "Python 3 is not installed"
    echo "Please install Python 3.8 or higher"
    exit 1
else
    PYTHON_VERSION=$(python3 -c 'import sys; print(".".join(map(str, sys.version_info[:2])))')
    print_status "Python $PYTHON_VERSION found"
fi

# Check Git
if ! command -v git &> /dev/null; then
    print_error "Git is not installed"
    echo "Please install Git: sudo apt install git"
    exit 1
else
    print_status "Git found"
fi

# Setup steps
print_header "Setup Options"
echo "1. Complete fresh installation"
echo "2. Install ngrok only (AI-STER already set up)"
echo "3. Configure ngrok authtoken only"
echo "4. Start AI-STER with ngrok"
echo "5. Install systemd service for auto-start"
echo "6. Exit"
echo ""
read -p "Select an option (1-6): " OPTION

case $OPTION in
    1)
        # Complete installation
        print_header "Complete Installation"
        
        # Create virtual environment
        print_status "Creating Python virtual environment..."
        python3 -m venv venv
        source venv/bin/activate
        
        # Install dependencies
        print_status "Installing Python dependencies..."
        pip install -r requirements.txt
        
        # Set up environment file
        if [ ! -f ".env" ]; then
            print_status "Creating environment configuration..."
            cp docs/env_template.txt .env
            print_warning "Please edit .env file and add your OpenAI API key"
            read -p "Press Enter to continue..."
        fi
        
        # Install ngrok
        print_status "Installing ngrok..."
        chmod +x deploy/install_ngrok.sh
        ./deploy/install_ngrok.sh
        
        # Configure ngrok
        print_header "Ngrok Configuration"
        echo "To use ngrok, you need a free account:"
        echo "1. Sign up at https://ngrok.com"
        echo "2. Get your authtoken from https://dashboard.ngrok.com/auth"
        echo ""
        read -p "Do you have an ngrok authtoken? (y/n): " HAS_TOKEN
        
        if [[ $HAS_TOKEN =~ ^[Yy]$ ]]; then
            read -p "Enter your ngrok authtoken: " NGROK_TOKEN
            ~/.local/bin/ngrok config add-authtoken "$NGROK_TOKEN"
            print_status "Ngrok configured successfully!"
        else
            print_warning "You'll need to configure ngrok later with:"
            echo "~/.local/bin/ngrok config add-authtoken YOUR_TOKEN"
        fi
        
        print_status "Installation complete!"
        echo ""
        read -p "Would you like to start AI-STER now? (y/n): " START_NOW
        if [[ $START_NOW =~ ^[Yy]$ ]]; then
            ./deploy/start_with_ngrok.sh
        fi
        ;;
        
    2)
        # Install ngrok only
        print_header "Installing Ngrok"
        chmod +x deploy/install_ngrok.sh
        ./deploy/install_ngrok.sh
        
        # Configure authtoken
        read -p "Would you like to configure ngrok authtoken now? (y/n): " CONFIG_NOW
        if [[ $CONFIG_NOW =~ ^[Yy]$ ]]; then
            read -p "Enter your ngrok authtoken: " NGROK_TOKEN
            ~/.local/bin/ngrok config add-authtoken "$NGROK_TOKEN"
            print_status "Ngrok configured successfully!"
        fi
        ;;
        
    3)
        # Configure ngrok authtoken
        print_header "Configure Ngrok Authtoken"
        if [ ! -f "$HOME/.local/bin/ngrok" ]; then
            print_error "Ngrok is not installed. Please run option 2 first."
            exit 1
        fi
        
        echo "Get your authtoken from: https://dashboard.ngrok.com/auth"
        read -p "Enter your ngrok authtoken: " NGROK_TOKEN
        ~/.local/bin/ngrok config add-authtoken "$NGROK_TOKEN"
        print_status "Ngrok configured successfully!"
        ;;
        
    4)
        # Start AI-STER
        print_header "Starting AI-STER with Ngrok"
        
        # Check if scripts are executable
        chmod +x deploy/*.sh
        
        echo "Start options:"
        echo "1. Foreground mode (see URL immediately, Ctrl+C to stop)"
        echo "2. Background mode (detached, use stop_deployment.sh to stop)"
        echo "3. Custom domain (requires paid ngrok plan)"
        read -p "Select mode (1-3): " START_MODE
        
        case $START_MODE in
            1)
                ./deploy/start_with_ngrok.sh
                ;;
            2)
                ./deploy/start_with_ngrok.sh --detached
                if [ -f "$HOME/.ai-ster/current_url.txt" ]; then
                    echo ""
                    print_status "AI-STER is running at: $(cat $HOME/.ai-ster/current_url.txt)"
                    print_info "To stop: ./deploy/stop_deployment.sh"
                fi
                ;;
            3)
                read -p "Enter your custom domain: " DOMAIN
                read -p "Run in background? (y/n): " BG_MODE
                if [[ $BG_MODE =~ ^[Yy]$ ]]; then
                    ./deploy/start_with_ngrok.sh --detached --domain "$DOMAIN"
                else
                    ./deploy/start_with_ngrok.sh --domain "$DOMAIN"
                fi
                ;;
        esac
        ;;
        
    5)
        # Install systemd service
        print_header "Install Systemd Service"
        print_warning "This will enable AI-STER to start automatically on boot"
        print_info "This requires sudo privileges"
        
        chmod +x deploy/install_systemd_service.sh
        sudo ./deploy/install_systemd_service.sh
        ;;
        
    6)
        print_info "Exiting..."
        exit 0
        ;;
        
    *)
        print_error "Invalid option"
        exit 1
        ;;
esac

print_header "Setup Complete"
print_info "For detailed documentation, see: docs/NGROK_DEPLOYMENT_GUIDE.md"
print_info "For support, visit: https://github.com/memari-majid/AI-STER/issues"
