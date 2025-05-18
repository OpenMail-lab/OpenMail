import requests
import smtplib
from email.mime.text import MIMEText
from flask import Blueprint, request

smtp_service = Blueprint("smtp_service", __name__, url_prefix="/smtp")

# ✅ Force IPv4 instead of IPv6
def get_public_ipv4():
    try:
        return requests.get("https://api4.ipify.org").text
    except:
        return "127.0.0.1"

SMTP_SERVER = get_public_ipv4()  # ✅ Uses IPv4 only
SMTP_PORT = 5001

@smtp_service.route("/send", methods=["GET", "POST"])
def send_email():
    sender = request.cookies.get("user_email")  
    if not sender:
        return redirect("/")  

    if request.method == "POST":
        receiver = request.form.get("receiver")
        subject = request.form.get("subject")
        message = request.form.get("message")

        msg = MIMEText(message)
        msg["From"] = sender
        msg["To"] = receiver
        msg["Subject"] = subject

        try:
            server = smtplib.SMTP(SMTP_SERVER, SMTP_PORT, timeout=30)  # ✅ Increase timeout
            server.starttls()
            server.login(sender, "stored-session-password")
            server.sendmail(sender, receiver, msg.as_string())
            server.quit()
            return f"<h2>Email sent successfully to {receiver}!</h2><br><a href='/mail_dashboard'>Back</a>"
        except Exception as e:
            return f"<h2>Failed to send email: {e}</h2><br><a href='/mail_dashboard'>Back</a>"

    return f"""
    <h2>Send Email</h2>
    <form action="/smtp/send" method="post">
        <p><strong>Your Email:</strong> {sender}</p>
        Recipient Email: <input type="text" name="receiver" required><br>
        Subject: <input type="text" name="subject" required><br>
        Message: <textarea name="message" required></textarea><br>
        <input type="submit" value="Send Email">
    </form>
    <br><a href='/mail_dashboard'>Back</a>
    """
