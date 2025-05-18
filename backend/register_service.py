from flask import Blueprint, request, redirect

register_service = Blueprint("register_service", __name__)
USER_DATABASE = {}

@register_service.route("/register", methods=["GET", "POST"])
def register():
    email_type = request.args.get("type")  # Check if user chose domain/local
    
    if request.method == "POST":
        username = request.form.get("username")
        custom_email = request.form.get("custom_email")

        if custom_email in USER_DATABASE:
            return "<h2>Email already exists. Try another.</h2><br><a href='/register'>Back</a>"

        USER_DATABASE[custom_email] = {"username": username, "email": custom_email}
        response = redirect("/mail_dashboard")
        response.set_cookie("user_email", custom_email)  # Store login session
        return response

    return f"""  
    <h2>Register for OpenMail - {email_type.title()}</h2>
    <form action="/register?type={email_type}" method="post">
        Username: <input type="text" name="username" required><br>
        Email Address: <input type="text" name="custom_email" required><br>
        <input type="submit" value="Register">
    </form>
    <br><a href='/'>Back</a>
    """
