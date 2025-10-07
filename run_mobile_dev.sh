#!/bin/bash

# Colors for output
GREEN='\033[0;32m'
BLUE='\033[0;34m'
RED='\033[0;31m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

echo -e "${BLUE}════════════════════════════════════════════════${NC}"
echo -e "${BLUE}🚀 StaffRoom Mobile Development Setup${NC}"
echo -e "${BLUE}════════════════════════════════════════════════${NC}\n"

# Get PC IP
echo -e "${GREEN}1. Finding your PC's IP address...${NC}"
PC_IP=$(hostname -I | awk '{print $1}')
if [ -z "$PC_IP" ]; then
    echo -e "   ${RED}✗ Could not detect IP address${NC}"
    echo -e "   Please run: ${YELLOW}ip addr show${NC} and find your IP manually\n"
    exit 1
fi
echo -e "   Your PC IP: ${GREEN}$PC_IP${NC}\n"

# Update API config
echo -e "${GREEN}2. Updating Flutter API configuration...${NC}"
API_CONFIG_FILE="flutter/teacher/lib/services/api_config.dart"
if [ -f "$API_CONFIG_FILE" ]; then
    # Backup original
    cp "$API_CONFIG_FILE" "$API_CONFIG_FILE.backup"
    
    # Update the baseUrl line
    sed -i "s|static const String baseUrl = 'http://.*';|static const String baseUrl = 'http://$PC_IP:5000';|" "$API_CONFIG_FILE"
    echo -e "   ✓ API configured to: ${BLUE}http://$PC_IP:5000${NC}\n"
else
    echo -e "   ${RED}✗ API config file not found!${NC}\n"
    exit 1
fi

# Check if Flask is running
echo -e "${GREEN}3. Checking Flask server...${NC}"
if lsof -Pi :5000 -sTCP:LISTEN -t > /dev/null 2>&1; then
    echo -e "   ✓ Flask server is already running on port 5000\n"
else
    echo -e "   ${YELLOW}⚠ Flask server not running${NC}"
    echo -e "   Starting Flask server with external access...\n"
    
    # Start Flask in background
    python3 web_app.py > flask.log 2>&1 &
    FLASK_PID=$!
    sleep 3
    
    if lsof -Pi :5000 -sTCP:LISTEN -t > /dev/null 2>&1; then
        echo -e "   ${GREEN}✓ Flask server started (PID: $FLASK_PID)${NC}\n"
    else
        echo -e "   ${RED}✗ Failed to start Flask server${NC}"
        echo -e "   Check flask.log for errors\n"
        exit 1
    fi
fi

# Check firewall
echo -e "${GREEN}4. Checking firewall...${NC}"
if command -v ufw > /dev/null 2>&1; then
    if sudo ufw status | grep -q "5000.*ALLOW" > /dev/null 2>&1; then
        echo -e "   ✓ Port 5000 is allowed through firewall\n"
    else
        echo -e "   ${YELLOW}⚠ Port 5000 not explicitly allowed${NC}"
        echo -e "   To allow: ${YELLOW}sudo ufw allow 5000/tcp${NC}\n"
    fi
else
    echo -e "   ℹ UFW not installed, skipping firewall check\n"
fi

# Instructions
echo -e "${BLUE}════════════════════════════════════════════════${NC}"
echo -e "${BLUE}📱 Next Steps:${NC}"
echo -e "${BLUE}════════════════════════════════════════════════${NC}\n"

echo -e "${YELLOW}On Your Phone:${NC}"
echo -e "  1. Connect to the same WiFi as this PC"
echo -e "  2. Enable USB debugging (Settings → Developer Options)"
echo -e "  3. Connect phone via USB cable"
echo -e "  4. Accept USB debugging prompt on phone\n"

echo -e "${YELLOW}Then Run:${NC}"
echo -e "  ${GREEN}cd flutter/teacher${NC}"
echo -e "  ${GREEN}flutter devices${NC}  ${NC}# Check if phone is detected"
echo -e "  ${GREEN}flutter run${NC}       ${NC}# Run app on phone\n"

echo -e "${BLUE}════════════════════════════════════════════════${NC}"
echo -e "${BLUE}📋 Test Access:${NC}"
echo -e "${BLUE}════════════════════════════════════════════════${NC}\n"

echo -e "From your phone browser, visit:"
echo -e "  ${GREEN}http://$PC_IP:5000${NC}\n"

echo -e "If it loads, the connection is working! ✓\n"

echo -e "${BLUE}════════════════════════════════════════════════${NC}\n"

# Cleanup on exit
trap "echo -e '\n${YELLOW}Shutting down...${NC}'; kill $FLASK_PID 2>/dev/null" EXIT SIGINT SIGTERM

