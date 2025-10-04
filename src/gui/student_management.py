"""
Student Management window for TeacherApp
Allows admins and teachers to manage students and enroll them in classes
"""

import tkinter as tk
from tkinter import ttk, messagebox, simpledialog

class StudentManagementWindow:
    def __init__(self, parent, auth_manager, db_manager, navigate_callback):
        self.parent = parent
        self.auth_manager = auth_manager
        self.db_manager = db_manager
        self.navigate_callback = navigate_callback
        
        self.create_widgets()
        self.refresh_students()
        
    def create_widgets(self):
        """Create student management interface"""
        # Header
        header_frame = ttk.Frame(self.parent)
        header_frame.pack(fill=tk.X, padx=20, pady=10)
        
        ttk.Label(header_frame, text="Student Management", style='Title.TLabel').pack(side=tk.LEFT)
        
        # Back button
        back_button = ttk.Button(header_frame, text="← Back to Dashboard", 
                                style='Secondary.TButton',
                                command=lambda: self.navigate_callback("dashboard"))
        back_button.pack(side=tk.RIGHT)
        
        # Main content
        main_frame = ttk.Frame(self.parent)
        main_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=10)
        
        # Left panel - Students list
        left_frame = ttk.LabelFrame(main_frame, text="Students")
        left_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=(0, 10))
        
        # Student management buttons
        button_frame = ttk.Frame(left_frame)
        button_frame.pack(fill=tk.X, padx=10, pady=10)
        
        ttk.Button(button_frame, text="Add Student", style='Primary.TButton',
                  command=self.add_student).pack(side=tk.LEFT, padx=(0, 5))
        ttk.Button(button_frame, text="Edit Student", style='Secondary.TButton',
                  command=self.edit_student).pack(side=tk.LEFT, padx=(0, 5))
        ttk.Button(button_frame, text="Refresh", style='Secondary.TButton',
                  command=self.refresh_students).pack(side=tk.LEFT)
        
        # Students listbox
        list_frame = ttk.Frame(left_frame)
        list_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=(0, 10))
        
        self.students_listbox = tk.Listbox(list_frame)
        self.students_listbox.pack(fill=tk.BOTH, expand=True)
        self.students_listbox.bind('<<ListboxSelect>>', self.on_student_select)
        
        # Right panel - Student details and class enrollment
        self.right_frame = ttk.LabelFrame(main_frame, text="Student Details & Class Enrollment")
        self.right_frame.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True)
        
        # Initially show placeholder
        self.show_student_placeholder()
        
    def refresh_students(self):
        """Refresh the students list"""
        self.students_listbox.delete(0, tk.END)
        
        students = self.db_manager.get_all_students()
        for student in students:
            self.students_listbox.insert(tk.END, f"{student['first_name']} {student['last_name']} ({student['username']})")
        
        self.selected_student = None
        
    def on_student_select(self, event):
        """Handle student selection"""
        selection = self.students_listbox.curselection()
        if selection:
            students = self.db_manager.get_all_students()
            if selection[0] < len(students):
                self.selected_student = students[selection[0]]
                self.show_student_details(self.selected_student)
                
    def show_student_placeholder(self):
        """Show placeholder when no student is selected"""
        for widget in self.right_frame.winfo_children():
            widget.destroy()
            
        placeholder_frame = ttk.Frame(self.right_frame)
        placeholder_frame.pack(expand=True)
        
        ttk.Label(placeholder_frame, text="Select a student to view details and manage classes", 
                 style='Info.TLabel').pack(expand=True)
        
    def show_student_details(self, student):
        """Show detailed information about selected student"""
        # Clear right frame
        for widget in self.right_frame.winfo_children():
            widget.destroy()
            
        # Student info frame
        info_frame = ttk.Frame(self.right_frame)
        info_frame.pack(fill=tk.X, padx=10, pady=10)
        
        ttk.Label(info_frame, text=f"{student['first_name']} {student['last_name']}", 
                 style='Heading.TLabel').pack(anchor=tk.W)
        ttk.Label(info_frame, text=f"Username: {student['username']}", 
                 style='Info.TLabel').pack(anchor=tk.W, pady=(5, 0))
        ttk.Label(info_frame, text=f"Email: {student['email']}", 
                 style='Info.TLabel').pack(anchor=tk.W, pady=(5, 0))
        
        # Enrolled classes section
        classes_frame = ttk.LabelFrame(self.right_frame, text="Enrolled Classes")
        classes_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=(0, 10))
        
        # Classes list
        classes_list_frame = ttk.Frame(classes_frame)
        classes_list_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        self.classes_listbox = tk.Listbox(classes_list_frame)
        self.classes_listbox.pack(fill=tk.BOTH, expand=True)
        
        # Load enrolled classes
        cursor = self.db_manager.connection.execute("""
            SELECT c.*, s.name as subject_name FROM classes c
            JOIN class_enrollments ce ON c.id = ce.class_id
            JOIN subjects s ON c.subject_id = s.id
            WHERE ce.student_id = ?
            ORDER BY c.grade_level, s.name
        """, (student['id'],))
        enrolled_classes = [dict(row) for row in cursor.fetchall()]
        
        for class_data in enrolled_classes:
            self.classes_listbox.insert(tk.END, 
                f"{class_data['name']} - {class_data['subject_name']} (Grade {class_data['grade_level']})")
        
        # Class management buttons
        class_button_frame = ttk.Frame(classes_frame)
        class_button_frame.pack(fill=tk.X, padx=10, pady=(0, 10))
        
        ttk.Button(class_button_frame, text="Enroll in Class", style='Primary.TButton',
                  command=lambda: self.enroll_student_in_class(student['id'])).pack(side=tk.LEFT, padx=(0, 5))
        ttk.Button(class_button_frame, text="Remove from Class", style='Secondary.TButton',
                  command=lambda: self.remove_student_from_class(student['id'])).pack(side=tk.LEFT)
        
    def add_student(self):
        """Add a new student"""
        dialog = AddStudentDialog(self.parent, self.db_manager)
        self.parent.wait_window(dialog.dialog)
        
        if dialog.student_added:
            messagebox.showinfo("Success", "Student added successfully!")
            self.refresh_students()
            
    def edit_student(self):
        """Edit selected student"""
        if not self.selected_student:
            messagebox.showwarning("No Selection", "Please select a student to edit")
            return
            
        dialog = EditStudentDialog(self.parent, self.selected_student, self.db_manager)
        self.parent.wait_window(dialog.dialog)
        
        if dialog.student_updated:
            messagebox.showinfo("Success", "Student updated successfully!")
            self.refresh_students()
            
    def enroll_student_in_class(self, student_id):
        """Enroll student in a class"""
        # Get available classes (not already enrolled)
        cursor = self.db_manager.connection.execute("""
            SELECT c.*, s.name as subject_name FROM classes c
            JOIN subjects s ON c.subject_id = s.id
            WHERE c.id NOT IN (
                SELECT class_id FROM class_enrollments WHERE student_id = ?
            )
            ORDER BY c.grade_level, s.name
        """, (student_id,))
        available_classes = [dict(row) for row in cursor.fetchall()]
        
        if not available_classes:
            messagebox.showinfo("No Classes", "No available classes to enroll in")
            return
            
        # Create selection dialog
        dialog = ClassSelectionDialog(self.parent, available_classes)
        self.parent.wait_window(dialog.dialog)
        
        if dialog.selected_class:
            if self.db_manager.enroll_student(dialog.selected_class['id'], student_id):
                messagebox.showinfo("Success", 
                    f"Student enrolled in {dialog.selected_class['name']} successfully!")
                self.show_student_details(self.selected_student)
            else:
                messagebox.showerror("Error", "Failed to enroll student in class")
                
    def remove_student_from_class(self, student_id):
        """Remove student from selected class"""
        selection = self.classes_listbox.curselection()
        if not selection:
            messagebox.showwarning("No Selection", "Please select a class to remove student from")
            return
            
        # Get enrolled classes
        cursor = self.db_manager.connection.execute("""
            SELECT c.* FROM classes c
            JOIN class_enrollments ce ON c.id = ce.class_id
            WHERE ce.student_id = ?
        """, (student_id,))
        enrolled_classes = [dict(row) for row in cursor.fetchall()]
        
        if selection[0] < len(enrolled_classes):
            class_data = enrolled_classes[selection[0]]
            
            # Confirm removal
            if messagebox.askyesno("Confirm Removal", 
                                  f"Remove student from {class_data['name']}?"):
                # Remove student
                self.db_manager.connection.execute("""
                    DELETE FROM class_enrollments 
                    WHERE class_id = ? AND student_id = ?
                """, (class_data['id'], student_id))
                self.db_manager.connection.commit()
                
                messagebox.showinfo("Success", "Student removed from class!")
                self.show_student_details(self.selected_student)

class AddStudentDialog:
    def __init__(self, parent, db_manager):
        self.parent = parent
        self.db_manager = db_manager
        self.student_added = False
        
        self.dialog = tk.Toplevel(parent)
        self.dialog.title("Add New Student")
        self.dialog.geometry("400x500")
        self.dialog.resizable(False, False)
        
        self.dialog.transient(parent)
        self.dialog.grab_set()
        
        self.create_widgets()
        
    def create_widgets(self):
        """Create add student form"""
        main_frame = ttk.Frame(self.dialog)
        main_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=20)
        
        ttk.Label(main_frame, text="Add New Student", style='Heading.TLabel').pack(pady=(0, 20))
        
        # Username
        ttk.Label(main_frame, text="Username:", style='Info.TLabel').pack(anchor=tk.W)
        self.username_entry = ttk.Entry(main_frame, width=40)
        self.username_entry.pack(fill=tk.X, pady=(0, 15))
        
        # Email
        ttk.Label(main_frame, text="Email:", style='Info.TLabel').pack(anchor=tk.W)
        self.email_entry = ttk.Entry(main_frame, width=40)
        self.email_entry.pack(fill=tk.X, pady=(0, 15))
        
        # First Name
        ttk.Label(main_frame, text="First Name:", style='Info.TLabel').pack(anchor=tk.W)
        self.first_name_entry = ttk.Entry(main_frame, width=40)
        self.first_name_entry.pack(fill=tk.X, pady=(0, 15))
        
        # Last Name
        ttk.Label(main_frame, text="Last Name:", style='Info.TLabel').pack(anchor=tk.W)
        self.last_name_entry = ttk.Entry(main_frame, width=40)
        self.last_name_entry.pack(fill=tk.X, pady=(0, 15))
        
        # Password
        ttk.Label(main_frame, text="Password:", style='Info.TLabel').pack(anchor=tk.W)
        self.password_entry = ttk.Entry(main_frame, width=40, show="*")
        self.password_entry.pack(fill=tk.X, pady=(0, 20))
        
        # Buttons
        button_frame = ttk.Frame(main_frame)
        button_frame.pack(fill=tk.X)
        
        ttk.Button(button_frame, text="Add Student", style='Primary.TButton',
                  command=self.add_student).pack(side=tk.RIGHT, padx=(10, 0))
        ttk.Button(button_frame, text="Cancel", style='Secondary.TButton',
                  command=self.dialog.destroy).pack(side=tk.RIGHT)
        
    def add_student(self):
        """Add the student"""
        username = self.username_entry.get().strip()
        email = self.email_entry.get().strip()
        first_name = self.first_name_entry.get().strip()
        last_name = self.last_name_entry.get().strip()
        password = self.password_entry.get()
        
        # Validate inputs
        if not all([username, email, first_name, last_name, password]):
            messagebox.showerror("Error", "Please fill in all fields")
            return
            
        if len(password) < 6:
            messagebox.showerror("Error", "Password must be at least 6 characters long")
            return
            
        # Add student
        if self.db_manager.create_user(username, email, password, first_name, last_name, "student"):
            self.student_added = True
            self.dialog.destroy()
        else:
            messagebox.showerror("Error", "Failed to add student. Username or email may already exist.")

class EditStudentDialog:
    def __init__(self, parent, student, db_manager):
        self.parent = parent
        self.student = student
        self.db_manager = db_manager
        self.student_updated = False
        
        self.dialog = tk.Toplevel(parent)
        self.dialog.title("Edit Student")
        self.dialog.geometry("400x500")
        self.dialog.resizable(False, False)
        
        self.dialog.transient(parent)
        self.dialog.grab_set()
        
        self.create_widgets()
        
    def create_widgets(self):
        """Create edit student form"""
        main_frame = ttk.Frame(self.dialog)
        main_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=20)
        
        ttk.Label(main_frame, text="Edit Student", style='Heading.TLabel').pack(pady=(0, 20))
        
        # Username
        ttk.Label(main_frame, text="Username:", style='Info.TLabel').pack(anchor=tk.W)
        self.username_entry = ttk.Entry(main_frame, width=40)
        self.username_entry.pack(fill=tk.X, pady=(0, 15))
        self.username_entry.insert(0, self.student['username'])
        
        # Email
        ttk.Label(main_frame, text="Email:", style='Info.TLabel').pack(anchor=tk.W)
        self.email_entry = ttk.Entry(main_frame, width=40)
        self.email_entry.pack(fill=tk.X, pady=(0, 15))
        self.email_entry.insert(0, self.student['email'])
        
        # First Name
        ttk.Label(main_frame, text="First Name:", style='Info.TLabel').pack(anchor=tk.W)
        self.first_name_entry = ttk.Entry(main_frame, width=40)
        self.first_name_entry.pack(fill=tk.X, pady=(0, 15))
        self.first_name_entry.insert(0, self.student['first_name'])
        
        # Last Name
        ttk.Label(main_frame, text="Last Name:", style='Info.TLabel').pack(anchor=tk.W)
        self.last_name_entry = ttk.Entry(main_frame, width=40)
        self.last_name_entry.pack(fill=tk.X, pady=(0, 15))
        self.last_name_entry.insert(0, self.student['last_name'])
        
        # Password
        ttk.Label(main_frame, text="New Password (leave blank to keep current):", style='Info.TLabel').pack(anchor=tk.W)
        self.password_entry = ttk.Entry(main_frame, width=40, show="*")
        self.password_entry.pack(fill=tk.X, pady=(0, 20))
        
        # Buttons
        button_frame = ttk.Frame(main_frame)
        button_frame.pack(fill=tk.X)
        
        ttk.Button(button_frame, text="Update Student", style='Primary.TButton',
                  command=self.update_student).pack(side=tk.RIGHT, padx=(10, 0))
        ttk.Button(button_frame, text="Cancel", style='Secondary.TButton',
                  command=self.dialog.destroy).pack(side=tk.RIGHT)
        
    def update_student(self):
        """Update the student"""
        username = self.username_entry.get().strip()
        email = self.email_entry.get().strip()
        first_name = self.first_name_entry.get().strip()
        last_name = self.last_name_entry.get().strip()
        password = self.password_entry.get()
        
        # Validate inputs
        if not all([username, email, first_name, last_name]):
            messagebox.showerror("Error", "Please fill in all required fields")
            return
            
        try:
            # Update student
            if password:
                password_hash = self.db_manager._hash_password(password)
                self.db_manager.connection.execute("""
                    UPDATE users SET username = ?, email = ?, first_name = ?, 
                                   last_name = ?, password_hash = ?
                    WHERE id = ?
                """, (username, email, first_name, last_name, password_hash, self.student['id']))
            else:
                self.db_manager.connection.execute("""
                    UPDATE users SET username = ?, email = ?, first_name = ?, 
                                   last_name = ?
                    WHERE id = ?
                """, (username, email, first_name, last_name, self.student['id']))
            
            self.db_manager.connection.commit()
            self.student_updated = True
            self.dialog.destroy()
            
        except Exception as e:
            messagebox.showerror("Error", f"Failed to update student: {str(e)}")

class ClassSelectionDialog:
    def __init__(self, parent, classes):
        self.parent = parent
        self.classes = classes
        self.selected_class = None
        
        self.dialog = tk.Toplevel(parent)
        self.dialog.title("Select Class")
        self.dialog.geometry("500x400")
        self.dialog.resizable(False, False)
        
        self.dialog.transient(parent)
        self.dialog.grab_set()
        
        self.create_widgets()
        
    def create_widgets(self):
        """Create class selection interface"""
        main_frame = ttk.Frame(self.dialog)
        main_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=20)
        
        ttk.Label(main_frame, text="Select Class to Enroll Student:", style='Heading.TLabel').pack(pady=(0, 10))
        
        # Classes listbox
        list_frame = ttk.Frame(main_frame)
        list_frame.pack(fill=tk.BOTH, expand=True)
        
        self.classes_listbox = tk.Listbox(list_frame)
        self.classes_listbox.pack(fill=tk.BOTH, expand=True)
        
        for class_data in self.classes:
            self.classes_listbox.insert(tk.END, 
                f"{class_data['name']} - {class_data['subject_name']} (Grade {class_data['grade_level']})")
        
        # Buttons
        button_frame = ttk.Frame(main_frame)
        button_frame.pack(fill=tk.X, pady=(10, 0))
        
        ttk.Button(button_frame, text="Select", style='Primary.TButton',
                  command=self.select_class).pack(side=tk.RIGHT, padx=(10, 0))
        ttk.Button(button_frame, text="Cancel", style='Secondary.TButton',
                  command=self.dialog.destroy).pack(side=tk.RIGHT)
        
    def select_class(self):
        """Select the chosen class"""
        selection = self.classes_listbox.curselection()
        if selection:
            self.selected_class = self.classes[selection[0]]
            self.dialog.destroy()
