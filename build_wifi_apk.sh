#!/bin/bash

# Colors
GREEN='\033[0;32m'
BLUE='\033[0;34m'
RED='\033[0;31m'
YELLOW='\033[1;33m'
CYAN='\033[0;36m'
NC='\033[0m'

echo -e "${BLUE}════════════════════════════════════════════════${NC}"
echo -e "${BLUE}📱 StaffRoom WiFi APK Builder${NC}"
echo -e "${BLUE}   (No USB Required After Installation!)${NC}"
echo -e "${BLUE}════════════════════════════════════════════════${NC}\n"

# Get PC IP
PC_IP=$(hostname -I | awk '{print $1}')

if [ -z "$PC_IP" ]; then
    echo -e "${RED}✗ Could not detect IP address${NC}"
    echo -e "Please find your IP manually with: ${YELLOW}ip addr show${NC}\n"
    exit 1
fi

echo -e "${GREEN}📍 Your PC's WiFi IP: ${CYAN}$PC_IP${NC}\n"

# Confirm or change IP
read -p "Is this IP correct? (y/n): " ip_confirm
if [ "$ip_confirm" != "y" ] && [ "$ip_confirm" != "Y" ]; then
    read -p "Enter your WiFi IP address: " PC_IP
fi

echo -e "\n${BLUE}════════════════════════════════════════════════${NC}"
echo -e "${GREEN}Step 1: Configuring Flutter App${NC}"
echo -e "${BLUE}════════════════════════════════════════════════${NC}\n"

# Update API config
API_CONFIG="flutter/teacher/lib/services/api_config.dart"
if [ -f "$API_CONFIG" ]; then
    # Backup
    cp "$API_CONFIG" "$API_CONFIG.backup"
    
    # Update baseUrl
    sed -i "s|static const String baseUrl = 'http://.*';|static const String baseUrl = 'http://$PC_IP:5000';|" "$API_CONFIG"
    
    echo -e "✓ Configured app to connect to: ${CYAN}http://$PC_IP:5000${NC}\n"
else
    echo -e "${RED}✗ Config file not found!${NC}\n"
    exit 1
fi

# Check Flutter installation
if ! command -v flutter &> /dev/null; then
    echo -e "${RED}✗ Flutter is not installed!${NC}"
    echo -e "Install with: ${YELLOW}sudo snap install flutter --classic${NC}\n"
    exit 1
fi

echo -e "${BLUE}════════════════════════════════════════════════${NC}"
echo -e "${GREEN}Step 2: Building APK${NC}"
echo -e "${BLUE}════════════════════════════════════════════════${NC}\n"

cd flutter/teacher || exit 1

# Get dependencies
echo -e "${CYAN}Installing dependencies...${NC}"
flutter pub get > /dev/null 2>&1

# Clean
echo -e "${CYAN}Cleaning previous builds...${NC}"
flutter clean > /dev/null 2>&1

# Build APK
echo -e "${CYAN}Building APK (this takes 2-3 minutes)...${NC}\n"
flutter build apk --release

APK_PATH="build/app/outputs/flutter-apk/app-release.apk"

if [ ! -f "$APK_PATH" ]; then
    echo -e "\n${RED}✗ Build failed!${NC}"
    echo -e "Run ${YELLOW}flutter doctor${NC} to check setup\n"
    exit 1
fi

echo -e "\n${BLUE}════════════════════════════════════════════════${NC}"
echo -e "${GREEN}✓ APK Built Successfully!${NC}"
echo -e "${BLUE}════════════════════════════════════════════════${NC}\n"

APK_FULL_PATH=$(realpath "$APK_PATH")
APK_SIZE=$(du -h "$APK_PATH" | cut -f1)

echo -e "📍 Location: ${CYAN}$APK_FULL_PATH${NC}"
echo -e "📊 Size: ${CYAN}$APK_SIZE${NC}\n"

echo -e "${BLUE}════════════════════════════════════════════════${NC}"
echo -e "${YELLOW}📲 How to Install APK on Your Phone${NC}"
echo -e "${BLUE}════════════════════════════════════════════════${NC}\n"

echo -e "${GREEN}Option 1: Download via WiFi (Recommended - No USB!)${NC}"
echo -e "  1. I'll start a web server for you..."
echo -e "  2. On your phone browser, go to:"
echo -e "     ${CYAN}http://$PC_IP:8000/app-release.apk${NC}"
echo -e "  3. Download and install!\n"

echo -e "${GREEN}Option 2: Transfer via USB (One-time)${NC}"
echo -e "  1. Connect phone via USB"
echo -e "  2. Copy APK to phone"
echo -e "  3. Tap to install"
echo -e "  4. Disconnect USB forever! 😊\n"

echo -e "${GREEN}Option 3: Share via Link${NC}"
echo -e "  1. Upload APK to Google Drive/Dropbox"
echo -e "  2. Share link"
echo -e "  3. Download on phone\n"

echo -e "${BLUE}════════════════════════════════════════════════${NC}\n"

# Ask to serve
read -p "Start web server for WiFi download? (y/n): " serve

if [ "$serve" = "y" ] || [ "$serve" = "Y" ]; then
    cd build/app/outputs/flutter-apk || exit 1
    
    echo -e "\n${BLUE}════════════════════════════════════════════════${NC}"
    echo -e "${GREEN}🌐 Web Server Started!${NC}"
    echo -e "${BLUE}════════════════════════════════════════════════${NC}\n"
    
    echo -e "${YELLOW}On your phone:${NC}"
    echo -e "  1. Connect to the same WiFi as this PC"
    echo -e "  2. Open browser"
    echo -e "  3. Go to: ${CYAN}http://$PC_IP:8000/app-release.apk${NC}"
    echo -e "  4. Download and install\n"
    
    echo -e "${YELLOW}Important:${NC}"
    echo -e "  • Phone and PC must be on ${GREEN}same WiFi${NC}"
    echo -e "  • Press ${RED}Ctrl+C${NC} to stop server after download\n"
    
    echo -e "${BLUE}════════════════════════════════════════════════${NC}\n"
    
    # Start server
    python3 -m http.server 8000
else
    echo -e "\n${YELLOW}Next Steps:${NC}"
    echo -e "  1. Transfer APK to your phone (any method)"
    echo -e "  2. Install on phone"
    echo -e "  3. Start Flask server on PC:"
    echo -e "     ${CYAN}python3 web_app.py${NC}"
    echo -e "  4. Open app on phone (both on same WiFi!)\n"
    
    echo -e "${GREEN}APK Ready!${NC} Transfer it to your phone and install.\n"
fi

echo -e "${BLUE}════════════════════════════════════════════════${NC}"
echo -e "${GREEN}📱 After Installation:${NC}"
echo -e "${BLUE}════════════════════════════════════════════════${NC}\n"

echo -e "1. ${GREEN}On PC:${NC} Run Flask server"
echo -e "   ${CYAN}cd /home/adnan/staffroom && python3 web_app.py${NC}\n"

echo -e "2. ${GREEN}On Phone:${NC} Open StaffRoom app\n"

echo -e "3. ${GREEN}Both:${NC} Must be on same WiFi!\n"

echo -e "4. ${GREEN}Login:${NC} teacher / teacher123\n"

echo -e "${YELLOW}⚠️  Remember:${NC} If PC's IP changes, rebuild APK with new IP!\n"

echo -e "${BLUE}════════════════════════════════════════════════${NC}\n"

