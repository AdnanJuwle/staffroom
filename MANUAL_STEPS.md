# 📱 Manual Steps to Run Mobile App

## 🎯 Simple Steps (Do These in Order)

### Step 1: Start Flask Server

Open a terminal and run:

```bash
cd /home/adnan/staffroom
python3 web_app.py
```

**Keep this terminal open!** You should see:
```
🚀 StaffRoom Server Starting
* Running on http://192.168.1.13:5000
```

### Step 2: Test from Phone Browser

On your phone browser, visit:
```
http://192.168.1.13:5000
```

You should see the StaffRoom login page. If you don't:
- Check both devices are on SAME WiFi
- Check firewall: `sudo ufw allow 5000/tcp`

### Step 3: Download New APK

Open **another terminal** (don't close Flask!) and run:

```bash
cd /home/adnan/staffroom/flutter/teacher/build/app/outputs/flutter-apk
python3 -m http.server 8000
```

On phone browser:
```
http://192.168.1.13:8000/app-release.apk
```

### Step 4: Install APK

1. **Uninstall old StaffRoom app** (if installed)
2. **Install new APK** you just downloaded
3. **Open app**
4. **Login:** teacher / teacher123

---

## ✅ What Should Happen

When you click login in the app:
- Flask terminal should show: `POST /api/login`
- App should show dashboard

If timeout occurs:
- Flask isn't receiving the request
- Network/firewall issue

---

## 🔧 Quick Test

Test API endpoint manually:

```bash
curl -X POST http://192.168.1.13:5000/api/login \
  -H "Content-Type: application/json" \
  -d '{"username":"teacher","password":"teacher123"}'
```

Should return JSON with user data.

---

## 📍 Files Location

**APK Location:**
```
/home/adnan/staffroom/flutter/teacher/build/app/outputs/flutter-apk/app-release.apk
```

**Server Code:**
```
/home/adnan/staffroom/web_app.py
```

---

## ⚠️ Common Issues

**Issue: Connection timeout**
- Flask not running
- Wrong IP address
- Different WiFi networks
- Firewall blocking

**Issue: Operation not permitted**
- Need new APK (with cleartext traffic enabled) ✓ Done

**Issue: Port in use**
- Kill old processes: `pkill -9 -f "python3 web_app.py"`

