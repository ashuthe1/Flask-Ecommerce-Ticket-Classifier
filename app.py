from flask import Flask, request, jsonify
import os
from dotenv import load_dotenv
import requests
import json
from ollama import Client

load_dotenv()

app = Flask(__name__)

categories = ["Payment", "Delivery", "Product/Merchant", "Satisfied"]


def classify_review_llama(text):
    client = Client(host='http://127.0.0.1:11434')
    
    prompt = f"Classify the given message into one of the following categories: {', '.join(categories)}. Message: \"{text}\". Return the final classification only."
    
    messages = [
        {
            'role': 'user',
            'content': prompt,
        },
    ]
    
    response = client.chat(model='llama3', messages=messages)
    
    classification = response['message']['content'].strip()
    return classification

def classify_review(text):

    API_KEY = os.getenv('GOOGLE_API_KEY')
    API_URL = 'https://generativelanguage.googleapis.com/v1beta/models/gemini-1.5-flash-latest:generateContent'

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
        raise Exception(f"Gemini returned non-200 status: {response.status_code}")

    result = response.json()

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

@app.route('/classify_review_llama', methods=['POST'])
def classify_review_llama_endpoint():
    if not request.is_json:
        return jsonify({"error": "Invalid input"}), 400
    
    data = request.get_json()
    review_text = data.get('text')
    
    if not review_text:
        return jsonify({"error": "Text is required"}), 400
    
    try:
        classification = classify_review_llama(review_text)
        return jsonify({"classification": classification})
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/health', methods=['GET'])
def health_check():
    return jsonify({"status": "server is healthy"}), 200

if __name__ == '__main__':
    app.run(port="6000", debug=True)
