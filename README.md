# E-commerce Review Classification API

This Flask application provides an endpoint to classify e-commerce reviews into predefined categories using the Google PaLM2 API.

## Prerequisites

- Python 3.x
- `pip` (Python package installer)

## Setup

### 1. Clone the Repository

```sh
git clone https://github.com/yourusername/yourrepository.git
cd yourrepository
```

### 2. Create a Virtual Environment

Create a virtual environment to manage dependencies:

- MacOS
```sh
python3 -m venv venv
```

- Linux
```sh
virtualenv venv
```

### 3. Activate the Virtual Environment

- **Windows:**

  ```sh
  .\venv\Scripts\activate
  ```

- **macOS/Linux:**

  ```sh
  source venv/bin/activate
  ```

### 4. Install Dependencies

Install the required packages using `pip`:

```sh
pip install -r requirements.txt
```

### 5. Create a `.env` File

Create a `.env` file in the root directory and add your Google API key:

```
GOOGLE_API_KEY=your_api_key
```

## Running the Server

Start the Flask server:

```sh
python3 app.py
```

The server will be running at `http://127.0.0.1:6000`.

## Testing the Endpoint

You can use `curl` or Postman to test the endpoint with various review messages.

### Using `curl`

#### Payment

```sh
curl -X POST http://127.0.0.1:6000/classify_review \
    -H "Content-Type: application/json" \
    -d '{"text": "I had issues with the payment processing."}'
```

#### Delivery

```sh
curl -X POST http://127.0.0.1:6000/classify_review \
    -H "Content-Type: application/json" \
    -d '{"text": "The delivery was delayed by two weeks."}'
```

#### Product/Merchant

```sh
curl -X POST http://127.0.0.1:6000/classify_review \
    -H "Content-Type: application/json" \
    -d '{"text": "The product quality is excellent and the merchant was very responsive."}'
```

#### Satisfied

```sh
curl -X POST http://127.0.0.1:6000/classify_review \
    -H "Content-Type: application/json" \
    -d '{"text": "I am very satisfied with my purchase."}'
```

## Automated Testing

Make sure your Flask server is running, then execute the test script:

```sh
python3 test_classification.py
```
