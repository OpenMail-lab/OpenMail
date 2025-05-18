import bcrypt
from flask import Flask, request, jsonify, make_response

app = Flask(__name__)

# Simulated database (replace with actual storage)
USER_DB = {}

def hash_password(password):
    return bcrypt.hashpw(password.encode(), bcrypt.gensalt())

@app.route("/register", methods=["POST"])
def register():
    data = request.json
    username, password = data.get("username"), data.get("password")

    if username in USER_DB:
        return jsonify({"error": "User already exists"}), 400

    USER_DB[username] = hash_password(password)  # Store hashed password
    return jsonify({"message": "Registration successful"}), 201

@app.route("/login", methods=["POST"])
def login():
    data = request.json
    username, password = data.get("username"), data.get("password")

    stored_password = USER_DB.get(username)
    if stored_password and bcrypt.checkpw(password.encode(), stored_password):
        response = make_response(jsonify({"message": "Login successful"}))
        response.set_cookie("session_token", username, httponly=True, secure=True)
        return response

    return jsonify({"error": "Invalid credentials"}), 401

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5001, debug=True)
