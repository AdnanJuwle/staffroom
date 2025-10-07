# 🔌 StaffRoom API Documentation

Complete API reference for the StaffRoom mobile and web applications.

---

## 🌐 Base URL

```
Local Development: http://localhost:5000
Network (Phone):    http://YOUR_PC_IP:5000
Production:         https://your-app.onrender.com
```

---

## 🔐 Authentication

All authenticated endpoints require a session cookie. Sessions are managed via Flask's session management.

### Session Flow
1. User logs in → receives session cookie
2. Cookie automatically included in subsequent requests
3. Session persists until logout or expiry

---

## 📋 API Endpoints

### Authentication Endpoints

#### POST `/login`
Login user and create session.

**Request (Form Data):**
```
username: string (required)
password: string (required)
```

**Response:**
- Success: `302 Redirect` to `/dashboard` + session cookie
- Failure: `200` with error message

**Example (Flutter):**
```dart
final response = await http.post(
  Uri.parse('$baseUrl/login'),
  headers: {'Content-Type': 'application/x-www-form-urlencoded'},
  body: {
    'username': 'teacher',
    'password': 'teacher123',
  },
);
```

---

#### POST `/register`
Register new user account.

**Request (Form Data):**
```
username: string (required, unique)
email: string (required, unique)
password: string (required, min 6 chars)
first_name: string (required)
last_name: string (required)
user_type: string (required: 'teacher' | 'student')
```

**Response:**
- Success: `302 Redirect` to `/login`
- Failure: `200` with error message

**Example:**
```dart
await http.post(
  Uri.parse('$baseUrl/register'),
  body: {
    'username': 'john_doe',
    'email': 'john@example.com',
    'password': 'secure123',
    'first_name': 'John',
    'last_name': 'Doe',
    'user_type': 'teacher',
  },
);
```

---

#### GET `/logout`
Logout user and clear session.

**Response:** `302 Redirect` to `/login`

---

### Dashboard & User Info

#### GET `/dashboard`
Get user dashboard data (requires authentication).

**Response:** HTML page or session data

---

### Classes Management

#### POST `/api/create_class`
Create a new class (teachers only).

**Request (JSON):**
```json
{
  "name": "Physics 101",
  "description": "Introduction to Physics",
  "subject_id": 3,
  "grade_level": 10
}
```

**Response:**
```json
{
  "success": true,
  "class_id": 123
}
```

**Example:**
```dart
final response = await apiService.post('/api/create_class', {
  'name': 'Physics 101',
  'description': 'Introduction to Physics',
  'subject_id': 3,
  'grade_level': 10,
});
```

---

#### GET `/classes`
Get all classes for logged-in teacher.

**Response:** HTML page with classes data

---

### Students Management

#### POST `/api/create_user`
Create new user (admin/teacher only).

**Request (JSON):**
```json
{
  "username": "student1",
  "email": "student1@example.com",
  "password": "password123",
  "first_name": "Jane",
  "last_name": "Smith",
  "user_type": "student"
}
```

**Response:**
```json
{
  "success": true
}
```

---

#### POST `/api/enroll_student`
Enroll student in class (admin/teacher only).

**Request (JSON):**
```json
{
  "class_id": 123,
  "student_id": 456
}
```

**Response:**
```json
{
  "success": true
}
```

---

#### GET `/students`
Get all students (admin/teacher only).

**Response:** HTML page with students list

---

### Organizations

#### GET `/organizations`
Get all organizations.

**Response:** HTML page with organizations list

---

#### POST `/api/create_organization`
Create new organization (teachers only).

**Request (Multipart Form Data):**
```
name: string (required)
description: string
about: string
location: string
contact_email: string
contact_phone: string
website: string
is_public: boolean
discussion_privacy: 'public' | 'private'
logo: file (optional)
```

**Response:**
```json
{
  "success": true,
  "organization_id": 789
}
```

**Example:**
```dart
final request = http.MultipartRequest(
  'POST',
  Uri.parse('$baseUrl/api/create_organization'),
);

request.fields['name'] = 'Springfield High School';
request.fields['description'] = 'A great school';
request.fields['is_public'] = 'on';

if (logoFile != null) {
  request.files.add(
    await http.MultipartFile.fromPath('logo', logoFile.path),
  );
}

final response = await request.send();
```

---

#### POST `/api/join_organization/<org_id>`
Join an organization.

**Response:**
```json
{
  "success": true,
  "message": "Successfully joined Organization Name",
  "switched": false
}
```

---

#### GET `/organization/<org_id>`
Get organization details.

**Response:** HTML page with organization details

---

### Discussions

#### POST `/api/create_discussion`
Create new discussion.

**Request (Multipart Form Data or JSON):**
```json
{
  "title": "Discussion Title",
  "content": "Discussion content here...",
  "category": "general"
}
```

With files (Form Data):
```
title: string
content: string
category: string
files: file[] (optional)
```

**Response:**
```json
{
  "success": true,
  "discussion_id": 101,
  "uploaded_files": [
    {
      "id": 1,
      "filename": "document.pdf",
      "file_type": "pdf",
      "file_size": 1024000
    }
  ]
}
```

---

#### POST `/api/add_reply`
Add reply to discussion.

**Request (Multipart Form Data or JSON):**
```json
{
  "discussion_id": 101,
  "content": "This is my reply..."
}
```

**Response:**
```json
{
  "success": true,
  "reply_id": 202
}
```

---

#### GET `/api/get_discussion_details/<discussion_id>`
Get discussion with replies.

**Response:**
```json
{
  "discussion": {
    "id": 101,
    "title": "Discussion Title",
    "content": "Content...",
    "author_id": 1,
    "first_name": "John",
    "last_name": "Doe",
    "created_at": "2025-10-07T10:30:00",
    "attachments": [...]
  },
  "replies": [
    {
      "id": 202,
      "content": "Reply content...",
      "author_id": 2,
      "first_name": "Jane",
      "created_at": "2025-10-07T11:00:00",
      "attachments": [...]
    }
  ]
}
```

---

#### GET `/discussions`
Get organization discussions.

**Response:** HTML page with discussions

---

### Global Discussions

#### POST `/api/create_global_discussion`
Create global discussion (cross-organization).

**Request (JSON):**
```json
{
  "title": "Global Discussion",
  "content": "Content visible to all organizations...",
  "category": "general",
  "tags": "education,teaching"
}
```

**Response:**
```json
{
  "success": true,
  "discussion_id": 301
}
```

---

#### POST `/api/add_global_reply`
Reply to global discussion.

**Request (JSON):**
```json
{
  "discussion_id": 301,
  "content": "My global reply..."
}
```

**Response:**
```json
{
  "success": true,
  "reply_id": 302
}
```

---

#### GET `/global-discussions`
Get global discussions.

**Query Parameters:**
- `category` (optional): Filter by category

**Response:** HTML page with global discussions

---

### Resources

#### POST `/api/create_resource`
Upload resource/file.

**Request (Multipart Form Data):**
```
title: string (required)
description: string
resource_type: 'note' | 'video' | 'pdf' | 'photo' | 'document' | 'link' | 'other'
grade_level: number (1-12)
subject_id: number
class_id: number
external_url: string (for links)
tags: string (comma-separated)
is_public: boolean
file: file (optional)
```

**Response:**
```json
{
  "success": true,
  "resource_id": 401
}
```

**Example:**
```dart
final request = http.MultipartRequest(
  'POST',
  Uri.parse('$baseUrl/api/create_resource'),
);

request.fields['title'] = 'Chapter 1 Notes';
request.fields['description'] = 'Introduction notes';
request.fields['resource_type'] = 'pdf';
request.fields['grade_level'] = '10';

request.files.add(
  await http.MultipartFile.fromPath('file', pdfFile.path),
);

final response = await request.send();
```

---

#### POST `/api/delete_resource/<resource_id>`
Delete a resource.

**Response:**
```json
{
  "success": true
}
```

---

#### GET `/resources`
Get resources for current organization.

**Query Parameters:**
- `grade` (optional): Filter by grade level
- `subject` (optional): Filter by subject ID
- `type` (optional): Filter by resource type

**Response:** HTML page with resources

---

### Schedule/Calendar

#### POST `/api/create_schedule_event`
Create schedule event.

**Request (JSON):**
```json
{
  "class_id": 123,
  "title": "Physics Lecture",
  "description": "Chapter 3 - Motion",
  "start_time": "2025-10-10T10:00:00",
  "end_time": "2025-10-10T11:00:00"
}
```

**Response:**
```json
{
  "success": true,
  "event_id": 501
}
```

---

#### GET `/schedule`
Get schedule events.

**Response:** HTML page with calendar

---

### File Downloads

#### GET `/download/<filename>`
Download uploaded file.

**Response:** File download

---

## 🔒 Error Responses

### Unauthorized (401)
```json
{
  "error": "Not authenticated"
}
```

### Forbidden (403)
```json
{
  "error": "Access denied"
}
```

### Bad Request (400)
```json
{
  "error": "Missing required field: title"
}
```

### Server Error (500)
```json
{
  "error": "Failed to create resource: Database error"
}
```

---

## 📊 Data Models

### User
```json
{
  "id": 1,
  "username": "teacher",
  "email": "teacher@example.com",
  "first_name": "John",
  "last_name": "Doe",
  "user_type": "teacher",
  "is_active": 1
}
```

### Class
```json
{
  "id": 123,
  "name": "Physics 101",
  "description": "Introduction to Physics",
  "subject_id": 3,
  "subject_name": "Physics",
  "grade_level": 10,
  "teacher_id": 1,
  "created_at": "2025-10-07T10:00:00"
}
```

### Organization
```json
{
  "id": 789,
  "name": "Springfield High School",
  "description": "A great school",
  "location": "Springfield",
  "contact_email": "info@springfield.edu",
  "is_public": true,
  "discussion_privacy": "public",
  "created_at": "2025-10-01T09:00:00"
}
```

### Subject
```json
{
  "id": 3,
  "name": "Physics",
  "description": "Physical sciences",
  "is_custom": false
}
```

---

## 🔧 Flutter Integration Examples

### Setup API Service

```dart
// lib/services/api_service.dart
class ApiService {
  final String baseUrl = 'http://YOUR_PC_IP:5000';
  
  Future<Map<String, dynamic>> login(String username, String password) async {
    final response = await http.post(
      Uri.parse('$baseUrl/login'),
      headers: {'Content-Type': 'application/x-www-form-urlencoded'},
      body: {'username': username, 'password': password},
    );
    
    // Extract session cookie
    final cookie = response.headers['set-cookie'];
    await saveSessionCookie(cookie);
    
    return {'success': response.statusCode == 200};
  }
  
  Future<dynamic> get(String endpoint) async {
    final cookie = await getSessionCookie();
    final response = await http.get(
      Uri.parse('$baseUrl$endpoint'),
      headers: {'Cookie': cookie ?? ''},
    );
    return json.decode(response.body);
  }
  
  Future<dynamic> post(String endpoint, Map<String, dynamic> data) async {
    final cookie = await getSessionCookie();
    final response = await http.post(
      Uri.parse('$baseUrl$endpoint'),
      headers: {
        'Content-Type': 'application/json',
        'Cookie': cookie ?? '',
      },
      body: json.encode(data),
    );
    return json.decode(response.body);
  }
}
```

---

## 🧪 Testing APIs

### Using cURL

```bash
# Login
curl -X POST http://localhost:5000/login \
  -d "username=teacher&password=teacher123" \
  -c cookies.txt

# Create class (with session)
curl -X POST http://localhost:5000/api/create_class \
  -H "Content-Type: application/json" \
  -b cookies.txt \
  -d '{"name":"Math 101","description":"Algebra","subject_id":1,"grade_level":9}'

# Get discussions
curl http://localhost:5000/discussions -b cookies.txt
```

### Using Postman

1. **Login:**
   - POST `http://localhost:5000/login`
   - Body → x-www-form-urlencoded
   - Add `username` and `password`
   - Save cookies automatically

2. **Authenticated Requests:**
   - Postman will include cookies automatically
   - Or manually add `Cookie` header

---

## 📝 Notes

- All authenticated endpoints require session cookie
- File uploads use `multipart/form-data`
- JSON endpoints use `application/json`
- Dates in ISO 8601 format
- Session expires on logout or server restart
- Database stores timestamps in SQLite datetime format

---

## 🔗 Related Documentation

- [Mobile Setup Guide](flutter/teacher/SETUP_GUIDE.md)
- [Quick Start](MOBILE_QUICKSTART.md)
- [Web README](WEB_README.md)
- [Deployment Guide](DEPLOYMENT_GUIDE.md)

