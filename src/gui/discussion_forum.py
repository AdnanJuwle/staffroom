"""
Discussion Forum window for TeacherApp
Handles teacher discussions, questions, and collaboration
"""

import tkinter as tk
from tkinter import ttk, messagebox, simpledialog
from datetime import datetime

class DiscussionForumWindow:
    def __init__(self, parent, auth_manager, db_manager, navigate_callback):
        self.parent = parent
        self.auth_manager = auth_manager
        self.db_manager = db_manager
        self.navigate_callback = navigate_callback
        
        self.create_widgets()
        self.refresh_discussions()
        
    def create_widgets(self):
        """Create discussion forum interface"""
        # Header
        header_frame = ttk.Frame(self.parent)
        header_frame.pack(fill=tk.X, padx=20, pady=10)
        
        ttk.Label(header_frame, text="Discussion Forum", style='Title.TLabel').pack(side=tk.LEFT)
        
        # Back button
        back_button = ttk.Button(header_frame, text="← Back to Dashboard", 
                                style='Secondary.TButton',
                                command=lambda: self.navigate_callback("dashboard"))
        back_button.pack(side=tk.RIGHT)
        
        # Main content
        main_frame = ttk.Frame(self.parent)
        main_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=10)
        
        # Left panel - Discussions list
        left_frame = ttk.LabelFrame(main_frame, text="Discussions")
        left_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=(0, 10))
        
        # Discussions listbox
        list_frame = ttk.Frame(left_frame)
        list_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        self.discussions_listbox = tk.Listbox(list_frame)
        self.discussions_listbox.pack(fill=tk.BOTH, expand=True)
        self.discussions_listbox.bind('<<ListboxSelect>>', self.on_discussion_select)
        
        # Discussion management buttons
        button_frame = ttk.Frame(left_frame)
        button_frame.pack(fill=tk.X, padx=10, pady=(0, 10))
        
        ttk.Button(button_frame, text="New Discussion", style='Primary.TButton',
                  command=self.create_new_discussion).pack(side=tk.LEFT, padx=(0, 5))
        ttk.Button(button_frame, text="Refresh", style='Secondary.TButton',
                  command=self.refresh_discussions).pack(side=tk.LEFT)
        
        # Right panel - Discussion details
        self.right_frame = ttk.LabelFrame(main_frame, text="Discussion Details")
        self.right_frame.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True)
        
        # Initially show placeholder
        self.show_discussion_placeholder()
        
    def show_discussion_placeholder(self):
        """Show placeholder when no discussion is selected"""
        for widget in self.right_frame.winfo_children():
            widget.destroy()
            
        placeholder_frame = ttk.Frame(self.right_frame)
        placeholder_frame.pack(expand=True)
        
        ttk.Label(placeholder_frame, text="Select a discussion to view details", 
                 style='Info.TLabel').pack(expand=True)
        
    def refresh_discussions(self):
        """Refresh the discussions list"""
        self.discussions_listbox.delete(0, tk.END)
        
        discussions = self.db_manager.get_all_discussions()
        for discussion in discussions:
            self.discussions_listbox.insert(tk.END, f"{discussion['title']} - {discussion['first_name']} {discussion['last_name']}")
        
        self.selected_discussion_id = None
        
    def on_discussion_select(self, event):
        """Handle discussion selection"""
        selection = self.discussions_listbox.curselection()
        if selection:
            discussions = self.db_manager.get_all_discussions()
            if selection[0] < len(discussions):
                discussion = discussions[selection[0]]
                self.selected_discussion_id = discussion['id']
                self.show_discussion_details(discussion)
                
    def show_discussion_details(self, discussion):
        """Show detailed information about selected discussion"""
        # Clear right frame
        for widget in self.right_frame.winfo_children():
            widget.destroy()
            
        # Discussion info frame
        info_frame = ttk.Frame(self.right_frame)
        info_frame.pack(fill=tk.X, padx=10, pady=10)
        
        ttk.Label(info_frame, text=discussion['title'], style='Heading.TLabel').pack(anchor=tk.W)
        
        # Author and date info
        author_frame = ttk.Frame(info_frame)
        author_frame.pack(fill=tk.X, pady=(5, 10))
        
        ttk.Label(author_frame, text=f"By: {discussion['first_name']} {discussion['last_name']}", 
                 style='Info.TLabel').pack(side=tk.LEFT)
        ttk.Label(author_frame, text=f"Category: {discussion['category']}", 
                 style='Info.TLabel').pack(side=tk.RIGHT)
        
        # Discussion content
        content_frame = ttk.LabelFrame(self.right_frame, text="Content")
        content_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=(0, 10))
        
        content_text = tk.Text(content_frame, wrap=tk.WORD, state=tk.DISABLED)
        content_text.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        # Enable text widget to insert content
        content_text.config(state=tk.NORMAL)
        content_text.insert("1.0", discussion['content'])
        content_text.config(state=tk.DISABLED)
        
        # Replies section
        replies_frame = ttk.LabelFrame(self.right_frame, text="Replies")
        replies_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=(0, 10))
        
        # Replies list
        replies_list_frame = ttk.Frame(replies_frame)
        replies_list_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        self.replies_listbox = tk.Listbox(replies_list_frame)
        self.replies_listbox.pack(fill=tk.BOTH, expand=True)
        
        # Load replies
        replies = self.db_manager.get_discussion_replies(discussion['id'])
        for reply in replies:
            self.replies_listbox.insert(tk.END, f"{reply['first_name']} {reply['last_name']}: {reply['content'][:50]}...")
        
        # Reply management
        reply_button_frame = ttk.Frame(replies_frame)
        reply_button_frame.pack(fill=tk.X, padx=10, pady=(0, 10))
        
        ttk.Button(reply_button_frame, text="Add Reply", style='Primary.TButton',
                  command=lambda: self.add_reply(discussion['id'])).pack(side=tk.LEFT)
        
    def create_new_discussion(self):
        """Create a new discussion"""
        dialog = NewDiscussionDialog(self.parent, self.auth_manager.get_current_user()['id'], self.db_manager)
        self.parent.wait_window(dialog.dialog)
        
        if dialog.discussion_created:
            messagebox.showinfo("Success", "Discussion created successfully!")
            self.refresh_discussions()
            
    def add_reply(self, discussion_id):
        """Add a reply to the discussion"""
        reply_content = simpledialog.askstring("Add Reply", "Enter your reply:")
        if reply_content:
            author_id = self.auth_manager.get_current_user()['id']
            reply_id = self.db_manager.add_discussion_reply(discussion_id, reply_content, author_id)
            
            if reply_id:
                messagebox.showinfo("Success", "Reply added successfully!")
                # Refresh the discussion details
                discussions = self.db_manager.get_all_discussions()
                for discussion in discussions:
                    if discussion['id'] == discussion_id:
                        self.show_discussion_details(discussion)
                        break
            else:
                messagebox.showerror("Error", "Failed to add reply")

class NewDiscussionDialog:
    def __init__(self, parent, user_id, db_manager):
        self.parent = parent
        self.user_id = user_id
        self.db_manager = db_manager
        self.discussion_created = False
        
        self.dialog = tk.Toplevel(parent)
        self.dialog.title("New Discussion")
        self.dialog.geometry("600x500")
        self.dialog.resizable(False, False)
        
        self.dialog.transient(parent)
        self.dialog.grab_set()
        
        self.create_widgets()
        
    def create_widgets(self):
        """Create new discussion form"""
        main_frame = ttk.Frame(self.dialog)
        main_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=20)
        
        ttk.Label(main_frame, text="Create New Discussion", style='Heading.TLabel').pack(pady=(0, 20))
        
        # Title
        ttk.Label(main_frame, text="Title:", style='Info.TLabel').pack(anchor=tk.W)
        self.title_entry = ttk.Entry(main_frame, width=60)
        self.title_entry.pack(fill=tk.X, pady=(0, 10))
        
        # Category
        ttk.Label(main_frame, text="Category:", style='Info.TLabel').pack(anchor=tk.W)
        self.category_var = tk.StringVar(value="general")
        category_frame = ttk.Frame(main_frame)
        category_frame.pack(fill=tk.X, pady=(0, 10))
        
        categories = ["general", "teaching", "resources", "questions", "announcements"]
        for i, category in enumerate(categories):
            ttk.Radiobutton(category_frame, text=category.title(), 
                           variable=self.category_var, value=category).pack(side=tk.LEFT, padx=(0, 20))
        
        # Content
        ttk.Label(main_frame, text="Content:", style='Info.TLabel').pack(anchor=tk.W, pady=(10, 5))
        self.content_text = tk.Text(main_frame, height=15, wrap=tk.WORD)
        self.content_text.pack(fill=tk.BOTH, expand=True, pady=(0, 20))
        
        # Buttons
        button_frame = ttk.Frame(main_frame)
        button_frame.pack(fill=tk.X)
        
        ttk.Button(button_frame, text="Create Discussion", style='Primary.TButton',
                  command=self.create_discussion).pack(side=tk.RIGHT, padx=(10, 0))
        ttk.Button(button_frame, text="Cancel", style='Secondary.TButton',
                  command=self.dialog.destroy).pack(side=tk.RIGHT)
        
    def create_discussion(self):
        """Create the discussion"""
        title = self.title_entry.get().strip()
        content = self.content_text.get("1.0", tk.END).strip()
        category = self.category_var.get()
        
        if not title:
            messagebox.showerror("Error", "Please enter a title")
            return
            
        if not content:
            messagebox.showerror("Error", "Please enter content")
            return
            
        discussion_id = self.db_manager.create_discussion(title, content, self.user_id, category)
        
        if discussion_id:
            self.discussion_created = True
            self.dialog.destroy()
        else:
            messagebox.showerror("Error", "Failed to create discussion")
