import turtle
import json

def draw_vs_code_theme():
    screen = turtle.Screen()
    screen.setup(800, 600)
    screen.bgcolor("#1e1e1e")
    
    t = turtle.Turtle()
    t.speed(0)
    t.hideturtle()
    
    # Draw sidebar
    draw_rectangle(t, -400, 300, 50, 600, "#333333")
    
    # Draw activity bar icons
    icons = ["📁", "🔍", "⚙️", "📦"]
    for i, icon in enumerate(icons):
        draw_icon(t, -375, 250 - (i * 50), icon)
    
    # Save as SVG for web use
    screen.getcanvas().postscript(file='ui_elements.svg')
    
def draw_rectangle(t, x, y, width, height, color):
    t.penup()
    t.goto(x, y)
    t.pendown()
    t.fillcolor(color)
    t.begin_fill()
    for _ in range(2):
        t.forward(width)
        t.right(90)
        t.forward(height)
        t.right(90)
    t.end_fill()

def draw_icon(t, x, y, icon):
    t.penup()
    t.goto(x, y)
    t.write(icon, font=("Arial", 14, "normal"))

if __name__ == "__main__":
    draw_vs_code_theme()
