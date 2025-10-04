"""
Authentication and user management module
Handles login, registration, and user session management
"""

from typing import Optional, Dict
from src.database import DatabaseManager

class AuthManager:
    def __init__(self, db_manager: DatabaseManager):
        self.db_manager = db_manager
        self.current_user: Optional[Dict] = None
        
    def login(self, username: str, password: str) -> bool:
        """Authenticate user and set current session"""
        user = self.db_manager.authenticate_user(username, password)
        if user:
            self.current_user = user
            return True
        return False
    
    def logout(self):
        """Clear current user session"""
        self.current_user = None
    
    def register(self, username: str, email: str, password: str,
                first_name: str, last_name: str, user_type: str) -> bool:
        """Register a new user"""
        return self.db_manager.create_user(username, email, password, 
                                         first_name, last_name, user_type)
    
    def is_logged_in(self) -> bool:
        """Check if user is currently logged in"""
        return self.current_user is not None
    
    def get_current_user(self) -> Optional[Dict]:
        """Get current user data"""
        return self.current_user
    
    def is_admin(self) -> bool:
        """Check if current user is admin"""
        return self.current_user and self.current_user['user_type'] == 'admin'
    
    def is_teacher(self) -> bool:
        """Check if current user is teacher"""
        return self.current_user and self.current_user['user_type'] == 'teacher'
    
    def is_student(self) -> bool:
        """Check if current user is student"""
        return self.current_user and self.current_user['user_type'] == 'student'
    
    def get_user_display_name(self) -> str:
        """Get user's display name"""
        if self.current_user:
            return f"{self.current_user['first_name']} {self.current_user['last_name']}"
        return "Guest"
