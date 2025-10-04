"""
Database management module for TeacherApp
Handles all database operations using SQLite
"""

import sqlite3
import hashlib
from datetime import datetime
from typing import List, Dict, Optional, Tuple

class DatabaseManager:
    def __init__(self, db_path: str = "teacher_app.db"):
        self.db_path = db_path
        self.connection = None
        
    def connect(self):
        """Establish database connection"""
        self.connection = sqlite3.connect(self.db_path)
        self.connection.row_factory = sqlite3.Row
        
    def disconnect(self):
        """Close database connection"""
        if self.connection:
            self.connection.close()
            
    def initialize_database(self):
        """Create all necessary tables"""
        self.connect()
        
        # Users table (teachers and students)
        self.connection.execute("""
            CREATE TABLE IF NOT EXISTS users (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                username TEXT UNIQUE NOT NULL,
                email TEXT UNIQUE NOT NULL,
                password_hash TEXT NOT NULL,
                first_name TEXT NOT NULL,
                last_name TEXT NOT NULL,
                user_type TEXT NOT NULL CHECK (user_type IN ('teacher', 'student', 'admin')),
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                is_active BOOLEAN DEFAULT 1
            )
        """)
        
        # Subjects table
        self.connection.execute("""
            CREATE TABLE IF NOT EXISTS subjects (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT UNIQUE NOT NULL,
                description TEXT,
                is_custom BOOLEAN DEFAULT 0,
                created_by INTEGER,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (created_by) REFERENCES users (id)
            )
        """)
        
        # Classes table (updated with subject and grade)
        self.connection.execute("""
            CREATE TABLE IF NOT EXISTS classes (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL,
                description TEXT,
                subject_id INTEGER NOT NULL,
                grade_level INTEGER NOT NULL CHECK (grade_level BETWEEN 1 AND 12),
                teacher_id INTEGER NOT NULL,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (subject_id) REFERENCES subjects (id),
                FOREIGN KEY (teacher_id) REFERENCES users (id)
            )
        """)
        
        # Class enrollments
        self.connection.execute("""
            CREATE TABLE IF NOT EXISTS class_enrollments (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                class_id INTEGER NOT NULL,
                student_id INTEGER NOT NULL,
                enrolled_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (class_id) REFERENCES classes (id),
                FOREIGN KEY (student_id) REFERENCES users (id),
                UNIQUE(class_id, student_id)
            )
        """)
        
        # Resources table
        self.connection.execute("""
            CREATE TABLE IF NOT EXISTS resources (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                title TEXT NOT NULL,
                description TEXT,
                resource_type TEXT NOT NULL CHECK (resource_type IN ('document', 'link', 'assignment', 'note')),
                content TEXT,
                file_path TEXT,
                class_id INTEGER NOT NULL,
                created_by INTEGER NOT NULL,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (class_id) REFERENCES classes (id),
                FOREIGN KEY (created_by) REFERENCES users (id)
            )
        """)
        
        # Teacher hierarchy (for managing other teachers)
        self.connection.execute("""
            CREATE TABLE IF NOT EXISTS teacher_hierarchy (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                supervisor_id INTEGER NOT NULL,
                subordinate_id INTEGER NOT NULL,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (supervisor_id) REFERENCES users (id),
                FOREIGN KEY (subordinate_id) REFERENCES users (id),
                UNIQUE(supervisor_id, subordinate_id)
            )
        """)
        
        # Discussion forum
        self.connection.execute("""
            CREATE TABLE IF NOT EXISTS discussions (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                title TEXT NOT NULL,
                content TEXT NOT NULL,
                author_id INTEGER NOT NULL,
                category TEXT DEFAULT 'general',
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (author_id) REFERENCES users (id)
            )
        """)
        
        # Discussion replies
        self.connection.execute("""
            CREATE TABLE IF NOT EXISTS discussion_replies (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                discussion_id INTEGER NOT NULL,
                author_id INTEGER NOT NULL,
                content TEXT NOT NULL,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (discussion_id) REFERENCES discussions (id),
                FOREIGN KEY (author_id) REFERENCES users (id)
            )
        """)
        
        # Assignments
        self.connection.execute("""
            CREATE TABLE IF NOT EXISTS assignments (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                title TEXT NOT NULL,
                description TEXT,
                class_id INTEGER NOT NULL,
                due_date TIMESTAMP,
                created_by INTEGER NOT NULL,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (class_id) REFERENCES classes (id),
                FOREIGN KEY (created_by) REFERENCES users (id)
            )
        """)
        
        # Assignment submissions
        self.connection.execute("""
            CREATE TABLE IF NOT EXISTS assignment_submissions (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                assignment_id INTEGER NOT NULL,
                student_id INTEGER NOT NULL,
                content TEXT,
                file_path TEXT,
                submitted_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                grade REAL,
                feedback TEXT,
                FOREIGN KEY (assignment_id) REFERENCES assignments (id),
                FOREIGN KEY (student_id) REFERENCES users (id),
                UNIQUE(assignment_id, student_id)
            )
        """)
        
        # Class schedule/calendar
        self.connection.execute("""
            CREATE TABLE IF NOT EXISTS class_schedule (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                class_id INTEGER NOT NULL,
                title TEXT NOT NULL,
                description TEXT,
                start_time TIMESTAMP NOT NULL,
                end_time TIMESTAMP NOT NULL,
                is_recurring BOOLEAN DEFAULT 0,
                recurrence_pattern TEXT, -- daily, weekly, monthly
                created_by INTEGER NOT NULL,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (class_id) REFERENCES classes (id),
                FOREIGN KEY (created_by) REFERENCES users (id)
            )
        """)
        
        self.connection.commit()
        
        # Create default admin user if not exists
        self._create_default_admin()
        
        # Create default subjects (Indian syllabus)
        self._create_default_subjects()
        
    def _create_default_admin(self):
        """Create default admin user"""
        cursor = self.connection.execute("SELECT COUNT(*) FROM users WHERE user_type = 'admin'")
        if cursor.fetchone()[0] == 0:
            password_hash = self._hash_password("admin123")
            self.connection.execute("""
                INSERT INTO users (username, email, password_hash, first_name, last_name, user_type)
                VALUES (?, ?, ?, ?, ?, ?)
            """, ("admin", "admin@teacherapp.com", password_hash, "Admin", "User", "admin"))
            self.connection.commit()
    
    def _create_default_subjects(self):
        """Create default subjects based on Indian syllabus"""
        cursor = self.connection.execute("SELECT COUNT(*) FROM subjects")
        if cursor.fetchone()[0] == 0:
            # Indian syllabus subjects
            subjects = [
                ("Mathematics", "Core mathematics curriculum"),
                ("Science", "Physics, Chemistry, Biology"),
                ("Physics", "Physical sciences"),
                ("Chemistry", "Chemical sciences"),
                ("Biology", "Life sciences"),
                ("English", "English language and literature"),
                ("Hindi", "Hindi language and literature"),
                ("Social Studies", "History, Geography, Civics"),
                ("History", "Historical studies"),
                ("Geography", "Geographical studies"),
                ("Civics", "Political science and civics"),
                ("Economics", "Economic studies"),
                ("Computer Science", "Computer studies and programming"),
                ("Physical Education", "Sports and physical activities"),
                ("Art", "Visual arts and crafts"),
                ("Music", "Musical studies"),
                ("Sanskrit", "Sanskrit language"),
                ("French", "French language"),
                ("German", "German language"),
                ("Business Studies", "Business and commerce"),
                ("Accountancy", "Financial accounting"),
                ("Psychology", "Psychological studies"),
                ("Sociology", "Sociological studies"),
                ("Political Science", "Political studies"),
                ("Environmental Science", "Environmental studies"),
                ("Home Science", "Home economics and nutrition"),
                ("Agriculture", "Agricultural studies"),
                ("Engineering Drawing", "Technical drawing"),
                ("Statistics", "Statistical studies"),
                ("Philosophy", "Philosophical studies")
            ]
            
            for subject_name, description in subjects:
                self.connection.execute("""
                    INSERT INTO subjects (name, description, is_custom)
                    VALUES (?, ?, 0)
                """, (subject_name, description))
            
            self.connection.commit()
    
    def _hash_password(self, password: str) -> str:
        """Hash password using SHA-256"""
        return hashlib.sha256(password.encode()).hexdigest()
    
    def verify_password(self, password: str, password_hash: str) -> bool:
        """Verify password against hash"""
        return self._hash_password(password) == password_hash
    
    # User management methods
    def create_user(self, username: str, email: str, password: str, 
                   first_name: str, last_name: str, user_type: str) -> bool:
        """Create a new user"""
        try:
            password_hash = self._hash_password(password)
            self.connection.execute("""
                INSERT INTO users (username, email, password_hash, first_name, last_name, user_type)
                VALUES (?, ?, ?, ?, ?, ?)
            """, (username, email, password_hash, first_name, last_name, user_type))
            self.connection.commit()
            return True
        except sqlite3.IntegrityError:
            return False
    
    def authenticate_user(self, username: str, password: str) -> Optional[Dict]:
        """Authenticate user and return user data"""
        cursor = self.connection.execute("""
            SELECT * FROM users WHERE username = ? AND is_active = 1
        """, (username,))
        user = cursor.fetchone()
        
        if user and self.verify_password(password, user['password_hash']):
            return dict(user)
        return None
    
    def get_user_by_id(self, user_id: int) -> Optional[Dict]:
        """Get user by ID"""
        cursor = self.connection.execute("SELECT * FROM users WHERE id = ?", (user_id,))
        user = cursor.fetchone()
        return dict(user) if user else None
    
    def get_all_teachers(self) -> List[Dict]:
        """Get all teachers"""
        cursor = self.connection.execute("SELECT * FROM users WHERE user_type = 'teacher' AND is_active = 1")
        return [dict(row) for row in cursor.fetchall()]
    
    def get_all_students(self) -> List[Dict]:
        """Get all students"""
        cursor = self.connection.execute("SELECT * FROM users WHERE user_type = 'student' AND is_active = 1")
        return [dict(row) for row in cursor.fetchall()]
    
    # Subject management methods
    def get_all_subjects(self) -> List[Dict]:
        """Get all subjects"""
        cursor = self.connection.execute("SELECT * FROM subjects ORDER BY name")
        return [dict(row) for row in cursor.fetchall()]
    
    def create_custom_subject(self, name: str, description: str, created_by: int) -> int:
        """Create a custom subject"""
        cursor = self.connection.execute("""
            INSERT INTO subjects (name, description, is_custom, created_by)
            VALUES (?, ?, 1, ?)
        """, (name, description, created_by))
        self.connection.commit()
        return cursor.lastrowid
    
    # Class management methods
    def create_class(self, name: str, description: str, subject_id: int, grade_level: int, teacher_id: int) -> int:
        """Create a new class"""
        cursor = self.connection.execute("""
            INSERT INTO classes (name, description, subject_id, grade_level, teacher_id)
            VALUES (?, ?, ?, ?, ?)
        """, (name, description, subject_id, grade_level, teacher_id))
        self.connection.commit()
        return cursor.lastrowid
    
    def get_teacher_classes(self, teacher_id: int) -> List[Dict]:
        """Get all classes for a teacher with subject and grade info"""
        cursor = self.connection.execute("""
            SELECT c.*, s.name as subject_name, s.description as subject_description
            FROM classes c
            JOIN subjects s ON c.subject_id = s.id
            WHERE c.teacher_id = ?
            ORDER BY c.grade_level, s.name
        """, (teacher_id,))
        return [dict(row) for row in cursor.fetchall()]
    
    def enroll_student(self, class_id: int, student_id: int) -> bool:
        """Enroll student in class"""
        try:
            self.connection.execute("""
                INSERT INTO class_enrollments (class_id, student_id)
                VALUES (?, ?)
            """, (class_id, student_id))
            self.connection.commit()
            return True
        except sqlite3.IntegrityError:
            return False
    
    def get_class_students(self, class_id: int) -> List[Dict]:
        """Get all students in a class"""
        cursor = self.connection.execute("""
            SELECT u.* FROM users u
            JOIN class_enrollments ce ON u.id = ce.student_id
            WHERE ce.class_id = ?
        """, (class_id,))
        return [dict(row) for row in cursor.fetchall()]
    
    # Resource management methods
    def add_resource(self, title: str, description: str, resource_type: str,
                    content: str, file_path: str, class_id: int, created_by: int) -> int:
        """Add a resource to a class"""
        cursor = self.connection.execute("""
            INSERT INTO resources (title, description, resource_type, content, file_path, class_id, created_by)
            VALUES (?, ?, ?, ?, ?, ?, ?)
        """, (title, description, resource_type, content, file_path, class_id, created_by))
        self.connection.commit()
        return cursor.lastrowid
    
    def get_class_resources(self, class_id: int) -> List[Dict]:
        """Get all resources for a class"""
        cursor = self.connection.execute("""
            SELECT r.*, u.first_name, u.last_name FROM resources r
            JOIN users u ON r.created_by = u.id
            WHERE r.class_id = ?
            ORDER BY r.created_at DESC
        """, (class_id,))
        return [dict(row) for row in cursor.fetchall()]
    
    # Discussion forum methods
    def create_discussion(self, title: str, content: str, author_id: int, category: str = 'general') -> int:
        """Create a new discussion"""
        cursor = self.connection.execute("""
            INSERT INTO discussions (title, content, author_id, category)
            VALUES (?, ?, ?, ?)
        """, (title, content, author_id, category))
        self.connection.commit()
        return cursor.lastrowid
    
    def get_all_discussions(self) -> List[Dict]:
        """Get all discussions"""
        cursor = self.connection.execute("""
            SELECT d.*, u.first_name, u.last_name FROM discussions d
            JOIN users u ON d.author_id = u.id
            ORDER BY d.updated_at DESC
        """)
        return [dict(row) for row in cursor.fetchall()]
    
    def add_discussion_reply(self, discussion_id: int, content: str, author_id: int) -> int:
        """Add reply to discussion"""
        cursor = self.connection.execute("""
            INSERT INTO discussion_replies (discussion_id, content, author_id)
            VALUES (?, ?, ?)
        """, (discussion_id, content, author_id))
        
        # Update discussion timestamp
        self.connection.execute("""
            UPDATE discussions SET updated_at = CURRENT_TIMESTAMP WHERE id = ?
        """, (discussion_id,))
        
        self.connection.commit()
        return cursor.lastrowid
    
    def get_discussion_replies(self, discussion_id: int) -> List[Dict]:
        """Get all replies for a discussion"""
        cursor = self.connection.execute("""
            SELECT dr.*, u.first_name, u.last_name FROM discussion_replies dr
            JOIN users u ON dr.author_id = u.id
            WHERE dr.discussion_id = ?
            ORDER BY dr.created_at ASC
        """, (discussion_id,))
        return [dict(row) for row in cursor.fetchall()]
    
    # Calendar/Scheduling methods
    def create_schedule_event(self, class_id: int, title: str, description: str,
                           start_time: str, end_time: str, created_by: int,
                           is_recurring: bool = False, recurrence_pattern: str = None) -> int:
        """Create a schedule event"""
        cursor = self.connection.execute("""
            INSERT INTO class_schedule (class_id, title, description, start_time, end_time, 
                                      is_recurring, recurrence_pattern, created_by)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?)
        """, (class_id, title, description, start_time, end_time, is_recurring, recurrence_pattern, created_by))
        self.connection.commit()
        return cursor.lastrowid
    
    def get_class_schedule(self, class_id: int) -> List[Dict]:
        """Get schedule for a class"""
        cursor = self.connection.execute("""
            SELECT * FROM class_schedule 
            WHERE class_id = ?
            ORDER BY start_time
        """, (class_id,))
        return [dict(row) for row in cursor.fetchall()]
    
    def get_teacher_schedule(self, teacher_id: int, start_date: str = None, end_date: str = None) -> List[Dict]:
        """Get all schedule events for a teacher"""
        query = """
            SELECT cs.*, c.name as class_name, s.name as subject_name, c.grade_level
            FROM class_schedule cs
            JOIN classes c ON cs.class_id = c.id
            JOIN subjects s ON c.subject_id = s.id
            WHERE c.teacher_id = ?
        """
        params = [teacher_id]
        
        if start_date and end_date:
            query += " AND cs.start_time BETWEEN ? AND ?"
            params.extend([start_date, end_date])
        
        query += " ORDER BY cs.start_time"
        
        cursor = self.connection.execute(query, params)
        return [dict(row) for row in cursor.fetchall()]
    
    def delete_schedule_event(self, event_id: int) -> bool:
        """Delete a schedule event"""
        try:
            self.connection.execute("DELETE FROM class_schedule WHERE id = ?", (event_id,))
            self.connection.commit()
            return True
        except:
            return False
    
    def __del__(self):
        """Cleanup on destruction"""
        self.disconnect()
