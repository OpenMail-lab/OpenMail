import tkinter as tk
from tkinter import ttk, messagebox
from .mail_service import mail_service
from .nat_traversal import get_public_ip, setup_nat_connection
import flask

class LocalEmailApp:
    def __init__(self):
        # Basic setup
        self.root = tk.Tk()
        self.root.title("OpenMail - Local Email")
        self.root.geometry("400x600")
        self.root.configure(bg="#001133")
        
        # Initialize data
        self.users = {}
        self.frames = {}
        self.current_frame = None
        self.ip_address = self.get_ip_safely()
        
        # Create main frame
        self.main_frame = tk.Frame(self.root, bg="#001133")
        self.main_frame.pack(fill="both", expand=True)
        
        # Create frames and show login
        self.setup_frames()
        self.show_frame("login")

    def get_ip_safely(self):
        """Get IP with fallback and error handling"""
        try:
            ip = get_public_ip()
            if setup_nat_connection():
                return ip
            return "127.0.0.1"
        except Exception as e:
            print(f"NAT Error: {str(e)}")
            return "127.0.0.1"
    
    def create_login_frame(self, container):
        frame = tk.Frame(container, bg="#001133")
        
        # Title
        tk.Label(
            frame,
            text="Local Email Login",
            font=("Arial", 24, "bold"),
            fg="#00f3ff",
            bg="#001133"
        ).pack(pady=(40,30))
        
        # Email
        tk.Label(
            frame,
            text="Email",
            font=("Arial", 12),
            fg="#00f3ff",
            bg="#001133"
        ).pack()
        
        email_frame = tk.Frame(frame, bg="#001133")
        email_frame.pack(pady=5)
        
        email = tk.Entry(email_frame, width=15)
        email.pack(side='left')
        
        # Get public IP for email domain
        public_ip = get_public_ip()
        tk.Label(
            email_frame,
            text=f"@{public_ip}.local",
            font=("Arial", 11),
            fg="#00f3ff",
            bg="#001133"
        ).pack(side='left')
        
        # Password
        tk.Label(
            frame,
            text="Password",
            font=("Arial", 12),
            fg="#00f3ff",
            bg="#001133"
        ).pack(pady=(15,5))
        
        password = tk.Entry(frame, width=30, show="•")
        password.pack()
        
        # Navigation buttons
        btn_frame = tk.Frame(frame, bg="#001133")
        btn_frame.pack(pady=30)
        
        tk.Button(
            btn_frame,
            text="← Back",
            command=self.root.destroy,
            bg="#1E88E5",
            fg="white",
            font=("Arial", 12),
            width=12
        ).pack(side=tk.LEFT, padx=5)
        
        tk.Button(
            btn_frame,
            text="Login →",
            command=lambda: self.login(email.get(), password.get()),
            bg="#2962ff",
            fg="white",
            font=("Arial", 12),
            width=12
        ).pack(side=tk.LEFT, padx=5)
        
        # Register link
        tk.Button(
            frame,
            text="Create Account →",
            command=lambda: self.show_frame("register"),
            bg="#001133",
            fg="#00f3ff",
            font=("Arial", 10),
            bd=0,
            cursor="hand2"
        ).pack(pady=10)
        
        return frame

    def create_register_frame(self, container):
        frame = tk.Frame(container, bg="#001133")
        
        # Title
        tk.Label(
            frame,
            text="Create Account",
            font=("Arial", 24, "bold"),
            fg="#00f3ff",
            bg="#001133"
        ).pack(pady=(40,30))
        
        # Form fields
        fields = [
            ("First Name", "first_name"),
            ("Last Name", "last_name"),
            ("Email", "email"),
            ("Password", "password"),
            ("Confirm Password", "confirm_password")
        ]
        
        entries = {}
        for label_text, field_name in fields:
            tk.Label(
                frame,
                text=label_text,
                font=("Arial", 12),
                fg="#00f3ff",
                bg="#001133"
            ).pack(pady=(10,0))
            
            if field_name == "email":
                # Special handling for email with domain
                email_frame = tk.Frame(frame, bg="#001133")
                email_frame.pack(pady=5)
                
                entry = tk.Entry(email_frame, width=15)
                entry.pack(side='left')
                
                public_ip = get_public_ip()
                tk.Label(
                    email_frame,
                    text=f"@{public_ip}.local",
                    font=("Arial", 11),
                    fg="#00f3ff",
                    bg="#001133"
                ).pack(side='left')
            else:
                entry = tk.Entry(
                    frame,
                    width=30,
                    font=("Arial", 11),
                    bg="#000a1f",
                    fg="white",
                    insertbackground="white"
                )
                if 'password' in field_name:
                    entry.configure(show="•")
                entry.pack(pady=5)
            
            entries[field_name] = entry
        
        # Navigation buttons
        btn_frame = tk.Frame(frame, bg="#001133")
        btn_frame.pack(pady=30)
        
        tk.Button(
            btn_frame,
            text="← Back",
            command=lambda: self.show_frame("login"),
            bg="#1E88E5",
            fg="white",
            font=("Arial", 12),
            width=12
        ).pack(side=tk.LEFT, padx=5)
        
        tk.Button(
            btn_frame,
            text="Register →",
            command=lambda: self.validate_and_register(entries),
            bg="#2962ff",
            fg="white",
            font=("Arial", 12),
            width=12
        ).pack(side=tk.LEFT, padx=5)
        
        return frame

    def show_frame(self, frame_name):
        """Show the specified frame"""
        if self.current_frame:
            self.current_frame.pack_forget()
        if frame_name in self.frames:
            self.current_frame = self.frames[frame_name]
            self.current_frame.pack(fill="both", expand=True)
        else:
            print(f"Frame {frame_name} not found")

    def setup_frames(self):
        """Initialize all frames"""
        self.frames = {
            "login": self.create_login_frame(self.main_frame),
            "register": self.create_register_frame(self.main_frame)
        }
        # Show initial login frame
        self.show_frame("login")

    def login(self, email, password):
        if email in self.users and self.users[email]['password'] == password:
            messagebox.showinfo("Success", "Login successful!")
            user_data = {
                'email': email,
                'password': self.users[email]['password'],
                'first_name': self.users[email]['first_name'],
                'last_name': self.users[email]['last_name']
            }
            
            # Clear current window contents
            for widget in self.root.winfo_children():
                widget.destroy()
                
            # Show dashboard in current window
            from .dashboard import MainDashboard
            dashboard = MainDashboard(self.root, user_data)
        else:
            messagebox.showerror("Error", "Invalid email or password")

    def validate_and_register(self, entries):
        # Get all values
        values = {k: v.get().strip() for k, v in entries.items()}
        
        # Validation
        if not all(values.values()):
            messagebox.showerror("Error", "All fields are required!")
            return
        
        if values['password'] != values['confirm_password']:
            messagebox.showerror("Error", "Passwords do not match!")
            return
        
        if values['email'] in self.users:
            messagebox.showerror("Error", "Email already registered!")
            return
        
        # Register user
        self.users[values['email']] = {
            'password': values['password'],
            'first_name': values['first_name'],
            'last_name': values['last_name']
        }
        
        messagebox.showinfo("Success", "Registration successful!")
        self.show_frame("login")  # Switch back to login frame

    def run(self):
        self.root.mainloop()
