#!/bin/bash

# Colors
GREEN='\033[0;32m'
BLUE='\033[0;34m'
RED='\033[0;31m'
YELLOW='\033[1;33m'
NC='\033[0m'

echo -e "${BLUE}════════════════════════════════════════════════${NC}"
echo -e "${BLUE}📦 Building StaffRoom APK${NC}"
echo -e "${BLUE}════════════════════════════════════════════════${NC}\n"

# Get PC IP
PC_IP=$(hostname -I | awk '{print $1}')
echo -e "${GREEN}Your PC IP: $PC_IP${NC}"
echo -e "${YELLOW}⚠ Make sure api_config.dart is configured with your network!${NC}\n"

# Check if Flutter is installed
if ! command -v flutter &> /dev/null; then
    echo -e "${RED}✗ Flutter is not installed!${NC}"
    echo -e "Install from: https://docs.flutter.dev/get-started/install\n"
    exit 1
fi

# Navigate to Flutter project
cd flutter/teacher || exit 1

# Ask user about API configuration
echo -e "${YELLOW}Choose API configuration:${NC}"
echo -e "  1. Local network (PC IP: $PC_IP) - for testing on same WiFi"
echo -e "  2. Production (Render/Cloud) - for internet access"
echo -e "  3. Keep current configuration"
read -p "Enter choice (1-3): " choice

case $choice in
    1)
        echo -e "\n${GREEN}Configuring for local network...${NC}"
        sed -i "s|static const String baseUrl = '.*';|static const String baseUrl = 'http://$PC_IP:5000';|" \
          lib/services/api_config.dart
        echo -e "✓ Configured to: http://$PC_IP:5000\n"
        ;;
    2)
        read -p "Enter your production URL (e.g., https://yourapp.onrender.com): " PROD_URL
        echo -e "\n${GREEN}Configuring for production...${NC}"
        sed -i "s|static const String baseUrl = '.*';|static const String baseUrl = '$PROD_URL';|" \
          lib/services/api_config.dart
        echo -e "✓ Configured to: $PROD_URL\n"
        ;;
    3)
        echo -e "\n${GREEN}Keeping current configuration${NC}\n"
        ;;
    *)
        echo -e "\n${RED}Invalid choice, keeping current configuration${NC}\n"
        ;;
esac

# Show current configuration
echo -e "${BLUE}Current API configuration:${NC}"
grep "baseUrl =" lib/services/api_config.dart | head -1
echo ""

# Get dependencies
echo -e "${GREEN}Installing dependencies...${NC}"
flutter pub get

if [ $? -ne 0 ]; then
    echo -e "${RED}✗ Failed to get dependencies${NC}\n"
    exit 1
fi

# Clean previous builds
echo -e "\n${GREEN}Cleaning previous builds...${NC}"
flutter clean

# Build APK
echo -e "\n${GREEN}Building release APK (this may take a few minutes)...${NC}\n"
flutter build apk --release

# Check result
APK_PATH="build/app/outputs/flutter-apk/app-release.apk"
if [ -f "$APK_PATH" ]; then
    echo -e "\n${BLUE}════════════════════════════════════════════════${NC}"
    echo -e "${GREEN}✓ APK built successfully!${NC}"
    echo -e "${BLUE}════════════════════════════════════════════════${NC}\n"
    
    echo -e "📍 Location: ${GREEN}$(realpath $APK_PATH)${NC}"
    echo -e "📊 Size: ${GREEN}$(du -h $APK_PATH | cut -f1)${NC}\n"
    
    echo -e "${BLUE}📲 Install Options:${NC}\n"
    
    echo -e "${YELLOW}Option 1: USB Install${NC}"
    echo -e "  ${GREEN}adb install $APK_PATH${NC}\n"
    
    echo -e "${YELLOW}Option 2: Manual Transfer${NC}"
    echo -e "  1. Copy APK to phone via USB cable"
    echo -e "  2. Open file manager on phone"
    echo -e "  3. Tap APK to install\n"
    
    echo -e "${YELLOW}Option 3: HTTP Download${NC}"
    echo -e "  Run this command:"
    echo -e "  ${GREEN}cd build/app/outputs/flutter-apk && python3 -m http.server 8000${NC}"
    echo -e "  Then on phone browser:"
    echo -e "  ${GREEN}http://$PC_IP:8000/app-release.apk${NC}\n"
    
    echo -e "${BLUE}════════════════════════════════════════════════${NC}\n"
    
    # Offer to serve the file
    read -p "Would you like to serve the APK via HTTP now? (y/n): " serve
    if [ "$serve" = "y" ] || [ "$serve" = "Y" ]; then
        cd build/app/outputs/flutter-apk
        echo -e "\n${GREEN}Starting HTTP server...${NC}"
        echo -e "Download from phone: ${BLUE}http://$PC_IP:8000/app-release.apk${NC}\n"
        echo -e "${YELLOW}Press Ctrl+C to stop the server${NC}\n"
        python3 -m http.server 8000
    fi
else
    echo -e "\n${BLUE}════════════════════════════════════════════════${NC}"
    echo -e "${RED}✗ Build failed!${NC}"
    echo -e "${BLUE}════════════════════════════════════════════════${NC}\n"
    echo -e "Check the error messages above for details.\n"
    echo -e "Common solutions:"
    echo -e "  - Run: ${GREEN}flutter doctor${NC}"
    echo -e "  - Run: ${GREEN}flutter clean && flutter pub get${NC}"
    echo -e "  - Check Android SDK installation\n"
    exit 1
fi

