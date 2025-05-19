import tkinter as tk
from tkinter import ttk, messagebox
import sys
import os
import requests
import json

class EmailApp:
    def __init__(self):
        self.window = tk.Tk()
        self.window.title("OpenMail")
        self.window.geometry("800x600")
        self.center_window()
        
        self.current_user = None
        self.emails = []
        self.data_dir = os.path.join(os.path.dirname(__file__), 'data')
        os.makedirs(self.data_dir, exist_ok=True)
        self.accounts_file = os.path.join(self.data_dir, 'accounts.json')
        self.emails_file = os.path.join(self.data_dir, 'emails.json')

    def center_window(self):
        x = (self.window.winfo_screenwidth() - 800) // 2
        y = (self.window.winfo_screenheight() - 600) // 2
        self.window.geometry(f"800x600+{x}+{y}")

    def setup_storage(self):
        self.data_dir = os.path.join(os.path.dirname(__file__), 'data')
        os.makedirs(self.data_dir, exist_ok=True)
        self.accounts_file = os.path.join(self.data_dir, 'accounts.json')
        self.emails_file = os.path.join(self.data_dir, 'emails.json')

    def setup_main_interface(self):
        # Clear window
        for widget in self.window.winfo_children():
            widget.destroy()

        # Create frames
        nav_frame = tk.Frame(self.window, bg='#001133', height=50)
        nav_frame.pack(fill='x')
        
        sidebar_frame = tk.Frame(self.window, bg='#1a237e', width=200)
        sidebar_frame.pack(side='left', fill='y')
        
        content_frame = tk.Frame(self.window, bg='white')
        content_frame.pack(side='left', fill='both', expand=True)

        # Add navigation elements
        tk.Label(
            nav_frame,
            text="OpenMail",
            font=("Arial", 14, "bold"),
            fg='white',
            bg='#001133'
        ).pack(side='left', padx=20, pady=10)

        # Add sidebar buttons
        sidebar_buttons = [
            ("📝 Compose", self.show_compose),
            ("📥 Inbox", self.show_inbox),
            ("📤 Sent", self.show_sent),
            ("📋 Drafts", self.show_drafts),
            ("⭐ Starred", self.show_starred),
            ("🗑️ Trash", self.show_trash),
            ("⚙️ Settings", self.show_settings),
            ("🚪 Logout", self.logout)
        ]

        for text, command in sidebar_buttons:
            btn = tk.Button(
                sidebar_frame,
                text=text,
                command=command,
                font=("Arial", 12),
                bg='#1a237e',
                fg='white',
                width=20,
                border=0,
                anchor='w'
            )
            btn.pack(pady=2, padx=5)

        # Check if user is logged in
        if os.path.exists(self.accounts_file):
            with open(self.accounts_file, 'r') as f:
                self.current_user = json.load(f)
                email = self.current_user.get('email')
                tk.Label(
                    nav_frame,
                    text=f"Welcome, {email}",
                    font=("Arial", 12),
                    fg='white',
                    bg='#001133'
                ).pack(side='right', padx=20, pady=10)
            
            self.show_dashboard(email)
        else:
            self.show_login()

    def show_login(self):
        # Clear window first
        self.clear_window()

        form_frame = tk.Frame(self.window)
        form_frame.pack(pady=20)

        tk.Label(form_frame, text="Email:").grid(row=0, column=0, pady=5)
        email_entry = tk.Entry(form_frame, width=30)
        email_entry.grid(row=0, column=1, pady=5)

        tk.Label(form_frame, text="Password:").grid(row=1, column=0, pady=5)
        password_entry = tk.Entry(form_frame, width=30, show="*")
        password_entry.grid(row=1, column=1, pady=5)

        tk.Button(
            form_frame,
            text="Login",
            command=lambda: self.login(
                email_entry.get(),
                password_entry.get()
            )
        ).grid(row=2, column=0, columnspan=2, pady=20)

        tk.Button(
            form_frame,
            text="Create Account",
            command=self.show_create_account
        ).grid(row=3, column=0, columnspan=2, pady=5)

    def show_create_account(self):
        # Clear window first
        self.clear_window()
        
        # Create account form
        form_frame = tk.Frame(self.window)
        form_frame.pack(pady=20)

        tk.Label(form_frame, text="First Name:").grid(row=0, column=0, pady=5)
        first_name_entry = tk.Entry(form_frame, width=30)
        first_name_entry.grid(row=0, column=1, pady=5)

        tk.Label(form_frame, text="Last Name:").grid(row=1, column=0, pady=5)
        last_name_entry = tk.Entry(form_frame, width=30)
        last_name_entry.grid(row=1, column=1, pady=5)

        tk.Label(form_frame, text="Username:").grid(row=2, column=0, pady=5)
        username_entry = tk.Entry(form_frame, width=30)
        username_entry.grid(row=2, column=1, pady=5)

        tk.Label(form_frame, text="Password:").grid(row=3, column=0, pady=5)
        password_entry = tk.Entry(form_frame, width=30, show="*")
        password_entry.grid(row=3, column=1, pady=5)

        tk.Label(form_frame, text="Domain:").grid(row=4, column=0, pady=5)
        domain_entry = tk.Entry(form_frame, width=30)
        domain_entry.grid(row=4, column=1, pady=5)

        tk.Button(
            form_frame,
            text="Create Account",
            command=lambda: self.create_account(
                {
                    'first_name': first_name_entry,
                    'last_name': last_name_entry,
                    'username': username_entry,
                    'password': password_entry,
                    'domain': domain_entry
                },
                "Domain"
            )
        ).grid(row=5, column=0, columnspan=2, pady=20)

        tk.Button(
            form_frame,
            text="Back to Login",
            command=self.show_login
        ).grid(row=6, column=0, columnspan=2, pady=5)

    def login(self, email, password):
        # Implement login logic
        if not os.path.exists(self.accounts_file):
            messagebox.showerror("Error", "No accounts found. Please create an account first.")
            return

        with open(self.accounts_file, 'r') as f:
            accounts = json.load(f)

        if email == accounts.get('email') and password == accounts.get('password'):
            messagebox.showinfo("Success", "Login successful!")
            self.show_dashboard(email)
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

    def show_dashboard(self, email):
        # Clear window first
        self.clear_window()
        
        # Create frames
        nav_frame = tk.Frame(self.window, bg='#001133', height=50)
        nav_frame.pack(fill='x')
        
        sidebar_frame = tk.Frame(self.window, bg='#1a237e', width=200)
        sidebar_frame.pack(side='left', fill='y')
        
        content_frame = tk.Frame(self.window, bg='white')
        content_frame.pack(side='left', fill='both', expand=True)

        # Add navigation elements
        tk.Label(
            nav_frame,
            text=f"OpenMail - {email}",
            font=("Arial", 14, "bold"),
            fg='white',
            bg='#001133'
        ).pack(side='left', padx=20, pady=10)

        # Add sidebar buttons
        sidebar_buttons = [
            ("📝 Compose", self.show_compose),
            ("📥 Inbox", self.show_inbox),
            ("📤 Sent", self.show_sent),
            ("📋 Drafts", self.show_drafts),
            ("⭐ Starred", self.show_starred),
            ("🗑️ Trash", self.show_trash),
            ("⚙️ Settings", self.show_settings),
            ("🚪 Logout", self.logout)
        ]

        for text, command in sidebar_buttons:
            btn = tk.Button(
                sidebar_frame,
                text=text,
                command=command,
                font=("Arial", 12),
                bg='#1a237e',
                fg='white',
                width=20,
                border=0,
                anchor='w'
            )
            btn.pack(pady=2, padx=5)

        # Load and display emails
        self.load_emails()
        self.display_emails(content_frame)

    def load_emails(self):
        # For now, just create some dummy emails
        self.emails = [
            {
                'from': 'john@example.com',
                'to': self.current_user['email'],
                'subject': 'Welcome to OpenMail!',
                'date': '2023-10-01',
                'body': 'Thank you for signing up for OpenMail. We are glad to have you!'
            },
            {
                'from': 'jane@example.com',
                'to': self.current_user['email'],
                'subject': 'Your first email',
                'date': '2023-10-02',
                'body': 'This is a test email. Welcome aboard!'
            }
        ]

    def display_emails(self, frame):
        for widget in frame.winfo_children():
            widget.destroy()

        for email in self.emails:
            tk.Label(frame, text=f"From: {email['from']}", anchor='w').pack(fill='x', padx=10, pady=5)
            tk.Label(frame, text=f"To: {email['to']}", anchor='w').pack(fill='x', padx=10, pady=5)
            tk.Label(frame, text=f"Subject: {email['subject']}", anchor='w').pack(fill='x', padx=10, pady=5)
            tk.Label(frame, text=f"Date: {email['date']}", anchor='w').pack(fill='x', padx=10, pady=5)
            tk.Label(frame, text=f"Body: {email['body']}", anchor='w').pack(fill='x', padx=10, pady=5)
            tk.Separator(frame, orient='horizontal').pack(fill='x', pady=5)

    def show_compose(self):
        # Clear window first
        self.clear_window()

        form_frame = tk.Frame(self.window)
        form_frame.pack(pady=20)

        tk.Label(form_frame, text="To:").grid(row=0, column=0, pady=5)
        to_entry = tk.Entry(form_frame, width=30)
        to_entry.grid(row=0, column=1, pady=5)

        tk.Label(form_frame, text="Subject:").grid(row=1, column=0, pady=5)
        subject_entry = tk.Entry(form_frame, width=30)
        subject_entry.grid(row=1, column=1, pady=5)

        tk.Label(form_frame, text="Body:").grid(row=2, column=0, pady=5)
        body_text = tk.Text(form_frame, width=30, height=10)
        body_text.grid(row=2, column=1, pady=5)

        tk.Button(
            form_frame,
            text="Send",
            command=lambda: self.send_email(
                to_entry.get(),
                subject_entry.get(),
                body_text.get("1.0", tk.END)
            )
        ).grid(row=3, column=0, columnspan=2, pady=20)

        tk.Button(
            form_frame,
            text="Back to Inbox",
            command=lambda: self.show_inbox()
        ).grid(row=4, column=0, columnspan=2, pady=5)

    def send_email(self, to, subject, body):
        # For now, just show a success message
        messagebox.showinfo("Success", "Email sent!")
        self.show_inbox()

    def show_inbox(self):
        # Clear window first
        self.clear_window()

        content_frame = tk.Frame(self.window, bg='white')
        content_frame.pack(side='left', fill='both', expand=True)

        tk.Label(content_frame, text="Inbox", font=("Arial", 16, "bold")).pack(pady=10)

        self.load_emails()
        self.display_emails(content_frame)

        tk.Button(
            content_frame,
            text="Refresh",
            command=lambda: self.show_inbox()
        ).pack(pady=10)

    def show_sent(self):
        # Clear window first
        self.clear_window()

        content_frame = tk.Frame(self.window, bg='white')
        content_frame.pack(side='left', fill='both', expand=True)

        tk.Label(content_frame, text="Sent Items", font=("Arial", 16, "bold")).pack(pady=10)

        # For now, just display a message
        tk.Label(content_frame, text="No sent items yet.", bg='white').pack(pady=20)

        tk.Button(
            content_frame,
            text="Back to Inbox",
            command=lambda: self.show_inbox()
        ).pack(pady=10)

    def show_drafts(self):
        # Clear window first
        self.clear_window()

        content_frame = tk.Frame(self.window, bg='white')
        content_frame.pack(side='left', fill='both', expand=True)

        tk.Label(content_frame, text="Drafts", font=("Arial", 16, "bold")).pack(pady=10)

        # For now, just display a message
        tk.Label(content_frame, text="No drafts yet.", bg='white').pack(pady=20)

        tk.Button(
            content_frame,
            text="Back to Inbox",
            command=lambda: self.show_inbox()
        ).pack(pady=10)

    def show_starred(self):
        # Clear window first
        self.clear_window()

        content_frame = tk.Frame(self.window, bg='white')
        content_frame.pack(side='left', fill='both', expand=True)

        tk.Label(content_frame, text="Starred", font=("Arial", 16, "bold")).pack(pady=10)

        # For now, just display a message
        tk.Label(content_frame, text="No starred emails yet.", bg='white').pack(pady=20)

        tk.Button(
            content_frame,
            text="Back to Inbox",
            command=lambda: self.show_inbox()
        ).pack(pady=10)

    def show_trash(self):
        # Clear window first
        self.clear_window()

        content_frame = tk.Frame(self.window, bg='white')
        content_frame.pack(side='left', fill='both', expand=True)

        tk.Label(content_frame, text="Trash", font=("Arial", 16, "bold")).pack(pady=10)

        # For now, just display a message
        tk.Label(content_frame, text="No trashed emails yet.", bg='white').pack(pady=20)

        tk.Button(
            content_frame,
            text="Back to Inbox",
            command=lambda: self.show_inbox()
        ).pack(pady=10)

    def show_settings(self):
        # Clear window first
        self.clear_window()

        content_frame = tk.Frame(self.window, bg='white')
        content_frame.pack(side='left', fill='both', expand=True)

        tk.Label(content_frame, text="Settings", font=("Arial", 16, "bold")).pack(pady=10)

        # For now, just display a message
        tk.Label(content_frame, text="No settings available yet.", bg='white').pack(pady=20)

        tk.Button(
            content_frame,
            text="Back to Inbox",
            command=lambda: self.show_inbox()
        ).pack(pady=10)

    def logout(self):
        if messagebox.askyesno("Confirm Logout", "Are you sure you want to logout?"):
            self.current_user = None
            if os.path.exists(self.accounts_file):
                os.remove(self.accounts_file)
            self.show_login()

    def clear_window(self):
        for widget in self.window.winfo_children():
            widget.destroy()

def main():
    app = EmailApp()
    app.window.mainloop()

if __name__ == "__main__":
    main()
