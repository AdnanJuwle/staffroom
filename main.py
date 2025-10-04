#!/usr/bin/env python3
"""
TeacherApp - A comprehensive teacher management application
Main entry point for the application
"""

import tkinter as tk
from tkinter import ttk
import sys
import os

# Add the current directory to Python path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from src.auth import AuthManager
from src.gui.main_window import MainWindow
from src.database import DatabaseManager

class TeacherApp:
    def __init__(self):
        self.root = tk.Tk()
        self.db_manager = DatabaseManager()
        self.auth_manager = AuthManager(self.db_manager)
        
        # Initialize database
        self.db_manager.initialize_database()
        
        # Create main window
        self.main_window = MainWindow(self.root, self.auth_manager, self.db_manager)
        
    def run(self):
        """Start the application"""
        self.root.title("TeacherApp - Teacher Management System")
        self.root.geometry("1200x800")
        self.root.minsize(1000, 600)
        
        # Center the window
        self.root.update_idletasks()
        x = (self.root.winfo_screenwidth() // 2) - (1200 // 2)
        y = (self.root.winfo_screenheight() // 2) - (800 // 2)
        self.root.geometry(f"1200x800+{x}+{y}")
        
        self.root.mainloop()

if __name__ == "__main__":
    app = TeacherApp()
    app.run()
