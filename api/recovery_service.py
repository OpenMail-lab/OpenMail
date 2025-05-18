from flask import Flask, jsonify
import subprocess

app = Flask(__name__)

@app.route('/api/recover')
def recover_services():
    crashed_pods = subprocess.run(["kubectl", "get", "pods", "--field-selector=status.phase!=Running"], capture_output=True, text=True)

    if crashed_pods.stdout.strip():
        subprocess.run(["kubectl", "rollout", "restart", "deployment", "-l", "app=openmail"])
        subprocess.run(["curl", "-X", "POST", "-H", "Content-Type: application/json", "-d", '{"type":"success"}', "http://localhost:5006/api/play-sound"])  # 🔊 Play success sound!
        return jsonify({"status": "✅ Recovery triggered! Success sound played."})

    subprocess.run(["curl", "-X", "POST", "-H", "Content-Type: application/json", "-d", '{"type":"error"}', "http://localhost:5006/api/play-sound"])  # 🔊 Play error sound!
    return jsonify({"status": "⚠️ No recovery needed. Error sound played!"})

if __name__ == '__main__':
    app.run(port=5004, debug=True)
