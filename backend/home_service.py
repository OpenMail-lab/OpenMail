import requests
import os
from flask import Flask, request, redirect, render_template
from smtp_service import smtp_service
from imap_service import imap_service
from setup_firewall import allow_flask_firewall  # ✅ Import auto firewall setup

app = Flask(__name__)

USER_DATABASE = {}

# ✅ Force IPv4 instead of IPv6
def get_public_ipv4():
    try:
        return requests.get("https://ipv4.icanhazip.com").text.strip()  # ✅ Get Public IPv4
    except:
        return "127.0.0.1"  # Fallback

# ✅ Automatically bind Flask to the user's public IP
if __name__ == "__main__":
    public_ip = get_public_ipv4()  # ✅ Dynamically fetch public IP
    app.run(host="0.0.0.0", port=5001, debug=True) 

@app.route("/")
def home():
    email = request.cookies.get("user_email")  
    if email:
        return redirect("/mail_dashboard")  
    return render_template("home.html")  

@app.route("/register", methods=["POST"])
def register():
    first_name = request.form.get("first_name")
    last_name = request.form.get("last_name")
    desired_email = request.form.get("desired_email")

    ipv4_address = get_public_ipv4()  # ✅ Fetch IPv4 before creating email
    final_email = f"{desired_email}@{ipv4_address}"  

    if final_email in USER_DATABASE:
        return "<h2>Email already exists. Try another.</h2><br><a href='/'>Back</a>"

    USER_DATABASE[final_email] = {"name": f"{first_name} {last_name}", "email": final_email}
    response = redirect("/mail_dashboard")
    response.set_cookie("user_email", final_email)  # Store session
    return response

@app.route("/mail_dashboard")
def mail_dashboard():
    email = request.cookies.get("user_email")  
    if not email:
        return redirect("/")  

    return f"""
    <h2>Welcome to OpenMail Dashboard</h2>
    <p>Your email: {email}</p>
    <ul>
        <li><a href='/smtp/send'>Send Email (SMTP)</a></li>
        <li><a href='/imap/inbox'>Check Inbox (IMAP)</a></li>
        <li><a href='/logout'>Logout</a></li>
    </ul>
    """

@app.route("/logout")
def logout():
    response = redirect("/")
    response.set_cookie("user_email", "", expires=0)  # ✅ Clears session
    return response

# ✅ Register blueprints automatically
app.register_blueprint(smtp_service, url_prefix="/smtp")
app.register_blueprint(imap_service, url_prefix="/imap")

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5001, debug=True)  # ✅ Flask runs on port 5001
