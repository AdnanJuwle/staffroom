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
- 🏷️ **Organization Tags** - Unique tags (@organizationname) for easy searching and identification
- 🔍 **Organization Search** - Search organizations by name, tag, or description
- 📚 **Class Management** - Organize classes by subject and grade (1st-12th)
- 👥 **Student Management** - Track student enrollments, attendance, and progress
- 📊 **Attendance System** - Mark and track student attendance with percentage calculations
- 📝 **Assignment System** - Create and manage assignments with due dates and categories
- 🎓 **Class Allocation** - Enroll students in specific classes with easy management
- 📢 **Announcements** - Create priority-based announcements (low, normal, high, urgent) with pinning support
- 📤 **Assignment Submissions** - Students can submit assignments with files/notes, teachers can grade and provide feedback
- 💬 **Discussion Forums** - Organization-wide and global discussions with reply system
- 🤖 **AI Summarization** - AI-powered content summarization for resources and discussions
- 📁 **Resource Library** - Upload and categorize educational materials (assignments, notes, test papers, practice questions)
- 📅 **Schedule Management** - Class schedules and calendar events (teacher-only)
- 👤 **Profile Management** - Customizable user profiles with photos
- 🏢 **Organization Branding** - Custom logos and banners for organizations
- 🌙 **Dark Mode** - Beautiful dark theme with persistent preference
- 🔐 **Role-Based Access** - Owner, Admin, Teacher, and Student roles with granular permissions
- 🔔 **Notification System** - Real-time notifications for join requests and approvals

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

**Teacher Account:**
- Username: `teacher`
- Password: `teacher123`
- Role: Can create classes, manage students, mark attendance

**Student Account:**
- Username: `student`
- Password: `student123`
- Role: View-only access, can edit own profile

**Demo Students:**
- Usernames: `student1` through `student10`
- Password: `student123` (for all)
- Auto-created for testing attendance and enrollment features

---

## 📱 Mobile App Features

### 🔐 Authentication
- ✅ Secure login and registration
- ✅ "Remember Me" functionality
- ✅ Offline demo mode for testing
- ✅ Auto-login on app restart

### 🏢 Organization Management
- ✅ Create new organizations (auto-assigned as Owner)
- ✅ Join organization via request (requires admin approval)
- ✅ View organization details with banner/logo overlay
- ✅ Upload custom organization logo and banner
- ✅ Edit organization details (Owner/Admin only)
- ✅ View all organization members with roles
- ✅ Manage member roles (Owner/Admin only)
- ✅ Remove members (Owner/Admin only)
- ✅ Role hierarchy: Owner > Admin > Teacher > Student
- ✅ Notification bell with pending join request count
- ✅ Approve/Reject join requests (Owner/Admin only)
- ✅ Auto-delete empty organizations

### 👤 Profile Management
- ✅ Edit first name, last name, phone number, and bio
- ✅ Upload profile photo
- ✅ View profile with custom avatar
- ✅ Beautiful profile UI with gradient header

### 📚 Classes
- ✅ View organization classes (teachers see all, students see enrolled only)
- ✅ Create new classes with subject and grade (teachers only)
- ✅ Manage student enrollments with checkbox interface
- ✅ View enrolled student count per class
- ✅ Organization-wide class visibility

### 👥 Students
- ✅ View all students in organization
- ✅ Create new student accounts (teachers only)
- ✅ View detailed student information cards
- ✅ Track attendance with percentage badges
- ✅ Edit student information (teachers can edit any, students only their own)
- ✅ Mark attendance (present/absent/late/excused)
- ✅ View attendance history and statistics
- ✅ Filter students by organization membership

### 📁 Resources
- ✅ View all resources with category filters
- ✅ Filter by: All, Assignments, Notes, Test Papers, Practice Questions, Other
- ✅ Upload new resources with categories (teachers only)
- ✅ Add assignments with due dates
- ✅ Download resources
- ✅ Delete resources (teachers only)
- ✅ Scrollable filter chips for easy navigation

### 💬 Discussions
- ✅ Organization discussions (members only)
- ✅ Global discussions (across all organizations)
- ✅ Create new discussion threads (teachers only)
- ✅ Reply to discussions (all users)
- ✅ View full discussion threads
- ✅ Permission-based discussion creation

### 📅 Schedule
- ✅ View class schedules (teachers only)
- ✅ Create schedule events
- ✅ Calendar view integration
- ✅ Hidden from students for focused experience

### 🎨 UI/UX Features
- ✅ Beautiful gradient theme matching web app
- ✅ Side navigation drawer on all pages
- ✅ Clickable dashboard statistics
- ✅ Responsive design for all phone sizes
- ✅ Image layering (banner + logo with perfect positioning)
- ✅ Loading states and error handling
- ✅ Bottom sheets for actions
- ✅ Confirmation dialogs for destructive actions
- ✅ Color-coded role badges (Owner/Admin/Teacher/Student)
- ✅ Attendance percentage badges with color indicators
- ✅ Scrollable filter chips for resource categories
- ✅ Real-time enrollment management with checkboxes
- ✅ Student info cards with detailed information

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
- **users** - User accounts with profiles, photos, and grades
- **organizations** - Educational institutions with logos and banners
- **organization_memberships** - User-organization relationships with roles (owner/admin/teacher/student)
- **organization_join_requests** - Pending join requests requiring approval
- **subjects** - Subject catalog
- **classes** - Class information with organization linkage
- **class_students** - Student class enrollments
- **attendance** - Daily attendance records with status tracking
- **resources** - Educational materials with categories and due dates
- **class_schedule** - Calendar events
- **discussions** - Discussion threads (organization and global)
- **discussion_replies** - Discussion responses
- **discussion_attachments** - File attachments for discussions
- **reply_attachments** - File attachments for replies

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
- `POST /api/join_organization/<id>` - Request to join organization
- `POST /api/update_organization` - Update organization (with logo/banner upload)
- `GET /api/get_organization_members/<id>` - Get members list
- `POST /api/update_member_role` - Change member role
- `POST /api/remove_member` - Remove member
- `GET /api/get_join_requests` - Get pending join requests
- `POST /api/approve_join_request` - Approve join request
- `POST /api/reject_join_request` - Reject join request
- `GET /api/get_notification_count` - Get pending request count

### Classes
- `GET /api/get_classes` - List classes (filtered by role)
- `POST /api/create_class` - Create class
- `POST /api/enroll_student` - Enroll student in class
- `POST /api/unenroll_student` - Remove student from class
- `GET /api/get_class_students/<id>` - Get enrolled students
- `GET /api/get_student_classes/<id>` - Get student's classes

### Students
- `GET /api/get_students` - List students (organization-filtered)
- `POST /api/create_student` - Add student
- `POST /api/update_student` - Update student information
- `POST /api/mark_attendance` - Mark student attendance
- `GET /api/get_attendance` - Get attendance records
- `GET /api/get_attendance_percentage` - Get attendance statistics

### Resources
- `GET /api/get_resources` - List resources (with category filter)
- `POST /api/create_resource` - Upload resource with category
- `DELETE /api/delete_resource/<id>` - Delete resource

### Discussions
- `GET /api/get_discussions` - Organization discussions
- `GET /api/get_global_discussions` - Global discussions
- `POST /api/create_discussion` - Create discussion (teachers only)
- `POST /api/add_reply` - Add reply to discussion
- `GET /api/get_discussion_details/<id>` - Get discussion with replies

### Schedule
- `GET /api/get_schedule` - Get schedule (teachers only)
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
- [x] Organization management system with approval workflow
- [x] Role-based access control (Owner/Admin/Teacher/Student)
- [x] Profile and organization photo uploads
- [x] Discussion forums with permissions
- [x] Resource management with categories
- [x] Assignment system with due dates
- [x] Attendance tracking system
- [x] Class allocation and enrollment
- [x] Schedule system (teacher-only)
- [x] Remember Me functionality
- [x] Notification system for join requests
- [x] Student permission restrictions
- [x] Organization-filtered data access

### Upcoming 🚀
- [ ] Student categorization by grade
- [ ] Gradebook system with marks
- [ ] Advanced analytics dashboard
- [ ] Export reports (PDF/Excel)
- [ ] Email notifications
- [ ] Push notifications for mobile
- [ ] Dark mode
- [ ] Calendar sync (Google Calendar)
- [ ] Video conferencing integration
- [ ] Advanced search and filters
- [ ] Multi-language support
- [ ] Parent portal access

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

- **Adnan Juwle** - Initial development, backend architecture, deployment, and core functionality
- **Naveen Kalage** - Flutter mobile app design and UI/UX implementation
- **Siddhant Khobaragade** - Cybersecurity, app security, and secure authentication implementation

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
- Contact: adnanjuwle1@gmail.com

---

<div align="center">

**Built with ❤️ for educators**

[⬆ Back to Top](#-staffroom---teacher-management-platform)

</div>
