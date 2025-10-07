# 📱 WiFi-Only Setup - No USB Required!

## 🎯 Goal
Install the APK on your phone and use it **without any USB cable** - just WiFi!

---

## 🌐 How It Works

```
┌─────────────┐                    ┌──────────────┐
│             │   Same WiFi        │              │
│  Your Phone │◄──────────────────►│   Your PC    │
│  (APK App)  │                    │  (Database)  │
└─────────────┘                    └──────────────┘
```

**Key Point:** Both devices connect via WiFi. No USB cable needed after initial APK installation!

---

## ✅ **Setup Steps (Do Once)**

### Step 1: Find Your PC's WiFi IP Address

```bash
hostname -I
# Example output: 192.168.1.100
```

**Write down this IP address!** (e.g., 192.168.1.100)

### Step 2: Configure the App with Your IP

Edit the config file:
```bash
nano flutter/teacher/lib/services/api_config.dart
```

Change this line to your PC's IP:
```dart
static const String baseUrl = 'http://192.168.1.100:5000';  // ← Your PC's IP here!
```

Save and exit (Ctrl+X, Y, Enter)

### Step 3: Build the APK

```bash
cd /home/adnan/staffroom
./build_apk.sh
```

Choose option **1** (Local network) when prompted.

### Step 4: Transfer APK to Your Phone

**Method 1: Download via Browser** (Easiest, no USB!)
```bash
# Start web server
cd flutter/teacher/build/app/outputs/flutter-apk
python3 -m http.server 8000

# On your phone browser, go to:
# http://YOUR_PC_IP:8000/app-release.apk
# Example: http://192.168.1.100:8000/app-release.apk
```

**Method 2: Transfer via USB** (one-time only)
- Connect phone via USB
- Copy APK file to phone
- Disconnect USB forever!

**Method 3: Email/Cloud**
- Email the APK to yourself
- Download on phone
- Install

### Step 5: Install APK on Phone

1. Tap the downloaded APK
2. Allow "Install from Unknown Sources" if asked
3. Install the app

### Step 6: Start Flask Server on PC

```bash
cd /home/adnan/staffroom
python3 web_app.py
```

**Keep this running!** This is your backend server.

### Step 7: Connect and Use!

1. **Ensure both PC and phone are on the SAME WiFi**
2. Open the StaffRoom app on your phone
3. Login with: `teacher` / `teacher123`
4. Use the app! ✨

---

## 🔄 **Daily Usage (After Setup)**

Every time you want to use the app:

1. **On PC:** Start Flask server
   ```bash
   cd /home/adnan/staffroom
   python3 web_app.py
   ```

2. **On Phone:** Open StaffRoom app (already installed)

3. **Both devices must be on same WiFi!**

That's it! No USB cable needed! 🎉

---

## 🚀 **Quick Build Script** (For WiFi Setup)

I've created a special script for you:

```bash
cd /home/adnan/staffroom
./build_wifi_apk.sh
```

This script will:
1. Ask for your WiFi IP
2. Auto-configure the app
3. Build the APK
4. Start a web server for download
5. Show QR code (if available)

---

## 🔧 **Troubleshooting**

### Problem: Can't connect to database

**Check 1: Same WiFi?**
- PC and phone must be on the **same WiFi network**
- Check WiFi settings on both devices

**Check 2: Flask running?**
```bash
# Check if Flask is running
lsof -i:5000
```

**Check 3: Firewall?**
```bash
# Allow Flask port
sudo ufw allow 5000/tcp
```

**Check 4: Test connection**
- On phone browser, visit: `http://YOUR_PC_IP:5000`
- Should see StaffRoom login page

### Problem: IP address changed

Your PC's WiFi IP can change! If app stops working:

1. Check current IP: `hostname -I`
2. If changed, rebuild APK with new IP
3. Reinstall on phone

**Tip:** Set a static IP on your router to avoid this!

---

## 📊 **Network Requirements**

```
✅ Required:
- PC and phone on same WiFi network
- PC IP address (find with: hostname -I)
- Flask server running on PC
- Firewall allows port 5000

❌ Not Required:
- USB cable (after initial APK install)
- Internet connection (local WiFi only)
- Cloud services
- Complex setup
```

---

## 🎯 **APK Configuration Scenarios**

### Scenario 1: Home WiFi Only
```dart
// Configure with home WiFi IP
static const String baseUrl = 'http://192.168.1.100:5000';
```
✅ Works at home
❌ Won't work outside home

### Scenario 2: Multiple Locations
Build different APKs for each location:
- `app-home.apk` → Home WiFi IP
- `app-office.apk` → Office WiFi IP

### Scenario 3: Cloud Access (Recommended for flexibility)
```dart
// Deploy backend to cloud
static const String baseUrl = 'https://your-app.onrender.com';
```
✅ Works anywhere with internet
✅ No IP address issues
✅ Professional solution

---

## 🌟 **Permanent Solution: Cloud Deployment**

For access from anywhere (not just same WiFi):

1. **Deploy backend to Render** (free tier available)
2. **Update APK config** to cloud URL
3. **Rebuild APK once**
4. **Use from anywhere!** ✨

See [DEPLOYMENT_GUIDE.md](DEPLOYMENT_GUIDE.md) for cloud setup.

---

## 📱 **APK Distribution**

Once built, you can share the APK with others:

1. **Share file directly** (WhatsApp, Email, etc.)
2. **Upload to Google Drive** and share link
3. **Host on web server** for download
4. **Deploy to Play Store** (for professional distribution)

**Important:** Everyone using the APK will connect to YOUR PC's database!

---

## ✅ **Quick Checklist**

Before using the app:

- [ ] PC's WiFi IP address noted
- [ ] APK built with correct IP
- [ ] APK installed on phone
- [ ] Flask server running on PC
- [ ] Firewall allows port 5000
- [ ] Both devices on same WiFi
- [ ] Tested connection from phone browser

---

## 🚀 **One-Command Setup**

For the absolute quickest setup:

```bash
# Run this single command
cd /home/adnan/staffroom && ./build_wifi_apk.sh && cd flutter/teacher/build/app/outputs/flutter-apk && python3 -m http.server 8000
```

Then on phone browser: `http://YOUR_PC_IP:8000/app-release.apk`

---

**Remember:** USB is only needed to build the APK (or transfer it once). After that, everything works over WiFi! 📶

