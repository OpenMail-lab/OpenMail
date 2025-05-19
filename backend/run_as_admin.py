import ctypes
import sys
import subprocess
from flask import Flask

def is_admin():
    try:
        return ctypes.windll.shell32.IsUserAnAdmin()
    except:
        return False

if __name__ == '__main__':
    if not is_admin():
        # Re-run with admin rights
        ctypes.windll.shell32.ShellExecuteW(None, "runas", sys.executable, " ".join(sys.argv), None, 1)
    else:
        # Create Flask app instance first
        app = Flask(__name__)
        
        # Add root route
        @app.route('/')
        def home():
            return """
            <h1>OpenMail Service</h1>
            <h2>Choose Your Email Type:</h2>
            <button onclick="window.location.href='/domain'">With Domain</button>
            <button onclick="window.location.href='/local'">Without Domain</button>
            """
        
        # Run with admin privileges
        app.run(host='0.0.0.0', port=5001, debug=True)
