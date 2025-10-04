"""
Login window for TeacherApp
Handles user authentication and registration
"""

import tkinter as tk
from tkinter import ttk, messagebox

class LoginWindow:
    def __init__(self, parent, auth_manager, on_success_callback):
        self.parent = parent
        self.auth_manager = auth_manager
        self.on_success_callback = on_success_callback
        
        self.create_widgets()
        
    def create_widgets(self):
        """Create login interface"""
        # Main frame
        main_frame = ttk.Frame(self.parent)
        main_frame.pack(expand=True, fill=tk.BOTH)
        
        # Center the login form
        center_frame = ttk.Frame(main_frame)
        center_frame.pack(expand=True)
        
        # Title
        title_label = ttk.Label(center_frame, text="TeacherApp", style='Title.TLabel')
        title_label.pack(pady=(50, 20))
        
        subtitle_label = ttk.Label(center_frame, text="Teacher Management System", style='Info.TLabel')
        subtitle_label.pack(pady=(0, 30))
        
        # Login form frame
        form_frame = ttk.Frame(center_frame, style='Card.TFrame')
        form_frame.pack(pady=20, padx=50)
        
        # Username
        ttk.Label(form_frame, text="Username:", style='Info.TLabel').pack(anchor=tk.W, pady=(20, 5), padx=20)
        self.username_entry = ttk.Entry(form_frame, width=30)
        self.username_entry.pack(pady=(0, 10), padx=20)
        
        # Password
        ttk.Label(form_frame, text="Password:", style='Info.TLabel').pack(anchor=tk.W, pady=(0, 5), padx=20)
        self.password_entry = ttk.Entry(form_frame, width=30, show="*")
        self.password_entry.pack(pady=(0, 20), padx=20)
        
        # Login button
        login_button = ttk.Button(form_frame, text="Login", style='Primary.TButton', 
                                command=self.login)
        login_button.pack(pady=(0, 10), padx=20)
        
        # Register button
        register_button = ttk.Button(form_frame, text="Register New User", style='Secondary.TButton',
                                   command=self.show_register)
        register_button.pack(pady=(0, 20), padx=20)
        
        # Default credentials info
        info_frame = ttk.Frame(center_frame)
        info_frame.pack(pady=20)
        
        ttk.Label(info_frame, text="Default Admin Login:", style='Info.TLabel').pack()
        ttk.Label(info_frame, text="Username: admin | Password: admin123", 
                 style='Info.TLabel', foreground='gray').pack()
        
        # Bind Enter key to login
        self.password_entry.bind('<Return>', lambda e: self.login())
        
    def login(self):
        """Handle login attempt"""
        username = self.username_entry.get().strip()
        password = self.password_entry.get()
        
        if not username or not password:
            messagebox.showerror("Error", "Please enter both username and password")
            return
            
        if self.auth_manager.login(username, password):
            self.on_success_callback()
        else:
            messagebox.showerror("Login Failed", "Invalid username or password")
            
    def show_register(self):
        """Show registration dialog"""
        RegisterDialog(self.parent, self.auth_manager)

class RegisterDialog:
    def __init__(self, parent, auth_manager):
        self.parent = parent
        self.auth_manager = auth_manager
        
        # Create dialog window
        self.dialog = tk.Toplevel(parent)
        self.dialog.title("Register New User")
        self.dialog.geometry("450x700")
        self.dialog.resizable(True, True)
        self.dialog.minsize(450, 600)
        
        # Center the dialog
        self.dialog.transient(parent)
        self.dialog.grab_set()
        
        self.create_widgets()
        
    def create_widgets(self):
        """Create registration form"""
        # Create main container with scrollbar
        main_container = ttk.Frame(self.dialog)
        main_container.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        # Create canvas and scrollbar for scrolling
        canvas = tk.Canvas(main_container)
        scrollbar = ttk.Scrollbar(main_container, orient="vertical", command=canvas.yview)
        scrollable_frame = ttk.Frame(canvas)
        
        scrollable_frame.bind(
            "<Configure>",
            lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
        )
        
        canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
        canvas.configure(yscrollcommand=scrollbar.set)
        
        # Pack canvas and scrollbar
        canvas.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")
        
        # Bind mouse wheel to canvas
        def _on_mousewheel(event):
            canvas.yview_scroll(int(-1*(event.delta/120)), "units")
        canvas.bind_all("<MouseWheel>", _on_mousewheel)
        
        # Unbind when dialog is destroyed
        def _unbind_mousewheel(event):
            canvas.unbind_all("<MouseWheel>")
        self.dialog.bind("<Destroy>", _unbind_mousewheel)
        
        # Main frame inside scrollable area
        main_frame = ttk.Frame(scrollable_frame)
        main_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=20)
        
        # Title
        ttk.Label(main_frame, text="Register New User", style='Title.TLabel').pack(pady=(0, 20))
        
        # Form fields
        fields_frame = ttk.Frame(main_frame)
        fields_frame.pack(fill=tk.X, pady=(0, 20))
        
        # Username
        ttk.Label(fields_frame, text="Username:", style='Info.TLabel').pack(anchor=tk.W, pady=(0, 5))
        self.username_entry = ttk.Entry(fields_frame, width=40)
        self.username_entry.pack(pady=(0, 15), fill=tk.X)
        
        # Email
        ttk.Label(fields_frame, text="Email:", style='Info.TLabel').pack(anchor=tk.W, pady=(0, 5))
        self.email_entry = ttk.Entry(fields_frame, width=40)
        self.email_entry.pack(pady=(0, 15), fill=tk.X)
        
        # First Name
        ttk.Label(fields_frame, text="First Name:", style='Info.TLabel').pack(anchor=tk.W, pady=(0, 5))
        self.first_name_entry = ttk.Entry(fields_frame, width=40)
        self.first_name_entry.pack(pady=(0, 15), fill=tk.X)
        
        # Last Name
        ttk.Label(fields_frame, text="Last Name:", style='Info.TLabel').pack(anchor=tk.W, pady=(0, 5))
        self.last_name_entry = ttk.Entry(fields_frame, width=40)
        self.last_name_entry.pack(pady=(0, 15), fill=tk.X)
        
        # Password
        ttk.Label(fields_frame, text="Password:", style='Info.TLabel').pack(anchor=tk.W, pady=(0, 5))
        self.password_entry = ttk.Entry(fields_frame, width=40, show="*")
        self.password_entry.pack(pady=(0, 15), fill=tk.X)
        
        # User Type
        ttk.Label(fields_frame, text="User Type:", style='Info.TLabel').pack(anchor=tk.W, pady=(0, 5))
        self.user_type_var = tk.StringVar(value="teacher")
        user_type_frame = ttk.Frame(fields_frame)
        user_type_frame.pack(fill=tk.X, pady=(0, 20))
        
        ttk.Radiobutton(user_type_frame, text="Teacher", variable=self.user_type_var, 
                       value="teacher").pack(side=tk.LEFT, padx=(0, 30))
        ttk.Radiobutton(user_type_frame, text="Student", variable=self.user_type_var, 
                       value="student").pack(side=tk.LEFT)
        
        # Buttons - Fixed at bottom of dialog
        button_frame = ttk.Frame(self.dialog)
        button_frame.pack(fill=tk.X, side=tk.BOTTOM, padx=20, pady=(10, 20))
        
        ttk.Button(button_frame, text="Register", style='Primary.TButton',
                  command=self.register).pack(side=tk.RIGHT, padx=(10, 0))
        ttk.Button(button_frame, text="Cancel", style='Secondary.TButton',
                  command=self.dialog.destroy).pack(side=tk.RIGHT)
        
    def register(self):
        """Handle registration"""
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
            
        # Register user
        if self.auth_manager.register(username, email, password, first_name, last_name, user_type):
            messagebox.showinfo("Success", "User registered successfully!")
            self.dialog.destroy()
        else:
            messagebox.showerror("Error", "Registration failed. Username or email may already exist.")
