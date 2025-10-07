#!/bin/bash

# Simple StaffRoom Server Launcher

echo "🚀 Starting StaffRoom Server..."

# Get PC IP
IP=$(hostname -I | awk '{print $1}')

# Kill any existing Python servers
pkill -9 -f "web_app.py" 2>/dev/null
sleep 1

# Start Flask server
cd /home/adnan/staffroom
export FLASK_ENV=development
python3 web_app.py

echo ""
echo "════════════════════════════════════════"
echo "✅ Server running on: http://$IP:5000"
echo "📱 Use this IP in your app"
echo "Press Ctrl+C to stop"
echo "════════════════════════════════════════"

