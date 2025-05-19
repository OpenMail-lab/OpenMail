import tkinter as tk
import pygame
import math
from PIL import Image, ImageTk, ImageDraw

class JarvisUI:
    def __init__(self, parent):
        self.parent = parent
        self.canvas = tk.Canvas(parent, bg='black', highlightthickness=0)
        self.canvas.pack(fill='both', expand=True)
        
        # Initialize sound effects
        pygame.mixer.init()
        self.sounds = {
            'hover': pygame.mixer.Sound('sounds/hover.wav'),
            'click': pygame.mixer.Sound('sounds/click.wav'),
            'open': pygame.mixer.Sound('sounds/open.wav'),
            'close': pygame.mixer.Sound('sounds/close.wav')
        }

    def animate_open(self, x, y, callback=None):
        """Create expanding animation from click point"""
        self.play_sound('open')
        lines = []
        
        # Create holographic lines
        for i in range(4):
            angle = i * math.pi/2
            end_x = x + math.cos(angle) * 20
            end_y = y + math.sin(angle) * 20
            line = self.canvas.create_line(x, y, end_x, end_y, fill='#00ffff', width=2)
            lines.append(line)

        def expand():
            """Expand lines until they reach screen edges"""
            done = True
            for line in lines:
                coords = self.canvas.coords(line)
                if coords[2] < self.parent.winfo_width() or coords[3] < self.parent.winfo_height():
                    # Expand line
                    self.canvas.coords(line,
                        coords[0], coords[1],
                        coords[2] + 10, coords[3] + 10)
                    done = False
                    
                # Add hologram particles
                if not done:
                    particle_x = coords[2] + np.random.randint(-10, 10)
                    particle_y = coords[3] + np.random.randint(-10, 10)
                    particle = self.canvas.create_oval(
                        particle_x, particle_y,
                        particle_x + 2, particle_y + 2,
                        fill='#00ffff', outline='#00ffff'
                    )
                    self.canvas.after(100, lambda p=particle: self.canvas.delete(p))

            if not done:
                self.parent.after(10, expand)
            else:
                if callback: callback()

        expand()

    def animate_close(self, callback=None):
        """Create collapsing animation"""
        self.play_sound('close')
        # Similar to animate_open but in reverse
        # ...existing animation code...

    def play_sound(self, sound_name):
        """Play UI sound effect"""
        self.sounds[sound_name].play()
