# 🚀 StaffRoom Mobile App - START HERE!

## 📱 Run on Your Phone in 3 Steps

### Step 1️⃣: Install Flutter (One-time)
```bash
sudo snap install flutter --classic
flutter doctor
```

### Step 2️⃣: Connect Your Phone
1. Enable **USB Debugging** on phone (Settings → Developer Options)
2. Connect phone via USB cable
3. Accept "Allow USB Debugging" prompt

### Step 3️⃣: Run the Magic Script
```bash
cd /home/adnan/staffroom
./run_mobile_dev.sh
```

Then:
```bash
cd flutter/teacher
flutter run
```

**Done! App is now running on your phone! 🎉**

---

## 📦 OR Build APK to Install

```bash
cd /home/adnan/staffroom
./build_apk.sh
```

Follow the script's instructions to install APK on your phone.

---

## 🔑 Login Credentials

```
Username: teacher
Password: teacher123
```

---

## 📚 Full Documentation

- **Quick Start:** [MOBILE_QUICKSTART.md](MOBILE_QUICKSTART.md)
- **Complete Summary:** [FLUTTER_INTEGRATION_SUMMARY.md](FLUTTER_INTEGRATION_SUMMARY.md)
- **API Docs:** [API_DOCUMENTATION.md](API_DOCUMENTATION.md)
- **Setup Guide:** [flutter/teacher/SETUP_GUIDE.md](flutter/teacher/SETUP_GUIDE.md)

---

## 🆘 Problems?

**Can't connect to server?**
- Ensure phone and PC on same WiFi
- Run: `sudo ufw allow 5000/tcp`
- Check Flask is running: `lsof -i:5000`

**Phone not detected?**
- Check USB debugging enabled
- Run: `flutter devices`

**Build fails?**
- Run: `flutter clean && flutter pub get`

---

**Everything is ready! Just run `./run_mobile_dev.sh`** 🚀
