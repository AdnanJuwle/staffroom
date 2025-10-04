"""
Main GUI window and navigation for TeacherApp
Provides the main interface with login, dashboard, and navigation
"""

import tkinter as tk
from tkinter import ttk, messagebox
from src.gui.login_window import LoginWindow
from src.gui.dashboard import Dashboard
from src.gui.enhanced_class_management import EnhancedClassManagementWindow
from src.gui.discussion_forum import DiscussionForumWindow
from src.gui.user_management import UserManagementWindow
from src.gui.student_management import StudentManagementWindow

class MainWindow:
    def __init__(self, root, auth_manager, db_manager):
        self.root = root
        self.auth_manager = auth_manager
        self.db_manager = db_manager
        
        # Configure style
        self.setup_styles()
        
        # Create main container
        self.main_container = ttk.Frame(root)
        self.main_container.pack(fill=tk.BOTH, expand=True)
        
        # Initialize with login window
        self.show_login()
        
    def setup_styles(self):
        """Configure modern styling"""
        style = ttk.Style()
        
        # Configure colors
        style.configure('Title.TLabel', font=('Arial', 16, 'bold'))
        style.configure('Heading.TLabel', font=('Arial', 12, 'bold'))
        style.configure('Info.TLabel', font=('Arial', 10))
        
        # Configure buttons
        style.configure('Primary.TButton', font=('Arial', 10, 'bold'))
        style.configure('Secondary.TButton', font=('Arial', 10))
        
        # Configure frames
        style.configure('Card.TFrame', relief='raised', borderwidth=1)
        
    def clear_window(self):
        """Clear all widgets from main container"""
        for widget in self.main_container.winfo_children():
            widget.destroy()
            
    def show_login(self):
        """Show login window"""
        self.clear_window()
        LoginWindow(self.main_container, self.auth_manager, self.on_login_success)
        
    def show_dashboard(self):
        """Show main dashboard"""
        self.clear_window()
        Dashboard(self.main_container, self.auth_manager, self.db_manager, self.navigate_to)
        
    def navigate_to(self, destination):
        """Navigate to different sections"""
        self.clear_window()
        
        if destination == "dashboard":
            self.show_dashboard()
        elif destination == "classes":
            EnhancedClassManagementWindow(self.main_container, self.auth_manager, self.db_manager, self.navigate_to)
        elif destination == "discussions":
            DiscussionForumWindow(self.main_container, self.auth_manager, self.db_manager, self.navigate_to)
        elif destination == "users":
            if self.auth_manager.is_admin():
                UserManagementWindow(self.main_container, self.auth_manager, self.db_manager, self.navigate_to)
            else:
                messagebox.showwarning("Access Denied", "Only administrators can access user management.")
                self.show_dashboard()
        elif destination == "students":
            if self.auth_manager.is_admin() or self.auth_manager.is_teacher():
                StudentManagementWindow(self.main_container, self.auth_manager, self.db_manager, self.navigate_to)
            else:
                messagebox.showwarning("Access Denied", "Only administrators and teachers can access student management.")
                self.show_dashboard()
        elif destination == "logout":
            self.auth_manager.logout()
            self.show_login()
            
    def on_login_success(self):
        """Handle successful login"""
        self.show_dashboard()
