import requests
from flask import Blueprint, request, redirect
from mail_service import mail_service

local_service = Blueprint("local_service", __name__)
USER_DATABASE = {}  # Temporary storage (replace with a secure database)

try:
    PUBLIC_IP = requests.get("https://api64.ipify.org").text
except:
    PUBLIC_IP = "127.0.0.1"

@local_service.route("/local", methods=["GET", "POST"])
def register_or_access_local():
    if request.method == "POST":
        first_name = request.form.get("first_name")
        last_name = request.form.get("last_name")
        custom_email = request.form.get("custom_email")

        full_name = f"{first_name} {last_name}".strip()
        ip_email = f"{custom_email}@{PUBLIC_IP}"

        if custom_email in USER_DATABASE:
            return "<h2>Email already taken. Try another.</h2><br><a href='/local'>Back</a>"

        USER_DATABASE[custom_email] = {"name": full_name, "email": ip_email}
        return redirect(f"/local/service?email={ip_email}")

    return f"""
    <h2>Register for OpenMail Without Domain</h2>
    <form action="/local" method="post">
        First Name: <input type="text" name="first_name" required><br>
        Last Name: <input type="text" name="last_name" required><br>
        Email Address: <input type="text" name="custom_email" required> @ {PUBLIC_IP}<br>
        <input type="submit" value="Register">
    </form>
    <br><a href='/'>Back</a>
    """

@local_service.route("/local/service")
def get_local_service():
    email = request.args.get("email", "Unknown Email")
    return f"""
    <h2>Welcome! Your IP-based email is {email}</h2>
    <h3>Email Features:</h3>
    <ul>
        <li><a href='/send'>Send Email</a></li>
        <li><a href='/mailbox?user={email}'>Check Inbox</a></li>
    </ul>
    <br><a href='/'>Back</a>
    """
