import turtle
import time

def draw_progress_bar(progress):
    turtle.clear()
    turtle.penup()
    turtle.goto(-150, 0)
    turtle.pendown()

    # Draw background bar
    turtle.fillcolor("grey")
    turtle.begin_fill()
    turtle.forward(300)
    turtle.right(90)
    turtle.forward(30)
    turtle.right(90)
    turtle.forward(300)
    turtle.right(90)
    turtle.forward(30)
    turtle.right(90)
    turtle.end_fill()

    # Draw progress
    turtle.fillcolor("green")
    turtle.begin_fill()
    turtle.forward(300 * progress / 100)
    turtle.right(90)
    turtle.forward(30)
    turtle.right(90)
    turtle.forward(300 * progress / 100)
    turtle.right(90)
    turtle.forward(30)
    turtle.right(90)
    turtle.end_fill()

    # Display percentage
    turtle.penup()
    turtle.goto(-20, -50)
    turtle.pendown()
    turtle.write(f"{progress}% Complete", align="center", font=("Arial", 14, "bold"))

def install_tools():
    turtle.speed(0)
    turtle.bgcolor("white")
    turtle.title("Installing OpenMail...")

    steps = ["Installing Python dependencies", "Setting up Kubernetes", "Deploying Microservices", "Starting services", "Finalizing installation"]
    
    for i, step in enumerate(steps):
        time.sleep(2)  # Simulate installation time
        draw_progress_bar((i + 1) * 20)
        print(f"✅ {step}... Done")

    turtle.done()

if __name__ == "__main__":
    install_tools()
