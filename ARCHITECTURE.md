# 🏗️ StaffRoom Architecture Overview

## 📊 System Architecture

```
┌─────────────────────────────────────────────────────────────┐
│                     STAFFROOM SYSTEM                         │
│                                                              │
│  ┌──────────────┐      ┌──────────────┐                    │
│  │   WEB APP    │      │  MOBILE APP  │                    │
│  │  (Browser)   │      │  (Flutter)   │                    │
│  └──────┬───────┘      └──────┬───────┘                    │
│         │                     │                             │
│         │    HTTP/REST        │                             │
│         └─────────┬───────────┘                             │
│                   │                                          │
│         ┌─────────▼──────────┐                              │
│         │   FLASK SERVER     │                              │
│         │   (web_app.py)     │                              │
│         │   Port: 5000       │                              │
│         │   Host: 0.0.0.0    │                              │
│         └─────────┬──────────┘                              │
│                   │                                          │
│         ┌─────────▼──────────┐                              │
│         │   SQLite DATABASE  │                              │
│         │ (teacher_app_web.db)│                             │
│         └────────────────────┘                              │
│                                                              │
└─────────────────────────────────────────────────────────────┘
```

## 🌐 Network Flow

### Local Development (Phone on Same WiFi)

```
┌─────────────┐                    ┌──────────────┐
│             │   WiFi Network     │              │
│  Your Phone │◄──────────────────►│   Your PC    │
│             │  192.168.1.x       │ 192.168.1.100│
└─────────────┘                    └──────────────┘
      │                                    │
      │                                    │
  ┌───▼────┐                          ┌───▼─────┐
  │ Flutter│                          │  Flask  │
  │  App   │  HTTP on Port 5000       │ Server  │
  └───┬────┘◄─────────────────────────┤  :5000  │
      │                                └─────────┘
      │
  API Calls:
  - POST /login
  - GET /dashboard
  - POST /api/create_class
  - etc.
```

### Production (Cloud Deployment)

```
┌─────────────┐                    ┌──────────────┐
│             │                    │              │
│  Any Phone  │   Internet         │   Render     │
│  (Anywhere) │◄──────────────────►│   Server     │
│             │  HTTPS             │              │
└─────────────┘                    └──────────────┘
      │                                    │
      │                                    │
  ┌───▼────┐                          ┌───▼─────┐
  │ Flutter│                          │  Flask  │
  │  App   │  HTTPS                   │ + PSQL  │
  └───┬────┘◄─────────────────────────┤         │
      │                                └─────────┘
      │
  API: https://your-app.onrender.com
```

## 📱 Flutter App Architecture

```
┌─────────────────────────────────────────────┐
│            Flutter App Structure             │
│                                              │
│  ┌────────────────────────────────────┐    │
│  │          UI Layer (Widgets)         │    │
│  │  - LoginPage                        │    │
│  │  - DashboardPage                    │    │
│  │  - ClassesPage                      │    │
│  │  - etc.                             │    │
│  └──────────────┬─────────────────────┘    │
│                 │                            │
│  ┌──────────────▼─────────────────────┐    │
│  │      State Management (Provider)    │    │
│  │  - AuthProvider                     │    │
│  │  - User session                     │    │
│  │  - Organization context             │    │
│  └──────────────┬─────────────────────┘    │
│                 │                            │
│  ┌──────────────▼─────────────────────┐    │
│  │        Service Layer                │    │
│  │  - ApiService (HTTP client)         │    │
│  │  - Session management               │    │
│  │  - Cookie storage                   │    │
│  └──────────────┬─────────────────────┘    │
│                 │                            │
│  ┌──────────────▼─────────────────────┐    │
│  │        Data Models                  │    │
│  │  - User                             │    │
│  │  - Organization                     │    │
│  │  - Class                            │    │
│  │  - Discussion                       │    │
│  │  - Resource                         │    │
│  └─────────────────────────────────────┘    │
│                                              │
└─────────────────────────────────────────────┘
```

## 🔐 Authentication Flow

```
┌─────────┐                                      ┌─────────┐
│  User   │                                      │  Server │
└────┬────┘                                      └────┬────┘
     │                                                 │
     │  1. Enter credentials                          │
     │───────────────────────────────────────────────►│
     │                                                 │
     │                                      2. Verify │
     │                                      credentials│
     │                                         in DB   │
     │                                                 │
     │  3. Return session cookie                      │
     │◄───────────────────────────────────────────────│
     │                                                 │
     │  4. Store cookie securely                      │
     │  (flutter_secure_storage)                      │
     │                                                 │
     │  5. Include cookie in all requests             │
     │───────────────────────────────────────────────►│
     │                                                 │
     │  6. Validate session                           │
     │                                                 │
     │  7. Return user data                           │
     │◄───────────────────────────────────────────────│
     │                                                 │
```

## 🗂️ Database Schema (SQLite)

```
┌─────────────┐     ┌──────────────────┐     ┌─────────────┐
│    users    │     │ organization_    │     │organizations│
│             │     │  memberships     │     │             │
├─────────────┤     ├──────────────────┤     ├─────────────┤
│ id          │────►│ user_id          │◄────│ id          │
│ username    │     │ organization_id  │     │ name        │
│ email       │     │ role             │     │ description │
│ password    │     └──────────────────┘     │ location    │
│ user_type   │                              │ is_public   │
└─────────────┘                              └─────────────┘
      │                                             
      │                                             
      │         ┌─────────────┐                     
      │         │   classes   │                     
      │         ├─────────────┤                     
      └────────►│ teacher_id  │                     
                │ name        │                     
                │ subject_id  │                     
                │ grade_level │                     
                └─────────────┘                     
                      │                             
                      │                             
        ┌─────────────┴──────────────┐             
        │                            │             
  ┌─────▼──────┐            ┌────────▼────────┐   
  │ resources  │            │  class_schedule │   
  ├────────────┤            ├─────────────────┤   
  │ class_id   │            │ class_id        │   
  │ title      │            │ title           │   
  │ file_path  │            │ start_time      │   
  └────────────┘            │ end_time        │   
                            └─────────────────┘   
```

## 📡 API Communication

### Request Flow

```
Flutter App                    Flask Server
───────────                    ────────────

1. User Action
   ↓
2. Call ApiService method
   ↓
3. Prepare HTTP request
   - Add session cookie
   - Add headers
   - Format body
   ↓
4. Send HTTP request ──────────────► 5. Receive request
                                     ↓
                                6. Authenticate session
                                     ↓
                                7. Process business logic
                                     ↓
                                8. Query database
                                     ↓
                                9. Format response
                                     ↓
10. Receive response ◄───────────── 11. Send response
    ↓
12. Parse JSON
    ↓
13. Update State (Provider)
    ↓
14. Rebuild UI
```

## 🔄 Development vs Production

### Development Setup
```
┌─────────────┐              ┌──────────────┐
│    Phone    │   USB/WiFi   │     PC       │
│             │◄────────────►│              │
│ Flutter App │              │ Flask:5000   │
│             │              │ SQLite DB    │
└─────────────┘              └──────────────┘

Connection: http://192.168.1.100:5000
Database: SQLite (local file)
Storage: Local filesystem
```

### Production Setup
```
┌─────────────┐              ┌──────────────┐
│  Any Phone  │   Internet   │   Render     │
│             │◄────────────►│              │
│ Flutter App │    HTTPS     │ Flask        │
│             │              │ PostgreSQL   │
└─────────────┘              └──────────────┘

Connection: https://your-app.onrender.com
Database: PostgreSQL (cloud)
Storage: Cloud storage (S3/Cloudinary)
```

## 🛠️ Build & Deploy Pipeline

```
Development                  Testing                 Production
───────────                 ────────                ──────────

flutter run    ────────►   flutter build   ────►   Deploy APK
    ↓                      apk --release            to Store
    ↓                           ↓                       ↓
Hot reload                  Test on phone         Users download
    ↓                           ↓                       ↓
Debug                      Validate APIs          Production use
```

## 📁 File Organization

```
staffroom/
│
├── 🌐 WEB BACKEND
│   ├── web_app.py          # Flask server
│   ├── src/                # Python modules
│   ├── templates/          # HTML templates
│   ├── static/             # CSS/JS files
│   └── uploads/            # User uploads
│
├── 📱 MOBILE APP
│   └── flutter/teacher/
│       ├── lib/            # Dart source code
│       ├── android/        # Android config
│       ├── ios/            # iOS config
│       └── build/          # Build outputs
│
├── 🛠️ SCRIPTS
│   ├── run_mobile_dev.sh   # Auto-setup
│   └── build_apk.sh        # APK builder
│
└── 📚 DOCUMENTATION
    ├── START_HERE.md
    ├── MOBILE_QUICKSTART.md
    ├── API_DOCUMENTATION.md
    └── ARCHITECTURE.md (this file)
```

## 🔑 Key Technologies

### Backend
- **Flask** - Web framework
- **SQLite** - Database (dev)
- **PostgreSQL** - Database (prod)
- **Session** - Authentication

### Frontend (Web)
- **HTML/CSS/JS** - Web UI
- **Jinja2** - Templates

### Mobile
- **Flutter** - UI framework
- **Dart** - Programming language
- **Provider** - State management
- **HTTP** - API client
- **flutter_secure_storage** - Secure storage

## 🚦 Data Flow Example: Login

```
1. User enters credentials in LoginPage
   ↓
2. LoginPage → AuthProvider.login()
   ↓
3. AuthProvider → ApiService.login()
   ↓
4. ApiService sends: POST /login {username, password}
   ↓
5. Flask authenticates with database
   ↓
6. Flask returns: session cookie
   ↓
7. ApiService stores cookie in secure storage
   ↓
8. AuthProvider updates state (isAuthenticated = true)
   ↓
9. Main app rebuilds → shows HomeScreen
   ↓
10. User sees Dashboard
```

---

**This architecture allows:**
- ✅ Local development (phone + PC)
- ✅ APK distribution
- ✅ Cloud deployment
- ✅ Scalable backend
- ✅ Secure authentication
- ✅ Cross-platform mobile app
