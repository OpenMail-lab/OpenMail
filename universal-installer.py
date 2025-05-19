import tkinter as tk
from tkinter import ttk, messagebox
import sys
import os
import requests

def get_public_ip():
    try:
        return requests.get("https://api.ipify.org").text.strip()
    except:
        return "127.0.0.1"

class MainApp:
    def __init__(self):
        # Create main window
        self.root = tk.Tk()
        self.root.title("OpenMail")
        self.root.geometry("800x600")
        self.root.configure(bg="#001133")
        
        # Center window
        screen_width = self.root.winfo_screenwidth()
        screen_height = self.root.winfo_screenheight()
        x = (screen_width - 800) // 2
        y = (screen_height - 600) // 2
        self.root.geometry(f"800x600+{x}+{y}")

        # Add elements
        self.setup_ui()

        self.current_user = None
        self.current_email = None
        self.emails = []  # Store user emails

        self.content_frame = None
        self.has_devops_tools = False  # Track DevOps tools initialization

    def setup_ui(self):
        # Title
        tk.Label(
            self.root,
            text="OpenMail",
            font=("Arial", 32, "bold"),
            fg="white",
            bg="#001133"
        ).pack(pady=40)

        # Button Frame
        btn_frame = tk.Frame(self.root, bg="#001133")
        btn_frame.pack(pady=20)

        # Email Buttons
        self.create_button(btn_frame, "Domain Email", self.show_domain_form)
        self.create_button(btn_frame, "Local Email", self.show_local_form)

    def create_button(self, parent, text, command):
        btn = tk.Button(
            parent,
            text=text,
            command=command,
            font=("Arial", 14),
            width=20,
            height=2,
            bg="#2962ff",
            fg="white"
        )
        btn.pack(pady=10)

    def show_domain_form(self):
        self.clear_window()
        self.show_form("Domain")

    def show_local_form(self):
        self.clear_window()
        
        # Get IP before creating form
        public_ip = get_public_ip()

        # Form Frame
        form_frame = tk.Frame(self.root, bg="#001133")
        form_frame.pack(pady=40)

        # Title
        tk.Label(
            form_frame,
            text="Create Local Email",
            font=("Arial", 24, "bold"),
            fg="white",
            bg="#001133"
        ).pack(pady=20)

        # Entry Frame
        entry_frame = tk.Frame(form_frame, bg="#001133")
        entry_frame.pack(pady=10)

        # Fields
        entries = {}
        fields = [
            ("First Name:", "first_name"),
            ("Last Name:", "last_name"),
            ("Username:", "username"),
            ("Password:", "password")
        ]

        for i, (label_text, field) in enumerate(fields):
            # Create frame for each row
            row_frame = tk.Frame(entry_frame, bg="#001133")
            row_frame.pack(pady=5, fill='x')

            # Label
            tk.Label(
                row_frame,
                text=label_text,
                font=("Arial", 12),
                fg="white",
                bg="#001133",
                width=15,
                anchor='e'
            ).pack(side='left', padx=5)

            # Entry
            entry = tk.Entry(row_frame, width=30)
            if 'password' in field:
                entry.configure(show='*')
            entry.pack(side='left', padx=5)
            entries[field] = entry

            # Add IP preview for username field
            if field == "username":
                tk.Label(
                    row_frame,
                    text=f"@{public_ip}",
                    font=("Arial", 12),
                    fg="#00ffff",
                    bg="#001133"
                ).pack(side='left', padx=5)

        # Preview Label
        self.preview_label = tk.Label(
            form_frame,
            text=f"Your email will be: _____@{public_ip}",
            font=("Arial", 12),
            fg="#00ffff",
            bg="#001133"
        )
        self.preview_label.pack(pady=20)

        # Update preview when typing username
        def update_preview(*args):
            username = entries['username'].get()
            if username:
                self.preview_label.config(text=f"Your email will be: {username}@{public_ip}")
            else:
                self.preview_label.config(text=f"Your email will be: _____@{public_ip}")

        entries['username'].bind('<KeyRelease>', update_preview)

        # Create Account Button
        tk.Button(
            form_frame,
            text="Create Account",
            command=lambda: self.create_local_account(entries, public_ip),
            font=("Arial", 14),
            bg="#2962ff",
            fg="white",
            width=20
        ).pack(pady=20)

        # Back Button
        tk.Button(
            form_frame,
            text="← Back",
            command=self.setup_ui,
            font=("Arial", 10),
            bg="#1E88E5",
            fg="white"
        ).pack(pady=10)

    def show_form(self, form_type):
        # Form Frame
        form_frame = tk.Frame(self.root, bg="#001133")
        form_frame.pack(pady=40)

        # Title
        tk.Label(
            form_frame,
            text=f"Create {form_type} Email",
            font=("Arial", 24, "bold"),
            fg="white",
            bg="#001133"
        ).pack(pady=20)

        # Form Fields
        entries = {}
        for field in ["First Name", "Last Name", "Username", "Password"]:
            frame = tk.Frame(form_frame, bg="#001133")
            frame.pack(pady=10)
            
            tk.Label(
                frame,
                text=f"{field}:",
                font=("Arial", 12),
                fg="white",
                bg="#001133"
            ).pack(side="left", padx=10)
            
            entry = tk.Entry(frame, width=30)
            if "Password" in field:
                entry.configure(show="*")
            entry.pack(side="left")
            entries[field] = entry

        # Submit Button
        tk.Button(
            form_frame,
            text="Create Account",
            command=lambda: self.create_account(entries, form_type),
            font=("Arial", 12),
            bg="#2962ff",
            fg="white"
        ).pack(pady=20)

        # Back Button
        tk.Button(
            form_frame,
            text="← Back",
            command=self.setup_ui,
            font=("Arial", 10),
            bg="#1E88E5",
            fg="white"
        ).pack()

    def create_account(self, entries, form_type):
        # Validate entries
        if not all(entry.get() for entry in entries.values()):
            messagebox.showerror("Error", "All fields are required!")
            return

        # Show success
        messagebox.showinfo("Success", "Account created successfully!")
        self.setup_ui()

    def create_local_account(self, entries, public_ip):
        # Validate entries
        if not all(entries[field].get() for field in entries.keys()):
            messagebox.showerror("Error", "All fields are required!")
            return

        # Create email address
        username = entries['username'].get()
        email = f"{username}@{public_ip}"
        
        # Store user data
        self.current_user = {
            'first_name': entries['first_name'].get(),
            'last_name': entries['last_name'].get(),
            'email': email,
            'username': username
        }
        self.current_email = email

        # Show success message and open dashboard
        messagebox.showinfo("Success", f"Account created successfully!\n\nYour email: {email}")
        self.show_main_dashboard(email)

    def show_main_dashboard(self, email):
        self.clear_window()

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

        # Email Management Section in Sidebar
        email_frame = tk.LabelFrame(sidebar, text="Email Management", bg="#f0f0f0", fg="#1a237e", font=("Arial", 12, "bold"))
        email_frame.pack(fill='x', padx=5, pady=5)

        email_buttons = [
            ("📝 Compose", lambda: self.show_compose()),
            ("📥 Inbox", lambda: self.show_section("Inbox")),
            ("📤 Sent", lambda: self.show_section("Sent")),
            ("📋 Drafts", lambda: self.show_section("Drafts")),
            ("⭐ Starred", lambda: self.show_section("Starred")),
            ("🗑️ Trash", lambda: self.show_section("Trash"))
        ]

        for text, cmd in email_buttons:
            self.create_menu_button(email_frame, text, cmd)

        # DevOps Tools Section in Sidebar
        devops_frame = tk.LabelFrame(sidebar, text="DevOps Tools", bg="#f0f0f0", fg="#1a237e", font=("Arial", 12, "bold"))
        devops_frame.pack(fill='x', padx=5, pady=5)

        devops_buttons = [
            ("🎮 Kubernetes", lambda: self.show_tool("Kubernetes")),
            ("⚙️ Terraform", lambda: self.show_tool("Terraform")),
            ("🔄 Ansible", lambda: self.show_tool("Ansible")),
            ("🌐 Istio", lambda: self.show_tool("Istio")),
            ("📊 Kiali", lambda: self.show_tool("Kiali")),
            ("📦 Helm", lambda: self.show_tool("Helm")),
            ("🚀 ArgoCD", lambda: self.show_tool("ArgoCD")),
            ("🚪 Logout", self.setup_ui)
        ]

        for text, cmd in devops_buttons:
            self.create_menu_button(devops_frame, text, cmd)

        # Show welcome content
        self.show_welcome_content()

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

    def show_section(self, section_name):
        self.clear_content_area()
        
        # Section header
        tk.Label(
            self.content_area,
            text=section_name,
            font=("Arial", 24, "bold"),
            fg="#1a237e",
            bg="white"
        ).pack(pady=20)

        # Content message
        tk.Label(
            self.content_area,
            text=f"No items in {section_name}",
            font=("Arial", 14),
            fg="#666666",
            bg="white"
        ).pack(pady=10)

    def show_tool(self, tool_name):
        self.clear_content_area()
        
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

    def show_welcome_content(self):
        self.clear_content_frame()
        
        # Welcome message
        tk.Label(
            self.content_frame,
            text="Welcome to OpenMail",
            font=("Arial", 24, "bold"),
            fg="#1a237e",
            bg="white"
        ).pack(pady=20)

        # Stats frame
        stats_frame = tk.Frame(self.content_frame, bg='white')
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

    def clear_content_area(self):
        for widget in self.content_area.winfo_children():
            widget.destroy()

    def clear_content_frame(self):
        for widget in self.content_frame.winfo_children():
            widget.destroy()

    def logout(self):
        if messagebox.askyesno("Logout", "Are you sure you want to logout?"):
            self.current_user = None
            self.current_email = None
            self.setup_ui()  # Return to main screen

    def show_compose(self):
        compose_window = tk.Toplevel(self.root)
        compose_window.title("New Message")
        compose_window.geometry("600x500")
        compose_window.configure(bg="white")
        compose_window.transient(self.root)
        compose_window.grab_set()

        # Add compose form with improved styling
        tk.Label(compose_window, text="To:", bg="white").pack(anchor='w', padx=10, pady=5)
        to_entry = tk.Entry(compose_window, width=50)
        to_entry.pack(fill='x', padx=10)

        tk.Label(compose_window, text="Subject:", bg="white").pack(anchor='w', padx=10, pady=5)
        subject_entry = tk.Entry(compose_window, width=50)
        subject_entry.pack(fill='x', padx=10)

        tk.Label(compose_window, text="Message:", bg="white").pack(anchor='w', padx=10, pady=5)
        message_text = tk.Text(compose_window, height=15)
        message_text.pack(fill='both', expand=True, padx=10, pady=5)

        # Buttons frame
        btn_frame = tk.Frame(compose_window, bg="white")
        btn_frame.pack(fill='x', padx=10, pady=10)

        # Send button
        tk.Button(
            btn_frame,
            text="Send",
            command=lambda: self.send_email(
                to_entry.get(),
                subject_entry.get(),
                message_text.get("1.0", "end"),
                compose_window
            ),
            bg="#2962ff",
            fg="white",
            width=15,
            height=2
        ).pack(side='left', padx=5)

        # Cancel button
        tk.Button(
            btn_frame,
            text="Cancel",
            command=compose_window.destroy,
            bg="#e0e0e0",
            fg="black",
            width=15,
            height=2
        ).pack(side='left', padx=5)

    # Add these empty methods to handle button clicks
    def show_sent(self): pass
    def show_drafts(self): pass
    def show_starred(self): pass
    def show_trash(self): pass
    def show_settings(self): pass

    def send_email(self, to, subject, message):
        messagebox.showinfo("Success", "Email sent successfully!")

    def clear_window(self):
        for widget in self.root.winfo_children():
            widget.destroy()

    def run(self):
        self.root.mainloop()

if __name__ == "__main__":
    app = MainApp()
    app.run()