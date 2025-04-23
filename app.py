from flask import Flask, request, jsonify
import joblib
import re
from flask_cors import CORS  # Import CORS

# Load the trained model and vectorizer
model = joblib.load("spam_detector_nb.pkl")
vectorizer = joblib.load("tfidf_vectorizer.pkl")

# Initialize Flask app
app = Flask(__name__)
CORS(app)  # Enable CORS for all routes

# Function to preprocess messages
def preprocess_text(text):
    text = text.lower()  # Convert to lowercase
    text = re.sub(r'\W', ' ', text)  # Remove special characters
    return text

# Default route (to avoid "Not Found" error)
@app.route("/")
def home():
    return "Flask server is running! Use the /predict endpoint to check messages."

# Define API route for spam prediction
@app.route("/predict", methods=["POST"])
def predict():
    try:
        data = request.get_json()  # Get JSON data
        message = data.get("message", "")

        if not message:
            return jsonify({"error": "No message provided"}), 400

        # Preprocess message and convert to TF-IDF format
        cleaned_message = preprocess_text(message)
        message_vector = vectorizer.transform([cleaned_message]).toarray()

        # Predict using the model
        prediction = model.predict(message_vector)[0]
        result = "Spam" if prediction == 1 else "Not Spam"

        return jsonify({"message": message, "prediction": result}) # Changed 'result' to 'prediction'

    except Exception as e:
        return jsonify({"error": str(e)}), 500

# Run Flask app
if __name__ == "__main__":
    app.run(debug=True)