from flask import Flask, render_template_string
import requests

app = Flask(__name__)

# Get public IP for email domain
def get_public_ip():
    try:
        return requests.get("https://api4.ipify.org").text.strip()
    except:
        return "127.0.0.1"

@app.route("/")
def home():
    public_ip = get_public_ip()
    return render_template_string("""
    <!DOCTYPE html>
    <html>
    <head>
        <title>OpenMail</title>
        <style>
            body { text-align: center; padding: 50px; }
            button { padding: 10px 20px; margin: 10px; }
        </style>
    </head>
    <body>
        <h1>Welcome to OpenMail</h1>
        <h2>Choose Email Type:</h2>
        <button onclick="window.location.href='/domain'">With Domain</button>
        <button onclick="window.location.href='/local'">Without Domain ({{ip}})</button>
    </body>
    </html>
    """, ip=public_ip)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5001, debug=True)
