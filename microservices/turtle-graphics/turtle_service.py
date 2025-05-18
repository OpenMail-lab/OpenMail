from flask import Flask, jsonify
import turtle

app = Flask(__name__)

STATUS = {
    "kiali": "running",
    "terraform": "stopped",
    "argocd": "running",
    "helm": "running",
    "ansible": "stopped",
    "docker": "running"
}

@app.route('/api/status')
def get_status():
    return jsonify(STATUS)

def draw_status():
    turtle.speed(0)
    turtle.bgcolor("white")
    positions = [(-200, 100), (0, 100), (200, 100), (-200, -100), (0, -100), (200, -100)]
    colors = ["green" if STATUS[key] == "running" else "red" for key in STATUS]

    for pos, color, tool in zip(positions, colors, STATUS.keys()):
        turtle.penup()
        turtle.goto(pos)
        turtle.pendown()
        turtle.fillcolor(color)
        turtle.begin_fill()
        turtle.circle(40)
        turtle.end_fill()
        turtle.penup()
        turtle.goto(pos[0], pos[1] - 60)
        turtle.pendown()
        turtle.write(tool.capitalize(), align="center", font=("Arial", 14, "bold"))

    turtle.done()

if __name__ == '__main__':
    draw_status()
