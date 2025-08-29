#!/bin/bash

# AI-STER Deployment Stop Script
# This script stops the running Streamlit and ngrok processes

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

# Check for PID file
PID_FILE="$HOME/.ai-ster/pids.txt"
STOPPED=false

if [ -f "$PID_FILE" ]; then
    source "$PID_FILE"
    
    # Stop Streamlit
    if [ ! -z "$STREAMLIT_PID" ] && kill -0 $STREAMLIT_PID 2>/dev/null; then
        print_warning "Stopping Streamlit (PID: $STREAMLIT_PID)..."
        kill $STREAMLIT_PID
        STOPPED=true
    fi
    
    # Stop ngrok
    if [ ! -z "$NGROK_PID" ] && kill -0 $NGROK_PID 2>/dev/null; then
        print_warning "Stopping ngrok (PID: $NGROK_PID)..."
        kill $NGROK_PID
        STOPPED=true
    fi
    
    # Remove PID file
    rm -f "$PID_FILE"
fi

# Also check for any running processes by name
if pgrep -f "streamlit run" > /dev/null; then
    print_warning "Found Streamlit processes, stopping them..."
    pkill -f "streamlit run"
    STOPPED=true
fi

if pgrep -f "ngrok http" > /dev/null; then
    print_warning "Found ngrok processes, stopping them..."
    pkill -f "ngrok http"
    STOPPED=true
fi

# Clean up URL file
if [ -f "$HOME/.ai-ster/current_url.txt" ]; then
    rm -f "$HOME/.ai-ster/current_url.txt"
fi

if [ "$STOPPED" = true ]; then
    print_status "AI-STER deployment stopped successfully!"
else
    print_error "No running AI-STER deployment found."
fi
