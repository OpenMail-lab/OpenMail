import smtplib, json, time
from flask import Blueprint, request

mail_service = Blueprint("mail_service", __name__)

USER_INBOX = {}  # Stores received emails
EMAIL_QUEUE = []  # Stores scheduled emails

# Send Email (Now or Later)
@mail_service.route("/send", methods=["POST"])
def send_email():
    sender = request.form.get("sender")
    receiver = request.form.get("receiver")
    subject = request.form.get("subject")
    message = request.form.get("message")
    schedule_time = request.form.get("schedule_time")  # Optional scheduling

    email_data = {"from": sender, "subject": subject, "message": message}

    if receiver not in USER_INBOX:
        USER_INBOX[receiver] = []  # Initialize inbox
    
    if schedule_time:
        EMAIL_QUEUE.append({"receiver": receiver, "email": email_data, "time": int(schedule_time)})
        return f"<h2>Email scheduled for {schedule_time} seconds from now.</h2><br><a href='/mailbox?user={sender}'>Go to Mailbox</a>"
    
    USER_INBOX[receiver].append(email_data)
    return f"<h2>Email sent successfully to {receiver}!</h2><br><a href='/mailbox?user={sender}'>Go to Mailbox</a>"

# Automated Email Sending from Queue
def process_email_queue():
    while True:
        current_time = int(time.time())
        for email_entry in EMAIL_QUEUE[:]:
            if email_entry["time"] <= current_time:
                USER_INBOX[email_entry["receiver"]].append(email_entry["email"])
                EMAIL_QUEUE.remove(email_entry)
        time.sleep(5)  # Check every 5 seconds

# View Mailbox (Inbox)
@mail_service.route("/mailbox", methods=["GET"])
def view_mailbox():
    user = request.args.get("user")
    inbox = USER_INBOX.get(user, [])
    inbox_html = f"<h2>Mailbox for {user}</h2><ul>"

    for mail in inbox:
        inbox_html += f"<li><strong>From:</strong> {mail['from']}<br><strong>Subject:</strong> {mail['subject']}<br>{mail['message']}</li><br>"

    inbox_html += "</ul><br><a href='/local/service'>Back</a>"
    return inbox_html
