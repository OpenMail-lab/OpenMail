import smtplib, json, time
from flask import Blueprint, request, redirect, render_template_string

mail_service = Blueprint("mail_service", __name__)

USER_INBOX = {}  # Stores received emails
EMAIL_QUEUE = []  # Stores scheduled emails

# Send Email (Now or Later)
@mail_service.route("/mail/send", methods=["GET", "POST"])
def send_email():
    if request.method == "GET":
        return render_template_string("""
            <h2>Send Email</h2>
            <form action="/mail/send" method="post">
                To: <input type="text" name="receiver" required><br>
                Subject: <input type="text" name="subject" required><br>
                Message: <textarea name="message" required></textarea><br>
                <input type="submit" value="Send">
            </form>
            <br><a href='/local/service'>Back</a>
        """)
    
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
        return f"<h2>Email scheduled for {schedule_time} seconds from now.</h2><br><a href='/mail/mailbox?user={sender}'>Go to Mailbox</a>"
    
    USER_INBOX[receiver].append(email_data)
    return f"<h2>Email sent successfully to {receiver}!</h2><br><a href='/mail/mailbox?user={sender}'>Go to Mailbox</a>"

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
@mail_service.route("/mail/mailbox", methods=["GET"])
def view_mailbox():
    user = request.args.get("user")
    inbox = USER_INBOX.get(user, [])
    inbox_html = f"""
    <h2>Mailbox for {user}</h2>
    <ul>
        {''.join([f"<li><strong>From:</strong> {mail['from']}<br><strong>Subject:</strong> {mail['subject']}<br>{mail['message']}</li><br>" for mail in inbox])}
    </ul>
    <br><a href='/local/service'>Back</a>
    """
    return inbox_html
