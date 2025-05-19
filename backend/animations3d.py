import tkinter as tk
try:
    from PIL import Image, ImageTk
except ImportError:
    # Fallback if PIL is not installed
    print("⚠️ PIL not found, installing...")
    import subprocess
    subprocess.run([sys.executable, "-m", "pip", "install", "Pillow"], check=True)
    from PIL import Image, ImageTk

import numpy as np

class JarvisAnimations:
    def __init__(self, master):
        self.master = master
        self.canvas = tk.Canvas(master, bg='black', highlightthickness=0)
        self.canvas.pack(fill='both', expand=True)
        
        # Hologram particles
        self.particles = []
        self.create_particles()

    def create_particles(self):
        for _ in range(100):
            x = np.random.randint(0, self.master.winfo_width())
            y = np.random.randint(0, self.master.winfo_height())
            self.particles.append(
                self.canvas.create_oval(x, y, x+2, y+2, fill='#00ffff')
            )

    def zoom_open(self, event_x, event_y, callback=None):
        """Create Iron Man style zooming animation from click point"""
        # Start small rectangle at click point
        rect = self.canvas.create_rectangle(
            event_x, event_y, event_x+1, event_y+1,
            outline='#00ffff', width=2
        )
        
        def animate():
            # Get current coordinates
            x1, y1, x2, y2 = self.canvas.coords(rect)
            
            # Expand rectangle
            self.canvas.coords(rect,
                x1 - 10, y1 - 10,
                x2 + 10, y2 + 10
            )
            
            # Add hologram effects
            self.canvas.create_line(x1, y1, x2, y2, fill='#00ffff', width=1)
            
            # Continue animation if not full size
            if x2 - x1 < self.master.winfo_width():
                self.master.after(10, animate)
            else:
                if callback: callback()

        animate()

    def zoom_close(self, callback=None):
        """Reverse zoom animation"""
        w = self.master.winfo_width()
        h = self.master.winfo_height()
        
        rect = self.canvas.create_rectangle(0, 0, w, h, outline='#00ffff', width=2)
        
        def animate():
            x1, y1, x2, y2 = self.canvas.coords(rect)
            center_x = (x1 + x2) / 2
            center_y = (y1 + y2) / 2
            
            # Shrink rectangle
            self.canvas.coords(rect,
                x1 + 10, y1 + 10,
                x2 - 10, y2 - 10
            )
            
            if x2 - x1 > 10:
                self.master.after(10, animate)
            else:
                self.canvas.delete(rect)
                if callback: callback()
        
        animate()

    def hologram_scan(self):
        """Create Jarvis-style scanning effect"""
        h = self.master.winfo_height()
        scan_line = self.canvas.create_line(
            0, 0, self.master.winfo_width(), 0,
            fill='#00ffff', width=2
        )
        
        def animate():
            _, y, _, _ = self.canvas.coords(scan_line)
            if y < h:
                self.canvas.move(scan_line, 0, 5)
                self.master.after(20, animate)
            else:
                self.canvas.delete(scan_line)
        
        animate()
