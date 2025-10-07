#!/bin/bash

# Kill any existing servers
pkill -9 -f "python3 web_app.py" 2>/dev/null
pkill -9 -f "http.server" 2>/dev/null
sleep 2

# Get IP
PC_IP=$(hostname -I | awk '{print $1}')

echo "════════════════════════════════════════════════"
echo "🚀 Starting StaffRoom Mobile Server"
echo "════════════════════════════════════════════════"
echo ""
echo "📍 Your PC IP: $PC_IP"
echo "🌐 Flask will run on: http://$PC_IP:5000"
echo ""
echo "════════════════════════════════════════════════"
echo ""

# Start Flask
cd /home/adnan/staffroom
python3 web_app.py &
FLASK_PID=$!

sleep 3

# Check if Flask started
if lsof -i:5000 > /dev/null 2>&1; then
    echo "✅ Flask server is running!"
    echo ""
    echo "════════════════════════════════════════════════"
    echo "📱 Test Connection from Phone Browser:"
    echo "   http://$PC_IP:5000"
    echo "════════════════════════════════════════════════"
    echo ""
    echo "Press Ctrl+C to stop server"
    echo ""
    
    # Keep running and show logs
    tail -f flask.log 2>/dev/null &
    wait $FLASK_PID
else
    echo "❌ Failed to start Flask server"
    echo "Check flask.log for errors"
fi

