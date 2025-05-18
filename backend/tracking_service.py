from flask import Blueprint, request

tracking_service = Blueprint("tracking_service", __name__)

EMAIL_TRACKING = {}  # Stores email open counts

@tracking_service.route("/track/<email_id>")
def track_email(email_id):
    EMAIL_TRACKING[email_id] = EMAIL_TRACKING.get(email_id, 0) + 1
    return f"<img src='tracking_pixel.png' width='1' height='1'>"

def get_email_tracking(email_id):
    return EMAIL_TRACKING.get(email_id, 0)  # Returns number of opens
