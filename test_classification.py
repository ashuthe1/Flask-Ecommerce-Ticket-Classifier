import requests
import json

# URL of the Flask endpoint
url = 'http://127.0.0.1:6000/classify_review'

# Test cases for different categories
test_cases = {
    "Payment": "I had issues with the payment processing.",
    "Delivery": "The delivery was delayed by two weeks.",
    "Product/Merchant": "The product quality is excellent and the merchant was very responsive.",
    "Satisfied": "I am very satisfied with my purchase."
}

# Function to test each case
def test_classification():
    for category, message in test_cases.items():
        payload = json.dumps({"text": message})
        headers = {'Content-Type': 'application/json'}
        response = requests.post(url, headers=headers, data=payload)

        if response.status_code == 200:
            result = response.json().get("classification", "")
            print(f"Test Case: {category}\nMessage: {message}\nClassification: {result}\n")
        else:
            print(f"Test Case: {category}\nMessage: {message}\nError: {response.text}\n")

if __name__ == '__main__':
    test_classification()
