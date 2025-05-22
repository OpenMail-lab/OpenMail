import tkinter as tk
import random

class ParticleSystem:
    def __init__(self, root):
        self.root = root
        self.particles = []
        self.canvas = tk.Canvas(
            root,
            width=800,
            height=600,
            bg='#001133',
            highlightthickness=0
        )
        self.canvas.place(x=0, y=0)
        
    def start(self):
        for _ in range(20):
            self.particles.append({
                'x': random.randint(0, 800),
                'y': random.randint(0, 600),
                'vx': random.uniform(-2, 2),
                'vy': random.uniform(-2, 2),
                'size': random.randint(2, 4)
            })
        self.animate()
            
    def animate(self):
        self.canvas.delete('particle')
        for p in self.particles:
            p['x'] += p['vx']
            p['y'] += p['vy']
            
            # Wrap around screen
            if p['x'] < 0: p['x'] = 800
            if p['x'] > 800: p['x'] = 0
            if p['y'] < 0: p['y'] = 600
            if p['y'] > 600: p['y'] = 0
            
            # Draw particle
            self.canvas.create_oval(
                p['x'] - p['size'],
                p['y'] - p['size'],
                p['x'] + p['size'],
                p['y'] + p['size'],
                fill='#00f3ff',
                outline='#00f3ff',
                tags='particle'
            )
        
        self.root.after(50, self.animate)
