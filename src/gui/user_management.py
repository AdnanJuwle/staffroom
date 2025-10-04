"""
User Management window for TeacherApp
Handles user creation, management, and teacher hierarchy (Admin only)
"""

import tkinter as tk
from tkinter import ttk, messagebox, simpledialog

class UserManagementWindow:
    def __init__(self, parent, auth_manager, db_manager, navigate_callback):
        self.parent = parent
        self.auth_manager = auth_manager
        self.db_manager = db_manager
        self.navigate_callback = navigate_callback
        
        self.create_widgets()
        self.refresh_users()
        
    def create_widgets(self):
        """Create user management interface"""
        # Header
        header_frame = ttk.Frame(self.parent)
        header_frame.pack(fill=tk.X, padx=20, pady=10)
        
        ttk.Label(header_frame, text="User Management", style='Title.TLabel').pack(side=tk.LEFT)
        
        # Back button
        back_button = ttk.Button(header_frame, text="← Back to Dashboard", 
                                style='Secondary.TButton',
                                command=lambda: self.navigate_callback("dashboard"))
        back_button.pack(side=tk.RIGHT)
        
        # Main content
        main_frame = ttk.Frame(self.parent)
        main_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=10)
        
        # User type selection
        type_frame = ttk.Frame(main_frame)
        type_frame.pack(fill=tk.X, pady=(0, 10))
        
        ttk.Label(type_frame, text="View:", style='Info.TLabel').pack(side=tk.LEFT, padx=(0, 10))
        
        self.user_type_var = tk.StringVar(value="all")
        ttk.Radiobutton(type_frame, text="All Users", variable=self.user_type_var, 
                       value="all", command=self.refresh_users).pack(side=tk.LEFT, padx=(0, 20))
        ttk.Radiobutton(type_frame, text="Teachers", variable=self.user_type_var, 
                       value="teacher", command=self.refresh_users).pack(side=tk.LEFT, padx=(0, 20))
        ttk.Radiobutton(type_frame, text="Students", variable=self.user_type_var, 
                       value="student", command=self.refresh_users).pack(side=tk.LEFT)
        
        # Users list frame
        users_frame = ttk.LabelFrame(main_frame, text="Users")
        users_frame.pack(fill=tk.BOTH, expand=True, padx=(0, 10))
        
        # Users listbox
        list_frame = ttk.Frame(users_frame)
        list_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        self.users_listbox = tk.Listbox(list_frame)
        self.users_listbox.pack(fill=tk.BOTH, expand=True)
        self.users_listbox.bind('<<ListboxSelect>>', self.on_user_select)
        
        # User management buttons
        button_frame = ttk.Frame(users_frame)
        button_frame.pack(fill=tk.X, padx=10, pady=(0, 10))
        
        ttk.Button(button_frame, text="Add User", style='Primary.TButton',
                  command=self.add_user).pack(side=tk.LEFT, padx=(0, 5))
        ttk.Button(button_frame, text="Edit User", style='Secondary.TButton',
                  command=self.edit_user).pack(side=tk.LEFT, padx=(0, 5))
        ttk.Button(button_frame, text="Deactivate User", style='Secondary.TButton',
                  command=self.deactivate_user).pack(side=tk.LEFT)
        
        # Teacher hierarchy frame
        hierarchy_frame = ttk.LabelFrame(main_frame, text="Teacher Hierarchy")
        hierarchy_frame.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True)
        
        # Hierarchy listbox
        hierarchy_list_frame = ttk.Frame(hierarchy_frame)
        hierarchy_list_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        self.hierarchy_listbox = tk.Listbox(hierarchy_list_frame)
        self.hierarchy_listbox.pack(fill=tk.BOTH, expand=True)
        
        # Hierarchy management buttons
        hierarchy_button_frame = ttk.Frame(hierarchy_frame)
        hierarchy_button_frame.pack(fill=tk.X, padx=10, pady=(0, 10))
        
        ttk.Button(hierarchy_button_frame, text="Assign Supervisor", style='Primary.TButton',
                  command=self.assign_supervisor).pack(side=tk.LEFT, padx=(0, 5))
        ttk.Button(hierarchy_button_frame, text="Remove Assignment", style='Secondary.TButton',
                  command=self.remove_supervisor_assignment).pack(side=tk.LEFT)
        
        self.refresh_hierarchy()
        
    def refresh_users(self):
        """Refresh the users list"""
        self.users_listbox.delete(0, tk.END)
        
        user_type = self.user_type_var.get()
        
        if user_type == "all":
            # Get all users except current user
            current_user_id = self.auth_manager.get_current_user()['id']
            cursor = self.db_manager.connection.execute("""
                SELECT * FROM users WHERE id != ? ORDER BY user_type, first_name
            """, (current_user_id,))
            users = [dict(row) for row in cursor.fetchall()]
        elif user_type == "teacher":
            users = self.db_manager.get_all_teachers()
        elif user_type == "student":
            users = self.db_manager.get_all_students()
        
        for user in users:
            status = "Active" if user['is_active'] else "Inactive"
            self.users_listbox.insert(tk.END, f"{user['first_name']} {user['last_name']} ({user['user_type']}) - {status}")
        
        self.selected_user = None
        
    def refresh_hierarchy(self):
        """Refresh the teacher hierarchy list"""
        self.hierarchy_listbox.delete(0, tk.END)
        
        cursor = self.db_manager.connection.execute("""
            SELECT th.*, s.first_name as supervisor_first, s.last_name as supervisor_last,
                   sub.first_name as subordinate_first, sub.last_name as subordinate_last
            FROM teacher_hierarchy th
            JOIN users s ON th.supervisor_id = s.id
            JOIN users sub ON th.subordinate_id = sub.id
            ORDER BY s.first_name, sub.first_name
        """)
        
        hierarchies = [dict(row) for row in cursor.fetchall()]
        
        for hierarchy in hierarchies:
            self.hierarchy_listbox.insert(tk.END, 
                f"{hierarchy['supervisor_first']} {hierarchy['supervisor_last']} → "
                f"{hierarchy['subordinate_first']} {hierarchy['subordinate_last']}")
        
    def on_user_select(self, event):
        """Handle user selection"""
        selection = self.users_listbox.curselection()
        if selection:
            user_type = self.user_type_var.get()
            
            if user_type == "all":
                current_user_id = self.auth_manager.get_current_user()['id']
                cursor = self.db_manager.connection.execute("""
                    SELECT * FROM users WHERE id != ? ORDER BY user_type, first_name
                """, (current_user_id,))
                users = [dict(row) for row in cursor.fetchall()]
            elif user_type == "teacher":
                users = self.db_manager.get_all_teachers()
            elif user_type == "student":
                users = self.db_manager.get_all_students()
            
            if selection[0] < len(users):
                self.selected_user = users[selection[0]]
                
    def add_user(self):
        """Add a new user"""
        dialog = AddUserDialog(self.parent, self.db_manager)
        self.parent.wait_window(dialog.dialog)
        
        if dialog.user_added:
            messagebox.showinfo("Success", "User added successfully!")
            self.refresh_users()
            
    def edit_user(self):
        """Edit selected user"""
        if not self.selected_user:
            messagebox.showwarning("No Selection", "Please select a user to edit")
            return
            
        dialog = EditUserDialog(self.parent, self.selected_user, self.db_manager)
        self.parent.wait_window(dialog.dialog)
        
        if dialog.user_updated:
            messagebox.showinfo("Success", "User updated successfully!")
            self.refresh_users()
            
    def deactivate_user(self):
        """Deactivate selected user"""
        if not self.selected_user:
            messagebox.showwarning("No Selection", "Please select a user to deactivate")
            return
            
        if messagebox.askyesno("Confirm Deactivation", 
                              f"Deactivate user {self.selected_user['first_name']} {self.selected_user['last_name']}?"):
            self.db_manager.connection.execute("""
                UPDATE users SET is_active = 0 WHERE id = ?
            """, (self.selected_user['id'],))
            self.db_manager.connection.commit()
            
            messagebox.showinfo("Success", "User deactivated successfully!")
            self.refresh_users()
            
    def assign_supervisor(self):
        """Assign a supervisor to a teacher"""
        dialog = AssignSupervisorDialog(self.parent, self.db_manager)
        self.parent.wait_window(dialog.dialog)
        
        if dialog.assignment_created:
            messagebox.showinfo("Success", "Supervisor assignment created successfully!")
            self.refresh_hierarchy()
            
    def remove_supervisor_assignment(self):
        """Remove supervisor assignment"""
        selection = self.hierarchy_listbox.curselection()
        if not selection:
            messagebox.showwarning("No Selection", "Please select an assignment to remove")
            return
            
        if messagebox.askyesno("Confirm Removal", "Remove this supervisor assignment?"):
            # Get the hierarchy data
            cursor = self.db_manager.connection.execute("""
                SELECT th.* FROM teacher_hierarchy th
                JOIN users s ON th.supervisor_id = s.id
                JOIN users sub ON th.subordinate_id = sub.id
                ORDER BY s.first_name, sub.first_name
            """)
            
            hierarchies = [dict(row) for row in cursor.fetchall()]
            
            if selection[0] < len(hierarchies):
                hierarchy = hierarchies[selection[0]]
                
                self.db_manager.connection.execute("""
                    DELETE FROM teacher_hierarchy WHERE id = ?
                """, (hierarchy['id'],))
                self.db_manager.connection.commit()
                
                messagebox.showinfo("Success", "Assignment removed successfully!")
                self.refresh_hierarchy()

class AddUserDialog:
    def __init__(self, parent, db_manager):
        self.parent = parent
        self.db_manager = db_manager
        self.user_added = False
        
        self.dialog = tk.Toplevel(parent)
        self.dialog.title("Add New User")
        self.dialog.geometry("400x500")
        self.dialog.resizable(False, False)
        
        self.dialog.transient(parent)
        self.dialog.grab_set()
        
        self.create_widgets()
        
    def create_widgets(self):
        """Create add user form"""
        main_frame = ttk.Frame(self.dialog)
        main_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=20)
        
        ttk.Label(main_frame, text="Add New User", style='Heading.TLabel').pack(pady=(0, 20))
        
        # Username
        ttk.Label(main_frame, text="Username:", style='Info.TLabel').pack(anchor=tk.W)
        self.username_entry = ttk.Entry(main_frame, width=30)
        self.username_entry.pack(fill=tk.X, pady=(0, 10))
        
        # Email
        ttk.Label(main_frame, text="Email:", style='Info.TLabel').pack(anchor=tk.W)
        self.email_entry = ttk.Entry(main_frame, width=30)
        self.email_entry.pack(fill=tk.X, pady=(0, 10))
        
        # First Name
        ttk.Label(main_frame, text="First Name:", style='Info.TLabel').pack(anchor=tk.W)
        self.first_name_entry = ttk.Entry(main_frame, width=30)
        self.first_name_entry.pack(fill=tk.X, pady=(0, 10))
        
        # Last Name
        ttk.Label(main_frame, text="Last Name:", style='Info.TLabel').pack(anchor=tk.W)
        self.last_name_entry = ttk.Entry(main_frame, width=30)
        self.last_name_entry.pack(fill=tk.X, pady=(0, 10))
        
        # Password
        ttk.Label(main_frame, text="Password:", style='Info.TLabel').pack(anchor=tk.W)
        self.password_entry = ttk.Entry(main_frame, width=30, show="*")
        self.password_entry.pack(fill=tk.X, pady=(0, 10))
        
        # User Type
        ttk.Label(main_frame, text="User Type:", style='Info.TLabel').pack(anchor=tk.W)
        self.user_type_var = tk.StringVar(value="teacher")
        user_type_frame = ttk.Frame(main_frame)
        user_type_frame.pack(fill=tk.X, pady=(0, 20))
        
        ttk.Radiobutton(user_type_frame, text="Teacher", variable=self.user_type_var, 
                       value="teacher").pack(side=tk.LEFT, padx=(0, 20))
        ttk.Radiobutton(user_type_frame, text="Student", variable=self.user_type_var, 
                       value="student").pack(side=tk.LEFT, padx=(0, 20))
        ttk.Radiobutton(user_type_frame, text="Admin", variable=self.user_type_var, 
                       value="admin").pack(side=tk.LEFT)
        
        # Buttons
        button_frame = ttk.Frame(main_frame)
        button_frame.pack(fill=tk.X, pady=(20, 0))
        
        ttk.Button(button_frame, text="Add User", style='Primary.TButton',
                  command=self.add_user).pack(side=tk.RIGHT, padx=(10, 0))
        ttk.Button(button_frame, text="Cancel", style='Secondary.TButton',
                  command=self.dialog.destroy).pack(side=tk.RIGHT)
        
    def add_user(self):
        """Add the user"""
        username = self.username_entry.get().strip()
        email = self.email_entry.get().strip()
        first_name = self.first_name_entry.get().strip()
        last_name = self.last_name_entry.get().strip()
        password = self.password_entry.get()
        user_type = self.user_type_var.get()
        
        # Validate inputs
        if not all([username, email, first_name, last_name, password]):
            messagebox.showerror("Error", "Please fill in all fields")
            return
            
        if len(password) < 6:
            messagebox.showerror("Error", "Password must be at least 6 characters long")
            return
            
        # Add user
        if self.db_manager.create_user(username, email, password, first_name, last_name, user_type):
            self.user_added = True
            self.dialog.destroy()
        else:
            messagebox.showerror("Error", "Failed to add user. Username or email may already exist.")

class EditUserDialog:
    def __init__(self, parent, user, db_manager):
        self.parent = parent
        self.user = user
        self.db_manager = db_manager
        self.user_updated = False
        
        self.dialog = tk.Toplevel(parent)
        self.dialog.title("Edit User")
        self.dialog.geometry("400x500")
        self.dialog.resizable(False, False)
        
        self.dialog.transient(parent)
        self.dialog.grab_set()
        
        self.create_widgets()
        
    def create_widgets(self):
        """Create edit user form"""
        main_frame = ttk.Frame(self.dialog)
        main_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=20)
        
        ttk.Label(main_frame, text="Edit User", style='Heading.TLabel').pack(pady=(0, 20))
        
        # Username
        ttk.Label(main_frame, text="Username:", style='Info.TLabel').pack(anchor=tk.W)
        self.username_entry = ttk.Entry(main_frame, width=30)
        self.username_entry.pack(fill=tk.X, pady=(0, 10))
        self.username_entry.insert(0, self.user['username'])
        
        # Email
        ttk.Label(main_frame, text="Email:", style='Info.TLabel').pack(anchor=tk.W)
        self.email_entry = ttk.Entry(main_frame, width=30)
        self.email_entry.pack(fill=tk.X, pady=(0, 10))
        self.email_entry.insert(0, self.user['email'])
        
        # First Name
        ttk.Label(main_frame, text="First Name:", style='Info.TLabel').pack(anchor=tk.W)
        self.first_name_entry = ttk.Entry(main_frame, width=30)
        self.first_name_entry.pack(fill=tk.X, pady=(0, 10))
        self.first_name_entry.insert(0, self.user['first_name'])
        
        # Last Name
        ttk.Label(main_frame, text="Last Name:", style='Info.TLabel').pack(anchor=tk.W)
        self.last_name_entry = ttk.Entry(main_frame, width=30)
        self.last_name_entry.pack(fill=tk.X, pady=(0, 10))
        self.last_name_entry.insert(0, self.user['last_name'])
        
        # Password
        ttk.Label(main_frame, text="New Password (leave blank to keep current):", style='Info.TLabel').pack(anchor=tk.W)
        self.password_entry = ttk.Entry(main_frame, width=30, show="*")
        self.password_entry.pack(fill=tk.X, pady=(0, 10))
        
        # User Type
        ttk.Label(main_frame, text="User Type:", style='Info.TLabel').pack(anchor=tk.W)
        self.user_type_var = tk.StringVar(value=self.user['user_type'])
        user_type_frame = ttk.Frame(main_frame)
        user_type_frame.pack(fill=tk.X, pady=(0, 20))
        
        ttk.Radiobutton(user_type_frame, text="Teacher", variable=self.user_type_var, 
                       value="teacher").pack(side=tk.LEFT, padx=(0, 20))
        ttk.Radiobutton(user_type_frame, text="Student", variable=self.user_type_var, 
                       value="student").pack(side=tk.LEFT, padx=(0, 20))
        ttk.Radiobutton(user_type_frame, text="Admin", variable=self.user_type_var, 
                       value="admin").pack(side=tk.LEFT)
        
        # Buttons
        button_frame = ttk.Frame(main_frame)
        button_frame.pack(fill=tk.X, pady=(20, 0))
        
        ttk.Button(button_frame, text="Update User", style='Primary.TButton',
                  command=self.update_user).pack(side=tk.RIGHT, padx=(10, 0))
        ttk.Button(button_frame, text="Cancel", style='Secondary.TButton',
                  command=self.dialog.destroy).pack(side=tk.RIGHT)
        
    def update_user(self):
        """Update the user"""
        username = self.username_entry.get().strip()
        email = self.email_entry.get().strip()
        first_name = self.first_name_entry.get().strip()
        last_name = self.last_name_entry.get().strip()
        password = self.password_entry.get()
        user_type = self.user_type_var.get()
        
        # Validate inputs
        if not all([username, email, first_name, last_name]):
            messagebox.showerror("Error", "Please fill in all required fields")
            return
            
        try:
            # Update user
            if password:
                password_hash = self.db_manager._hash_password(password)
                self.db_manager.connection.execute("""
                    UPDATE users SET username = ?, email = ?, first_name = ?, 
                                   last_name = ?, user_type = ?, password_hash = ?
                    WHERE id = ?
                """, (username, email, first_name, last_name, user_type, password_hash, self.user['id']))
            else:
                self.db_manager.connection.execute("""
                    UPDATE users SET username = ?, email = ?, first_name = ?, 
                                   last_name = ?, user_type = ?
                    WHERE id = ?
                """, (username, email, first_name, last_name, user_type, self.user['id']))
            
            self.db_manager.connection.commit()
            self.user_updated = True
            self.dialog.destroy()
            
        except sqlite3.IntegrityError:
            messagebox.showerror("Error", "Username or email already exists")

class AssignSupervisorDialog:
    def __init__(self, parent, db_manager):
        self.parent = parent
        self.db_manager = db_manager
        self.assignment_created = False
        
        self.dialog = tk.Toplevel(parent)
        self.dialog.title("Assign Supervisor")
        self.dialog.geometry("400x300")
        self.dialog.resizable(False, False)
        
        self.dialog.transient(parent)
        self.dialog.grab_set()
        
        self.create_widgets()
        
    def create_widgets(self):
        """Create supervisor assignment form"""
        main_frame = ttk.Frame(self.dialog)
        main_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=20)
        
        ttk.Label(main_frame, text="Assign Supervisor", style='Heading.TLabel').pack(pady=(0, 20))
        
        # Get all teachers
        teachers = self.db_manager.get_all_teachers()
        
        # Supervisor selection
        ttk.Label(main_frame, text="Supervisor:", style='Info.TLabel').pack(anchor=tk.W)
        self.supervisor_var = tk.StringVar()
        supervisor_combo = ttk.Combobox(main_frame, textvariable=self.supervisor_var, state="readonly")
        supervisor_combo.pack(fill=tk.X, pady=(0, 10))
        
        supervisor_options = [f"{t['first_name']} {t['last_name']} ({t['username']})" for t in teachers]
        supervisor_combo['values'] = supervisor_options
        
        # Subordinate selection
        ttk.Label(main_frame, text="Subordinate:", style='Info.TLabel').pack(anchor=tk.W)
        self.subordinate_var = tk.StringVar()
        subordinate_combo = ttk.Combobox(main_frame, textvariable=self.subordinate_var, state="readonly")
        subordinate_combo.pack(fill=tk.X, pady=(0, 20))
        
        subordinate_options = [f"{t['first_name']} {t['last_name']} ({t['username']})" for t in teachers]
        subordinate_combo['values'] = subordinate_options
        
        # Buttons
        button_frame = ttk.Frame(main_frame)
        button_frame.pack(fill=tk.X, pady=(20, 0))
        
        ttk.Button(button_frame, text="Assign", style='Primary.TButton',
                  command=self.assign_supervisor).pack(side=tk.RIGHT, padx=(10, 0))
        ttk.Button(button_frame, text="Cancel", style='Secondary.TButton',
                  command=self.dialog.destroy).pack(side=tk.RIGHT)
        
    def assign_supervisor(self):
        """Create supervisor assignment"""
        supervisor_text = self.supervisor_var.get()
        subordinate_text = self.subordinate_var.get()
        
        if not supervisor_text or not subordinate_text:
            messagebox.showerror("Error", "Please select both supervisor and subordinate")
            return
            
        if supervisor_text == subordinate_text:
            messagebox.showerror("Error", "Supervisor and subordinate cannot be the same person")
            return
            
        # Extract usernames
        supervisor_username = supervisor_text.split("(")[1].rstrip(")")
        subordinate_username = subordinate_text.split("(")[1].rstrip(")")
        
        # Get user IDs
        cursor = self.db_manager.connection.execute("""
            SELECT id FROM users WHERE username = ?
        """, (supervisor_username,))
        supervisor_id = cursor.fetchone()[0]
        
        cursor = self.db_manager.connection.execute("""
            SELECT id FROM users WHERE username = ?
        """, (subordinate_username,))
        subordinate_id = cursor.fetchone()[0]
        
        try:
            # Create assignment
            self.db_manager.connection.execute("""
                INSERT INTO teacher_hierarchy (supervisor_id, subordinate_id)
                VALUES (?, ?)
            """, (supervisor_id, subordinate_id))
            self.db_manager.connection.commit()
            
            self.assignment_created = True
            self.dialog.destroy()
            
        except sqlite3.IntegrityError:
            messagebox.showerror("Error", "This assignment already exists")
