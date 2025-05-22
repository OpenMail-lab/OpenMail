import tkinter as tk

class NeonTextEffect:
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

    def create_text(self, x, y, text, size=30, color='#00f3ff'):
        # Clear previous text
        self.canvas.delete('neon_text')

        # Create multiple layers for glow effect
        layers = [
            {'offset': 3, 'color': f'{color}22'},  # Outer glow
            {'offset': 2, 'color': f'{color}44'},
            {'offset': 1, 'color': f'{color}88'},
            {'offset': 0, 'color': color}          # Main text
        ]

        text_items = []
        for layer in layers:
            text_items.append(
                self.canvas.create_text(
                    x + layer['offset'],
                    y + layer['offset'],
                    text=text,
                    font=('Arial', size, 'bold'),
                    fill=layer['color'],
                    tags='neon_text'
                )
            )

        return text_items
