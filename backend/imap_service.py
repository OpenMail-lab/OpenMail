import requests
import imaplib
from flask import Blueprint, request

imap_service = Blueprint("imap_service", __name__, url_prefix="/imap")

# ✅ Force IPv4 instead of IPv6
def get_public_ipv4():
    try:
        return requests.get("https://api4.ipify.org").text
    except:
        return "127.0.0.1"

IMAP_SERVER = get_public_ipv4()  # ✅ Uses IPv4 only
IMAP_PORT = 5001  

@imap_service.route("/inbox", methods=["GET"])
def inbox_email():
    email = request.cookies.get("user_email")  
    if not email:
        return redirect("/")  

    try:
        server = imaplib.IMAP4_SSL(IMAP_SERVER, IMAP_PORT)
        server.login(email, "stored-session-password")
        server.select("INBOX")

        status, messages = server.search(None, "ALL")
        email_ids = messages[0].split()
        email_list = "<h2>Your Inbox</h2><ul>"

        for email_id in email_ids[:10]:  
            status, msg_data = server.fetch(email_id, "(RFC822)")
            email_list += f"<li>{msg_data[0][1].decode('utf-8')}</li><br>"

        server.logout()
        return email_list + "<br><a href='/mail_dashboard'>Back</a>"
    except Exception as e:
        return f"<h2>Failed to retrieve emails: {e}</h2><br><a href='/mail_dashboard'>Back</a>"
