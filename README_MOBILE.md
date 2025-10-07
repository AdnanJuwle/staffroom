# 📱 StaffRoom Mobile App - Complete Guide

## ✅ Setup Complete!

✓ Flutter installed on your PC  
✓ Mobile app integrated with backend  
✓ WiFi connection configured  
✓ Build scripts ready  

---

## 🚀 **Quick Start (Choose One)**

### **Option 1: WiFi Only (Recommended - No USB!)**

```bash
./build_wifi_apk.sh
```

Then download on phone: `http://YOUR_PC_IP:8000/app-release.apk`

📖 **Guide:** [SIMPLE_START.md](SIMPLE_START.md)

---

### **Option 2: USB Development**

```bash
./run_mobile_dev.sh
cd flutter/teacher
flutter run
```

📖 **Guide:** [MOBILE_QUICKSTART.md](MOBILE_QUICKSTART.md)

---

## 🎯 **How It Works**

### **Architecture:**

```
Phone (WiFi) ←→ PC (Flask Server) ←→ Database (SQLite)
```

- **Phone:** Runs the Flutter app (APK installed)
- **PC:** Runs Flask server with database
- **Connection:** WiFi (both on same network)
- **No USB:** After APK installation, only WiFi needed!

### **Key Points:**

1. ✅ **Database stays on PC** (not on phone)
2. ✅ **WiFi connection** (same network required)
3. ✅ **No USB needed** (after APK install)
4. ✅ **No internet needed** (local WiFi only)
5. ✅ **Multiple phones** can connect to same database

---

## 📚 **Documentation**

### **Getting Started:**
- 🟢 **[SIMPLE_START.md](SIMPLE_START.md)** ← Start here! (Easiest)
- 🔵 **[WIFI_SETUP_GUIDE.md](WIFI_SETUP_GUIDE.md)** ← WiFi-only setup
- 🟡 **[MOBILE_QUICKSTART.md](MOBILE_QUICKSTART.md)** ← USB development

### **Advanced:**
- **[API_DOCUMENTATION.md](API_DOCUMENTATION.md)** - Complete API reference
- **[ARCHITECTURE.md](ARCHITECTURE.md)** - System architecture
- **[flutter/teacher/SETUP_GUIDE.md](flutter/teacher/SETUP_GUIDE.md)** - Detailed setup

### **Scripts:**
- `./build_wifi_apk.sh` - Build WiFi APK
- `./build_apk.sh` - General APK builder
- `./run_mobile_dev.sh` - Development setup

---

## 🔐 **Login Credentials**

```
Username: teacher
Password: teacher123
```

---

## 📋 **Prerequisites**

### **One-Time Setup:**
- [x] Flutter installed ✓
- [ ] PC and phone on same WiFi
- [ ] Firewall allows port 5000: `sudo ufw allow 5000/tcp`

### **Every Use:**
- [ ] Flask server running: `python3 web_app.py`
- [ ] Both devices on same WiFi

---

## 🎯 **Common Scenarios**

### **Scenario 1: First Time Setup**

```bash
# 1. Build APK
./build_wifi_apk.sh

# 2. Download on phone browser
http://YOUR_PC_IP:8000/app-release.apk

# 3. Install APK on phone

# 4. Start Flask
python3 web_app.py

# 5. Open app on phone
```

---

### **Scenario 2: Daily Use**

```bash
# On PC (keep running)
python3 web_app.py

# On Phone
# Just open the app!
```

---

### **Scenario 3: Share with Others**

1. Build APK once with your WiFi IP
2. Share APK file with others
3. They install on their phones
4. All phones connect to your PC's database
5. Everyone shares same data!

---

## 🔧 **Troubleshooting**

### **Can't connect to database?**

```bash
# Check 1: Same WiFi?
# Verify both devices on same network

# Check 2: Flask running?
lsof -i:5000

# Check 3: Firewall?
sudo ufw allow 5000/tcp

# Check 4: Test connection
# On phone browser: http://YOUR_PC_IP:5000
```

### **IP address changed?**

```bash
# Find new IP
hostname -I

# Rebuild APK with new IP
./build_wifi_apk.sh

# Reinstall on phone
```

### **Build failed?**

```bash
flutter clean
flutter pub get
flutter doctor
```

---

## 🌟 **Features**

### **✅ Working:**
- Login/Registration
- Authentication
- Dashboard
- Navigation
- API integration

### **🚧 To Complete:**
- Classes management (UI ready)
- Organizations (UI ready)
- Discussions (UI ready)
- Resources (UI ready)
- Schedule (UI ready)

Your junior created the UI, I've added the backend integration!

---

## 📊 **Network Setup**

### **Development (Same WiFi):**
```
baseUrl = 'http://192.168.1.100:5000'  // Your PC's IP
```
- ✅ Free
- ✅ No internet needed
- ✅ Fast
- ❌ Only works on same WiFi

### **Production (Cloud):**
```
baseUrl = 'https://your-app.onrender.com'
```
- ✅ Works anywhere
- ✅ No IP issues
- ✅ Professional
- ❌ Requires cloud deployment

See [DEPLOYMENT_GUIDE.md](DEPLOYMENT_GUIDE.md) for cloud setup.

---

## 🔑 **Key Commands**

```bash
# Build WiFi APK (easiest)
./build_wifi_apk.sh

# Build APK with options
./build_apk.sh

# Development mode
./run_mobile_dev.sh

# Manual build
cd flutter/teacher
flutter build apk --release

# Install via USB
adb install build/app/outputs/flutter-apk/app-release.apk

# Start Flask server
python3 web_app.py

# Check Flutter
flutter doctor

# Find PC IP
hostname -I

# Test connection
curl http://localhost:5000
```

---

## 📁 **Important Files**

```
/home/adnan/staffroom/
├── build_wifi_apk.sh          ← Build WiFi APK (START HERE!)
├── SIMPLE_START.md            ← Simplest guide
├── WIFI_SETUP_GUIDE.md        ← WiFi setup details
├── web_app.py                 ← Flask server (modified for WiFi)
│
└── flutter/teacher/
    ├── lib/services/api_config.dart  ← Network configuration
    └── build/app/outputs/flutter-apk/
        └── app-release.apk    ← Your APK file!
```

---

## 🎉 **Success Checklist**

After setup, you should be able to:

- [x] Build APK with one command
- [x] Download APK via WiFi (no USB)
- [x] Install APK on phone
- [x] Run Flask server on PC
- [x] Open app on phone
- [x] Login successfully
- [x] See dashboard
- [x] Navigate pages

---

## 🆘 **Need Help?**

1. **Quick Guide:** [SIMPLE_START.md](SIMPLE_START.md)
2. **WiFi Setup:** [WIFI_SETUP_GUIDE.md](WIFI_SETUP_GUIDE.md)
3. **Troubleshooting:** Check guides above
4. **Architecture:** [ARCHITECTURE.md](ARCHITECTURE.md)

---

## 🚀 **Next Steps**

### **For Testing:**
1. Run `./build_wifi_apk.sh`
2. Install APK on phone
3. Start Flask: `python3 web_app.py`
4. Test the app!

### **For Development:**
1. Complete placeholder pages
2. Add real API calls
3. Implement file uploads
4. Add error handling

### **For Production:**
1. Deploy to cloud (Render/Railway)
2. Update API config to cloud URL
3. Rebuild APK
4. Distribute to users

---

**Everything is ready! Just run:**

```bash
./build_wifi_apk.sh
```

**🎊 Enjoy your mobile app!**

