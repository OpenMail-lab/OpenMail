import tkinter as tk
from tkinter import messagebox

class MainDashboard:
    def __init__(self, root, user_data):
        self.root = root
        self.root.title("OpenMail")
        self.root.geometry("800x600")
        self.root.configure(bg="white")
        self.root.protocol("WM_DELETE_WINDOW", self.on_closing)  # Add window close handler
        
        self.current_user = user_data
        self.current_email = user_data['email']
        self.content_area = None
        self.content_frame = None
        
        self.show_main_dashboard(user_data['email'])

    def show_main_dashboard(self, email):
        # Main container
        main_container = tk.Frame(self.root)
        main_container.pack(fill='both', expand=True)

        # Top navigation bar with blue background
        nav_bar = tk.Frame(main_container, bg="#1a237e", height=50)
        nav_bar.pack(fill='x')
        
        # Logo and email display
        tk.Label(nav_bar, text="OpenMail", font=("Arial", 20, "bold"), fg="white", bg="#1a237e").pack(side='left', padx=20)
        tk.Label(nav_bar, text=f"👤 {email}", font=("Arial", 12), fg="white", bg="#1a237e").pack(side='right', padx=20)

        # Create fixed-width sidebar
        sidebar = tk.Frame(main_container, bg="#f0f0f0", width=250)
        sidebar.pack(side='left', fill='y')
        sidebar.pack_propagate(False)  # Keep fixed width

        # Create content area
        self.content_area = tk.Frame(main_container, bg="white")
        self.content_area.pack(side='left', fill='both', expand=True)
        
        # Create content frame
        self.content_frame = tk.Frame(self.content_area, bg="white")
        self.content_frame.pack(fill='both', expand=True)

        # Add sections
        self.add_email_section(sidebar)
        self.add_devops_section(sidebar)
        self.show_welcome_content()

    def add_email_section(self, parent):
        section = tk.LabelFrame(parent, text="Email Management", bg="#f0f0f0", fg="#1a237e", font=("Arial", 12, "bold"))
        section.pack(fill='x', padx=5, pady=5)

        buttons = [
            ("📝 Compose", self.show_compose),
            ("📥 Inbox", lambda: self.show_section("Inbox")),
            ("📤 Sent", lambda: self.show_section("Sent")),
            ("📋 Drafts", lambda: self.show_section("Drafts")),
            ("⭐ Starred", lambda: self.show_section("Starred")),
            ("🗑️ Trash", lambda: self.show_section("Trash"))
        ]

        for text, cmd in buttons:
            self.create_menu_button(parent, text, cmd)

    def add_devops_section(self, parent):
        section = tk.LabelFrame(parent, text="DevOps Tools", bg="#f0f0f0", fg="#1a237e", font=("Arial", 12, "bold"))
        section.pack(fill='x', padx=5, pady=5)

        buttons = [
            ("🎮 Kubernetes", lambda: self.show_tool("Kubernetes")),
            ("⚙️ Terraform", lambda: self.show_tool("Terraform")),
            ("🔄 Ansible", lambda: self.show_tool("Ansible")),
            ("🌐 Istio", lambda: self.show_tool("Istio")),
            ("📊 Monitoring", lambda: self.show_tool("Monitoring")),
            ("📦 CI/CD", lambda: self.show_tool("CI/CD")),
            ("🚪 Logout", self.logout)
        ]

        for text, cmd in buttons:
            self.create_menu_button(parent, text, cmd)

    def create_menu_button(self, parent, text, command):
        btn = tk.Button(
            parent,
            text=text,
            command=command,
            font=("Arial", 11),
            bg="white",
            fg="#1a237e",
            width=25,
            relief='flat',
            anchor='w',
            cursor='hand2'
        )
        btn.pack(fill='x', pady=1)
        btn.bind('<Enter>', lambda e: e.widget.config(bg='#e3f2fd'))
        btn.bind('<Leave>', lambda e: e.widget.config(bg='white'))

    def show_welcome_content(self):
        self.clear_content()
        
        # Welcome message
        tk.Label(
            self.content_frame,
            text=f"Welcome {self.current_user['first_name']}!",
            font=("Arial", 24, "bold"),
            fg="#1a237e",
            bg="white"
        ).pack(pady=20)

        # Stats boxes
        stats_frame = tk.Frame(self.content_frame, bg="white")
        stats_frame.pack(pady=20)

        stats = [
            ("📧 Total Emails", "0"),
            ("📥 Unread", "0"),
            ("⚙️ Services", "Active"),
            ("🔄 Last Sync", "Just Now")
        ]

        for title, value in stats:
            stat_box = tk.Frame(stats_frame, bg='#f5f5f5', padx=20, pady=10)
            stat_box.pack(side='left', padx=10)
            tk.Label(stat_box, text=title, font=("Arial", 12, "bold"), bg='#f5f5f5').pack()
            tk.Label(stat_box, text=value, font=("Arial", 16), bg='#f5f5f5').pack()

    def clear_content(self):
        for widget in self.content_frame.winfo_children():
            widget.destroy()

    def show_compose(self): pass
    def show_section(self, name): pass
    def show_tool(self, name): pass
    def logout(self): 
        if messagebox.askyesno("Logout", "Are you sure you want to logout?"):
            # Clear dashboard
            for widget in self.root.winfo_children():
                widget.destroy()
            # Return to login
            from .local_email import LocalEmailApp
            app = LocalEmailApp()
            app.show_frame("login")

    def on_closing(self):
        """Handle window close button"""
        if messagebox.askyesno("Quit", "Do you want to quit?"):
            self.root.quit()
