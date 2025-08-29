#!/bin/bash

# AI-STER Streamlit + Ngrok Startup Script
# This script starts the Streamlit app and exposes it via ngrok

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

# Configuration
STREAMLIT_PORT=8501
APP_NAME="AI-STER"
PROJECT_ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
VENV_PATH="$PROJECT_ROOT/venv"
NGROK_CONFIG_FILE="$HOME/.ai-ster/ngrok.yml"

# Parse command line arguments
DETACHED=false
CUSTOM_DOMAIN=""
REGION="us"

while [[ $# -gt 0 ]]; do
    case $1 in
        -d|--detached)
            DETACHED=true
            shift
            ;;
        --domain)
            CUSTOM_DOMAIN="$2"
            shift 2
            ;;
        --region)
            REGION="$2"
            shift 2
            ;;
        -h|--help)
            echo "Usage: $0 [options]"
            echo "Options:"
            echo "  -d, --detached     Run in detached mode (background)"
            echo "  --domain DOMAIN    Use custom domain (requires paid ngrok plan)"
            echo "  --region REGION    Ngrok region (us, eu, ap, au, sa, jp, in)"
            echo "  -h, --help         Show this help message"
            exit 0
            ;;
        *)
            print_error "Unknown option: $1"
            exit 1
            ;;
    esac
done

# Check if ngrok is installed
if ! command -v ngrok &> /dev/null; then
    print_error "Ngrok is not installed. Please install ngrok first."
    exit 1
fi

# Check if virtual environment exists
if [ ! -d "$VENV_PATH" ]; then
    print_warning "Virtual environment not found. Creating one..."
    cd "$PROJECT_ROOT"
    python3 -m venv venv
    source "$VENV_PATH/bin/activate"
    pip install -r requirements.txt
else
    source "$VENV_PATH/bin/activate"
fi

# Check if .env file exists
if [ ! -f "$PROJECT_ROOT/.env" ] && [ -f "$PROJECT_ROOT/docs/env_template.txt" ]; then
    print_warning "No .env file found. Creating from template..."
    cp "$PROJECT_ROOT/docs/env_template.txt" "$PROJECT_ROOT/.env"
    print_warning "Please edit .env file and add your OpenAI API key"
fi

# Kill any existing Streamlit processes
print_info "Checking for existing Streamlit processes..."
if pgrep -f "streamlit run" > /dev/null; then
    print_warning "Found existing Streamlit process. Stopping it..."
    pkill -f "streamlit run" || true
    sleep 2
fi

# Kill any existing ngrok processes
if pgrep -f "ngrok http" > /dev/null; then
    print_warning "Found existing ngrok process. Stopping it..."
    pkill -f "ngrok http" || true
    sleep 2
fi

# Function to cleanup on exit
cleanup() {
    print_info "Shutting down..."
    if [ ! -z "$STREAMLIT_PID" ]; then
        kill $STREAMLIT_PID 2>/dev/null || true
    fi
    if [ ! -z "$NGROK_PID" ]; then
        kill $NGROK_PID 2>/dev/null || true
    fi
    exit 0
}

# Set up trap for cleanup
trap cleanup INT TERM

# Start Streamlit
print_status "Starting Streamlit app on port $STREAMLIT_PORT..."
cd "$PROJECT_ROOT"

if [ "$DETACHED" = true ]; then
    nohup streamlit run app.py \
        --server.port=$STREAMLIT_PORT \
        --server.address=0.0.0.0 \
        --server.headless=true \
        > "$HOME/.ai-ster/streamlit.log" 2>&1 &
    STREAMLIT_PID=$!
else
    streamlit run app.py \
        --server.port=$STREAMLIT_PORT \
        --server.address=0.0.0.0 \
        --server.headless=true &
    STREAMLIT_PID=$!
fi

# Wait for Streamlit to start
print_info "Waiting for Streamlit to start..."
for i in {1..30}; do
    if curl -s http://localhost:$STREAMLIT_PORT > /dev/null; then
        print_status "Streamlit is running!"
        break
    fi
    sleep 1
done

# Start ngrok
print_status "Starting ngrok tunnel..."

# Build ngrok command
NGROK_CMD="ngrok http $STREAMLIT_PORT --region=$REGION"

# Add custom domain if specified
if [ ! -z "$CUSTOM_DOMAIN" ]; then
    NGROK_CMD="$NGROK_CMD --domain=$CUSTOM_DOMAIN"
    print_info "Using custom domain: $CUSTOM_DOMAIN"
fi

if [ "$DETACHED" = true ]; then
    nohup $NGROK_CMD > "$HOME/.ai-ster/ngrok.log" 2>&1 &
    NGROK_PID=$!
    sleep 3
    
    # Get ngrok URL from API
    print_info "Retrieving ngrok URL..."
    NGROK_URL=$(curl -s http://localhost:4040/api/tunnels | python3 -c "import sys, json; print(json.load(sys.stdin)['tunnels'][0]['public_url'])" 2>/dev/null || echo "")
    
    if [ ! -z "$NGROK_URL" ]; then
        print_status "AI-STER is accessible at: $NGROK_URL"
        echo "$NGROK_URL" > "$HOME/.ai-ster/current_url.txt"
        
        # Save process information
        echo "STREAMLIT_PID=$STREAMLIT_PID" > "$HOME/.ai-ster/pids.txt"
        echo "NGROK_PID=$NGROK_PID" >> "$HOME/.ai-ster/pids.txt"
        
        print_info "Running in detached mode. To stop:"
        print_info "  ./deploy/stop_deployment.sh"
    else
        print_error "Failed to retrieve ngrok URL"
    fi
else
    print_status "Starting ngrok in foreground mode..."
    print_info "Your AI-STER instance will be accessible via the ngrok URL shown below"
    print_info "Press Ctrl+C to stop both Streamlit and ngrok"
    echo ""
    $NGROK_CMD
fi
