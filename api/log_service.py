from flask import Flask, Response

app = Flask(__name__)

LOG_FILE = "openmail_install.log"

@app.route('/api/install-log')
def get_install_log():
    try:
        with open(LOG_FILE, "r") as log:
            return Response(log.read(), mimetype="text/plain")
    except FileNotFoundError:
        return Response("No log file found.", mimetype="text/plain")

if __name__ == "__main__":
    app.run(port=5009, debug=True)
