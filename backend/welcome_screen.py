import tkinter as tk
from tkinter import ttk, messagebox
from .local_email import LocalEmailApp
from .domain_email import DomainEmailApp

class WelcomeScreen:
    def __init__(self):
        # Colors
        self.COLORS = {
            'bg': '#001133',
            'nav_bg': '#000a1f',
            'sidebar_bg': '#000a1f',
            'text': '#00f3ff',
            'button': '#2962ff',
            'button_hover': '#1565C0'
        }

        # Initialize root
        self.root = tk.Tk()
        self.root.title("OpenMail")
        self.root.geometry("800x600")
        self.root.configure(bg=self.COLORS['bg'])

        # Initialize sidebar state
        self.sidebar_visible = True
        self.sidebar_width = 200

        # Initialize buttons info
        self.buttons_info = {
            "🌐 Domain Email": {
                "command": self.show_domain_email,
                "color": "#2962ff",
                "description": "Create professional email with your own domain"
            },
            "💻 Without Domain Email": {
                "command": self.show_local_email,
                "color": "#1E88E5",
                "description": "Quick local email setup"
            }
        }

        # Create frames in correct order
        self.setup_navbar()
        self.setup_sidebar()
        self.setup_main_frame()
        self.setup_ui()

    def setup_navbar(self):
        # Create navbar
        navbar = tk.Frame(self.root, bg=self.COLORS['nav_bg'], height=50)
        navbar.pack(fill='x', side='top')

        # Add menu button
        menu_btn = tk.Button(
            navbar,
            text="☰",
            font=("Arial", 16),
            bg=self.COLORS['nav_bg'],
            fg=self.COLORS['text'],
            bd=0,
            command=self.toggle_sidebar
        )
        menu_btn.pack(side='left', padx=10)

        # Add title
        tk.Label(
            navbar,
            text="OpenMail",
            font=("Arial", 16, "bold"),
            bg=self.COLORS['nav_bg'],
            fg=self.COLORS['text']
        ).pack(side='left', padx=10)

    def setup_sidebar(self):
        # Create sidebar
        self.sidebar = tk.Frame(
            self.root,
            bg=self.COLORS['sidebar_bg'],
            width=self.sidebar_width
        )
        self.sidebar.pack(side='left', fill='y')
        
        # Prevent sidebar from shrinking
        self.sidebar.pack_propagate(False)

        # Add sidebar options
        options = [
            ("About", self.show_about),
            ("Settings", self.show_settings),
            ("Help", self.show_help)
        ]

        for text, command in options:
            tk.Button(
                self.sidebar,
                text=text,
                font=("Arial", 12),
                bg=self.COLORS['sidebar_bg'],
                fg=self.COLORS['text'],
                bd=0,
                command=command
            ).pack(fill='x', pady=2)

    def setup_main_frame(self):
        # Create main frame
        self.main_frame = tk.Frame(self.root, bg=self.COLORS['bg'])
        self.main_frame.pack(fill='both', expand=True)

    def setup_ui(self):
        # Clear existing content
        for widget in self.main_frame.winfo_children():
            widget.destroy()

        # Title
        title = tk.Label(
            self.main_frame,
            text="OpenMail",
            font=("Arial", 36, "bold"),
            fg=self.COLORS['text'],
            bg=self.COLORS['bg']
        )
        title.pack(pady=(100, 50))

        # Create button frame
        btn_frame = tk.Frame(self.main_frame, bg=self.COLORS['bg'])
        btn_frame.pack(pady=30)

        # Create buttons
        for text, info in self.buttons_info.items():
            btn = tk.Button(
                btn_frame,
                text=text,
                command=info["command"],
                font=("Arial", 14, "bold"),
                width=30,
                height=2,
                bg=info["color"],
                fg="white",
                relief="flat"
            )
            btn.pack(pady=15)

    def toggle_sidebar(self):
        if self.sidebar_visible:
            self.sidebar.pack_forget()
            self.sidebar_visible = False
        else:
            self.sidebar.pack(side='left', fill='y', before=self.main_frame)
            self.sidebar_visible = True

    def show_about(self):
        messagebox.showinfo("About", "OpenMail v1.0")

    def show_settings(self):
        messagebox.showinfo("Settings", "Settings coming soon!")

    def show_help(self):
        messagebox.showinfo("Help", "Help documentation coming soon!")

    def show_domain_email(self):
        self.root.destroy()
        app = DomainEmailApp()
        app.run()

    def show_local_email(self):
        self.root.destroy()
        try:
            app = LocalEmailApp()
            app.run()
        except Exception as e:
            print(f"Error launching Local Email: {e}")

    def run(self):
        self.root.mainloop()

__all__ = ['WelcomeScreen']
