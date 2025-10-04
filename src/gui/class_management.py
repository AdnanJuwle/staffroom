"""
Class Management window for TeacherApp
Handles class creation, student enrollment, and resource management
"""

import tkinter as tk
from tkinter import ttk, messagebox, simpledialog
from datetime import datetime

class ClassManagementWindow:
    def __init__(self, parent, auth_manager, db_manager, navigate_callback):
        self.parent = parent
        self.auth_manager = auth_manager
        self.db_manager = db_manager
        self.navigate_callback = navigate_callback
        
        self.create_widgets()
        self.refresh_classes()
        
    def create_widgets(self):
        """Create class management interface"""
        # Header
        header_frame = ttk.Frame(self.parent)
        header_frame.pack(fill=tk.X, padx=20, pady=10)
        
        ttk.Label(header_frame, text="Class Management", style='Title.TLabel').pack(side=tk.LEFT)
        
        # Back button
        back_button = ttk.Button(header_frame, text="← Back to Dashboard", 
                                style='Secondary.TButton',
                                command=lambda: self.navigate_callback("dashboard"))
        back_button.pack(side=tk.RIGHT)
        
        # Main content
        main_frame = ttk.Frame(self.parent)
        main_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=10)
        
        # Left panel - Classes list
        left_frame = ttk.LabelFrame(main_frame, text="My Classes")
        left_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=(0, 10))
        
        # Classes listbox
        list_frame = ttk.Frame(left_frame)
        list_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        self.classes_listbox = tk.Listbox(list_frame)
        self.classes_listbox.pack(fill=tk.BOTH, expand=True)
        self.classes_listbox.bind('<<ListboxSelect>>', self.on_class_select)
        
        # Class management buttons
        button_frame = ttk.Frame(left_frame)
        button_frame.pack(fill=tk.X, padx=10, pady=(0, 10))
        
        ttk.Button(button_frame, text="New Class", style='Primary.TButton',
                  command=self.create_new_class).pack(side=tk.LEFT, padx=(0, 5))
        ttk.Button(button_frame, text="Delete Class", style='Secondary.TButton',
                  command=self.delete_class).pack(side=tk.LEFT)
        
        # Right panel - Class details
        self.right_frame = ttk.LabelFrame(main_frame, text="Class Details")
        self.right_frame.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True)
        
        # Initially show placeholder
        self.show_class_placeholder()
        
    def show_class_placeholder(self):
        """Show placeholder when no class is selected"""
        for widget in self.right_frame.winfo_children():
            widget.destroy()
            
        placeholder_frame = ttk.Frame(self.right_frame)
        placeholder_frame.pack(expand=True)
        
        ttk.Label(placeholder_frame, text="Select a class to view details", 
                 style='Info.TLabel').pack(expand=True)
        
    def refresh_classes(self):
        """Refresh the classes list"""
        self.classes_listbox.delete(0, tk.END)
        
        if self.auth_manager.is_teacher():
            classes = self.db_manager.get_teacher_classes(self.auth_manager.get_current_user()['id'])
            for class_data in classes:
                self.classes_listbox.insert(tk.END, f"{class_data['name']} (ID: {class_data['id']})")
        elif self.auth_manager.is_student():
            # Show enrolled classes for students
            user_id = self.auth_manager.get_current_user()['id']
            cursor = self.db_manager.connection.execute("""
                SELECT c.* FROM classes c
                JOIN class_enrollments ce ON c.id = ce.class_id
                WHERE ce.student_id = ?
            """, (user_id,))
            classes = [dict(row) for row in cursor.fetchall()]
            for class_data in classes:
                self.classes_listbox.insert(tk.END, f"{class_data['name']} (ID: {class_data['id']})")
        
        self.selected_class_id = None
        
    def on_class_select(self, event):
        """Handle class selection"""
        selection = self.classes_listbox.curselection()
        if selection:
            class_text = self.classes_listbox.get(selection[0])
            # Extract class ID from the text
            class_id = int(class_text.split("ID: ")[1].rstrip(")"))
            self.selected_class_id = class_id
            self.show_class_details(class_id)
            
    def show_class_details(self, class_id):
        """Show detailed information about selected class"""
        # Clear right frame
        for widget in self.right_frame.winfo_children():
            widget.destroy()
            
        # Get class data
        cursor = self.db_manager.connection.execute("SELECT * FROM classes WHERE id = ?", (class_id,))
        class_data = cursor.fetchone()
        
        if not class_data:
            return
            
        # Class info frame
        info_frame = ttk.Frame(self.right_frame)
        info_frame.pack(fill=tk.X, padx=10, pady=10)
        
        ttk.Label(info_frame, text=class_data['name'], style='Heading.TLabel').pack(anchor=tk.W)
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
        
        # Student management buttons (teachers only)
        if self.auth_manager.is_teacher():
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
        
        # Resource management buttons (teachers only)
        if self.auth_manager.is_teacher():
            resource_button_frame = ttk.Frame(resources_frame)
            resource_button_frame.pack(fill=tk.X, padx=10, pady=(0, 10))
            
            ttk.Button(resource_button_frame, text="Add Resource", style='Primary.TButton',
                      command=lambda: self.add_resource_to_class(class_id)).pack(side=tk.LEFT, padx=(0, 5))
            ttk.Button(resource_button_frame, text="View Resource", style='Secondary.TButton',
                      command=lambda: self.view_resource(class_id)).pack(side=tk.LEFT)
        
    def create_new_class(self):
        """Create a new class"""
        if not self.auth_manager.is_teacher():
            messagebox.showerror("Access Denied", "Only teachers can create classes")
            return
            
        # Get class details
        name = simpledialog.askstring("New Class", "Enter class name:")
        if not name:
            return
            
        description = simpledialog.askstring("New Class", "Enter class description (optional):")
        if description is None:
            return
            
        # Create class
        teacher_id = self.auth_manager.get_current_user()['id']
        class_id = self.db_manager.create_class(name, description or "", teacher_id)
        
        if class_id:
            messagebox.showinfo("Success", f"Class '{name}' created successfully!")
            self.refresh_classes()
        else:
            messagebox.showerror("Error", "Failed to create class")
            
    def delete_class(self):
        """Delete selected class"""
        if not self.selected_class_id:
            messagebox.showwarning("No Selection", "Please select a class to delete")
            return
            
        if not self.auth_manager.is_teacher():
            messagebox.showerror("Access Denied", "Only teachers can delete classes")
            return
            
        # Confirm deletion
        if messagebox.askyesno("Confirm Delete", "Are you sure you want to delete this class?"):
            # Delete class and related data
            self.db_manager.connection.execute("DELETE FROM class_enrollments WHERE class_id = ?", 
                                             (self.selected_class_id,))
            self.db_manager.connection.execute("DELETE FROM resources WHERE class_id = ?", 
                                             (self.selected_class_id,))
            self.db_manager.connection.execute("DELETE FROM classes WHERE id = ?", 
                                             (self.selected_class_id,))
            self.db_manager.connection.commit()
            
            messagebox.showinfo("Success", "Class deleted successfully!")
            self.refresh_classes()
            self.show_class_placeholder()
            
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

class StudentSelectionDialog:
    def __init__(self, parent, students):
        self.parent = parent
        self.students = students
        self.selected_student = None
        
        self.dialog = tk.Toplevel(parent)
        self.dialog.title("Select Student")
        self.dialog.geometry("400x300")
        self.dialog.resizable(False, False)
        
        self.dialog.transient(parent)
        self.dialog.grab_set()
        
        self.create_widgets()
        
    def create_widgets(self):
        """Create student selection interface"""
        main_frame = ttk.Frame(self.dialog)
        main_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=20)
        
        ttk.Label(main_frame, text="Select Student to Add:", style='Heading.TLabel').pack(pady=(0, 10))
        
        # Students listbox
        list_frame = ttk.Frame(main_frame)
        list_frame.pack(fill=tk.BOTH, expand=True)
        
        self.students_listbox = tk.Listbox(list_frame)
        self.students_listbox.pack(fill=tk.BOTH, expand=True)
        
        for student in self.students:
            self.students_listbox.insert(tk.END, f"{student['first_name']} {student['last_name']} ({student['username']})")
        
        # Buttons
        button_frame = ttk.Frame(main_frame)
        button_frame.pack(fill=tk.X, pady=(10, 0))
        
        ttk.Button(button_frame, text="Select", style='Primary.TButton',
                  command=self.select_student).pack(side=tk.RIGHT, padx=(10, 0))
        ttk.Button(button_frame, text="Cancel", style='Secondary.TButton',
                  command=self.dialog.destroy).pack(side=tk.RIGHT)
        
    def select_student(self):
        """Select the chosen student"""
        selection = self.students_listbox.curselection()
        if selection:
            self.selected_student = self.students[selection[0]]
            self.dialog.destroy()

class ResourceDialog:
    def __init__(self, parent, class_id, user_id, db_manager):
        self.parent = parent
        self.class_id = class_id
        self.user_id = user_id
        self.db_manager = db_manager
        self.resource_added = False
        
        self.dialog = tk.Toplevel(parent)
        self.dialog.title("Add Resource")
        self.dialog.geometry("500x400")
        self.dialog.resizable(False, False)
        
        self.dialog.transient(parent)
        self.dialog.grab_set()
        
        self.create_widgets()
        
    def create_widgets(self):
        """Create resource form"""
        main_frame = ttk.Frame(self.dialog)
        main_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=20)
        
        ttk.Label(main_frame, text="Add New Resource", style='Heading.TLabel').pack(pady=(0, 20))
        
        # Title
        ttk.Label(main_frame, text="Title:", style='Info.TLabel').pack(anchor=tk.W)
        self.title_entry = ttk.Entry(main_frame, width=50)
        self.title_entry.pack(fill=tk.X, pady=(0, 10))
        
        # Description
        ttk.Label(main_frame, text="Description:", style='Info.TLabel').pack(anchor=tk.W)
        self.description_text = tk.Text(main_frame, height=4, width=50)
        self.description_text.pack(fill=tk.X, pady=(0, 10))
        
        # Resource type
        ttk.Label(main_frame, text="Resource Type:", style='Info.TLabel').pack(anchor=tk.W)
        self.resource_type_var = tk.StringVar(value="note")
        type_frame = ttk.Frame(main_frame)
        type_frame.pack(fill=tk.X, pady=(0, 10))
        
        ttk.Radiobutton(type_frame, text="Note", variable=self.resource_type_var, 
                       value="note").pack(side=tk.LEFT, padx=(0, 20))
        ttk.Radiobutton(type_frame, text="Assignment", variable=self.resource_type_var, 
                       value="assignment").pack(side=tk.LEFT, padx=(0, 20))
        ttk.Radiobutton(type_frame, text="Document", variable=self.resource_type_var, 
                       value="document").pack(side=tk.LEFT)
        
        # Content
        ttk.Label(main_frame, text="Content:", style='Info.TLabel').pack(anchor=tk.W)
        self.content_text = tk.Text(main_frame, height=6, width=50)
        self.content_text.pack(fill=tk.X, pady=(0, 20))
        
        # Buttons
        button_frame = ttk.Frame(main_frame)
        button_frame.pack(fill=tk.X)
        
        ttk.Button(button_frame, text="Add Resource", style='Primary.TButton',
                  command=self.add_resource).pack(side=tk.RIGHT, padx=(10, 0))
        ttk.Button(button_frame, text="Cancel", style='Secondary.TButton',
                  command=self.dialog.destroy).pack(side=tk.RIGHT)
        
    def add_resource(self):
        """Add the resource"""
        title = self.title_entry.get().strip()
        description = self.description_text.get("1.0", tk.END).strip()
        content = self.content_text.get("1.0", tk.END).strip()
        resource_type = self.resource_type_var.get()
        
        if not title:
            messagebox.showerror("Error", "Please enter a title")
            return
            
        resource_id = self.db_manager.add_resource(title, description, resource_type, 
                                                 content, "", self.class_id, self.user_id)
        
        if resource_id:
            self.resource_added = True
            self.dialog.destroy()
        else:
            messagebox.showerror("Error", "Failed to add resource")

class ResourceViewDialog:
    def __init__(self, parent, resource):
        self.parent = parent
        
        self.dialog = tk.Toplevel(parent)
        self.dialog.title(f"Resource: {resource['title']}")
        self.dialog.geometry("600x500")
        
        self.dialog.transient(parent)
        self.dialog.grab_set()
        
        self.create_widgets(resource)
        
    def create_widgets(self, resource):
        """Create resource view interface"""
        main_frame = ttk.Frame(self.dialog)
        main_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=20)
        
        # Title
        ttk.Label(main_frame, text=resource['title'], style='Heading.TLabel').pack(anchor=tk.W)
        
        # Type and author
        info_frame = ttk.Frame(main_frame)
        info_frame.pack(fill=tk.X, pady=(5, 10))
        
        ttk.Label(info_frame, text=f"Type: {resource['resource_type'].title()}", 
                 style='Info.TLabel').pack(side=tk.LEFT)
        ttk.Label(info_frame, text=f"By: {resource['first_name']} {resource['last_name']}", 
                 style='Info.TLabel').pack(side=tk.RIGHT)
        
        # Description
        if resource['description']:
            ttk.Label(main_frame, text="Description:", style='Info.TLabel').pack(anchor=tk.W, pady=(10, 5))
            desc_text = tk.Text(main_frame, height=3, wrap=tk.WORD)
            desc_text.pack(fill=tk.X, pady=(0, 10))
            desc_text.insert("1.0", resource['description'])
            desc_text.config(state=tk.DISABLED)
        
        # Content
        ttk.Label(main_frame, text="Content:", style='Info.TLabel').pack(anchor=tk.W, pady=(10, 5))
        content_text = tk.Text(main_frame, wrap=tk.WORD)
        content_text.pack(fill=tk.BOTH, expand=True)
        content_text.insert("1.0", resource['content'] or "No content available")
        content_text.config(state=tk.DISABLED)
        
        # Close button
        ttk.Button(main_frame, text="Close", style='Primary.TButton',
                  command=self.dialog.destroy).pack(pady=(10, 0))
