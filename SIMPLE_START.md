# 🚀 StaffRoom Mobile - Super Simple Guide

## ✅ Flutter Installed!

Flutter is already installed on your PC. Now let's build the APK!

---

## 📱 **Build APK (No USB Debugging Needed!)**

### Just run this ONE command:

```bash
cd /home/adnan/staffroom
./build_wifi_apk.sh
```

This will:
1. ✅ Find your WiFi IP automatically
2. ✅ Configure the app
3. ✅ Build the APK
4. ✅ Start download server for your phone

---

## 📲 **Install on Phone (3 Steps)**

### Step 1: Download APK
- On your **phone browser**, go to:
  ```
  http://YOUR_PC_IP:8000/app-release.apk
  ```
  (The script will show you the exact URL)

### Step 2: Install
- Tap the downloaded file
- Allow "Unknown Sources" if asked
- Install

### Step 3: Use!
- Open StaffRoom app
- Login: `teacher` / `teacher123`

---

## 🔥 **Daily Use**

### On PC:
```bash
cd /home/adnan/staffroom
python3 web_app.py
```
(Keep this running!)

### On Phone:
- Open StaffRoom app
- Use normally!

### ⚠️ Important:
**Both PC and phone must be on the SAME WiFi!**

---

## 🎯 **Quick Summary**

```
1. Build APK:    ./build_wifi_apk.sh
2. Download:     Phone browser → http://PC_IP:8000/app-release.apk
3. Install:      Tap APK on phone
4. Run Flask:    python3 web_app.py (on PC)
5. Use App:      Open on phone (same WiFi!)
```

---

## ❓ **FAQ**

**Q: Do I need USB cable?**
A: No! Only WiFi connection needed.

**Q: Does it need internet?**
A: No! Just local WiFi between PC and phone.

**Q: Where is the database?**
A: On your PC (teacher_app_web.db)

**Q: Can multiple phones use it?**
A: Yes! Build the APK once, install on many phones. All connect to your PC's database via WiFi.

**Q: What if my PC's IP changes?**
A: Rebuild APK with new IP: `./build_wifi_apk.sh`

---

**That's it! Super simple!** 🎉
