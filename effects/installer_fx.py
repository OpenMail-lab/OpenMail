import turtle
import tkinter as tk
import math
import random

class InstallerEffects:
    def __init__(self, parent):
        self.canvas = tk.Canvas(
            parent, 
            bg='#001133', 
            width=800, 
            height=200, 
            highlightthickness=0
        )
        self.canvas.pack(pady=20)
        self.screen = turtle.TurtleScreen(self.canvas)
        self.screen.bgcolor('#001133')
        self.t = turtle.RawTurtle(self.screen)
        self.t.hideturtle()
        self.t.speed(0)
        self.active = True

    def draw_infinity_logo(self):
        colors = ['blue', 'cyan', 'purple']  # Using standard color names
        size = 30
        angle = 0
        
        while self.active:
            self.t.clear()
            self.t.penup()
            self.t.pensize(2)
            
            for color in colors:
                self.t.pencolor(color)
                self.t.goto(-size, 0)
                self.t.pendown()
                
                # Draw infinity
                for i in range(360):
                    rad = math.radians(i + angle)
                    x = size * math.sin(rad)
                    y = size * math.sin(rad * 2)
                    self.t.goto(x, y)
                
                self.t.penup()
            
            angle += 5
            self.screen.update()

    def particle_field(self):
        particles = []
        for _ in range(20):
            x = random.randint(-350, 350)
            y = random.randint(-80, 80)
            dx = random.uniform(-2, 2)
            dy = random.uniform(-2, 2)
            particles.append([x, y, dx, dy])
        
        while self.active:
            self.t.clear()
            
            for p in particles:
                # Move particle
                p[0] += p[2]
                p[1] += p[3]
                
                # Wrap around screen
                if p[0] < -350: p[0] = 350
                if p[0] > 350: p[0] = -350
                if p[1] < -80: p[1] = 80
                if p[1] > 80: p[1] = -80
                
                # Draw particle
                self.t.penup()
                self.t.goto(p[0], p[1])
                self.t.dot(4, 'cyan')  # Using standard color name
            
            self.screen.update()
