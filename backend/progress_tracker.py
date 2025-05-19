import tkinter as tk
from tkinter import ttk
import threading
import time
import webbrowser

class InstallationProgress:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("OpenMail Installation Progress")
        self.root.geometry("400x300")
        
        # Progress bar
        self.progress = ttk.Progressbar(self.root, length=300, mode='determinate')
        self.progress.pack(pady=20)
        
        # Status label
        self.status_label = tk.Label(self.root, text="Starting installation...")
        self.status_label.pack(pady=10)
        
        # Details text
        self.details_text = tk.Text(self.root, height=10, width=40)
        self.details_text.pack(pady=10)
        
        self.current_progress = 0
        self.installation_steps = [
            "Configuring NAT settings...",
            "Setting up Flask server...",
            "Installing dependencies...",
            "Starting mail services...",
            "Configuring firewall...",
            "Setting up database...",
            "Finalizing installation..."
        ]
        self.installation_complete = False

    def update_progress(self, step_name, progress):
        self.progress['value'] = progress
        self.status_label['text'] = step_name
        self.details_text.insert(tk.END, f"✅ {step_name}\n")
        self.details_text.see(tk.END)
        self.root.update()

    def complete_installation(self):
        self.installation_complete = True
        self.root.after(1000, self.launch_application)  # Wait 1 second before launching

    def launch_application(self):
        self.root.destroy()  # Close progress window
        webbrowser.open('http://localhost:5001')  # Open main application

    def start(self):
        # Create a separate thread for installation
        install_thread = threading.Thread(target=self.simulate_installation)
        install_thread.start()
        self.root.mainloop()

    def simulate_installation(self):
        total_steps = len(self.installation_steps)
        for i, step in enumerate(self.installation_steps):
            progress = (i + 1) * (100 // total_steps)
            self.update_progress(step, progress)
            time.sleep(1)  # Simulate installation time
        
        self.status_label['text'] = "Installation Complete!"
        self.complete_installation()  # Call the complete installation method

if __name__ == "__main__":
    progress = InstallationProgress()
    progress.start()
