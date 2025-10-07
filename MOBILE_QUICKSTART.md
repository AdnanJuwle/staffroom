# 📱 StaffRoom Mobile App - Quick Start Guide

## 🎯 Goal
Run the StaffRoom Flutter app on your Android phone and connect it to the database on your PC.

---

## ⚡ Super Quick Setup (5 Steps)

### Step 1: Install Flutter (One-time setup)

```bash
# Option 1: Using Snap (Easiest)
sudo snap install flutter --classic

# Option 2: Manual download
# Visit: https://docs.flutter.dev/get-started/install/linux

# Verify installation
flutter doctor
```

### Step 2: Enable USB Debugging on Your Phone

1. Go to **Settings** → **About Phone**
2. Tap **Build Number** 7 times
3. Go back to **Settings** → **Developer Options**
4. Enable **USB Debugging**
5. Connect phone via USB cable
6. Accept "Allow USB Debugging" on phone

### Step 3: Run the Auto-Setup Script

```bash
cd /home/adnan/staffroom
./run_mobile_dev.sh
```

This script will:
- ✓ Find your PC's IP address
- ✓ Configure the Flutter app automatically
- ✓ Start the Flask server with network access
- ✓ Show you the next steps

### Step 4: Check Your Phone is Connected

```bash
cd flutter/teacher
flutter devices
```

You should see your phone listed!

### Step 5: Run the App

```bash
flutter run
```

That's it! The app will install and run on your phone! 🎉

---

## 📦 Build APK (For Installing Without USB)

### Quick Build

```bash
cd /home/adnan/staffroom
./build_apk.sh
```

This script will:
1. Ask how you want to configure the API (local network or production)
2. Build the APK file
3. Show you 3 ways to install it on your phone

### Manual Build

```bash
cd /home/adnan/staffroom/flutter/teacher

# Build the APK
flutter build apk --release

# APK location:
# flutter/teacher/build/app/outputs/flutter-apk/app-release.apk
```

### Install APK on Phone

**Method 1: USB Install (Fastest)**
```bash
adb install flutter/teacher/build/app/outputs/flutter-apk/app-release.apk
```

**Method 2: Download via Browser**
```bash
# Start a simple web server
cd flutter/teacher/build/app/outputs/flutter-apk
python3 -m http.server 8000

# On your phone browser, go to:
# http://YOUR_PC_IP:8000/app-release.apk
# (Get your PC IP by running: hostname -I)
```

**Method 3: Manual Transfer**
1. Copy APK to phone via USB cable
2. On phone: Files → Downloads → tap the APK
3. Allow "Install from Unknown Sources" if asked
4. Install the app

---

## 🌐 Network Setup

### Important: Both devices must be on the SAME WiFi!

**Check your PC's IP:**
```bash
hostname -I
# Example output: 192.168.1.100
```

**Configure the app to use your PC's IP:**

The `run_mobile_dev.sh` script does this automatically, but if you need to do it manually:

Edit: `flutter/teacher/lib/services/api_config.dart`
```dart
static const String baseUrl = 'http://192.168.1.100:5000';  // ← Use YOUR PC's IP
```

### Test the Connection

**From your phone's browser, visit:**
```
http://YOUR_PC_IP:5000
```

If you see the StaffRoom login page, the connection works! ✓

---

## 🔥 Troubleshooting

### Problem: Can't connect to server

**Solution 1: Check Firewall**
```bash
sudo ufw allow 5000/tcp
```

**Solution 2: Verify Flask is running**
```bash
# Check if Flask is running on port 5000
lsof -i:5000

# If not, start it:
python3 web_app.py
```

**Solution 3: Verify same WiFi**
- PC and phone must be on same WiFi network
- Check WiFi settings on both devices

### Problem: Phone not detected

**Solution:**
```bash
# Reconnect USB cable
# Make sure USB debugging is enabled
# Check connection:
flutter devices

# If not showing:
adb devices
# If you see "unauthorized", accept the prompt on phone
```

### Problem: Build fails

**Solution:**
```bash
flutter clean
flutter pub get
flutter doctor -v
```

### Problem: App crashes

**Check:**
1. Is Flask server running?
2. Is the IP address in `api_config.dart` correct?
3. Are both devices on same WiFi?
4. Check logs: `flutter logs`

---

## 📋 Complete Checklist

**One-time Setup:**
- [ ] Flutter installed (`flutter doctor` works)
- [ ] USB debugging enabled on phone
- [ ] Phone and PC on same WiFi

**Every Time You Run:**
- [ ] Phone connected via USB (for `flutter run`)
- [ ] Flask server running
- [ ] Correct IP in `api_config.dart` (auto-configured by script)

**For APK:**
- [ ] APK built successfully
- [ ] APK transferred to phone
- [ ] APK installed on phone

---

## 🚀 Quick Commands Cheat Sheet

```bash
# Setup and run on phone
./run_mobile_dev.sh           # Auto-setup everything
cd flutter/teacher
flutter devices               # Check phone connected
flutter run                   # Run app on phone

# Build APK
./build_apk.sh               # Guided APK build
# OR
cd flutter/teacher
flutter build apk --release  # Manual build

# Useful commands
hostname -I                  # Get PC IP
lsof -i:5000                # Check if Flask running
flutter doctor              # Check Flutter setup
flutter clean               # Clean build cache
adb devices                 # Check phone connection
flutter logs                # View app logs
```

---

## 🎯 Development Workflow

### For Active Development (with USB)
1. Connect phone via USB
2. Run `./run_mobile_dev.sh`
3. Run `flutter run`
4. Make code changes → Hot reload automatically!

### For Testing Without USB (APK)
1. Run `./build_apk.sh`
2. Choose local network option
3. Transfer APK to phone
4. Install and test

### For Production (Cloud)
1. Deploy Flask to Render/Railway
2. Update `api_config.dart` with production URL
3. Run `flutter build apk --release`
4. Upload to Play Store (optional)

---

## 📱 Demo Credentials

When the app loads:
- **Username:** `teacher`
- **Password:** `teacher123`

---

## 🆘 Need Help?

**Check these in order:**

1. **Flutter Setup**
   ```bash
   flutter doctor
   ```

2. **Network Connection**
   ```bash
   # Test from phone browser
   http://YOUR_PC_IP:5000
   ```

3. **Phone Connection**
   ```bash
   flutter devices
   adb devices
   ```

4. **Flask Server**
   ```bash
   lsof -i:5000
   curl http://localhost:5000
   ```

5. **View Logs**
   ```bash
   flutter logs
   # OR
   adb logcat | grep flutter
   ```

---

## 🌟 What's Working

✅ **Currently Implemented:**
- Login/Registration
- Authentication
- Dashboard (basic UI)
- Navigation menu
- API service layer
- State management

🚧 **Placeholder Pages:**
- Classes (shows placeholder)
- Organizations (shows placeholder)
- Discussions (shows placeholder)
- Resources (shows placeholder)
- Schedule (shows placeholder)
- Students (shows placeholder)

Your junior developer created the UI structure, and I've integrated:
- API communication
- Authentication flow
- Network configuration
- Build scripts

---

## 📂 File Structure

```
/home/adnan/staffroom/
├── web_app.py                    # Flask backend (configured for network access)
├── run_mobile_dev.sh            # Auto-setup script ← START HERE
├── build_apk.sh                 # APK build script
└── flutter/teacher/
    ├── lib/
    │   ├── main.dart            # App entry point
    │   ├── models/              # Data models
    │   ├── services/            # API services
    │   │   └── api_config.dart  # Network configuration
    │   ├── providers/           # State management
    │   ├── pages/               # Login/Register pages
    │   └── *_page.dart          # Feature pages
    ├── pubspec.yaml             # Dependencies
    ├── README.md                # Detailed docs
    └── SETUP_GUIDE.md           # Complete setup guide
```

---

**🎉 You're all set! Run `./run_mobile_dev.sh` to get started!**

