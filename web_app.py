#!/usr/bin/env python3
"""
StaffRoom Web Version - Flask Web Application
Modern web interface for teacher management system
"""

from flask import Flask, render_template, request, redirect, url_for, flash, session, jsonify, send_file
from werkzeug.security import generate_password_hash, check_password_hash
import sqlite3
import os
from datetime import datetime, timedelta
import json
import uuid
from werkzeug.utils import secure_filename

app = Flask(__name__)

# Production-ready configuration
app.config.update(
    SECRET_KEY=os.environ.get('SECRET_KEY', 'teacherapp_secret_key_2024'),
    UPLOAD_FOLDER=os.environ.get('UPLOAD_FOLDER', 'uploads'),
    MAX_CONTENT_LENGTH=16 * 1024 * 1024,  # 16MB max file size
    DATABASE_URL=os.environ.get('DATABASE_URL', 'sqlite:///teacher_app_web.db')
)

# Database configuration
def get_database_url():
    """Get database URL from environment or use SQLite fallback"""
    if 'DATABASE_URL' in os.environ:
        url = os.environ['DATABASE_URL']
        # Fix for older PostgreSQL URLs
        if url.startswith('postgres://'):
            url = url.replace('postgres://', 'postgresql://', 1)
        return url
    return 'sqlite:///teacher_app_web.db'

DB_PATH = get_database_url()

# File upload configuration
UPLOAD_FOLDER = 'uploads'
ALLOWED_EXTENSIONS = {'txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif', 'doc', 'docx', 'ppt', 'pptx', 'xls', 'xlsx'}
MAX_FILE_SIZE = 16 * 1024 * 1024  # 16MB max file size

# Configure upload folder
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['MAX_CONTENT_LENGTH'] = MAX_FILE_SIZE

class WebDatabaseManager:
    def __init__(self, db_path=DB_PATH):
        self.db_path = db_path
        self.init_database()
    
    def get_connection(self):
        """Get database connection - supports both SQLite and PostgreSQL"""
        if self.db_path.startswith('postgresql://'):
            import psycopg2
            from psycopg2.extras import RealDictCursor
            conn = psycopg2.connect(self.db_path, cursor_factory=RealDictCursor)
        else:
            # For SQLite, use a simple filename
            db_file = self.db_path.replace('sqlite:///', '')
            conn = sqlite3.connect(db_file)
            conn.row_factory = sqlite3.Row
        return conn
    
    def init_database(self):
        """Initialize database with web-optimized schema"""
        conn = self.get_connection()
        
        # Users table
        conn.execute("""
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
        conn.execute("""
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
        
        # Classes table
        conn.execute("""
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
        conn.execute("""
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
        conn.execute("""
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
        
        # Class schedule
        conn.execute("""
            CREATE TABLE IF NOT EXISTS class_schedule (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                class_id INTEGER NOT NULL,
                title TEXT NOT NULL,
                description TEXT,
                start_time TIMESTAMP NOT NULL,
                end_time TIMESTAMP NOT NULL,
                is_recurring BOOLEAN DEFAULT 0,
                recurrence_pattern TEXT,
                created_by INTEGER NOT NULL,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (class_id) REFERENCES classes (id),
                FOREIGN KEY (created_by) REFERENCES users (id)
            )
        """)
        
        # Discussions table
        conn.execute("""
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
        conn.execute("""
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
        
        # File attachments for discussions and replies
        conn.execute("""
            CREATE TABLE IF NOT EXISTS discussion_attachments (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                discussion_id INTEGER,
                reply_id INTEGER,
                filename TEXT NOT NULL,
                original_filename TEXT NOT NULL,
                file_path TEXT NOT NULL,
                file_size INTEGER NOT NULL,
                file_type TEXT NOT NULL,
                uploaded_by INTEGER NOT NULL,
                uploaded_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (discussion_id) REFERENCES discussions (id),
                FOREIGN KEY (reply_id) REFERENCES discussion_replies (id),
                FOREIGN KEY (uploaded_by) REFERENCES users (id),
                CHECK ((discussion_id IS NOT NULL AND reply_id IS NULL) OR 
                       (discussion_id IS NULL AND reply_id IS NOT NULL))
            )
        """)
        
        # Organizations
        conn.execute("""
            CREATE TABLE IF NOT EXISTS organizations (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL,
                description TEXT,
                about TEXT,
                location TEXT,
                contact_email TEXT,
                contact_phone TEXT,
                website TEXT,
                logo_filename TEXT,
                logo_path TEXT,
                is_public BOOLEAN DEFAULT 1,
                discussion_privacy TEXT DEFAULT 'public' CHECK (discussion_privacy IN ('public', 'private')),
                created_by INTEGER NOT NULL,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (created_by) REFERENCES users (id)
            )
        """)
        
        # Organization memberships
        conn.execute("""
            CREATE TABLE IF NOT EXISTS organization_memberships (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                organization_id INTEGER NOT NULL,
                user_id INTEGER NOT NULL,
                role TEXT DEFAULT 'member' CHECK (role IN ('admin', 'moderator', 'member')),
                joined_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (organization_id) REFERENCES organizations (id),
                FOREIGN KEY (user_id) REFERENCES users (id),
                UNIQUE(organization_id, user_id)
            )
        """)
        
        # Update discussions table to include organization_id (if not exists)
        try:
            conn.execute("""
                ALTER TABLE discussions ADD COLUMN organization_id INTEGER REFERENCES organizations (id)
            """)
        except sqlite3.OperationalError:
            # Column already exists, ignore
            pass
        
        # Resources table
        conn.execute("""
            CREATE TABLE IF NOT EXISTS resources (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                title TEXT NOT NULL,
                description TEXT,
                resource_type TEXT NOT NULL CHECK (resource_type IN ('note', 'video', 'pdf', 'photo', 'document', 'link', 'other')),
                file_path TEXT,
                file_name TEXT,
                file_size INTEGER,
                external_url TEXT,
                grade_level INTEGER,
                subject_id INTEGER,
                class_id INTEGER,
                organization_id INTEGER,
                uploaded_by INTEGER NOT NULL,
                tags TEXT,
                is_public BOOLEAN DEFAULT 1,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (subject_id) REFERENCES subjects (id),
                FOREIGN KEY (class_id) REFERENCES classes (id),
                FOREIGN KEY (organization_id) REFERENCES organizations (id),
                FOREIGN KEY (uploaded_by) REFERENCES users (id)
            )
        """)
        
        # Global discussions table (cross-organization)
        conn.execute("""
            CREATE TABLE IF NOT EXISTS global_discussions (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                title TEXT NOT NULL,
                content TEXT NOT NULL,
                author_id INTEGER NOT NULL,
                author_organization TEXT,
                category TEXT DEFAULT 'general',
                tags TEXT,
                is_pinned BOOLEAN DEFAULT 0,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (author_id) REFERENCES users (id)
            )
        """)
        
        # Global discussion replies
        conn.execute("""
            CREATE TABLE IF NOT EXISTS global_discussion_replies (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                discussion_id INTEGER NOT NULL,
                author_id INTEGER NOT NULL,
                author_organization TEXT,
                content TEXT NOT NULL,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (discussion_id) REFERENCES global_discussions (id),
                FOREIGN KEY (author_id) REFERENCES users (id)
            )
        """)
        
        conn.commit()
        
        # Create default admin user
        self.create_default_admin()
        
        # Create default subjects
        self.create_default_subjects()
        
        conn.close()
    
    def create_default_admin(self):
        """Create default teacher user for testing"""
        conn = self.get_connection()
        cursor = conn.execute("SELECT COUNT(*) FROM users WHERE username = 'teacher'")
        if cursor.fetchone()[0] == 0:
            password_hash = generate_password_hash("teacher123")
            conn.execute("""
                INSERT INTO users (username, email, password_hash, first_name, last_name, user_type)
                VALUES (?, ?, ?, ?, ?, ?)
            """, ("teacher", "teacher@teacherapp.com", password_hash, "Test", "Teacher", "teacher"))
            conn.commit()
        conn.close()
    
    def create_default_subjects(self):
        """Create default subjects"""
        conn = self.get_connection()
        cursor = conn.execute("SELECT COUNT(*) FROM subjects")
        if cursor.fetchone()[0] == 0:
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
                conn.execute("""
                    INSERT INTO subjects (name, description, is_custom)
                    VALUES (?, ?, 0)
                """, (subject_name, description))
            
            conn.commit()
        conn.close()
    
    def authenticate_user(self, username, password):
        """Authenticate user and return with organization context"""
        conn = self.get_connection()
        cursor = conn.execute("SELECT * FROM users WHERE username = ? AND is_active = 1", (username,))
        user = cursor.fetchone()
        
        if user and check_password_hash(user['password_hash'], password):
            user_dict = dict(user)
            
            # Get user's organizations
            cursor = conn.execute("""
                SELECT o.*, om.role 
                FROM organizations o
                JOIN organization_memberships om ON o.id = om.organization_id
                WHERE om.user_id = ?
            """, (user['id'],))
            organizations = [dict(row) for row in cursor.fetchall()]
            user_dict['organizations'] = organizations
            
            conn.close()
            return user_dict
        
        conn.close()
        return None
    
    def create_user(self, username, email, password, first_name, last_name, user_type, organization_id=None):
        """Create a new user"""
        conn = self.get_connection()
        try:
            password_hash = generate_password_hash(password)
            cursor = conn.execute("""
                INSERT INTO users (username, email, password_hash, first_name, last_name, user_type)
                VALUES (?, ?, ?, ?, ?, ?)
            """, (username, email, password_hash, first_name, last_name, user_type))
            user_id = cursor.lastrowid
            
            # If organization_id is provided, add user to organization
            if organization_id:
                conn.execute("""
                    INSERT INTO organization_memberships (organization_id, user_id, role)
                    VALUES (?, ?, ?)
                """, (organization_id, user_id, user_type))
            
            conn.commit()
            return True
        except sqlite3.IntegrityError:
            return False
        finally:
            conn.close()
    
    def get_all_subjects(self):
        """Get all subjects"""
        conn = self.get_connection()
        cursor = conn.execute("SELECT * FROM subjects ORDER BY name")
        subjects = [dict(row) for row in cursor.fetchall()]
        conn.close()
        return subjects
    
    def create_class(self, name, description, subject_id, grade_level, teacher_id):
        """Create a new class"""
        conn = self.get_connection()
        cursor = conn.execute("""
            INSERT INTO classes (name, description, subject_id, grade_level, teacher_id)
            VALUES (?, ?, ?, ?, ?)
        """, (name, description, subject_id, grade_level, teacher_id))
        conn.commit()
        class_id = cursor.lastrowid
        conn.close()
        return class_id
    
    def get_teacher_classes(self, teacher_id):
        """Get all classes for a teacher"""
        conn = self.get_connection()
        cursor = conn.execute("""
            SELECT c.*, s.name as subject_name, s.description as subject_description
            FROM classes c
            JOIN subjects s ON c.subject_id = s.id
            WHERE c.teacher_id = ?
            ORDER BY c.grade_level, s.name
        """, (teacher_id,))
        classes = [dict(row) for row in cursor.fetchall()]
        conn.close()
        return classes
    
    def get_all_students(self):
        """Get all students"""
        conn = self.get_connection()
        cursor = conn.execute("SELECT * FROM users WHERE user_type = 'student' AND is_active = 1")
        students = [dict(row) for row in cursor.fetchall()]
        conn.close()
        return students
    
    def enroll_student(self, class_id, student_id):
        """Enroll student in class"""
        conn = self.get_connection()
        try:
            conn.execute("""
                INSERT INTO class_enrollments (class_id, student_id)
                VALUES (?, ?)
            """, (class_id, student_id))
            conn.commit()
            return True
        except sqlite3.IntegrityError:
            return False
        finally:
            conn.close()
    
    def get_class_students(self, class_id):
        """Get all students in a class"""
        conn = self.get_connection()
        cursor = conn.execute("""
            SELECT u.* FROM users u
            JOIN class_enrollments ce ON u.id = ce.student_id
            WHERE ce.class_id = ?
        """, (class_id,))
        students = [dict(row) for row in cursor.fetchall()]
        conn.close()
        return students
    
    def get_discussions_by_organization(self, organization_id):
        """Get discussions for an organization"""
        conn = self.get_connection()
        try:
            cursor = conn.execute("""
                SELECT d.*, u.first_name, u.last_name,
                       (SELECT COUNT(*) FROM discussion_replies dr WHERE dr.discussion_id = d.id) as reply_count
                FROM discussions d
                LEFT JOIN users u ON d.author_id = u.id
                WHERE d.organization_id = ?
                ORDER BY d.created_at DESC
            """, (organization_id,))
            discussions = [dict(row) for row in cursor.fetchall()]
            return discussions
        except Exception as e:
            print(f"Error getting discussions by organization: {e}")
            return []
        finally:
            conn.close()

    def get_all_discussions(self):
        """Get all discussions with author information"""
        conn = self.get_connection()
        cursor = conn.execute("""
            SELECT d.*, u.first_name, u.last_name, u.username
            FROM discussions d
            JOIN users u ON d.author_id = u.id
            ORDER BY d.created_at DESC
        """)
        discussions = [dict(row) for row in cursor.fetchall()]
        conn.close()
        return discussions
    
    def create_discussion(self, title, content, author_id, category='general', organization_id=None):
        """Create a new discussion"""
        conn = self.get_connection()
        try:
            cursor = conn.execute("""
                INSERT INTO discussions (title, content, author_id, category, organization_id)
                VALUES (?, ?, ?, ?, ?)
            """, (title, content, author_id, category, organization_id))
            discussion_id = cursor.lastrowid
            conn.commit()
            return discussion_id
        except Exception as e:
            print(f"Error creating discussion: {e}")
            conn.rollback()
            return None
        finally:
            conn.close()
    
    def add_discussion_reply(self, discussion_id, content, author_id):
        """Add a reply to a discussion"""
        conn = self.get_connection()
        cursor = conn.execute("""
            INSERT INTO discussion_replies (discussion_id, content, author_id)
            VALUES (?, ?, ?)
        """, (discussion_id, content, author_id))
        reply_id = cursor.lastrowid
        conn.commit()
        conn.close()
        return reply_id
    
    def get_discussion_replies(self, discussion_id):
        """Get replies for a discussion"""
        conn = self.get_connection()
        cursor = conn.execute("""
            SELECT dr.*, u.first_name, u.last_name, u.username
            FROM discussion_replies dr
            JOIN users u ON dr.author_id = u.id
            WHERE dr.discussion_id = ?
            ORDER BY dr.created_at ASC
        """, (discussion_id,))
        replies = [dict(row) for row in cursor.fetchall()]
        conn.close()
        return replies
    
    def add_discussion_attachment(self, discussion_id, reply_id, filename, original_filename, file_path, file_size, file_type, uploaded_by):
        """Add file attachment to discussion or reply"""
        conn = self.get_connection()
        cursor = conn.execute("""
            INSERT INTO discussion_attachments 
            (discussion_id, reply_id, filename, original_filename, file_path, file_size, file_type, uploaded_by)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?)
        """, (discussion_id, reply_id, filename, original_filename, file_path, file_size, file_type, uploaded_by))
        attachment_id = cursor.lastrowid
        conn.commit()
        conn.close()
        return attachment_id
    
    def get_discussion_attachments(self, discussion_id):
        """Get attachments for a discussion"""
        conn = self.get_connection()
        cursor = conn.execute("""
            SELECT da.*, u.first_name, u.last_name
            FROM discussion_attachments da
            JOIN users u ON da.uploaded_by = u.id
            WHERE da.discussion_id = ?
            ORDER BY da.uploaded_at ASC
        """, (discussion_id,))
        attachments = [dict(row) for row in cursor.fetchall()]
        conn.close()
        return attachments
    
    def get_reply_attachments(self, reply_id):
        """Get attachments for a reply"""
        conn = self.get_connection()
        cursor = conn.execute("""
            SELECT da.*, u.first_name, u.last_name
            FROM discussion_attachments da
            JOIN users u ON da.uploaded_by = u.id
            WHERE da.reply_id = ?
            ORDER BY da.uploaded_at ASC
        """, (reply_id,))
        attachments = [dict(row) for row in cursor.fetchall()]
        conn.close()
        return attachments
    
    def get_discussions_by_organization(self, organization_id):
        """Get discussions for an organization"""
        conn = self.get_connection()
        try:
            cursor = conn.execute("""
                SELECT d.*, u.first_name, u.last_name,
                       (SELECT COUNT(*) FROM discussion_replies dr WHERE dr.discussion_id = d.id) as reply_count
                FROM discussions d
                LEFT JOIN users u ON d.author_id = u.id
                WHERE d.organization_id = ?
                ORDER BY d.created_at DESC
            """, (organization_id,))
            discussions = [dict(row) for row in cursor.fetchall()]
            return discussions
        except Exception as e:
            print(f"Error getting discussions by organization: {e}")
            return []
        finally:
            conn.close()

    def create_global_discussion(self, title, content, author_id, author_organization, category='general', tags=None):
        """Create a new global discussion"""
        conn = self.get_connection()
        try:
            cursor = conn.execute("""
                INSERT INTO global_discussions 
                (title, content, author_id, author_organization, category, tags)
                VALUES (?, ?, ?, ?, ?, ?)
            """, (title, content, author_id, author_organization, category, tags))
            discussion_id = cursor.lastrowid
            conn.commit()
            return discussion_id
        except Exception as e:
            print(f"Error creating global discussion: {e}")
            conn.rollback()
            return None
        finally:
            conn.close()
    
    def get_global_discussions(self, category=None, limit=50):
        """Get global discussions with optional category filter"""
        conn = self.get_connection()
        try:
            query = """
                SELECT gd.*, u.first_name, u.last_name,
                       (SELECT COUNT(*) FROM global_discussion_replies gdr WHERE gdr.discussion_id = gd.id) as reply_count
                FROM global_discussions gd
                LEFT JOIN users u ON gd.author_id = u.id
            """
            params = []
            
            if category:
                query += " WHERE gd.category = ?"
                params.append(category)
            
            query += " ORDER BY gd.is_pinned DESC, gd.created_at DESC LIMIT ?"
            params.append(limit)
            
            cursor = conn.execute(query, params)
            discussions = [dict(row) for row in cursor.fetchall()]
            return discussions
        except Exception as e:
            print(f"Error getting global discussions: {e}")
            return []
        finally:
            conn.close()
    
    def add_global_discussion_reply(self, discussion_id, author_id, author_organization, content):
        """Add a reply to a global discussion"""
        conn = self.get_connection()
        try:
            cursor = conn.execute("""
                INSERT INTO global_discussion_replies 
                (discussion_id, author_id, author_organization, content)
                VALUES (?, ?, ?, ?)
            """, (discussion_id, author_id, author_organization, content))
            reply_id = cursor.lastrowid
            conn.commit()
            return reply_id
        except Exception as e:
            print(f"Error adding global discussion reply: {e}")
            conn.rollback()
            return None
        finally:
            conn.close()
    
    def get_global_discussion_replies(self, discussion_id):
        """Get replies for a global discussion"""
        conn = self.get_connection()
        try:
            cursor = conn.execute("""
                SELECT gdr.*, u.first_name, u.last_name
                FROM global_discussion_replies gdr
                LEFT JOIN users u ON gdr.author_id = u.id
                WHERE gdr.discussion_id = ?
                ORDER BY gdr.created_at ASC
            """, (discussion_id,))
            replies = [dict(row) for row in cursor.fetchall()]
            return replies
        except Exception as e:
            print(f"Error getting global discussion replies: {e}")
            return []
        finally:
            conn.close()

    def create_resource(self, title, description, resource_type, file_path=None, file_name=None, file_size=None, external_url=None, grade_level=None, subject_id=None, class_id=None, organization_id=None, uploaded_by=None, tags=None, is_public=True):
        """Create a new resource"""
        conn = self.get_connection()
        try:
            cursor = conn.execute("""
                INSERT INTO resources 
                (title, description, resource_type, file_path, file_name, file_size, external_url, 
                 grade_level, subject_id, class_id, organization_id, uploaded_by, tags, is_public)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            """, (title, description, resource_type, file_path, file_name, file_size, external_url,
                  grade_level, subject_id, class_id, organization_id, uploaded_by, tags, is_public))
            resource_id = cursor.lastrowid
            conn.commit()
            return resource_id
        except Exception as e:
            print(f"Error creating resource: {e}")
            conn.rollback()
            return None
        finally:
            conn.close()
    
    def get_resources_by_organization(self, organization_id, grade_level=None, subject_id=None, resource_type=None):
        """Get resources for an organization with optional filters"""
        conn = self.get_connection()
        try:
            # Check if organization_id column exists
            cursor = conn.execute("PRAGMA table_info(resources)")
            columns = [row[1] for row in cursor.fetchall()]
            
            if 'organization_id' not in columns:
                # Fallback: get all resources if organization_id column doesn't exist
                query = """
                    SELECT r.*, s.name as subject_name, u.first_name, u.last_name
                    FROM resources r
                    LEFT JOIN subjects s ON r.subject_id = s.id
                    LEFT JOIN users u ON r.uploaded_by = u.id
                """
                params = []
            else:
                query = """
                    SELECT r.*, s.name as subject_name, u.first_name, u.last_name
                    FROM resources r
                    LEFT JOIN subjects s ON r.subject_id = s.id
                    LEFT JOIN users u ON r.uploaded_by = u.id
                    WHERE r.organization_id = ?
                """
                params = [organization_id]
            
            if grade_level:
                query += " AND r.grade_level = ?"
                params.append(grade_level)
            
            if subject_id:
                query += " AND r.subject_id = ?"
                params.append(subject_id)
            
            if resource_type:
                query += " AND r.resource_type = ?"
                params.append(resource_type)
            
            query += " ORDER BY r.created_at DESC"
            
            cursor = conn.execute(query, params)
            resources = [dict(row) for row in cursor.fetchall()]
            return resources
        except Exception as e:
            print(f"Error getting resources: {e}")
            return []
        finally:
            conn.close()
    
    def get_resources_by_class(self, class_id):
        """Get resources for a specific class"""
        conn = self.get_connection()
        try:
            # Check what columns exist in resources table
            cursor = conn.execute("PRAGMA table_info(resources)")
            columns = [row[1] for row in cursor.fetchall()]
            
            # Build query based on available columns
            base_query = "SELECT r.*, u.first_name, u.last_name"
            from_clause = "FROM resources r LEFT JOIN users u ON r.uploaded_by = u.id"
            where_clause = "WHERE r.class_id = ?"
            params = [class_id]
            
            # Add subject join if subject_id column exists
            if 'subject_id' in columns:
                base_query += ", s.name as subject_name"
                from_clause += " LEFT JOIN subjects s ON r.subject_id = s.id"
            
            query = f"{base_query} {from_clause} {where_clause} ORDER BY r.created_at DESC"
            
            cursor = conn.execute(query, params)
            resources = [dict(row) for row in cursor.fetchall()]
            return resources
        except Exception as e:
            print(f"Error getting class resources: {e}")
            return []
        finally:
            conn.close()
    
    def delete_resource(self, resource_id):
        """Delete a resource"""
        conn = self.get_connection()
        try:
            cursor = conn.execute("DELETE FROM resources WHERE id = ?", (resource_id,))
            conn.commit()
            return cursor.rowcount > 0
        except Exception as e:
            print(f"Error deleting resource: {e}")
            conn.rollback()
            return False
        finally:
            conn.close()
    
    def update_resource(self, resource_id, title=None, description=None, tags=None, is_public=None):
        """Update resource details"""
        conn = self.get_connection()
        try:
            updates = []
            params = []
            
            if title is not None:
                updates.append("title = ?")
                params.append(title)
            
            if description is not None:
                updates.append("description = ?")
                params.append(description)
            
            if tags is not None:
                updates.append("tags = ?")
                params.append(tags)
            
            if is_public is not None:
                updates.append("is_public = ?")
                params.append(is_public)
            
            if updates:
                updates.append("updated_at = CURRENT_TIMESTAMP")
                params.append(resource_id)
                
                query = f"UPDATE resources SET {', '.join(updates)} WHERE id = ?"
                cursor = conn.execute(query, params)
                conn.commit()
                return cursor.rowcount > 0
            
            return True
        except Exception as e:
            print(f"Error updating resource: {e}")
            conn.rollback()
            return False
        finally:
            conn.close()

    def create_schedule_event(self, class_id, title, description, start_time, end_time, created_by):
        """Create a schedule event"""
        conn = self.get_connection()
        try:
            cursor = conn.execute("""
                INSERT INTO class_schedule (class_id, title, description, start_time, end_time, created_by)
                VALUES (?, ?, ?, ?, ?, ?)
            """, (class_id, title, description, start_time, end_time, created_by))
            event_id = cursor.lastrowid
            conn.commit()
            return event_id
        except Exception as e:
            print(f"Error creating schedule event: {e}")
            conn.rollback()
            return None
        finally:
            conn.close()
    
    def get_teacher_schedule(self, teacher_id, start_date=None, end_date=None):
        """Get all schedule events for a teacher"""
        conn = self.get_connection()
        try:
            query = """
                SELECT cs.*, c.name as class_name
                FROM class_schedule cs
                LEFT JOIN classes c ON cs.class_id = c.id
                WHERE c.teacher_id = ? OR cs.class_id IS NULL
            """
            params = [teacher_id]
            
            if start_date and end_date:
                query += " AND cs.start_time BETWEEN ? AND ?"
                params.extend([start_date, end_date])
            
            query += " ORDER BY cs.start_time ASC"
            
            cursor = conn.execute(query, params)
            events = [dict(row) for row in cursor.fetchall()]
            return events
        except Exception as e:
            print(f"Error getting teacher schedule: {e}")
            return []
        finally:
            conn.close()
    
    def get_class_schedule(self, class_id):
        """Get schedule for a class"""
        conn = self.get_connection()
        try:
            cursor = conn.execute("""
                SELECT * FROM class_schedule 
                WHERE class_id = ?
                ORDER BY start_time ASC
            """, (class_id,))
            events = [dict(row) for row in cursor.fetchall()]
            return events
        except Exception as e:
            print(f"Error getting class schedule: {e}")
            return []
        finally:
            conn.close()
    
    def delete_schedule_event(self, event_id):
        """Delete a schedule event"""
        conn = self.get_connection()
        try:
            cursor = conn.execute("DELETE FROM class_schedule WHERE id = ?", (event_id,))
            conn.commit()
            return cursor.rowcount > 0
        except Exception as e:
            print(f"Error deleting schedule event: {e}")
            conn.rollback()
            return False
        finally:
            conn.close()

    def create_organization(self, name, description, about, location, contact_email, contact_phone, website, logo_filename, logo_path, created_by, is_public=True, discussion_privacy='public'):
        """Create a new organization"""
        conn = self.get_connection()
        try:
            cursor = conn.execute("""
                INSERT INTO organizations 
                (name, description, about, location, contact_email, contact_phone, website, logo_filename, logo_path, created_by, is_public, discussion_privacy)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            """, (name, description, about, location, contact_email, contact_phone, website, logo_filename, logo_path, created_by, is_public, discussion_privacy))
            org_id = cursor.lastrowid
            conn.commit()
            return org_id
        except Exception as e:
            print(f"Error creating organization: {e}")
            conn.rollback()
            return None
        finally:
            conn.close()
    
    def get_all_organizations(self):
        """Get all organizations"""
        conn = self.get_connection()
        cursor = conn.execute("""
            SELECT o.*, u.first_name, u.last_name
            FROM organizations o
            JOIN users u ON o.created_by = u.id
            ORDER BY o.created_at DESC
        """)
        organizations = [dict(row) for row in cursor.fetchall()]
        conn.close()
        return organizations
    
    def get_organization_by_id(self, org_id):
        """Get organization by ID"""
        conn = self.get_connection()
        cursor = conn.execute("""
            SELECT o.*, u.first_name, u.last_name
            FROM organizations o
            JOIN users u ON o.created_by = u.id
            WHERE o.id = ?
        """, (org_id,))
        organization = cursor.fetchone()
        conn.close()
        return dict(organization) if organization else None
    
    def update_organization(self, org_id, name, description, about, location, contact_email, contact_phone, website, logo_filename, logo_path, is_public, discussion_privacy):
        """Update organization details"""
        conn = self.get_connection()
        cursor = conn.execute("""
            UPDATE organizations 
            SET name = ?, description = ?, about = ?, location = ?, contact_email = ?, 
                contact_phone = ?, website = ?, logo_filename = ?, logo_path = ?, 
                is_public = ?, discussion_privacy = ?, updated_at = CURRENT_TIMESTAMP
            WHERE id = ?
        """, (name, description, about, location, contact_email, contact_phone, website, logo_filename, logo_path, is_public, discussion_privacy, org_id))
        conn.commit()
        conn.close()
        return cursor.rowcount > 0
    
    def add_organization_member(self, organization_id, user_id, role='member'):
        """Add user to organization (enforces single organization per user)"""
        conn = self.get_connection()
        try:
            # Check if user is already a member of any organization
            cursor = conn.execute("""
                SELECT organization_id FROM organization_memberships 
                WHERE user_id = ?
            """, (user_id,))
            existing_membership = cursor.fetchone()
            
            if existing_membership:
                # User is already in an organization, remove them first
                conn.execute("""
                    DELETE FROM organization_memberships 
                    WHERE user_id = ?
                """, (user_id,))
            
            # Add user to new organization
            cursor = conn.execute("""
                INSERT INTO organization_memberships (organization_id, user_id, role)
                VALUES (?, ?, ?)
            """, (organization_id, user_id, role))
            conn.commit()
            return True
        except Exception as e:
            print(f"Error adding organization member: {e}")
            conn.rollback()
            return False
        finally:
            conn.close()
    
    def get_organization_members(self, organization_id):
        """Get all members of an organization"""
        conn = self.get_connection()
        cursor = conn.execute("""
            SELECT om.*, u.first_name, u.last_name, u.username, u.user_type
            FROM organization_memberships om
            JOIN users u ON om.user_id = u.id
            WHERE om.organization_id = ?
            ORDER BY om.joined_at ASC
        """, (organization_id,))
        members = [dict(row) for row in cursor.fetchall()]
        conn.close()
        return members
    
    def get_user_organizations(self, user_id):
        """Get organization user is member of (single organization per user)"""
        conn = self.get_connection()
        cursor = conn.execute("""
            SELECT o.*, om.role, om.joined_at
            FROM organizations o
            JOIN organization_memberships om ON o.id = om.organization_id
            WHERE om.user_id = ?
            ORDER BY om.joined_at DESC
            LIMIT 1
        """, (user_id,))
        result = cursor.fetchone()
        conn.close()
        return [dict(result)] if result else []
    
    def get_user_current_organization(self, user_id):
        """Get user's current organization (single organization per user)"""
        conn = self.get_connection()
        cursor = conn.execute("""
            SELECT o.*, om.role, om.joined_at
            FROM organizations o
            JOIN organization_memberships om ON o.id = om.organization_id
            WHERE om.user_id = ?
            ORDER BY om.joined_at DESC
            LIMIT 1
        """, (user_id,))
        result = cursor.fetchone()
        conn.close()
        return dict(result) if result else None
    
    def is_organization_member(self, organization_id, user_id):
        """Check if user is member of organization"""
        conn = self.get_connection()
        cursor = conn.execute("""
            SELECT role, joined_at FROM organization_memberships 
            WHERE organization_id = ? AND user_id = ?
        """, (organization_id, user_id))
        result = cursor.fetchone()
        conn.close()
        return dict(result) if result else None

# Initialize database
db = WebDatabaseManager()

# Utility functions
def allowed_file(filename):
    """Check if file extension is allowed"""
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

def get_file_icon(file_type):
    """Get appropriate icon for file type"""
    icons = {
        'pdf': 'fas fa-file-pdf text-danger',
        'doc': 'fas fa-file-word text-primary',
        'docx': 'fas fa-file-word text-primary',
        'txt': 'fas fa-file-alt text-secondary',
        'ppt': 'fas fa-file-powerpoint text-warning',
        'pptx': 'fas fa-file-powerpoint text-warning',
        'xls': 'fas fa-file-excel text-success',
        'xlsx': 'fas fa-file-excel text-success',
        'png': 'fas fa-file-image text-info',
        'jpg': 'fas fa-file-image text-info',
        'jpeg': 'fas fa-file-image text-info',
        'gif': 'fas fa-file-image text-info'
    }
    return icons.get(file_type.lower(), 'fas fa-file text-secondary')

def require_organization_access(f):
    """Decorator to require user to be in an organization"""
    def decorated_function(*args, **kwargs):
        if 'user_id' not in session:
            return redirect(url_for('login'))
        
        user_organizations = db.get_user_organizations(session['user_id'])
        if not user_organizations:
            flash('You must join an organization to access this feature.', 'warning')
            return redirect(url_for('organizations'))
        
        return f(*args, **kwargs)
    decorated_function.__name__ = f.__name__
    return decorated_function

# Routes
@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        
        user = db.authenticate_user(username, password)
        if user:
            session['user_id'] = user['id']
            session['username'] = user['username']
            session['user_type'] = user['user_type']
            session['first_name'] = user['first_name']
            session['last_name'] = user['last_name']
            # Get user's current organization (single organization per user)
            current_org = db.get_user_current_organization(user['id'])
            if current_org:
                session['current_org_id'] = current_org['id']
                session['current_org_role'] = current_org['role']
                session['current_org_name'] = current_org['name']
            else:
                session['current_org_id'] = None
                session['current_org_role'] = None
                session['current_org_name'] = None
            
            flash('Login successful!', 'success')
            return redirect(url_for('dashboard'))
        else:
            flash('Invalid username or password', 'error')
    
    if 'user_id' in session:
        return redirect(url_for('dashboard'))
    return render_template('login.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        
        user = db.authenticate_user(username, password)
        if user:
            session['user_id'] = user['id']
            session['username'] = user['username']
            session['user_type'] = user['user_type']
            session['first_name'] = user['first_name']
            session['last_name'] = user['last_name']
            flash('Login successful!', 'success')
            return redirect(url_for('dashboard'))
        else:
            flash('Invalid username or password', 'error')
    
    return render_template('login.html')

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        email = request.form['email']
        first_name = request.form['first_name']
        last_name = request.form['last_name']
        password = request.form['password']
        user_type = request.form['user_type']
        
        if db.create_user(username, email, password, first_name, last_name, user_type):
            flash('Registration successful! Please login.', 'success')
            return redirect(url_for('login'))
        else:
            flash('Registration failed. Username or email may already exist.', 'error')
    
    return render_template('register.html')

@app.route('/dashboard')
@require_organization_access
def dashboard():
    if 'user_id' not in session:
        return redirect(url_for('login'))
    
    user_type = session['user_type']
    user_id = session['user_id']
    
    # Get organization-specific data (always fetch from DB to ensure accuracy)
    current_org = db.get_user_current_organization(user_id)
    current_org_id = current_org['id'] if current_org else None
    current_org_name = current_org['name'] if current_org else 'No Organization'
    
    # Update session with current organization data
    if current_org:
        session['current_org_id'] = current_org['id']
        session['current_org_role'] = current_org['role']
        session['current_org_name'] = current_org['name']
    
    if user_type == 'teacher':
        # Get classes for this teacher in the current organization
        classes = db.get_teacher_classes(user_id)
        # Filter classes by organization (if classes have organization_id field)
        org_classes = [c for c in classes if c.get('organization_id') == current_org_id] if current_org_id else classes
        
        # Get more useful stats
        total_students = sum(len(db.get_class_students(c['id'])) for c in org_classes)
        
        # Group classes by subject for better insights
        subjects = {}
        for cls in org_classes:
            subject = cls.get('subject_name', 'Unknown')
            if subject not in subjects:
                subjects[subject] = 0
            subjects[subject] += 1
        
        # Get resources count
        resources_count = len(db.get_resources_by_organization(current_org_id)) if current_org_id else 0
        
        # Get events count
        events = db.get_teacher_schedule(user_id) if user_type == 'teacher' else []
        events_count = len(events)
        
        # Get discussions count
        discussions = db.get_discussions_by_organization(current_org_id) if current_org_id else []
        discussions_count = len(discussions)
        
        stats = {
            'classes': len(org_classes),
            'total_students': total_students,
            'subjects': len(subjects),
            'organization_name': current_org_name,
            'subject_breakdown': subjects,
            'resources': resources_count,
            'events': events_count,
            'discussions': discussions_count
        }
    elif user_type == 'admin':
        # Get organization-specific data for admin
        org_members = db.get_organization_members(current_org_id) if current_org_id else []
        teachers_in_org = [m for m in org_members if m['user_type'] == 'teacher']
        students_in_org = [m for m in org_members if m['user_type'] == 'student']
        
        # Get resources count
        resources_count = len(db.get_resources_by_organization(current_org_id)) if current_org_id else 0
        
        # Get events count (admin can see all events in organization)
        events_count = 0  # We'll implement this later if needed
        
        # Get discussions count
        discussions = db.get_discussions_by_organization(current_org_id) if current_org_id else []
        discussions_count = len(discussions)
        
        stats = {
            'students': len(students_in_org),
            'teachers': len(teachers_in_org),
            'total_members': len(org_members),
            'organization_name': current_org_name,
            'resources': resources_count,
            'events': events_count,
            'discussions': discussions_count
        }
    else:
        stats = {
            'enrolled_classes': 0,
            'organization_name': current_org_name
        }
    
    return render_template('dashboard.html', user_type=user_type, stats=stats)

@app.route('/classes')
@require_organization_access
def classes():
    if 'user_id' not in session:
        return redirect(url_for('login'))
    
    user_type = session['user_type']
    user_id = session['user_id']
    
    if user_type == 'teacher':
        classes = db.get_teacher_classes(user_id)
        subjects = db.get_all_subjects()
        return render_template('classes.html', classes=classes, subjects=subjects)
    else:
        flash('Access denied. Only teachers can access class management.', 'error')
        return redirect(url_for('dashboard'))

@app.route('/students')
@require_organization_access
def students():
    if 'user_id' not in session:
        return redirect(url_for('login'))
    
    user_type = session['user_type']
    if user_type not in ['admin', 'teacher']:
        flash('Access denied. Only administrators and teachers can access student management.', 'error')
        return redirect(url_for('dashboard'))
    
    students = db.get_all_students()
    return render_template('students.html', students=students)

@app.route('/resources')
@require_organization_access
def resources():
    """Resources management page"""
    if 'user_id' not in session:
        return redirect(url_for('login'))
    
    user_type = session['user_type']
    user_id = session['user_id']
    current_org_id = session.get('current_org_id')
    
    # Get filters from query parameters
    grade_filter = request.args.get('grade')
    subject_filter = request.args.get('subject')
    type_filter = request.args.get('type')
    
    # Get resources with filters
    resources = db.get_resources_by_organization(
        current_org_id, 
        grade_level=int(grade_filter) if grade_filter else None,
        subject_id=int(subject_filter) if subject_filter else None,
        resource_type=type_filter if type_filter else None
    )
    
    # Get subjects for filter dropdown
    subjects = db.get_all_subjects()
    
    # Get classes for the current user
    classes = db.get_teacher_classes(user_id) if user_type == 'teacher' else []
    
    return render_template('resources.html', 
                         resources=resources, 
                         subjects=subjects, 
                         classes=classes,
                         user_type=user_type,
                         current_filters={
                             'grade': grade_filter,
                             'subject': subject_filter,
                             'type': type_filter
                         })

@app.route('/api/create_resource', methods=['POST'])
def api_create_resource():
    """Create a new resource"""
    if 'user_id' not in session:
        return jsonify({'error': 'Not authenticated'}), 401
    
    try:
        # Handle form data with file upload
        if request.form:
            title = request.form.get('title')
            description = request.form.get('description', '')
            resource_type = request.form.get('resource_type')
            grade_level = request.form.get('grade_level')
            subject_id = request.form.get('subject_id')
            class_id = request.form.get('class_id')
            external_url = request.form.get('external_url')
            tags = request.form.get('tags', '')
            is_public = request.form.get('is_public') == 'on'
            
            if not title or not resource_type:
                return jsonify({'error': 'Title and resource type are required'}), 400
            
            # Handle file upload
            file_path = None
            file_name = None
            file_size = None
            
            if 'file' in request.files and request.files['file'].filename:
                file = request.files['file']
                if file and allowed_file(file.filename):
                    file_name = str(uuid.uuid4()) + '.' + file.filename.rsplit('.', 1)[1].lower()
                    file_path = os.path.join(app.config['UPLOAD_FOLDER'], 'resources', file_name)
                    
                    # Ensure resources directory exists
                    os.makedirs(os.path.join(app.config['UPLOAD_FOLDER'], 'resources'), exist_ok=True)
                    
                    # Save file
                    file.save(file_path)
                    file_size = os.path.getsize(file_path)
            
            # Create resource
            resource_id = db.create_resource(
                title=title,
                description=description,
                resource_type=resource_type,
                file_path=file_path,
                file_name=file_name,
                file_size=file_size,
                external_url=external_url,
                grade_level=int(grade_level) if grade_level else None,
                subject_id=int(subject_id) if subject_id else None,
                class_id=int(class_id) if class_id else None,
                organization_id=session.get('current_org_id'),
                uploaded_by=session['user_id'],
                tags=tags,
                is_public=is_public
            )
            
            if resource_id:
                return jsonify({'success': True, 'resource_id': resource_id})
            else:
                return jsonify({'error': 'Failed to create resource'}), 500
                
    except Exception as e:
        print(f"Error creating resource: {e}")
        return jsonify({'error': f'Failed to create resource: {str(e)}'}), 500
    
    return jsonify({'error': 'Invalid request'}), 400

@app.route('/api/delete_resource/<int:resource_id>', methods=['POST'])
def api_delete_resource(resource_id):
    """Delete a resource"""
    if 'user_id' not in session:
        return jsonify({'error': 'Not authenticated'}), 401
    
    try:
        success = db.delete_resource(resource_id)
        if success:
            return jsonify({'success': True})
        else:
            return jsonify({'error': 'Failed to delete resource'}), 500
    except Exception as e:
        print(f"Error deleting resource: {e}")
        return jsonify({'error': f'Failed to delete resource: {str(e)}'}), 500

@app.route('/global-discussions')
@require_organization_access
def global_discussions():
    """Global discussions page for cross-organization educator networking"""
    if 'user_id' not in session:
        return redirect(url_for('login'))
    
    # Get category filter from query parameters
    category_filter = request.args.get('category')
    
    # Get global discussions
    discussions = db.get_global_discussions(category=category_filter)
    
    # Get user's organization name for display
    current_org = db.get_user_current_organization(session['user_id'])
    user_org_name = current_org['name'] if current_org else 'No Organization'
    
    return render_template('global_discussions.html', 
                         discussions=discussions,
                         user_org_name=user_org_name,
                         current_filter=category_filter)

@app.route('/api/create_global_discussion', methods=['POST'])
def api_create_global_discussion():
    """Create a new global discussion"""
    if 'user_id' not in session:
        return jsonify({'error': 'Not authenticated'}), 401
    
    try:
        data = request.get_json()
        title = data.get('title')
        content = data.get('content')
        category = data.get('category', 'general')
        tags = data.get('tags', '')
        
        if not title or not content:
            return jsonify({'error': 'Title and content are required'}), 400
        
        # Get user's organization name
        current_org = db.get_user_current_organization(session['user_id'])
        user_org_name = current_org['name'] if current_org else 'No Organization'
        
        discussion_id = db.create_global_discussion(
            title=title,
            content=content,
            author_id=session['user_id'],
            author_organization=user_org_name,
            category=category,
            tags=tags
        )
        
        if discussion_id:
            return jsonify({'success': True, 'discussion_id': discussion_id})
        else:
            return jsonify({'error': 'Failed to create discussion'}), 500
            
    except Exception as e:
        print(f"Error creating global discussion: {e}")
        return jsonify({'error': f'Failed to create discussion: {str(e)}'}), 500

@app.route('/api/add_global_reply', methods=['POST'])
def api_add_global_reply():
    """Add a reply to a global discussion"""
    if 'user_id' not in session:
        return jsonify({'error': 'Not authenticated'}), 401
    
    try:
        data = request.get_json()
        discussion_id = data.get('discussion_id')
        content = data.get('content')
        
        if not discussion_id or not content:
            return jsonify({'error': 'Discussion ID and content are required'}), 400
        
        # Get user's organization name
        current_org = db.get_user_current_organization(session['user_id'])
        user_org_name = current_org['name'] if current_org else 'No Organization'
        
        reply_id = db.add_global_discussion_reply(
            discussion_id=discussion_id,
            author_id=session['user_id'],
            author_organization=user_org_name,
            content=content
        )
        
        if reply_id:
            return jsonify({'success': True, 'reply_id': reply_id})
        else:
            return jsonify({'error': 'Failed to add reply'}), 500
            
    except Exception as e:
        print(f"Error adding global reply: {e}")
        return jsonify({'error': f'Failed to add reply: {str(e)}'}), 500

@app.route('/schedule')
@require_organization_access
def schedule():
    """Schedule/Calendar page"""
    if 'user_id' not in session:
        return redirect(url_for('login'))
    
    user_type = session['user_type']
    user_id = session['user_id']
    
    # Get schedule events for the user
    if user_type == 'teacher':
        # Get teacher's schedule events
        events = db.get_teacher_schedule(user_id)
        # Get teacher's classes for the dropdown
        classes = db.get_teacher_classes(user_id)
    else:
        # For students, get events from classes they're enrolled in
        events = []
        classes = []
        # TODO: Implement student schedule view
    
    return render_template('schedule.html', events=events, classes=classes, user_type=user_type)

@app.route('/logout')
def logout():
    session.clear()
    flash('You have been logged out.', 'info')
    return redirect(url_for('login'))

# API Routes
@app.route('/api/create_class', methods=['POST'])
def api_create_class():
    if 'user_id' not in session or session['user_type'] != 'teacher':
        return jsonify({'error': 'Access denied'}), 403
    
    data = request.get_json()
    class_id = db.create_class(
        data['name'],
        data['description'],
        data['subject_id'],
        data['grade_level'],
        session['user_id']
    )
    
    return jsonify({'success': True, 'class_id': class_id})

@app.route('/api/enroll_student', methods=['POST'])
def api_enroll_student():
    if 'user_id' not in session or session['user_type'] not in ['admin', 'teacher']:
        return jsonify({'error': 'Access denied'}), 403
    
    data = request.get_json()
    success = db.enroll_student(data['class_id'], data['student_id'])
    
    return jsonify({'success': success})

@app.route('/api/create_user', methods=['POST'])
def api_create_user():
    if 'user_id' not in session or session['user_type'] not in ['admin', 'teacher']:
        return jsonify({'error': 'Access denied'}), 403
    
    data = request.get_json()
    success = db.create_user(
        data['username'],
        data['email'],
        data['password'],
        data['first_name'],
        data['last_name'],
        data['user_type']
    )
    
    return jsonify({'success': success})

@app.route('/discussions')
@require_organization_access
def discussions():
    """Organization discussions page"""
    user_type = session['user_type']
    user_id = session['user_id']
    current_org_id = session.get('current_org_id')
    
    # Get organization discussions
    # For now, get all discussions since organization_id column might not exist
    try:
        org_discussions = db.get_discussions_by_organization(current_org_id) if current_org_id else []
    except Exception as e:
        print(f"Error getting discussions by organization: {e}")
        # Fallback: get all discussions
        org_discussions = db.get_all_discussions()
    
    for discussion in org_discussions:
        discussion['attachments'] = db.get_discussion_attachments(discussion['id'])
    
    return render_template('discussions.html', 
                         discussions=org_discussions,
                         user_type=user_type,
                         get_file_icon=get_file_icon)

@app.route('/api/create_discussion', methods=['POST'])
def api_create_discussion():
    if 'user_id' not in session:
        return jsonify({'error': 'Not authenticated'}), 401
    
    # Handle form data with files
    if request.form:
        title = request.form.get('title')
        content = request.form.get('content')
        category = request.form.get('category', 'general')
        
        if not title or not content:
            return jsonify({'error': 'Title and content are required'}), 400
        
        # Create discussion
        discussion_id = db.create_discussion(
            title, 
            content, 
            session['user_id'], 
            category, 
            session.get('current_org_id')
        )
        
        if discussion_id:
            # Handle file uploads
            uploaded_files = []
            if 'files' in request.files:
                files = request.files.getlist('files')
                for file in files:
                    if file and file.filename and allowed_file(file.filename):
                        # Generate unique filename
                        filename = str(uuid.uuid4()) + '.' + file.filename.rsplit('.', 1)[1].lower()
                        file_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
                        
                        # Ensure upload directory exists
                        os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)
                        
                        # Save file
                        file.save(file_path)
                        
                        # Get file info
                        file_size = os.path.getsize(file_path)
                        file_type = file.filename.rsplit('.', 1)[1].lower()
                        
                        # Add to database
                        attachment_id = db.add_discussion_attachment(
                            discussion_id, None, filename, file.filename, 
                            file_path, file_size, file_type, session['user_id']
                        )
                        
                        uploaded_files.append({
                            'id': attachment_id,
                            'filename': file.filename,
                            'file_type': file_type,
                            'file_size': file_size
                        })
            
            return jsonify({
                'success': True, 
                'discussion_id': discussion_id,
                'uploaded_files': uploaded_files
            })
        else:
            return jsonify({'error': 'Failed to create discussion'}), 500
    
    # Handle JSON data (for API calls without files)
    data = request.get_json()
    discussion_id = db.create_discussion(
        data['title'],
        data['content'],
        session['user_id'],
        data.get('category', 'general')
    )
    
    return jsonify({'success': discussion_id is not None, 'discussion_id': discussion_id})

@app.route('/api/add_reply', methods=['POST'])
def api_add_reply():
    if 'user_id' not in session:
        return jsonify({'error': 'Not authenticated'}), 401
    
    # Handle form data with files
    if request.form:
        discussion_id = request.form.get('discussion_id')
        content = request.form.get('content')
        
        if not discussion_id or not content:
            return jsonify({'error': 'Discussion ID and content are required'}), 400
        
        # Create reply
        reply_id = db.add_discussion_reply(int(discussion_id), content, session['user_id'])
        
        if reply_id:
            # Handle file uploads
            uploaded_files = []
            if 'files' in request.files:
                files = request.files.getlist('files')
                for file in files:
                    if file and file.filename and allowed_file(file.filename):
                        # Generate unique filename
                        filename = str(uuid.uuid4()) + '.' + file.filename.rsplit('.', 1)[1].lower()
                        file_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
                        
                        # Ensure upload directory exists
                        os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)
                        
                        # Save file
                        file.save(file_path)
                        
                        # Get file info
                        file_size = os.path.getsize(file_path)
                        file_type = file.filename.rsplit('.', 1)[1].lower()
                        
                        # Add to database
                        attachment_id = db.add_discussion_attachment(
                            None, reply_id, filename, file.filename, 
                            file_path, file_size, file_type, session['user_id']
                        )
                        
                        uploaded_files.append({
                            'id': attachment_id,
                            'filename': file.filename,
                            'file_type': file_type,
                            'file_size': file_size
                        })
            
            return jsonify({
                'success': True, 
                'reply_id': reply_id,
                'uploaded_files': uploaded_files
            })
        else:
            return jsonify({'error': 'Failed to create reply'}), 500
    
    # Handle JSON data (for API calls without files)
    data = request.get_json()
    reply_id = db.add_discussion_reply(
        data['discussion_id'],
        data['content'],
        session['user_id']
    )
    
    return jsonify({'success': reply_id is not None, 'reply_id': reply_id})

@app.route('/organizations')
def organizations():
    """Organizations page"""
    if 'user_id' not in session:
        return redirect(url_for('login'))
    
    organizations = db.get_all_organizations()
    user_organizations = db.get_user_organizations(session['user_id'])
    
    return render_template('organizations.html', 
                         organizations=organizations, 
                         user_organizations=user_organizations,
                         can_create_org=session['user_type'] == 'teacher')

@app.route('/organization/<int:org_id>')
def organization_detail(org_id):
    """Organization detail page"""
    if 'user_id' not in session:
        return redirect(url_for('login'))
    
    organization = db.get_organization_by_id(org_id)
    if not organization:
        return "Organization not found", 404
    
    members = db.get_organization_members(org_id)
    user_membership = db.is_organization_member(org_id, session['user_id'])
    
    return render_template('organization_detail.html', 
                         organization=organization,
                         members=members,
                         user_membership=user_membership,
                         is_org_admin=user_membership and user_membership['role'] == 'admin')

@app.route('/api/create_organization', methods=['POST'])
def api_create_organization():
    """Create new organization (Teachers can create, becoming admin)"""
    if 'user_id' not in session or session['user_type'] not in ['teacher']:
        return jsonify({'error': 'Only teachers can create organizations'}), 403
    
    # Handle form data with logo upload
    if request.form:
        name = request.form.get('name')
        description = request.form.get('description')
        about = request.form.get('about')
        location = request.form.get('location')
        contact_email = request.form.get('contact_email')
        contact_phone = request.form.get('contact_phone')
        website = request.form.get('website')
        is_public = request.form.get('is_public') == 'on'
        discussion_privacy = request.form.get('discussion_privacy', 'public')
        
        if not name:
            return jsonify({'error': 'Organization name is required'}), 400
        
        # Handle logo upload
        logo_filename = None
        logo_path = None
        if 'logo' in request.files:
            logo_file = request.files['logo']
            if logo_file and logo_file.filename and allowed_file(logo_file.filename):
                logo_filename = str(uuid.uuid4()) + '.' + logo_file.filename.rsplit('.', 1)[1].lower()
                logo_path = os.path.join(app.config['UPLOAD_FOLDER'], 'logos', logo_filename)
                
                # Ensure logos directory exists
                os.makedirs(os.path.join(app.config['UPLOAD_FOLDER'], 'logos'), exist_ok=True)
                
                # Save logo
                logo_file.save(logo_path)
        
        # Create organization
        try:
            org_id = db.create_organization(
                name, description, about, location, contact_email, 
                contact_phone, website, logo_filename, logo_path, 
                session['user_id'], is_public, discussion_privacy
            )
            
            if org_id and org_id > 0:
                # Add creator as admin
                db.add_organization_member(org_id, session['user_id'], 'admin')
                return jsonify({'success': True, 'organization_id': org_id})
            else:
                return jsonify({'error': 'Failed to create organization'}), 500
        except Exception as e:
            print(f"Error in API create_organization: {e}")
            return jsonify({'error': f'Failed to create organization: {str(e)}'}), 500
    
    return jsonify({'error': 'Invalid request'}), 400

@app.route('/api/create_schedule_event', methods=['POST'])
def api_create_schedule_event():
    """Create a new schedule event"""
    if 'user_id' not in session:
        return jsonify({'error': 'Not authenticated'}), 401
    
    data = request.get_json()
    if not data:
        return jsonify({'error': 'No data provided'}), 400
    
    title = data.get('title')
    description = data.get('description', '')
    start_time = data.get('start_time')
    end_time = data.get('end_time')
    class_id = data.get('class_id')
    
    if not title or not start_time or not end_time:
        return jsonify({'error': 'Title, start time, and end time are required'}), 400
    
    if not class_id:
        return jsonify({'error': 'Class is required for schedule events'}), 400
    
    try:
        # Create schedule event
        event_id = db.create_schedule_event(
            class_id=int(class_id),
            title=title,
            description=description,
            start_time=start_time,
            end_time=end_time,
            created_by=session['user_id']
        )
        
        if event_id:
            return jsonify({'success': True, 'event_id': event_id})
        else:
            return jsonify({'error': 'Failed to create event'}), 500
            
    except Exception as e:
        print(f"Error creating schedule event: {e}")
        return jsonify({'error': f'Failed to create event: {str(e)}'}), 500

@app.route('/api/join_organization/<int:org_id>', methods=['POST'])
def api_join_organization(org_id):
    """Join organization (switches from current organization if any)"""
    if 'user_id' not in session:
        return jsonify({'error': 'Not authenticated'}), 401
    
    # Check if user is already in an organization
    current_org = db.get_user_current_organization(session['user_id'])
    if current_org:
        # User is switching organizations
        success = db.add_organization_member(org_id, session['user_id'])
        if success:
            # Update session with new organization
            new_org = db.get_organization_by_id(org_id)
            session['current_org_id'] = org_id
            session['current_org_name'] = new_org['name'] if new_org else 'Unknown Organization'
            session['current_org_role'] = 'member'
            return jsonify({
                'success': True, 
                'message': f'Successfully switched to {new_org["name"] if new_org else "the organization"}',
                'switched': True
            })
        else:
            return jsonify({'error': 'Failed to join organization'}), 500
    else:
        # User is joining their first organization
        success = db.add_organization_member(org_id, session['user_id'])
        if success:
            # Update session with new organization
            new_org = db.get_organization_by_id(org_id)
            session['current_org_id'] = org_id
            session['current_org_name'] = new_org['name'] if new_org else 'Unknown Organization'
            session['current_org_role'] = 'member'
            return jsonify({
                'success': True, 
                'message': f'Successfully joined {new_org["name"] if new_org else "the organization"}',
                'switched': False
            })
        else:
            return jsonify({'error': 'Failed to join organization'}), 500

@app.route('/api/get_discussion_details/<int:discussion_id>')
def api_get_discussion_details(discussion_id):
    """Get detailed discussion information including replies and attachments"""
    if 'user_id' not in session:
        return jsonify({'error': 'Not authenticated'}), 401
    
    # Get discussion details
    discussions = db.get_all_discussions()
    discussion = next((d for d in discussions if d['id'] == discussion_id), None)
    
    if not discussion:
        return jsonify({'error': 'Discussion not found'}), 404
    
    # Get attachments
    discussion['attachments'] = db.get_discussion_attachments(discussion_id)
    
    # Get replies with attachments
    replies = db.get_discussion_replies(discussion_id)
    for reply in replies:
        reply['attachments'] = db.get_reply_attachments(reply['id'])
    
    return jsonify({
        'discussion': discussion,
        'replies': replies
    })

@app.route('/download/<path:filename>')
def download_file(filename):
    """Download uploaded files"""
    if 'user_id' not in session:
        return redirect(url_for('login'))
    
    file_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
    if os.path.exists(file_path):
        return send_file(file_path, as_attachment=True)
    else:
        return "File not found", 404

def create_default_admin():
    """Create a default teacher user for testing"""
    try:
        db = WebDatabaseManager()
        # Check if any users exist by trying to get a user
        try:
            db.get_user_by_username('teacher')
            print("Default teacher user already exists")
        except:
            # Create a default teacher user
            db.create_user(
                username='teacher',
                password='password',
                first_name='Test',
                last_name='Teacher',
                user_type='teacher'
            )
            print("Default teacher user created: username='teacher', password='password'")
    except Exception as e:
        print(f"Error creating default admin: {e}")

if __name__ == '__main__':
    # Production-ready configuration
    debug_mode = os.environ.get('FLASK_ENV') != 'production'
    port = int(os.environ.get('PORT', 5000))
    
    # Ensure directories exist
    os.makedirs('templates', exist_ok=True)
    os.makedirs('static/css', exist_ok=True)
    os.makedirs('static/js', exist_ok=True)
    os.makedirs('uploads', exist_ok=True)
    os.makedirs('uploads/logos', exist_ok=True)
    os.makedirs(os.path.join(app.config['UPLOAD_FOLDER'], 'resources'), exist_ok=True)
    
    # Create default admin user
    create_default_admin()
    
    app.run(debug=debug_mode, host='0.0.0.0', port=port)
