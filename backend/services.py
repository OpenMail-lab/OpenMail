from flask import Flask, render_template, request, make_response, session
import requests
import os
from domain_service import domain_service
from local_service import local_service
from home_service import OpenMailApp
from threading import Thread
from progress_tracker import InstallationProgress

app = Flask(__name__, template_folder='../templates')  # Point to templates directory
app.secret_key = 'openmail_secret'  # Required for session management

# Register blueprints
app.register_blueprint(domain_service)
app.register_blueprint(local_service)

# Get system's public IP for email addresses
try:
    PUBLIC_IP = requests.get("https://api64.ipify.org").text.strip()
except:
    PUBLIC_IP = "127.0.0.1"  # Fallback to localhost if API fails

@app.route("/", methods=['GET'])
def home():
    """Main page with domain/local email options"""
    # First, ensure templates directory exists
    os.makedirs('../templates', exist_ok=True)
    
    # Return direct HTML for now (we'll move to templates later)
    return f"""
    <!DOCTYPE html>
    <html>
    <head>
        <title>OpenMail Service</title>
        <style>
            body {{ font-family: Arial, sans-serif; margin: 40px; }}
            button {{ padding: 10px 20px; margin: 10px; cursor: pointer; }}
        </style>
    </head>
    <body>
        <h1>OpenMail Service</h1>
        <h2>Choose Your Email Type:</h2>
        <button onclick="window.location.href='/domain'">With Domain</button>
        <button onclick="window.location.href='/local'">Without Domain ({PUBLIC_IP})</button>
    </body>
    </html>
    """

def start_services():
    # Create and start the main GUI
    app = OpenMailApp()
    
    # Show progress during startup
    progress = InstallationProgress()
    progress_thread = Thread(target=progress.start)
    progress_thread.daemon = True
    progress_thread.start()
    
    # Start the main GUI loop
    app.run()

if __name__ == "__main__":
    # Ensure we're listening on all interfaces
    app.run(host="0.0.0.0", port=5001, debug=True)
    start_services()
