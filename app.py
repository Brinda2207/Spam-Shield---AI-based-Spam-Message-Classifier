from flask import Flask, request, jsonify
from flask_cors import CORS

app = Flask(__name__)

# Allow CORS for all origins

CORS(app)

@app.route("/predict", methods=["POST"])
def predict():
    try:
        data = request.get_json()
        message = data.get("text", "").strip().lower()

        if not message:
            return jsonify({"error": "No message provided"}), 400

        # Improved spam detection logic
        spam_keywords = ["win", "free", "lottery", "prize", "urgent", "click", "subscribe"]
        strict_spam_phrases = ["limited time offer", "exclusive deal", "click here to claim"]

        # Detect spam based on phrases first (stronger signal)
        if any(phrase in message for phrase in strict_spam_phrases):
            prediction = "Spam"
        elif sum(1 for word in spam_keywords if word in message) >= 2:
            prediction = "Spam"
        else:
            prediction = "Not Spam"

        return jsonify({"result": prediction})

    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == "__main__":
    app.run(debug=True)
