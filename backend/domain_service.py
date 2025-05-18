from flask import Blueprint

domain_service = Blueprint("domain_service", __name__)

@domain_service.route("/domain")
def get_domain():
    return "<h2>OpenMail is running with a domain!</h2><br><a href='/'>Back</a>"
