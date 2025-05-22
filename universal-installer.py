import tkinter as tk
from tkinter import ttk, scrolledtext, messagebox
import threading
import time
import sys
import os

# Add this at the top to ensure backend is in path
sys.path.append(os.path.join(os.path.dirname(__file__)))

class InstallerUI:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("OpenMail Setup")
        self.root.geometry("800x600")
        self.root.configure(bg='#001133')
        
        self.accepted_terms = tk.BooleanVar()
        self.accepted_privacy = tk.BooleanVar()
        self.installation_complete = False  # Add flag for completion
        self.setup_ui()

    def setup_ui(self):
        # Title
        tk.Label(
            self.root,
            text="OpenMail Setup",
            font=("Arial", 32, "bold"),
            fg='cyan',
            bg='#001133'
        ).pack(pady=20)

        # Progress Frame - Moved to top
        self.progress_frame = tk.LabelFrame(
            self.root,
            text="Installation Progress",
            fg='cyan',
            bg='#001133',
            font=("Arial", 12)
        )
        self.progress_frame.pack(pady=20, fill='x', padx=50)

        # Overall progress
        tk.Label(
            self.progress_frame,
            text="Overall Progress:",
            fg='white',
            bg='#001133'
        ).pack()
        
        self.main_progress = ttk.Progressbar(
            self.progress_frame,
            length=700,
            mode='determinate'
        )
        self.main_progress.pack(pady=5)

        # Current task progress
        self.status_label = tk.Label(
            self.progress_frame,
            text="Please review terms and conditions below...",
            fg='white',
            bg='#001133'
        )
        self.status_label.pack()

        self.detail_label = tk.Label(
            self.progress_frame,
            text="",
            fg='cyan',
            bg='#001133'
        )
        self.detail_label.pack()

        self.task_progress = ttk.Progressbar(
            self.progress_frame,
            length=700,
            mode='determinate'
        )
        self.task_progress.pack(pady=5)

        # Terms & Privacy - Moved below progress
        terms_frame = tk.Frame(self.root, bg='#001133')
        terms_frame.pack(pady=10, fill='x', padx=50)

        # Terms text
        terms_text = scrolledtext.ScrolledText(
            terms_frame, 
            width=60, 
            height=8,
            font=("Arial", 10)
        )
        terms_text.pack(pady=10)
        terms_text.insert('1.0', """Terms and Conditions:
1. By installing OpenMail, you agree to use the software responsibly
2. This software includes open source components
3. You agree to not modify or reverse engineer the software
4. The software is provided "as is" without warranty

Privacy Policy:
1. We collect basic usage statistics to improve the software
2. Your email data remains private and encrypted
3. We do not share your data with third parties
4. You can opt-out of analytics at any time""")
        terms_text.configure(state='disabled')

        # Checkboxes
        tk.Checkbutton(
            terms_frame,
            text="I accept the Terms and Conditions",
            variable=self.accepted_terms,
            bg='#001133',
            fg='white',
            selectcolor='#2962ff',
            command=self.check_acceptance
        ).pack()

        tk.Checkbutton(
            terms_frame,
            text="I accept the Privacy Policy",
            variable=self.accepted_privacy,
            bg='#001133',
            fg='white',
            selectcolor='#2962ff',
            command=self.check_acceptance
        ).pack()

        # Control buttons
        self.btn_frame = tk.Frame(self.root, bg='#001133')
        self.btn_frame.pack(side='bottom', pady=20)
        
        self.install_btn = tk.Button(
            self.btn_frame,
            text="Install",
            command=self.start_installation,
            font=("Arial", 12),
            bg='#2962ff',
            fg='white',
            width=15,
            state='disabled'
        )
        self.install_btn.pack(side='right', padx=5)

        tk.Button(
            self.btn_frame,
            text="Cancel",
            command=self.root.destroy,
            font=("Arial", 12),
            bg='#434343',
            fg='white',
            width=15
        ).pack(side='right', padx=5)

    def check_acceptance(self):
        if self.installation_complete:
            # Always enable if installation is complete
            self.install_btn.configure(state='normal')
        elif self.accepted_terms.get() and self.accepted_privacy.get():
            # Enable only if both checkboxes are checked during pre-install
            self.install_btn.configure(state='normal')
        else:
            # Disable only if not installed and checkboxes unchecked
            self.install_btn.configure(state='disabled')

    def start_installation(self):
        self.install_btn.configure(state='disabled')
        thread = threading.Thread(target=self.installation_sequence)
        thread.start()

    def installation_sequence(self):
        tasks = [
            ("Core Components", [
                ("Python Environment", 3),
                ("Database Setup", 4),
                ("UI Components", 3)
            ]),
            ("Email Services", [
                ("SMTP Configuration", 3),
                ("Security Protocols", 4),
                ("Email Templates", 3)
            ]),
            ("DevOps Tools", [
                ("Kubernetes Tools", 3),
                ("Docker Support", 4),
                ("CI/CD Setup", 3)
            ])
        ]

        total_steps = sum(len(subtasks) for _, subtasks in tasks)
        step = 0

        for main_task, subtasks in tasks:
            self.status_label.config(text=f"Installing {main_task}")
            
            for subtask, duration in subtasks:
                step += 1
                self.detail_label.config(text=subtask)
                self.main_progress['value'] = (step / total_steps) * 100

                # Subtask progress animation
                self.task_progress['value'] = 0
                for i in range(10):
                    self.task_progress['value'] += 10
                    time.sleep(duration/10)
                    self.root.update()

        self.complete_installation()

    def complete_installation(self):
        self.installation_complete = True  # Set completion flag
        self.status_label.config(text="Installation Complete!")
        self.detail_label.config(text="Click Launch to start OpenMail")
        self.main_progress['value'] = 100
        self.task_progress['value'] = 100
        
        self.install_btn.configure(
            text="Launch",
            command=self.launch_welcome_screen,
            state='normal'  # Always enable after completion
        )

    def launch_welcome_screen(self):
        try:
            self.root.destroy()
            from backend.welcome_screen import WelcomeScreen
            welcome = WelcomeScreen()
            welcome.run()
        except Exception as e:
            messagebox.showerror("Error", f"Failed to launch: {str(e)}")
            sys.exit(1)

def main():
    installer = InstallerUI()
    installer.root.mainloop()

if __name__ == "__main__":
    main()