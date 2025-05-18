from flask import Flask, jsonify
import subprocess

app = Flask(__name__)

@app.route('/api/logs')
def get_logs():
    logs = subprocess.run(["kubectl", "logs", "-l", "app=openmail"], capture_output=True, text=True)
    return jsonify(logs.stdout.split("\n"))

if __name__ == '__main__':
    app.run(port=5002, debug=True)
