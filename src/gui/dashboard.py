"""
Dashboard window for TeacherApp
Main interface showing overview and navigation options
"""

import tkinter as tk
from tkinter import ttk

class Dashboard:
    def __init__(self, parent, auth_manager, db_manager, navigate_callback):
        self.parent = parent
        self.auth_manager = auth_manager
        self.db_manager = db_manager
        self.navigate_callback = navigate_callback
        
        self.create_widgets()
        
    def create_widgets(self):
        """Create dashboard interface"""
        # Header frame
        header_frame = ttk.Frame(self.parent)
        header_frame.pack(fill=tk.X, padx=20, pady=10)
        
        # Welcome message
        user_name = self.auth_manager.get_user_display_name()
        user_type = self.auth_manager.get_current_user()['user_type'].title()
        
        welcome_label = ttk.Label(header_frame, 
                                 text=f"Welcome, {user_name} ({user_type})", 
                                 style='Title.TLabel')
        welcome_label.pack(side=tk.LEFT)
        
        # Logout button
        logout_button = ttk.Button(header_frame, text="Logout", style='Secondary.TButton',
                                  command=lambda: self.navigate_callback("logout"))
        logout_button.pack(side=tk.RIGHT)
        
        # Main content frame
        content_frame = ttk.Frame(self.parent)
        content_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=10)
        
        # Create navigation cards
        self.create_navigation_cards(content_frame)
        
        # Stats frame
        self.create_stats_section(content_frame)
        
    def create_navigation_cards(self, parent):
        """Create navigation cards for different features"""
        cards_frame = ttk.Frame(parent)
        cards_frame.pack(fill=tk.X, pady=(0, 20))
        
        # Class Management Card
        class_card = ttk.Frame(cards_frame, style='Card.TFrame')
        class_card.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=(0, 10))
        
        ttk.Label(class_card, text="📚", font=('Arial', 24)).pack(pady=(20, 10))
        ttk.Label(class_card, text="Class Management", style='Heading.TLabel').pack()
        ttk.Label(class_card, text="Manage classes, students, and resources", 
                 style='Info.TLabel', wraplength=200).pack(pady=(5, 15))
        ttk.Button(class_card, text="Open", style='Primary.TButton',
                  command=lambda: self.navigate_callback("classes")).pack(pady=(0, 20))
        
        # Discussion Forum Card
        discussion_card = ttk.Frame(cards_frame, style='Card.TFrame')
        discussion_card.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=5)
        
        ttk.Label(discussion_card, text="💬", font=('Arial', 24)).pack(pady=(20, 10))
        ttk.Label(discussion_card, text="Discussion Forum", style='Heading.TLabel').pack()
        ttk.Label(discussion_card, text="Connect with other teachers", 
                 style='Info.TLabel', wraplength=200).pack(pady=(5, 15))
        ttk.Button(discussion_card, text="Open", style='Primary.TButton',
                  command=lambda: self.navigate_callback("discussions")).pack(pady=(0, 20))
        
        # Student Management Card (Admin and Teachers)
        if self.auth_manager.is_admin() or self.auth_manager.is_teacher():
            student_card = ttk.Frame(cards_frame, style='Card.TFrame')
            student_card.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=(5, 0))
            
            ttk.Label(student_card, text="🎓", font=('Arial', 24)).pack(pady=(20, 10))
            ttk.Label(student_card, text="Student Management", style='Heading.TLabel').pack()
            ttk.Label(student_card, text="Manage students and enrollments", 
                     style='Info.TLabel', wraplength=200).pack(pady=(5, 15))
            ttk.Button(student_card, text="Open", style='Primary.TButton',
                      command=lambda: self.navigate_callback("students")).pack(pady=(0, 20))
        
        # User Management Card (Admin only)
        if self.auth_manager.is_admin():
            user_card = ttk.Frame(cards_frame, style='Card.TFrame')
            user_card.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=(10, 0))
            
            ttk.Label(user_card, text="👥", font=('Arial', 24)).pack(pady=(20, 10))
            ttk.Label(user_card, text="User Management", style='Heading.TLabel').pack()
            ttk.Label(user_card, text="Manage teachers and students", 
                     style='Info.TLabel', wraplength=200).pack(pady=(5, 15))
            ttk.Button(user_card, text="Open", style='Primary.TButton',
                      command=lambda: self.navigate_callback("users")).pack(pady=(0, 20))
        
    def create_stats_section(self, parent):
        """Create statistics section"""
        stats_frame = ttk.LabelFrame(parent, text="Quick Stats", style='Card.TFrame')
        stats_frame.pack(fill=tk.X, pady=(0, 20))
        
        stats_content = ttk.Frame(stats_frame)
        stats_content.pack(fill=tk.X, padx=20, pady=10)
        
        # Get user stats
        user_id = self.auth_manager.get_current_user()['id']
        
        if self.auth_manager.is_teacher():
            # Teacher stats
            classes = self.db_manager.get_teacher_classes(user_id)
            total_students = sum(len(self.db_manager.get_class_students(c['id'])) for c in classes)
            
            ttk.Label(stats_content, text=f"Classes: {len(classes)}", style='Info.TLabel').pack(side=tk.LEFT, padx=(0, 30))
            ttk.Label(stats_content, text=f"Total Students: {total_students}", style='Info.TLabel').pack(side=tk.LEFT, padx=(0, 30))
            
        elif self.auth_manager.is_student():
            # Student stats - get enrolled classes
            cursor = self.db_manager.connection.execute("""
                SELECT COUNT(*) FROM class_enrollments WHERE student_id = ?
            """, (user_id,))
            enrolled_classes = cursor.fetchone()[0]
            
            ttk.Label(stats_content, text=f"Enrolled Classes: {enrolled_classes}", style='Info.TLabel').pack(side=tk.LEFT)
            
        elif self.auth_manager.is_admin():
            # Admin stats
            teachers = self.db_manager.get_all_teachers()
            students = self.db_manager.get_all_students()
            
            ttk.Label(stats_content, text=f"Teachers: {len(teachers)}", style='Info.TLabel').pack(side=tk.LEFT, padx=(0, 30))
            ttk.Label(stats_content, text=f"Students: {len(students)}", style='Info.TLabel').pack(side=tk.LEFT, padx=(0, 30))
            
        # Recent activity section
        activity_frame = ttk.LabelFrame(parent, text="Recent Activity", style='Card.TFrame')
        activity_frame.pack(fill=tk.BOTH, expand=True)
        
        activity_content = ttk.Frame(activity_frame)
        activity_content.pack(fill=tk.BOTH, expand=True, padx=20, pady=10)
        
        # Get recent discussions
        discussions = self.db_manager.get_all_discussions()[:5]
        
        if discussions:
            for discussion in discussions:
                activity_item = ttk.Frame(activity_content)
                activity_item.pack(fill=tk.X, pady=2)
                
                ttk.Label(activity_item, text=f"💬 {discussion['title']}", 
                         style='Info.TLabel').pack(anchor=tk.W)
                ttk.Label(activity_item, text=f"by {discussion['first_name']} {discussion['last_name']}", 
                         style='Info.TLabel', foreground='gray').pack(anchor=tk.W)
        else:
            ttk.Label(activity_content, text="No recent activity", 
                     style='Info.TLabel', foreground='gray').pack()
