@app.route('/verify', methods=['GET'])
def verify_token():
    token = request.headers.get("Authorization")

    if not token:
        return jsonify({"error": "Token missing"}), 403

    try:
        decoded = jwt.decode(token, SECRET_KEY, algorithms=["HS256"])
        return jsonify({"user": decoded["user"], "role": "admin"})  # 🔥 Default full access for all users
    except jwt.ExpiredSignatureError:
        return jsonify({"error": "Token expired"}), 403
    except jwt.InvalidTokenError:
        return jsonify({"error": "Invalid token"}), 403
