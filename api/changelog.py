from flask import Flask, jsonify
import requests

app = Flask(__name__)
GITHUB_REPO = "https://api.github.com/repos/openmail-lab/OpenMail/releases/latest"

@app.route('/api/changelog')
def fetch_changelog():
    response = requests.get(GITHUB_REPO)
    changelog = response.json().get("body", "No changelog available.")
    
    return jsonify({"changelog": changelog})

if __name__ == "__main__":
    app.run(port=5007, debug=True)
