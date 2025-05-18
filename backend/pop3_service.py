import poplib
from flask import Blueprint, request

pop3_service = Blueprint("pop3_service", __name__)

POP3_SERVER = "pop.example.com"  # Replace with your POP3 server
POP3_PORT = 995  # Secure port
POP3_USERNAME = "your-email@example.com"
POP3_PASSWORD = "your-password"

@pop3_service.route("/receive", methods=["GET"])
def receive_email():
    try:
        server = poplib.POP3_SSL(POP3_SERVER, POP3_PORT)
        server.user(POP3_USERNAME)
        server.pass_(POP3_PASSWORD)

        email_count, _ = server.stat()  # Get email count
        messages = [server.retr(i) for i in range(1, email_count + 1)]  # Fetch emails
        email_list = "<h2>Your Emails</h2><ul>"

        for msg in messages:
            email_data = "\n".join(msg[1].decode("utf-8") for msg in msg[1:])
            email_list += f"<li>{email_data}</li><br>"

        server.quit()
        return email_list + "<br><a href='/mail_dashboard'>Back</a>"
    except Exception as e:
        return f"<h2>Failed to retrieve emails: {e}</h2><br><a href='/mail_dashboard'>Back</a>"
