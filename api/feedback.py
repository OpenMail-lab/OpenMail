from flask import Flask, request, jsonify

app = Flask(__name__)
FEEDBACK_STORE = "feedback.txt"

@app.route('/api/feedback', methods=['POST'])
def collect_feedback():
    data = request.json
    feedback_text = f"User: {data['user']}\nFeedback: {data['message']}\n---\n"

    with open(FEEDBACK_STORE, "a") as f:
        f.write(feedback_text)

    return jsonify({"status": "✅ Feedback submitted! Thank you!"})

if __name__ == "__main__":
    app.run(port=5008, debug=True)
