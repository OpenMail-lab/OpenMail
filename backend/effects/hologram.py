import tkinter as tk
import math

class HologramEffect:
    def __init__(self, root):
        self.root = root
        self.canvas = tk.Canvas(
            root,
            bg='#001133',
            highlightthickness=0,
            width=800,
            height=600
        )
        self.canvas.place(x=0, y=0)  # Use place instead of pack

        self.COLORS = {
            'grid': '#00f3ff',  # Bright cyan for grid lines
            'grid_dim': '#003744'  # Dimmer version for subtle lines
        }
    
    def create_grid(self):
        self.canvas.delete('grid')  # Clear existing grid

        # Create grid effect
        spacing = 40

        for i in range(0, 800, spacing):
            # Vertical lines
            self.canvas.create_line(
                i, 0, i, 600,
                fill=self.COLORS['grid_dim'],
                tags='grid'
            )
            # Horizontal lines
            self.canvas.create_line(
                0, i, 800, i,
                fill=self.COLORS['grid_dim'],
                tags='grid'
            )

        self.animate_grid()

    def animate_grid(self):
        angle = 0
        def update():
            self.canvas.delete('grid')
            spacing = 40
            
            # Create moving grid pattern
            for i in range(0, 800, spacing):
                offset = math.sin(angle + i/100) * 5
                
                self.canvas.create_line(
                    i + offset, 0, i + offset, 600,
                    fill=self.COLORS['grid_dim'],
                    tags='grid'
                )
                self.canvas.create_line(
                    0, i + offset, 800, i + offset,
                    fill=self.COLORS['grid_dim'],
                    tags='grid'
                )
                
            angle += 0.05
            self.root.after(50, update)
            
        update()
