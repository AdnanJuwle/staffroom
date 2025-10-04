"""
Dialog classes for enhanced class management features
"""

import tkinter as tk
from tkinter import ttk, messagebox
from datetime import datetime, timedelta

# Import existing dialog classes
from src.gui.class_management import StudentSelectionDialog, ResourceDialog, ResourceViewDialog

class NewClassDialog:
    def __init__(self, parent, user_id, db_manager):
        self.parent = parent
        self.user_id = user_id
        self.db_manager = db_manager
        self.class_created = False
        
        self.dialog = tk.Toplevel(parent)
        self.dialog.title("Create New Class")
        self.dialog.geometry("500x600")
        self.dialog.resizable(False, False)
        
        self.dialog.transient(parent)
        self.dialog.grab_set()
        
        self.create_widgets()
        
    def create_widgets(self):
        """Create new class form"""
        main_frame = ttk.Frame(self.dialog)
        main_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=20)
        
        ttk.Label(main_frame, text="Create New Class", style='Heading.TLabel').pack(pady=(0, 20))
        
        # Class name
        ttk.Label(main_frame, text="Class Name:", style='Info.TLabel').pack(anchor=tk.W)
        self.class_name_entry = ttk.Entry(main_frame, width=50)
        self.class_name_entry.pack(fill=tk.X, pady=(0, 15))
        
        # Subject selection
        ttk.Label(main_frame, text="Subject:", style='Info.TLabel').pack(anchor=tk.W)
        self.subject_var = tk.StringVar()
        subject_combo = ttk.Combobox(main_frame, textvariable=self.subject_var, state="readonly")
        subject_combo.pack(fill=tk.X, pady=(0, 15))
        
        # Load subjects
        subjects = self.db_manager.get_all_subjects()
        subject_options = [f"{s['name']}" for s in subjects]
        subject_combo['values'] = subject_options
        
        # Grade level
        ttk.Label(main_frame, text="Grade Level:", style='Info.TLabel').pack(anchor=tk.W)
        self.grade_var = tk.StringVar(value="1")
        grade_frame = ttk.Frame(main_frame)
        grade_frame.pack(fill=tk.X, pady=(0, 15))
        
        # Grade selection (1-12)
        grades = [str(i) for i in range(1, 13)]
        grade_combo = ttk.Combobox(grade_frame, textvariable=self.grade_var, state="readonly")
        grade_combo['values'] = grades
        grade_combo.pack(side=tk.LEFT)
        
        ttk.Label(grade_frame, text="(1st to 12th Grade)", style='Info.TLabel').pack(side=tk.LEFT, padx=(10, 0))
        
        # Description
        ttk.Label(main_frame, text="Description:", style='Info.TLabel').pack(anchor=tk.W)
        self.description_text = tk.Text(main_frame, height=4, wrap=tk.WORD)
        self.description_text.pack(fill=tk.X, pady=(0, 20))
        
        # Buttons
        button_frame = ttk.Frame(main_frame)
        button_frame.pack(fill=tk.X)
        
        ttk.Button(button_frame, text="Create Class", style='Primary.TButton',
                  command=self.create_class).pack(side=tk.RIGHT, padx=(10, 0))
        ttk.Button(button_frame, text="Cancel", style='Secondary.TButton',
                  command=self.dialog.destroy).pack(side=tk.RIGHT)
        
    def create_class(self):
        """Create the class"""
        class_name = self.class_name_entry.get().strip()
        subject_name = self.subject_var.get()
        grade_level = int(self.grade_var.get())
        description = self.description_text.get("1.0", tk.END).strip()
        
        if not class_name:
            messagebox.showerror("Error", "Please enter a class name")
            return
            
        if not subject_name:
            messagebox.showerror("Error", "Please select a subject")
            return
            
        # Get subject ID
        subjects = self.db_manager.get_all_subjects()
        subject_id = None
        for subject in subjects:
            if subject['name'] == subject_name:
                subject_id = subject['id']
                break
                
        if not subject_id:
            messagebox.showerror("Error", "Selected subject not found")
            return
            
        class_id = self.db_manager.create_class(class_name, description, subject_id, grade_level, self.user_id)
        
        if class_id:
            self.class_created = True
            self.dialog.destroy()
        else:
            messagebox.showerror("Error", "Failed to create class")

class SubjectManagementDialog:
    def __init__(self, parent, db_manager):
        self.parent = parent
        self.db_manager = db_manager
        
        self.dialog = tk.Toplevel(parent)
        self.dialog.title("Manage Subjects")
        self.dialog.geometry("600x500")
        self.dialog.resizable(True, True)
        
        self.dialog.transient(parent)
        self.dialog.grab_set()
        
        self.create_widgets()
        self.refresh_subjects()
        
    def create_widgets(self):
        """Create subject management interface"""
        main_frame = ttk.Frame(self.dialog)
        main_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=20)
        
        ttk.Label(main_frame, text="Manage Subjects", style='Heading.TLabel').pack(pady=(0, 20))
        
        # Subjects list
        list_frame = ttk.LabelFrame(main_frame, text="Available Subjects")
        list_frame.pack(fill=tk.BOTH, expand=True, pady=(0, 20))
        
        # Treeview for subjects
        tree_frame = ttk.Frame(list_frame)
        tree_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        self.subjects_tree = ttk.Treeview(tree_frame, columns=('type',), show='tree headings')
        self.subjects_tree.heading('#0', text='Subject Name')
        self.subjects_tree.heading('type', text='Type')
        
        self.subjects_tree.column('#0', width=300)
        self.subjects_tree.column('type', width=100)
        
        # Scrollbar
        tree_scroll = ttk.Scrollbar(tree_frame, orient=tk.VERTICAL, command=self.subjects_tree.yview)
        self.subjects_tree.configure(yscrollcommand=tree_scroll.set)
        
        self.subjects_tree.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        tree_scroll.pack(side=tk.RIGHT, fill=tk.Y)
        
        # Buttons
        button_frame = ttk.Frame(main_frame)
        button_frame.pack(fill=tk.X)
        
        ttk.Button(button_frame, text="Add Custom Subject", style='Primary.TButton',
                  command=self.add_custom_subject).pack(side=tk.LEFT, padx=(0, 10))
        ttk.Button(button_frame, text="Close", style='Secondary.TButton',
                  command=self.dialog.destroy).pack(side=tk.RIGHT)
        
    def refresh_subjects(self):
        """Refresh the subjects list"""
        for item in self.subjects_tree.get_children():
            self.subjects_tree.delete(item)
            
        subjects = self.db_manager.get_all_subjects()
        
        # Group by type
        standard_subjects = []
        custom_subjects = []
        
        for subject in subjects:
            if subject['is_custom']:
                custom_subjects.append(subject)
            else:
                standard_subjects.append(subject)
        
        # Add standard subjects
        if standard_subjects:
            standard_node = self.subjects_tree.insert('', 'end', text='Standard Subjects', values=('',))
            for subject in standard_subjects:
                self.subjects_tree.insert(standard_node, 'end', text=subject['name'], 
                                        values=('Standard',))
        
        # Add custom subjects
        if custom_subjects:
            custom_node = self.subjects_tree.insert('', 'end', text='Custom Subjects', values=('',))
            for subject in custom_subjects:
                self.subjects_tree.insert(custom_node, 'end', text=subject['name'], 
                                        values=('Custom',))
        
    def add_custom_subject(self):
        """Add a custom subject"""
        dialog = AddCustomSubjectDialog(self.dialog, self.db_manager)
        self.dialog.wait_window(dialog.dialog)
        
        if dialog.subject_added:
            messagebox.showinfo("Success", "Custom subject added successfully!")
            self.refresh_subjects()

class AddCustomSubjectDialog:
    def __init__(self, parent, db_manager):
        self.parent = parent
        self.db_manager = db_manager
        self.subject_added = False
        
        self.dialog = tk.Toplevel(parent)
        self.dialog.title("Add Custom Subject")
        self.dialog.geometry("400x300")
        self.dialog.resizable(False, False)
        
        self.dialog.transient(parent)
        self.dialog.grab_set()
        
        self.create_widgets()
        
    def create_widgets(self):
        """Create add custom subject form"""
        main_frame = ttk.Frame(self.dialog)
        main_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=20)
        
        ttk.Label(main_frame, text="Add Custom Subject", style='Heading.TLabel').pack(pady=(0, 20))
        
        # Subject name
        ttk.Label(main_frame, text="Subject Name:", style='Info.TLabel').pack(anchor=tk.W)
        self.subject_name_entry = ttk.Entry(main_frame, width=40)
        self.subject_name_entry.pack(fill=tk.X, pady=(0, 15))
        
        # Description
        ttk.Label(main_frame, text="Description:", style='Info.TLabel').pack(anchor=tk.W)
        self.description_text = tk.Text(main_frame, height=6, wrap=tk.WORD)
        self.description_text.pack(fill=tk.X, pady=(0, 20))
        
        # Buttons
        button_frame = ttk.Frame(main_frame)
        button_frame.pack(fill=tk.X)
        
        ttk.Button(button_frame, text="Add Subject", style='Primary.TButton',
                  command=self.add_subject).pack(side=tk.RIGHT, padx=(10, 0))
        ttk.Button(button_frame, text="Cancel", style='Secondary.TButton',
                  command=self.dialog.destroy).pack(side=tk.RIGHT)
        
    def add_subject(self):
        """Add the custom subject"""
        subject_name = self.subject_name_entry.get().strip()
        description = self.description_text.get("1.0", tk.END).strip()
        
        if not subject_name:
            messagebox.showerror("Error", "Please enter a subject name")
            return
            
        # For custom subjects, we'll use a dummy user ID (admin)
        admin_id = 1  # Assuming admin has ID 1
        
        subject_id = self.db_manager.create_custom_subject(subject_name, description, admin_id)
        
        if subject_id:
            self.subject_added = True
            self.dialog.destroy()
        else:
            messagebox.showerror("Error", "Failed to add subject. Subject name may already exist.")

class ScheduleEventDialog:
    def __init__(self, parent, user_id, db_manager):
        self.parent = parent
        self.user_id = user_id
        self.db_manager = db_manager
        self.event_created = False
        
        self.dialog = tk.Toplevel(parent)
        self.dialog.title("Create Schedule Event")
        self.dialog.geometry("500x600")
        self.dialog.resizable(False, False)
        
        self.dialog.transient(parent)
        self.dialog.grab_set()
        
        self.create_widgets()
        
    def create_widgets(self):
        """Create schedule event form"""
        main_frame = ttk.Frame(self.dialog)
        main_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=20)
        
        ttk.Label(main_frame, text="Create Schedule Event", style='Heading.TLabel').pack(pady=(0, 20))
        
        # Class selection
        ttk.Label(main_frame, text="Class:", style='Info.TLabel').pack(anchor=tk.W)
        self.class_var = tk.StringVar()
        class_combo = ttk.Combobox(main_frame, textvariable=self.class_var, state="readonly")
        class_combo.pack(fill=tk.X, pady=(0, 15))
        
        # Load classes
        classes = self.db_manager.get_teacher_classes(self.user_id)
        class_options = [f"{c['name']} - {c['subject_name']} (Grade {c['grade_level']})" for c in classes]
        class_combo['values'] = class_options
        
        # Event title
        ttk.Label(main_frame, text="Event Title:", style='Info.TLabel').pack(anchor=tk.W)
        self.title_entry = ttk.Entry(main_frame, width=50)
        self.title_entry.pack(fill=tk.X, pady=(0, 15))
        
        # Description
        ttk.Label(main_frame, text="Description:", style='Info.TLabel').pack(anchor=tk.W)
        self.description_text = tk.Text(main_frame, height=4, wrap=tk.WORD)
        self.description_text.pack(fill=tk.X, pady=(0, 15))
        
        # Date and time
        datetime_frame = ttk.Frame(main_frame)
        datetime_frame.pack(fill=tk.X, pady=(0, 15))
        
        # Start date
        ttk.Label(datetime_frame, text="Start Date:", style='Info.TLabel').pack(anchor=tk.W)
        self.start_date_entry = ttk.Entry(datetime_frame, width=15)
        self.start_date_entry.pack(side=tk.LEFT, padx=(0, 10))
        self.start_date_entry.insert(0, datetime.now().strftime("%Y-%m-%d"))
        
        # Start time
        ttk.Label(datetime_frame, text="Start Time:", style='Info.TLabel').pack(anchor=tk.W, pady=(10, 0))
        self.start_time_entry = ttk.Entry(datetime_frame, width=10)
        self.start_time_entry.pack(side=tk.LEFT, padx=(0, 10))
        self.start_time_entry.insert(0, "09:00")
        
        # End time
        ttk.Label(datetime_frame, text="End Time:", style='Info.TLabel').pack(anchor=tk.W, pady=(10, 0))
        self.end_time_entry = ttk.Entry(datetime_frame, width=10)
        self.end_time_entry.pack(side=tk.LEFT)
        self.end_time_entry.insert(0, "10:00")
        
        # Recurring options
        recurring_frame = ttk.LabelFrame(main_frame, text="Recurring Options")
        recurring_frame.pack(fill=tk.X, pady=(0, 20))
        
        self.is_recurring_var = tk.BooleanVar()
        ttk.Checkbutton(recurring_frame, text="Make this a recurring event", 
                       variable=self.is_recurring_var).pack(anchor=tk.W, padx=10, pady=5)
        
        self.recurrence_var = tk.StringVar(value="weekly")
        recurrence_frame = ttk.Frame(recurring_frame)
        recurrence_frame.pack(fill=tk.X, padx=10, pady=(0, 10))
        
        ttk.Radiobutton(recurrence_frame, text="Daily", variable=self.recurrence_var, 
                       value="daily").pack(side=tk.LEFT, padx=(0, 20))
        ttk.Radiobutton(recurrence_frame, text="Weekly", variable=self.recurrence_var, 
                       value="weekly").pack(side=tk.LEFT, padx=(0, 20))
        ttk.Radiobutton(recurrence_frame, text="Monthly", variable=self.recurrence_var, 
                       value="monthly").pack(side=tk.LEFT)
        
        # Buttons
        button_frame = ttk.Frame(main_frame)
        button_frame.pack(fill=tk.X)
        
        ttk.Button(button_frame, text="Create Event", style='Primary.TButton',
                  command=self.create_event).pack(side=tk.RIGHT, padx=(10, 0))
        ttk.Button(button_frame, text="Cancel", style='Secondary.TButton',
                  command=self.dialog.destroy).pack(side=tk.RIGHT)
        
    def create_event(self):
        """Create the schedule event"""
        class_text = self.class_var.get()
        title = self.title_entry.get().strip()
        description = self.description_text.get("1.0", tk.END).strip()
        start_date = self.start_date_entry.get().strip()
        start_time = self.start_time_entry.get().strip()
        end_time = self.end_time_entry.get().strip()
        is_recurring = self.is_recurring_var.get()
        recurrence_pattern = self.recurrence_var.get() if is_recurring else None
        
        if not class_text:
            messagebox.showerror("Error", "Please select a class")
            return
            
        if not title:
            messagebox.showerror("Error", "Please enter an event title")
            return
            
        # Get class ID
        classes = self.db_manager.get_teacher_classes(self.user_id)
        class_id = None
        for class_data in classes:
            class_option = f"{class_data['name']} - {class_data['subject_name']} (Grade {class_data['grade_level']})"
            if class_option == class_text:
                class_id = class_data['id']
                break
                
        if not class_id:
            messagebox.showerror("Error", "Selected class not found")
            return
            
        # Create datetime strings
        start_datetime = f"{start_date} {start_time}:00"
        end_datetime = f"{start_date} {end_time}:00"
        
        event_id = self.db_manager.create_schedule_event(
            class_id, title, description, start_datetime, end_datetime,
            self.user_id, is_recurring, recurrence_pattern
        )
        
        if event_id:
            self.event_created = True
            self.dialog.destroy()
        else:
            messagebox.showerror("Error", "Failed to create schedule event")
