# StaffRoom Web Version

A modern web application version of StaffRoom built with Flask and Bootstrap 5.

## Features

### 🎯 **Core Features**
- **Modern Web UI**: Responsive design with Bootstrap 5 and custom CSS
- **User Authentication**: Secure login and registration system
- **Class Management**: Create and manage classes by subject and grade
- **Student Management**: Add, edit, and manage student enrollments
- **Subject Management**: 30+ Indian syllabus subjects + custom subjects
- **Grade Organization**: Support for 1st to 12th grade classes
- **Dashboard**: Comprehensive overview with statistics

### 🎨 **Modern UI Features**
- **Responsive Design**: Works on desktop, tablet, and mobile
- **Gradient Backgrounds**: Beautiful color schemes
- **Card-based Layout**: Clean, modern interface
- **Interactive Elements**: Hover effects and smooth transitions
- **Font Awesome Icons**: Professional iconography
- **Bootstrap Components**: Modern UI components

### 🔐 **Security Features**
- **Password Hashing**: Secure password storage with Werkzeug
- **Session Management**: Secure user sessions
- **Access Control**: Role-based permissions
- **Input Validation**: Form validation and sanitization

## Installation & Setup

### Prerequisites
- Python 3.7 or higher
- pip (Python package installer)

### Quick Start

1. **Install Dependencies**:
   ```bash
   pip install -r web_requirements.txt
   ```

2. **Run the Application**:
   ```bash
   python web_app.py
   ```

3. **Access the Application**:
   - Open your browser and go to: `http://localhost:5000`
   - Default admin login: `admin` / `admin123`

## Usage Guide

### **For Administrators**
1. **Login** with admin credentials
2. **Dashboard**: View system statistics
3. **Student Management**: Add and manage students
4. **User Management**: Manage teachers and students
5. **System Overview**: Monitor all activities

### **For Teachers**
1. **Login** with teacher credentials
2. **Class Management**: Create classes by subject and grade
3. **Student Management**: Enroll students in classes
4. **Subject Management**: Add custom subjects (teachers only)
5. **Dashboard**: View teaching statistics

### **For Students**
1. **Login** with student credentials
2. **View Classes**: See enrolled classes and resources
3. **Access Resources**: Download/view materials
4. **Submit Assignments**: Complete assignments

## Web App Features

### **📱 Responsive Design**
- **Mobile-First**: Optimized for mobile devices
- **Tablet Support**: Perfect for tablet usage
- **Desktop Experience**: Full-featured desktop interface
- **Cross-Browser**: Works on all modern browsers

### **🎨 Modern UI Components**
- **Login/Register**: Beautiful authentication forms
- **Dashboard**: Card-based layout with statistics
- **Class Management**: Grid layout with class cards
- **Student Management**: Student cards with avatars
- **Modals**: Interactive popup forms
- **Navigation**: Clean, intuitive navigation

### **⚡ Performance Features**
- **Fast Loading**: Optimized CSS and JavaScript
- **CDN Resources**: Bootstrap and Font Awesome from CDN
- **Efficient Queries**: Optimized database queries
- **Session Management**: Efficient session handling

## API Endpoints

### **Authentication**
- `POST /login` - User login
- `POST /register` - User registration
- `GET /logout` - User logout

### **Dashboard**
- `GET /dashboard` - Main dashboard
- `GET /classes` - Class management
- `GET /students` - Student management

### **API Routes**
- `POST /api/create_class` - Create new class
- `POST /api/enroll_student` - Enroll student in class
- `POST /api/create_user` - Create new user

## Database Schema

The web app uses the same SQLite database schema as the desktop version:

- **users**: User accounts and profiles
- **subjects**: Subject information
- **classes**: Class information with subject and grade
- **class_enrollments**: Student enrollments
- **resources**: Class materials
- **class_schedule**: Calendar events
- **discussions**: Forum discussions

## Deployment

### **Development**
```bash
python web_app.py
```

### **Production**
```bash
# Install gunicorn
pip install gunicorn

# Run with gunicorn
gunicorn -w 4 -b 0.0.0.0:5000 web_app:app
```

### **Docker Deployment**
```dockerfile
FROM python:3.9-slim
WORKDIR /app
COPY requirements.txt .
RUN pip install -r requirements.txt
COPY . .
EXPOSE 5000
CMD ["gunicorn", "-w", "4", "-b", "0.0.0.0:5000", "web_app:app"]
```

## File Structure

```
teacherapp/
├── web_app.py              # Main Flask application
├── web_requirements.txt    # Web app dependencies
├── templates/              # HTML templates
│   ├── login.html         # Login page
│   ├── register.html      # Registration page
│   ├── dashboard.html     # Main dashboard
│   ├── classes.html      # Class management
│   └── students.html     # Student management
└── static/                # Static files (CSS, JS, images)
    ├── css/
    └── js/
```

## Key Differences from Desktop Version

### **✅ Advantages**
- **Cross-Platform**: Works on any device with a browser
- **No Installation**: No need to install Python or dependencies
- **Modern UI**: Beautiful, responsive web interface
- **Easy Deployment**: Can be deployed to cloud platforms
- **Mobile Support**: Native mobile experience
- **Multi-User**: Multiple users can access simultaneously

### **🔄 Same Core Features**
- **Database Schema**: Identical database structure
- **User Management**: Same authentication system
- **Class Management**: Same subject-grade organization
- **Student Management**: Same enrollment system
- **Security**: Same security features

## Future Enhancements

### **Planned Features**
- **Real-time Notifications**: WebSocket support
- **File Upload**: Document and image uploads
- **Calendar Integration**: Full calendar view
- **Mobile App**: React Native mobile app
- **API Documentation**: Swagger/OpenAPI docs
- **Advanced Analytics**: Detailed reporting

### **Technical Improvements**
- **Caching**: Redis caching for better performance
- **Database**: PostgreSQL for production
- **Authentication**: OAuth integration
- **Testing**: Comprehensive test suite
- **CI/CD**: Automated deployment pipeline

## Support

For questions or issues with the web version:
1. Check the console for error messages
2. Verify all dependencies are installed
3. Ensure port 5000 is available
4. Check database permissions

---

**StaffRoom Web Version** - Modern web interface for teacher management! 🌐✨
