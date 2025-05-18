from flask import Flask, jsonify
import turtle
import subprocess

app = Flask(__name__)

def draw_circle(x, y, color, label):
    turtle.penup()
    turtle.goto(x, y)
    turtle.pendown()
    turtle.fillcolor(color)
    turtle.begin_fill()
    turtle.circle(40)
    turtle.end_fill()
    turtle.penup()
    turtle.goto(x, y - 60)
    turtle.pendown()
    turtle.write(label, align="center", font=("Arial", 14, "bold"))

@app.route('/api/recovery-visual')
def visualize_recovery():
    turtle.speed(0)
    turtle.bgcolor("white")

    # Check service statuses
    services = ["kiali", "terraform", "argocd", "helm", "ansible", "docker"]
    positions = [(-200, 100), (0, 100), (200, 100), (-200, -100), (0, -100), (200, -100)]
    
    for service, pos in zip(services, positions):
        status_cmd = ["kubectl", "get", "pods", "-l", f"app={service}", "--field-selector=status.phase=Running"]
        status_result = subprocess.run(status_cmd, capture_output=True, text=True).stdout.strip()
        color = "green" if status_result else "red"

        draw_circle(pos[0], pos[1], color, service.capitalize())

    turtle.done()
    return jsonify({"status": "✅ Recovery Visualization Complete!"})

if __name__ == '__main__':
    app.run(port=5005, debug=True)
