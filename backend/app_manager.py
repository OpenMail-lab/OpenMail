import tkinter as tk
from .local_email import LocalEmailFrame
from .domain_email import DomainEmailFrame
from .mail_service import MailServiceFrame
from .welcome_screen import WelcomeFrame

class AppManager:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("OpenMail")
        self.root.geometry("800x600")
        self.root.configure(bg="#001133")
        
        self.frames = {}
        self.current_frame = None
        self.setup_frames()
    
    def setup_frames(self):
        container = tk.Frame(self.root, bg="#001133")
        container.pack(fill="both", expand=True)
        
        # Initialize all frames
        self.frames["welcome"] = WelcomeFrame(container, self.switch_frame)
        self.frames["local_email"] = LocalEmailFrame(container, self.switch_frame)
        self.frames["domain_email"] = DomainEmailFrame(container, self.switch_frame)
        self.frames["mail_service"] = MailServiceFrame(container, self.switch_frame)
        
        self.switch_frame("welcome")
    
    def switch_frame(self, frame_name, user_data=None):
        if self.current_frame:
            self.current_frame.pack_forget()
        
        self.current_frame = self.frames[frame_name]
        if user_data:
            self.current_frame.set_user_data(user_data)
        self.current_frame.pack(fill="both", expand=True)
    
    def run(self):
        self.root.mainloop()
