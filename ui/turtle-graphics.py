import turtle

def draw_status_circle(x, y, color, label):
    turtle.penup()
    turtle.goto(x, y)
    turtle.pendown()
    turtle.fillcolor(color)
    turtle.begin_fill()
    turtle.circle(40)
    turtle.end_fill()

    # Add label
    turtle.penup()
    turtle.goto(x, y - 60)
    turtle.pendown()
    turtle.write(label, align="center", font=("Arial", 14, "bold"))

# Setup screen
turtle.speed(0)
turtle.bgcolor("white")

# Example status indicators
draw_status_circle(-200, 100, "green", "✅ Kiali Running")
draw_status_circle(0, 100, "red", "❌ Terraform Stopped")
draw_status_circle(200, 100, "green", "✅ ArgoCD Running")
draw_status_circle(-200, -100, "green", "✅ Helm Active")
draw_status_circle(0, -100, "red", "❌ Ansible Not Configured")
draw_status_circle(200, -100, "green", "✅ Docker Healthy")

# Keep window open
turtle.done()
