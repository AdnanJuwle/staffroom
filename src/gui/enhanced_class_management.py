"""
Enhanced Class Management window for TeacherApp
Handles subject-grade based class organization, scheduling, and dynamic tabs
"""

import tkinter as tk
from tkinter import ttk, messagebox, simpledialog
from datetime import datetime, timedelta
import calendar

# Import the existing dialog classes
from src.gui.class_management import StudentSelectionDialog, ResourceDialog, ResourceViewDialog
from src.gui.enhanced_dialogs import NewClassDialog, SubjectManagementDialog, ScheduleEventDialog

class EnhancedClassManagementWindow:
    def __init__(self, parent, auth_manager, db_manager, navigate_callback):
        self.parent = parent
        self.auth_manager = auth_manager
        self.db_manager = db_manager
        self.navigate_callback = navigate_callback
        
        self.create_widgets()
        self.refresh_classes()
        
    def create_widgets(self):
        """Create enhanced class management interface"""
        # Header
        header_frame = ttk.Frame(self.parent)
        header_frame.pack(fill=tk.X, padx=20, pady=10)
        
        ttk.Label(header_frame, text="Class Management", style='Title.TLabel').pack(side=tk.LEFT)
        
        # Back button
        back_button = ttk.Button(header_frame, text="← Back to Dashboard", 
                                style='Secondary.TButton',
                                command=lambda: self.navigate_callback("dashboard"))
        back_button.pack(side=tk.RIGHT)
        
        # Main content with notebook for tabs
        main_frame = ttk.Frame(self.parent)
        main_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=10)
        
        # Create notebook for dynamic tabs
        self.notebook = ttk.Notebook(main_frame)
        self.notebook.pack(fill=tk.BOTH, expand=True)
        
        # Add management tab
        self.create_management_tab()
        
        # Add calendar tab
        self.create_calendar_tab()
        
    def create_management_tab(self):
        """Create the main management tab"""
        management_frame = ttk.Frame(self.notebook)
        self.notebook.add(management_frame, text="📚 Class Management")
        
        # Left panel - Classes organized by subject-grade
        left_frame = ttk.LabelFrame(management_frame, text="My Classes")
        left_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=(0, 10))
        
        # Class management buttons
        button_frame = ttk.Frame(left_frame)
        button_frame.pack(fill=tk.X, padx=10, pady=10)
        
        ttk.Button(button_frame, text="New Class", style='Primary.TButton',
                  command=self.create_new_class).pack(side=tk.LEFT, padx=(0, 5))
        # Only teachers and admins can manage subjects
        if self.auth_manager.is_teacher() or self.auth_manager.is_admin():
            ttk.Button(button_frame, text="Manage Subjects", style='Secondary.TButton',
                      command=self.manage_subjects).pack(side=tk.LEFT)
        
        # Classes treeview organized by subject-grade
        tree_frame = ttk.Frame(left_frame)
        tree_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=(0, 10))
        
        self.classes_tree = ttk.Treeview(tree_frame, columns=('grade', 'students'), show='tree headings')
        self.classes_tree.heading('#0', text='Subject')
        self.classes_tree.heading('grade', text='Grade')
        self.classes_tree.heading('students', text='Students')
        
        self.classes_tree.column('#0', width=200)
        self.classes_tree.column('grade', width=80)
        self.classes_tree.column('students', width=80)
        
        # Scrollbar for treeview
        tree_scroll = ttk.Scrollbar(tree_frame, orient=tk.VERTICAL, command=self.classes_tree.yview)
        self.classes_tree.configure(yscrollcommand=tree_scroll.set)
        
        self.classes_tree.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        tree_scroll.pack(side=tk.RIGHT, fill=tk.Y)
        
        self.classes_tree.bind('<<TreeviewSelect>>', self.on_class_select)
        
        # Right panel - Class details
        self.right_frame = ttk.LabelFrame(management_frame, text="Class Details")
        self.right_frame.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True)
        
        # Initially show placeholder
        self.show_class_placeholder()
        
    def create_calendar_tab(self):
        """Create the calendar/scheduling tab"""
        calendar_frame = ttk.Frame(self.notebook)
        self.notebook.add(calendar_frame, text="📅 Schedule")
        
        # Calendar controls
        controls_frame = ttk.Frame(calendar_frame)
        controls_frame.pack(fill=tk.X, padx=10, pady=10)
        
        ttk.Button(controls_frame, text="New Schedule", style='Primary.TButton',
                  command=self.create_schedule_event).pack(side=tk.LEFT, padx=(0, 10))
        
        # Month navigation
        nav_frame = ttk.Frame(controls_frame)
        nav_frame.pack(side=tk.RIGHT)
        
        self.prev_month_btn = ttk.Button(nav_frame, text="◀", command=self.prev_month)
        self.prev_month_btn.pack(side=tk.LEFT, padx=(0, 5))
        
        self.month_label = ttk.Label(nav_frame, text="", style='Heading.TLabel')
        self.month_label.pack(side=tk.LEFT, padx=10)
        
        self.next_month_btn = ttk.Button(nav_frame, text="▶", command=self.next_month)
        self.next_month_btn.pack(side=tk.LEFT, padx=(5, 0))
        
        # Calendar display
        calendar_display_frame = ttk.Frame(calendar_frame)
        calendar_display_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=(0, 10))
        
        # Calendar grid
        self.calendar_frame = ttk.Frame(calendar_display_frame)
        self.calendar_frame.pack(fill=tk.BOTH, expand=True)
        
        # Initialize calendar
        self.current_date = datetime.now()
        self.update_calendar()
        
    def refresh_classes(self):
        """Refresh the classes tree organized by subject-grade"""
        # Clear existing items
        for item in self.classes_tree.get_children():
            self.classes_tree.delete(item)
        
        if self.auth_manager.is_teacher():
            classes = self.db_manager.get_teacher_classes(self.auth_manager.get_current_user()['id'])
            
            # Group classes by subject
            subjects_dict = {}
            for class_data in classes:
                subject_name = class_data['subject_name']
                if subject_name not in subjects_dict:
                    subjects_dict[subject_name] = []
                subjects_dict[subject_name].append(class_data)
            
            # Add to treeview
            for subject_name, subject_classes in subjects_dict.items():
                subject_node = self.classes_tree.insert('', 'end', text=subject_name, 
                                                       values=('', f"{len(subject_classes)} classes"))
                
                # Add classes under each subject
                for class_data in subject_classes:
                    students_count = len(self.db_manager.get_class_students(class_data['id']))
                    self.classes_tree.insert(subject_node, 'end', 
                                           text=f"{class_data['name']}",
                                           values=(f"Grade {class_data['grade_level']}", f"{students_count} students"),
                                           tags=(str(class_data['id']),))
        
        self.selected_class_id = None
        
    def on_class_select(self, event):
        """Handle class selection"""
        selection = self.classes_tree.selection()
        if selection:
            item = self.classes_tree.item(selection[0])
            tags = item['tags']
            if tags and str(tags[0]).isdigit():
                class_id = int(tags[0])
                self.selected_class_id = class_id
                self.show_class_details(class_id)
                
    def show_class_placeholder(self):
        """Show placeholder when no class is selected"""
        for widget in self.right_frame.winfo_children():
            widget.destroy()
            
        placeholder_frame = ttk.Frame(self.right_frame)
        placeholder_frame.pack(expand=True)
        
        ttk.Label(placeholder_frame, text="Select a class to view details", 
                 style='Info.TLabel').pack(expand=True)
        
    def show_class_details(self, class_id):
        """Show detailed information about selected class"""
        # Clear right frame
        for widget in self.right_frame.winfo_children():
            widget.destroy()
            
        # Get class data
        cursor = self.db_manager.connection.execute("""
            SELECT c.*, s.name as subject_name FROM classes c
            JOIN subjects s ON c.subject_id = s.id
            WHERE c.id = ?
        """, (class_id,))
        class_data = cursor.fetchone()
        
        if not class_data:
            return
            
        # Class info frame
        info_frame = ttk.Frame(self.right_frame)
        info_frame.pack(fill=tk.X, padx=10, pady=10)
        
        ttk.Label(info_frame, text=class_data['name'], style='Heading.TLabel').pack(anchor=tk.W)
        ttk.Label(info_frame, text=f"{class_data['subject_name']} - Grade {class_data['grade_level']}", 
                 style='Info.TLabel').pack(anchor=tk.W, pady=(5, 0))
        if class_data['description']:
            ttk.Label(info_frame, text=class_data['description'], 
                     style='Info.TLabel', wraplength=400).pack(anchor=tk.W, pady=(5, 0))
        
        # Students section
        students_frame = ttk.LabelFrame(self.right_frame, text="Students")
        students_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=(0, 10))
        
        # Students list
        students_list_frame = ttk.Frame(students_frame)
        students_list_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        self.students_listbox = tk.Listbox(students_list_frame)
        self.students_listbox.pack(fill=tk.BOTH, expand=True)
        
        # Load students
        students = self.db_manager.get_class_students(class_id)
        for student in students:
            self.students_listbox.insert(tk.END, f"{student['first_name']} {student['last_name']} ({student['username']})")
        
        # Student management buttons
        student_button_frame = ttk.Frame(students_frame)
        student_button_frame.pack(fill=tk.X, padx=10, pady=(0, 10))
        
        ttk.Button(student_button_frame, text="Add Student", style='Primary.TButton',
                  command=lambda: self.add_student_to_class(class_id)).pack(side=tk.LEFT, padx=(0, 5))
        ttk.Button(student_button_frame, text="Remove Student", style='Secondary.TButton',
                  command=lambda: self.remove_student_from_class(class_id)).pack(side=tk.LEFT)
        
        # Resources section
        resources_frame = ttk.LabelFrame(self.right_frame, text="Resources")
        resources_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=(0, 10))
        
        # Resources list
        resources_list_frame = ttk.Frame(resources_frame)
        resources_list_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        self.resources_listbox = tk.Listbox(resources_list_frame)
        self.resources_listbox.pack(fill=tk.BOTH, expand=True)
        
        # Load resources
        resources = self.db_manager.get_class_resources(class_id)
        for resource in resources:
            self.resources_listbox.insert(tk.END, f"{resource['title']} ({resource['resource_type']})")
        
        # Resource management buttons
        resource_button_frame = ttk.Frame(resources_frame)
        resource_button_frame.pack(fill=tk.X, padx=10, pady=(0, 10))
        
        ttk.Button(resource_button_frame, text="Add Resource", style='Primary.TButton',
                  command=lambda: self.add_resource_to_class(class_id)).pack(side=tk.LEFT, padx=(0, 5))
        ttk.Button(resource_button_frame, text="View Resource", style='Secondary.TButton',
                  command=lambda: self.view_resource(class_id)).pack(side=tk.LEFT)
        
    def create_new_class(self):
        """Create a new class with subject and grade selection"""
        if not self.auth_manager.is_teacher():
            messagebox.showerror("Access Denied", "Only teachers can create classes")
            return
            
        dialog = NewClassDialog(self.parent, self.auth_manager.get_current_user()['id'], self.db_manager)
        self.parent.wait_window(dialog.dialog)
        
        if dialog.class_created:
            messagebox.showinfo("Success", "Class created successfully!")
            self.refresh_classes()
            
    def manage_subjects(self):
        """Open subject management dialog"""
        SubjectManagementDialog(self.parent, self.db_manager)
        
    def add_student_to_class(self, class_id):
        """Add a student to the class"""
        # Get all students not in this class
        cursor = self.db_manager.connection.execute("""
            SELECT u.* FROM users u
            WHERE u.user_type = 'student' AND u.is_active = 1
            AND u.id NOT IN (
                SELECT student_id FROM class_enrollments WHERE class_id = ?
            )
        """, (class_id,))
        available_students = [dict(row) for row in cursor.fetchall()]
        
        if not available_students:
            messagebox.showinfo("No Students", "No available students to add")
            return
            
        # Create selection dialog
        dialog = StudentSelectionDialog(self.parent, available_students)
        self.parent.wait_window(dialog.dialog)
        
        if dialog.selected_student:
            if self.db_manager.enroll_student(class_id, dialog.selected_student['id']):
                messagebox.showinfo("Success", f"Student {dialog.selected_student['first_name']} {dialog.selected_student['last_name']} added to class!")
                self.show_class_details(class_id)
            else:
                messagebox.showerror("Error", "Failed to add student to class")
                
    def remove_student_from_class(self, class_id):
        """Remove selected student from class"""
        selection = self.students_listbox.curselection()
        if not selection:
            messagebox.showwarning("No Selection", "Please select a student to remove")
            return
            
        # Get student info
        student_text = self.students_listbox.get(selection[0])
        username = student_text.split("(")[1].rstrip(")")
        
        # Confirm removal
        if messagebox.askyesno("Confirm Remove", f"Remove {student_text} from this class?"):
            # Remove student
            self.db_manager.connection.execute("""
                DELETE FROM class_enrollments 
                WHERE class_id = ? AND student_id = (
                    SELECT id FROM users WHERE username = ?
                )
            """, (class_id, username))
            self.db_manager.connection.commit()
            
            messagebox.showinfo("Success", "Student removed from class!")
            self.show_class_details(class_id)
            
    def add_resource_to_class(self, class_id):
        """Add a resource to the class"""
        dialog = ResourceDialog(self.parent, class_id, self.auth_manager.get_current_user()['id'], self.db_manager)
        self.parent.wait_window(dialog.dialog)
        
        if dialog.resource_added:
            messagebox.showinfo("Success", "Resource added successfully!")
            self.show_class_details(class_id)
            
    def view_resource(self, class_id):
        """View selected resource details"""
        selection = self.resources_listbox.curselection()
        if not selection:
            messagebox.showwarning("No Selection", "Please select a resource to view")
            return
            
        # Get resource details
        resources = self.db_manager.get_class_resources(class_id)
        if selection[0] < len(resources):
            resource = resources[selection[0]]
            ResourceViewDialog(self.parent, resource)
    
    # Calendar methods
    def update_calendar(self):
        """Update the calendar display"""
        # Clear existing calendar
        for widget in self.calendar_frame.winfo_children():
            widget.destroy()
            
        # Calendar header
        month_year = self.current_date.strftime("%B %Y")
        self.month_label.config(text=month_year)
        
        # Get calendar data
        cal = calendar.monthcalendar(self.current_date.year, self.current_date.month)
        
        # Day headers
        headers = ['Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat', 'Sun']
        for i, header in enumerate(headers):
            label = ttk.Label(self.calendar_frame, text=header, style='Heading.TLabel')
            label.grid(row=0, column=i, padx=2, pady=2, sticky='ew')
        
        # Calendar days
        for week_num, week in enumerate(cal):
            for day_num, day in enumerate(week):
                if day != 0:
                    day_frame = ttk.Frame(self.calendar_frame, relief='raised', borderwidth=1)
                    day_frame.grid(row=week_num + 1, column=day_num, padx=1, pady=1, sticky='nsew')
                    
                    # Day number
                    day_label = ttk.Label(day_frame, text=str(day), style='Info.TLabel')
                    day_label.pack(anchor='nw', padx=2, pady=2)
                    
                    # Add events for this day
                    self.add_events_to_day(day_frame, day)
        
        # Configure grid weights
        for i in range(7):
            self.calendar_frame.grid_columnconfigure(i, weight=1)
        for i in range(len(cal) + 1):
            self.calendar_frame.grid_rowconfigure(i, weight=1)
            
    def add_events_to_day(self, day_frame, day):
        """Add events to a specific day"""
        # Get events for this day
        date_str = f"{self.current_date.year}-{self.current_date.month:02d}-{day:02d}"
        events = self.db_manager.get_teacher_schedule(
            self.auth_manager.get_current_user()['id'],
            f"{date_str} 00:00:00",
            f"{date_str} 23:59:59"
        )
        
        # Add event labels
        for event in events[:3]:  # Show max 3 events per day
            event_label = ttk.Label(day_frame, text=f"• {event['title'][:15]}...", 
                                   style='Info.TLabel', foreground='blue')
            event_label.pack(anchor='w', padx=2)
            
    def prev_month(self):
        """Go to previous month"""
        if self.current_date.month == 1:
            self.current_date = self.current_date.replace(year=self.current_date.year - 1, month=12)
        else:
            self.current_date = self.current_date.replace(month=self.current_date.month - 1)
        self.update_calendar()
        
    def next_month(self):
        """Go to next month"""
        if self.current_date.month == 12:
            self.current_date = self.current_date.replace(year=self.current_date.year + 1, month=1)
        else:
            self.current_date = self.current_date.replace(month=self.current_date.month + 1)
        self.update_calendar()
        
    def create_schedule_event(self):
        """Create a new schedule event"""
        dialog = ScheduleEventDialog(self.parent, self.auth_manager.get_current_user()['id'], self.db_manager)
        self.parent.wait_window(dialog.dialog)
        
        if dialog.event_created:
            messagebox.showinfo("Success", "Schedule event created successfully!")
            self.update_calendar()

