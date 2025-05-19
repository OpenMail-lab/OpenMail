import requests
import json
import os
from flask import Blueprint, request, redirect, session, make_response
from backend.setup_nat import get_public_ipv4

local_service = Blueprint("local_service", __name__)

class LocalEmailService:
    def __init__(self):
        self.accounts_file = os.path.join(os.path.dirname(__file__), 'accounts.json')
        self.load_accounts()
        
    def load_accounts(self):
        """Load existing accounts"""
        try:
            with open(self.accounts_file, 'r') as f:
                self.accounts = json.load(f)
        except FileNotFoundError:
            self.accounts = {}
            
    def save_accounts(self):
        """Save accounts to file"""
        with open(self.accounts_file, 'w') as f:
            json.dump(self.accounts, f, indent=4)
            
    def create_account(self, first_name, last_name, username, password):
        """Create new email account"""
        if username in self.accounts:
            return None
            
        public_ip = get_public_ipv4()
        email = f"{username}@{public_ip}"
        
        account = {
            'email': email,
            'first_name': first_name,
            'last_name': last_name,
            'password': password,  # In production, hash this!
            'created_at': str(datetime.now())
        }
        
        self.accounts[username] = account
        self.save_accounts()
        
        return account

USER_DATABASE = {}

def get_public_ipv4():
    """Force IPv4 address for email domains"""
    try:
        # Use multiple IPv4-only services for redundancy
        services = [
            "https://api4.ipify.org",
            "https://ipv4.icanhazip.com",
            "https://v4.ident.me"
        ]
        for service in services:
            try:
                return requests.get(service, timeout=5).text.strip()
            except:
                continue
        return "127.0.0.1"
    except:
        return "127.0.0.1"

PUBLIC_IP = get_public_ipv4()  # ✅ Force IPv4 for email domain

@local_service.route("/local")  # Make sure this matches the URL being accessed
def register_or_access_local():
    # Check if user is already registered
    if session.get('user_email'):
        return redirect(f"/local/service?email={session['user_email']}")

    if request.method == "POST":
        first_name = request.form.get("first_name")
        last_name = request.form.get("last_name")
        custom_email = request.form.get("custom_email")

        full_name = f"{first_name} {last_name}".strip()
        public_ip = get_public_ipv4()  # ✅ Get fresh public IP
        ip_email = f"{custom_email}@{public_ip}"

        if custom_email in USER_DATABASE:
            return "<h2>Email already taken. Try another.</h2><br><a href='/local'>Back</a>"

        USER_DATABASE[custom_email] = {"name": full_name, "email": ip_email}
        
        # Store in session
        session['user_email'] = ip_email
        response = make_response(redirect(f"/local/service?email={ip_email}"))
        response.set_cookie('user_email', ip_email)
        return response

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
        <li><a href='/mail/send'>Send Email</a></li>
        <li><a href='/mail/mailbox?user={email}'>Check Inbox</a></li>
    </ul>
    <br><a href='/'>Back</a>
    """
