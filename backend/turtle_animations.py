import tkinter as tk
import turtle

class TurtleUI:
    @staticmethod
    def draw_logo(window):
        # Create canvas for turtle
        canvas = tk.Canvas(window, width=200, height=200)
        canvas.pack(pady=20)
        
        # Initialize turtle screen
        screen = turtle.TurtleScreen(canvas)
        screen.bgcolor("white")
        t = turtle.RawTurtle(screen)
        t.hideturtle()
        
        # Draw OpenMail logo
        t.penup()
        t.goto(-50, 0)
        t.pendown()
        t.color("#2962ff")
        t.pensize(3)
        
        # Draw envelope shape
        t.forward(100)
        t.right(90)
        t.forward(60)
        t.right(90)
        t.forward(100)
        t.right(90)
        t.forward(60)
        
        # Draw @ symbol
        t.penup()
        t.goto(0, -20)
        t.pendown()
        t.circle(20)
        
        screen.update()
