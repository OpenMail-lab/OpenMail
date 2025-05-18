from flask import Flask, jsonify
import subprocess

app = Flask(__name__)

@app.route('/api/alerts')
def check_status():
    crashed_pods = subprocess.run(["kubectl", "get", "pods", "--field-selector=status.phase!=Running"], capture_output=True, text=True)
    alert_message = "✅ All services are running!" if not crashed_pods.stdout.strip() else f"⚠️ Issues detected:\n{crashed_pods.stdout}"

    return jsonify({"alert": alert_message})

if __name__ == '__main__':
    app.run(port=5003, debug=True)
