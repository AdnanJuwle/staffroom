# 🎓 StaffRoom - Teacher Management Platform

<div align="center">

**A comprehensive teacher management system with web and mobile applications**

[![Flutter](https://img.shields.io/badge/Flutter-02569B?style=for-the-badge&logo=flutter&logoColor=white)](https://flutter.dev)
[![Flask](https://img.shields.io/badge/Flask-000000?style=for-the-badge&logo=flask&logoColor=white)](https://flask.palletsprojects.com/)
[![SQLite](https://img.shields.io/badge/SQLite-07405E?style=for-the-badge&logo=sqlite&logoColor=white)](https://www.sqlite.org/)

</div>

---

## 📋 Overview

StaffRoom is a modern, full-featured educational management platform designed for teachers and educational institutions. It provides a seamless experience across web and mobile platforms for managing classes, students, resources, discussions, and schedules.

### ✨ Key Features

- 🎯 **Organization Management** - Create and manage educational organizations with role-based access control
- 📚 **Class Management** - Organize classes by subject and grade (1st-12th)
- 👥 **Student Management** - Track student enrollments and progress
- 💬 **Discussion Forums** - Organization-wide and global discussions
- 📁 **Resource Library** - Upload and share educational materials
- 📅 **Schedule Management** - Class schedules and calendar events
- 👤 **Profile Management** - Customizable user profiles with photos
- 🏢 **Organization Branding** - Custom logos and banners for organizations
- 🔐 **Role-Based Access** - Owner, Admin, and Member roles with appropriate permissions

---

## 🚀 Quick Start

### Prerequisites

- **Python 3.7+** (for backend)
- **Flutter 3.8.1+** (for mobile app)
- **Git**

### Backend Setup

1. **Clone the repository:**
   ```bash
   git clone https://github.com/yourusername/staffroom.git
   cd staffroom
   ```

2. **Install Python dependencies:**
   ```bash
   pip install -r web_requirements.txt
   ```

3. **Start the server:**
   ```bash
   chmod +x start.sh
   ./start.sh
   ```

4. **Access the web app:**
   - Open your browser: `http://localhost:5000`
   - Default credentials: `teacher` / `teacher123`

### Mobile App Setup

1. **Navigate to Flutter directory:**
   ```bash
   cd flutter/teacher
   ```

2. **Install Flutter dependencies:**
   ```bash
   flutter pub get
   ```

3. **Update API endpoint:**
   
   Edit `lib/services/api_service.dart`:
   ```dart
   // For WiFi testing on physical device
   final String baseUrl = 'http://YOUR_IP:5000';
   
   // For Android emulator
   final String baseUrl = 'http://10.0.2.2:5000';
   ```

4. **Build and install APK:**
   ```bash
   flutter build apk --release
   ```
   
   The APK will be at: `build/app/outputs/flutter-apk/app-release.apk`

### Testing Credentials

**Online Mode (requires server connection):**
- Username: `teacher`
- Password: `teacher123`

**Offline Mode (for testing without server):**
- Username: `admin`
- Password: `admin123`

---

## 📱 Mobile App Features

### 🔐 Authentication
- ✅ Secure login and registration
- ✅ "Remember Me" functionality
- ✅ Offline demo mode for testing
- ✅ Auto-login on app restart

### 🏢 Organization Management
- ✅ Create new organizations (auto-assigned as Owner)
- ✅ Join existing organizations
- ✅ View organization details with banner/logo
- ✅ Upload custom organization logo and banner
- ✅ Edit organization details (Owner/Admin only)
- ✅ View all organization members with roles
- ✅ Manage member roles (Owner/Admin only)
- ✅ Remove members (Owner/Admin only)
- ✅ Role hierarchy: Owner > Admin > Member

### 👤 Profile Management
- ✅ Edit first name, last name, phone number, and bio
- ✅ Upload profile photo
- ✅ View profile with custom avatar
- ✅ Beautiful profile UI with gradient header

### 📚 Classes
- ✅ View all classes
- ✅ Create new classes with subject and grade
- ✅ View class details
- ✅ Navigate to class-specific resources

### 👥 Students
- ✅ View all students in organization
- ✅ Add new students to classes
- ✅ View student profiles

### 📁 Resources
- ✅ View all resources by class
- ✅ Upload new resources (PDF, images, documents)
- ✅ Download resources
- ✅ Delete resources

### 💬 Discussions
- ✅ Organization discussions
- ✅ Global discussions (across all organizations)
- ✅ Create new discussion threads
- ✅ Reply to discussions
- ✅ View full discussion threads

### 📅 Schedule
- ✅ View class schedules
- ✅ Create schedule events
- ✅ Calendar view integration

### 🎨 UI/UX Features
- ✅ Beautiful gradient theme matching web app
- ✅ Side navigation drawer on all pages
- ✅ Clickable dashboard statistics
- ✅ Responsive design for all phone sizes
- ✅ Image layering (banner + logo)
- ✅ Loading states and error handling
- ✅ Bottom sheets for actions
- ✅ Confirmation dialogs for destructive actions

---

## 🌐 Web App Features

### 🎯 Core Functionality
- **Modern Responsive UI** - Bootstrap 5 with custom CSS
- **Dashboard** - Comprehensive statistics and quick actions
- **Class Management** - Create, view, and manage classes
- **Student Management** - Add, enroll, and track students
- **User Management** - Admin controls for user accounts
- **Organization System** - Multi-tenant organization support
- **Discussion Forums** - Threaded discussions with replies
- **Resource Library** - File upload and management
- **Schedule System** - Calendar and event management

### 🔐 Security
- Password hashing with Werkzeug
- Secure session management
- Role-based access control
- Input validation and sanitization
- CORS support for mobile apps

---

## 🏗️ Architecture

### Backend (Flask)
```
staffroom/
├── web_app.py              # Main Flask application
├── src/
│   ├── auth.py            # Authentication logic
│   ├── database.py        # Database management
│   └── gui/               # Desktop GUI (legacy)
├── templates/             # HTML templates
│   ├── login.html
│   ├── dashboard.html
│   ├── classes.html
│   ├── students.html
│   ├── organizations.html
│   ├── discussions.html
│   ├── resources.html
│   └── schedule.html
├── static/
│   ├── css/              # Custom stylesheets
│   └── js/               # JavaScript files
├── uploads/
│   ├── profiles/         # User profile photos
│   ├── logos/           # Organization logos
│   ├── banners/         # Organization banners
│   └── resources/       # Educational materials
└── teacher_app_web.db   # SQLite database
```

### Mobile App (Flutter)
```
flutter/teacher/
├── lib/
│   ├── main.dart                    # App entry point
│   ├── models/                      # Data models
│   │   ├── user.dart
│   │   ├── organization.dart
│   │   ├── class.dart
│   │   ├── student.dart
│   │   ├── discussion.dart
│   │   ├── resource.dart
│   │   └── subject.dart
│   ├── providers/                   # State management
│   │   └── auth_provider.dart
│   ├── services/                    # API services
│   │   └── api_service.dart
│   ├── pages/                       # App screens
│   │   ├── login_page.dart
│   │   ├── dashboard_page.dart
│   │   ├── classes_page.dart
│   │   ├── students_page.dart
│   │   ├── organizations_page.dart
│   │   ├── organization_detail_page.dart
│   │   ├── discussions_page.dart
│   │   ├── resources_page.dart
│   │   ├── schedule_page.dart
│   │   └── profile_page.dart
│   └── widgets/                     # Reusable widgets
│       └── app_drawer.dart
└── pubspec.yaml                     # Dependencies
```

### Database Schema
- **users** - User accounts with profiles
- **organizations** - Educational institutions
- **organization_memberships** - User-organization relationships with roles
- **subjects** - Subject catalog
- **classes** - Class information
- **class_enrollments** - Student enrollments
- **resources** - Educational materials
- **class_schedule** - Calendar events
- **discussions** - Discussion threads
- **discussion_replies** - Discussion responses

---

## 🔌 API Endpoints

### Authentication
- `POST /api/login` - Mobile login (returns JSON)
- `POST /api/register` - User registration
- `GET /logout` - Logout

### Profile
- `GET /api/get_profile` - Get user profile
- `POST /api/update_profile` - Update profile (with photo upload)

### Organizations
- `GET /api/get_organizations` - List all organizations
- `POST /api/create_organization` - Create new organization
- `POST /api/join_organization/<id>` - Join organization
- `POST /api/update_organization` - Update organization (with logo/banner upload)
- `GET /api/get_organization_members/<id>` - Get members list
- `POST /api/update_member_role` - Change member role
- `POST /api/remove_member` - Remove member

### Classes
- `GET /api/get_classes` - List classes
- `POST /api/create_class` - Create class

### Students
- `GET /api/get_students` - List students
- `POST /api/create_student` - Add student

### Resources
- `GET /api/get_resources` - List resources
- `POST /api/create_resource` - Upload resource

### Discussions
- `GET /api/get_discussions` - Organization discussions
- `GET /api/get_global_discussions` - Global discussions
- `POST /api/create_discussion` - Create discussion

### Schedule
- `GET /api/get_schedule` - Get schedule
- `POST /api/create_schedule_event` - Create event

### Static Files
- `GET /uploads/<path>` - Serve uploaded files

---

## 🛠️ Technologies Used

### Backend
- **Flask** - Python web framework
- **SQLite** - Database
- **Werkzeug** - Security utilities
- **Flask-CORS** - Cross-origin resource sharing

### Mobile App
- **Flutter/Dart** - Cross-platform mobile framework
- **Provider** - State management
- **HTTP** - API communication
- **Shared Preferences** - Local storage
- **Image Picker** - Photo selection
- **Intl** - Date formatting

### Web Frontend
- **Bootstrap 5** - UI framework
- **Font Awesome** - Icons
- **Custom CSS** - Gradient themes

---

## 📦 Dependencies

### Backend (`web_requirements.txt`)
```
Flask==3.0.0
Werkzeug==3.0.1
flask-cors==4.0.0
```

### Mobile (`pubspec.yaml`)
```yaml
http: ^1.2.0
provider: ^6.1.1
shared_preferences: ^2.2.2
image_picker: ^1.0.4
intl: ^0.19.0
```

---

## 🚢 Deployment

### Web App Deployment

**Option 1: Render.com**
```bash
# Already configured with render.yaml
git push origin main
# Connect repository to Render
```

**Option 2: Heroku**
```bash
heroku create staffroom-app
git push heroku main
```

**Option 3: Docker**
```dockerfile
FROM python:3.9-slim
WORKDIR /app
COPY web_requirements.txt .
RUN pip install -r web_requirements.txt
COPY . .
EXPOSE 5000
CMD ["python", "web_app.py"]
```

### Mobile App Deployment

**Android (Google Play Store):**
1. Create keystore for signing
2. Update `android/key.properties`
3. Build release APK: `flutter build apk --release`
4. Upload to Google Play Console

**iOS (App Store):**
1. Open in Xcode
2. Configure signing
3. Archive and upload to App Store Connect

---

## 🎯 Roadmap

### Completed ✅
- [x] Web application with full CRUD
- [x] Mobile app with all core features
- [x] Organization management system
- [x] Role-based access control
- [x] Profile and organization photo uploads
- [x] Discussion forums
- [x] Resource management
- [x] Schedule system
- [x] Remember Me functionality
- [x] Offline demo mode

### Upcoming 🚀
- [ ] Real-time notifications
- [ ] Push notifications for mobile
- [ ] Dark mode
- [ ] Attendance tracking
- [ ] Gradebook system
- [ ] Advanced analytics dashboard
- [ ] Export reports (PDF/Excel)
- [ ] Email notifications
- [ ] Calendar sync (Google Calendar)
- [ ] Video conferencing integration
- [ ] Advanced search and filters
- [ ] Multi-language support

---

## 🤝 Contributing

Contributions are welcome! Please follow these steps:

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

---

## 🐛 Troubleshooting

### Mobile App Issues

**Connection Error on Physical Device:**
- Ensure phone and computer are on the same WiFi network
- Update `baseUrl` in `api_service.dart` with your computer's IP address
- Check firewall settings

**"Operation not permitted" error:**
- Already fixed with `android:usesCleartextTraffic="true"` in AndroidManifest.xml

**Images not displaying:**
- Ensure Flask server is running
- Check `/uploads` route is accessible
- Verify image paths in database

**Remember Me not working:**
- Clear app data and reinstall
- Already fixed in latest version

### Backend Issues

**Port 5000 already in use:**
```bash
# Kill existing Flask processes
pkill -9 -f "python3 web_app.py"
./start.sh
```

**Database locked:**
```bash
# Stop all Flask instances
# Delete database and restart (will recreate with default users)
```

---

## 📄 License

This project is open source and available for educational purposes.

---

## 👥 Authors

- **Your Name** - Initial work and development

---

## 🙏 Acknowledgments

- Flutter team for the amazing framework
- Flask community for the excellent web framework
- Bootstrap team for the beautiful UI components
- All contributors and testers

---

## 📞 Support

For issues, questions, or suggestions:
- Open an issue on GitHub
- Contact: [your-email@example.com]

---

<div align="center">

**Built with ❤️ for educators**

[⬆ Back to Top](#-staffroom---teacher-management-platform)

</div>
