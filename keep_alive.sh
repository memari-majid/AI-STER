#!/bin/bash
# AI-STER Keep-Alive Script
# This script ensures AI-STER stays running continuously

set -e

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
LOG_FILE="$HOME/.ai-ster/keep_alive.log"

# Colors for output
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
RED='\033[0;31m'
NC='\033[0m' # No Color

log() {
    echo "$(date): $1" | tee -a "$LOG_FILE"
}

log_colored() {
    echo -e "$1" | tee -a "$LOG_FILE"
}

# Create log directory if it doesn't exist
mkdir -p "$HOME/.ai-ster"

log "Starting AI-STER Keep-Alive Monitor..."

while true; do
    # Check if tunnel is responding (using Cloudflare now)
    TUNNEL_URL=$(cat ~/.ai-ster/cloudflared.log | grep -o "https://.*trycloudflare.com" | tail -1)
    if [ -z "$TUNNEL_URL" ]; then
        TUNNEL_URL="https://aister.ngrok.app"  # fallback
    fi
    
    if curl -s --max-time 10 "$TUNNEL_URL" > /dev/null 2>&1; then
        log_colored "${GREEN}✅ AI-STER is accessible at $TUNNEL_URL${NC}"
    else
        log_colored "${RED}❌ AI-STER is not accessible, attempting restart...${NC}"
        
        # Stop existing processes
        cd "$SCRIPT_DIR"
        ./deploy/stop_deployment.sh >> "$LOG_FILE" 2>&1 || true
        sleep 3
        
        # Start services
        ./deploy/start_with_ngrok.sh --domain aister.ngrok.app --detached >> "$LOG_FILE" 2>&1
        
        if [ $? -eq 0 ]; then
            log_colored "${GREEN}✅ AI-STER restarted successfully${NC}"
        else
            log_colored "${RED}❌ Failed to restart AI-STER${NC}"
        fi
    fi
    
    # Wait 60 seconds before next check
    sleep 60
done
