from flask import Flask, request, jsonify
import requests
import json
from dotenv import load_dotenv
import os

# Load environment variables from .env file
load_dotenv()

app = Flask(__name__)

# Retrieve the Google API key from environment variables
API_KEY = os.getenv('GOOGLE_API_KEY')
API_URL = 'https://generativelanguage.googleapis.com/v1beta/models/gemini-1.5-flash-latest:generateContent'

categories = ["Payment", "Delivery", "Product/Merchant", "Satisfied"]

def classify_review(text):
    url = f"{API_URL}?key={API_KEY}"
    prompt = f"Classify the given message into one of the following categories: {', '.join(categories)}. Message: \"{text}\". Return the final classification only."
    
    payload = {
        "contents": [
            {
                "parts": [
                    {
                        "text": prompt,
                    },
                ],
            },
        ],
    }

    headers = {
        'Content-Type': 'application/json',
    }

    response = requests.post(url, headers=headers, data=json.dumps(payload))

    if response.status_code != 200:
        raise Exception(f"Google PaLM2 API returned non-200 status: {response.status_code}")

    result = response.json()

    # Extract the classification from the response
    candidates = result.get("candidates", [])
    if not candidates:
        raise Exception("Failed to extract candidates from response")

    content = candidates[0].get("content", {})
    parts = content.get("parts", [])
    if not parts:
        raise Exception("Failed to extract parts from content")

    classification = parts[0].get("text", "").strip()
    if not classification:
        raise Exception("Failed to extract classification text from parts")

    return classification

@app.route('/classify_review', methods=['POST'])
def classify_review_endpoint():
    if not request.is_json:
        return jsonify({"error": "Invalid input"}), 400
    
    data = request.get_json()
    review_text = data.get('text')
    
    if not review_text:
        return jsonify({"error": "Text is required"}), 400
    
    try:
        classification = classify_review(review_text)
        return jsonify({"classification": classification})
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    app.run(port="6000", debug=True)