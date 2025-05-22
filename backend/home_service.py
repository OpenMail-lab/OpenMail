import tkinter as tk
from tkinter import ttk, messagebox
import sys
import os
import requests
import json
from .dashboard import DashboardUI

class EmailApp:
    def __init__(self):
        self.window = tk.Tk()
        self.window.title("OpenMail")
        self.window.geometry("800x600")
        self.window.configure(bg="white")  # Set initial window background
        self.center_window()
        
        self.current_user = None
        self.emails = []
        self.data_dir = os.path.join(os.path.dirname(__file__), 'data')
        os.makedirs(self.data_dir, exist_ok=True)
        self.accounts_file = os.path.join(self.data_dir, 'accounts.json')
        self.emails_file = os.path.join(self.data_dir, 'emails.json')
        self.page = 0
        self.items_per_page = 10
        self.history = []
        self.current_view = None
        self.window_initialized = False
        
        self.COLORS = {
            'bg': '#001133',
            'nav_bg': '#1a237e',
            'text': '#ffffff',
            'button': '#2962ff',
            'hover': '#1565C0'
        }
        
        # Setup storage before UI
        self.setup_storage()
        
        # Create main frame first - with white background
        self.main_frame = tk.Frame(self.window, bg='white')
        self.main_frame.pack(fill='both', expand=True)
        
        self.show_login()
        
    def center_window(self):
        x = (self.window.winfo_screenwidth() - 800) // 2
        y = (self.window.winfo_screenheight() - 600) // 2
        self.window.geometry(f"800x600+{x}+{y}")

    def setup_storage(self):
        self.data_dir = os.path.join(os.path.dirname(__file__), 'data')
        os.makedirs(self.data_dir, exist_ok=True)
        self.accounts_file = os.path.join(self.data_dir, 'accounts.json')
        self.emails_file = os.path.join(self.data_dir, 'emails.json')

    def show_login(self):
        self.clear_window()
        # Start closing animation before showing login
        self.closing_gen = self.closing_sequence()
        self.run_closing_animation()
        
        # Create futuristic login form
        login_frame = tk.Frame(self.window)
        login_frame.pack(expand=True)
        
        # Modern login inputs
        email = tk.Entry(login_frame, width=30)
        email.pack(pady=10)
        email.insert(0, "Email")
        
        password = tk.Entry(login_frame, width=30, show="*")
        password.pack(pady=10)
        password.insert(0, "Password")
        
        login_btn = tk.Button(
            login_frame,
            text="Login",
            width=20,
            command=lambda: self.login(email.get(), password.get())
        )
        login_btn.pack(pady=20)

    def closing_sequence(self):
        pass
    
    def run_closing_animation(self):
        self.setup_main_interface()

    def login(self, email, password):
        if not os.path.exists(self.accounts_file):
            messagebox.showerror("Error", "No accounts found. Please create an account first.")
            return

        with open(self.accounts_file, 'r') as f:
            accounts = json.load(f)

        if email == accounts.get('email') and password == accounts.get('password'):
            messagebox.showinfo("Success", "Login successful!")
            self.clear_window()
            from .dashboard import MainDashboard
            dashboard = MainDashboard(self.window, accounts)
        else:
            messagebox.showerror("Error", "Invalid email or password.")

    def get_public_ip(self):
        try:
            return requests.get("https://api.ipify.org").text.strip()
        except:
            return "127.0.0.1"

    def create_account(self, entries, form_type):
        if not all(entries[k].get() for k in entries):
            messagebox.showerror("Error", "All fields are required!")
            return

        public_ip = self.get_public_ip()
        email = f"{entries['username'].get()}@{public_ip}"
        
        account = {
            'email': email,
            'first_name': entries['first_name'].get(),
            'last_name': entries['last_name'].get(),
            'password': entries['password'].get()
        }

        # Save account
        with open(self.accounts_file, 'w') as f:
            json.dump(account, f)

        messagebox.showinfo("Success", f"Account created!\nYour email: {email}")
        self.show_dashboard(email)

    def setup_navbar(self, email):
        nav_frame = tk.Frame(self.window, bg=self.COLORS['nav_bg'], height=50)
        nav_frame.pack(fill='x', side='top')

        # App name
        tk.Label(
            nav_frame,
            text="OpenMail",
            font=("Arial", 20, "bold"),
            fg=self.COLORS['text'],
            bg=self.COLORS['nav_bg']
        ).pack(side='left', padx=20)

        # Right side menu
        right_menu = tk.Frame(nav_frame, bg=self.COLORS['nav_bg'])
        right_menu.pack(side='right', padx=20)

        # Email address
        tk.Label(
            right_menu,
            text=f"👤 {email}",
            font=("Arial", 12),
            fg=self.COLORS['text'],
            bg=self.COLORS['nav_bg']
        ).pack(side='left', padx=10)

        # Settings dropdown
        settings_btn = tk.Menubutton(
            right_menu,
            text="⚙️",
            font=("Arial", 16),
            bg=self.COLORS['nav_bg'],
            fg=self.COLORS['text']
        )
        settings_btn.pack(side='left')

        settings_menu = tk.Menu(settings_btn, tearoff=0)
        settings_btn['menu'] = settings_menu
        settings_menu.add_command(label="Settings", command=self.show_settings)
        settings_menu.add_separator()
        settings_menu.add_command(label="Logout", command=self.logout)

    def show_dashboard(self, email):
        self.clear_window()
        
        # Setup navbar first
        self.setup_navbar(email)
        
        # Main container
        main_container = tk.Frame(self.window)
        main_container.pack(fill='both', expand=True)
        
        # Create fixed-width sidebar
        sidebar = tk.Frame(main_container, bg="#f0f0f0", width=250)
        sidebar.pack(side='left', fill='y')
        sidebar.pack_propagate(False)
        
        # Create content area
        self.content_area = tk.Frame(main_container, bg="white")
        self.content_area.pack(side='left', fill='both', expand=True)
        
        # Add sidebar sections
        self.add_email_section(sidebar)
        self.add_devops_section(sidebar)
        
        # Show welcome stats
        self.show_welcome_content()

    def add_email_section(self, sidebar):
        email_frame = tk.LabelFrame(
            sidebar, 
            text="Email Management",
            bg="#f0f0f0",
            fg="#1a237e",
            font=("Arial", 12, "bold")
        )
        email_frame.pack(fill='x', padx=5, pady=5)

        email_buttons = [
            ("📝 Compose", self.show_compose),
            ("📥 Inbox", lambda: self.show_section("Inbox")),
            ("📤 Sent", lambda: self.show_section("Sent")),
            ("📋 Drafts", lambda: self.show_section("Drafts")),
            ("⭐ Starred", lambda: self.show_section("Starred")),
            ("🗑️ Trash", lambda: self.show_section("Trash"))
        ]

        for text, cmd in email_buttons:
            self.create_menu_button(email_frame, text, cmd)

    def add_devops_section(self, sidebar):
        devops_frame = tk.LabelFrame(
            sidebar,
            text="DevOps Tools",
            bg="#f0f0f0",
            fg="#1a237e",
            font=("Arial", 12, "bold")
        )
        devops_frame.pack(fill='x', padx=5, pady=5)

        devops_buttons = [
            ("🎮 Kubernetes", lambda: self.show_tool("Kubernetes")),
            ("⚙️ Terraform", lambda: self.show_tool("Terraform")),
            ("🔄 Ansible", lambda: self.show_tool("Ansible")),
            ("🌐 Istio", lambda: self.show_tool("Istio")),
            ("📊 Kiali", lambda: self.show_tool("Kiali")),
            ("📦 Helm", lambda: self.show_tool("Helm")),
            ("🚀 ArgoCD", lambda: self.show_tool("ArgoCD")),
            ("🚪 Logout", self.logout)
        ]

        for text, cmd in devops_buttons:
            self.create_menu_button(devops_frame, text, cmd)

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
        
        # Welcome message with user name
        welcome_text = f"Welcome {self.current_user.get('first_name', '')}!"
        tk.Label(
            self.content_area,
            text=welcome_text,
            font=("Arial", 24, "bold"),
            fg="#1a237e",
            bg="white"
        ).pack(pady=20)

        # Stats boxes
        self.show_stats_boxes()

    def show_stats_boxes(self):
        """Show email and system statistics"""
        stats_frame = tk.Frame(self.content_area, bg='white')
        stats_frame.pack(pady=20)

        stats = [
            ("📧 Total Emails", "0"),
            ("📥 Unread", "0"),
            ("⚙️ Services", "All Active"),
            ("🔄 Last Sync", "Just Now")
        ]

        for title, value in stats:
            stat_box = tk.Frame(stats_frame, bg='#f5f5f5', padx=20, pady=10)
            stat_box.pack(side='left', padx=10)
            
            tk.Label(stat_box, text=title, font=("Arial", 12, "bold"), bg='#f5f5f5').pack()
            tk.Label(stat_box, text=value, font=("Arial", 16), bg='#f5f5f5').pack()

    def show_tool(self, tool_name):
        """Show DevOps tool interface"""
        self.clear_content()
        
        # Tool header
        tk.Label(
            self.content_area,
            text=f"{tool_name}",
            font=("Arial", 24, "bold"),
            fg="#1a237e",
            bg="white"
        ).pack(pady=20)

        # Tool description
        descriptions = {
            "Kubernetes": "Container Orchestration Platform",
            "Terraform": "Infrastructure as Code Tool",
            "Ansible": "Automation Platform",
            "Istio": "Service Mesh for Kubernetes",
            "Kiali": "Observability for Service Mesh",
            "Helm": "Package Manager for Kubernetes",
            "ArgoCD": "Declarative GitOps CD"
        }

        tk.Label(
            self.content_area,
            text=descriptions.get(tool_name, "DevOps Tool"),
            font=("Arial", 14),
            fg="#666666",
            bg="white"
        ).pack(pady=10)

        # Status indicator
        tk.Label(
            self.content_area,
            text="Status: Ready ✅",
            font=("Arial", 12),
            fg="green",
            bg="white"
        ).pack(pady=10)

    def clear_content(self):
        """Clear only the content area"""
        if hasattr(self, 'content_area'):
            for widget in self.content_area.winfo_children():
                widget.destroy()
            self.content_area.configure(bg="white")  # Ensure white background

    def show_main_dashboard(self, user_data):
        """Initialize and show the dashboard"""
        self.clear_window()
        from .dashboard import MainDashboard
        MainDashboard(self.window, user_data)

def main():
    app = EmailApp()
    app.window.mainloop()

if __name__ == "__main__":
    main()
