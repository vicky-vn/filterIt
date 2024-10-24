from flask import Flask, jsonify, request
from flask_cors import CORS
from db import collection  # MongoDB connection setup in `db.py`
from tokenization import process_text_with_spacy  # Import the spaCy processing function

app = Flask(__name__)
CORS(app, resources={r"/*": {"origins": "*"}})  # Enable CORS for all routes

# Index route (welcome message)
@app.route('/', methods=['GET'])
def index():
    return "Welcome to the MedRecShield Database Viewer!", 200

# GET API to retrieve all stored records from MongoDB
@app.route('/get_patient_records', methods=['GET'])
def get_patient_records():
    try:
        # Fetch all documents from the MongoDB collection
        records = list(collection.find())
        output = []
        for record in records:
            record['_id'] = str(record['_id'])  # Convert ObjectId to string for JSON serialization
            output.append(record)
        
        # Return the fetched records
        return jsonify(output), 200
    except Exception as e:
        print(f"Error: {e}")
        return jsonify({"error": str(e)}), 500

# Simple POST API to add a new record to MongoDB
@app.route('/add_patient_record', methods=['POST'])
def add_patient_record():
    try:
        # Debug: Check if the request is received
        print("Received POST request.")
        print(f"Request headers: {request.headers}")  # Print headers for debugging
        print(f"Request body: {request.data}")        # Print raw request body

        # Extract JSON data from the request body
        data = request.json
        
        if data is None:
            print("No JSON data received.")
            return jsonify({"error": "Invalid JSON"}), 400
        
        # Insert the received data into MongoDB
        result = collection.insert_one(data)

        # Prepare the response data with the inserted ObjectId as a string
        data['_id'] = str(result.inserted_id)

        # Return a success message with the inserted data
        return jsonify({
            "message": "Data successfully inserted into the database",
            "data": data
        }), 200
    except Exception as e:
        print(f"Error: {e}")
        return jsonify({"error": str(e)}), 500

# POST API to process and tokenize text, then store results in MongoDB
@app.route('/process_and_tokenize', methods=['POST'])
def process_and_tokenize():
    try:
        # Debug: Check if the request is received
        print("Received POST request for text processing.")
        print(f"Request headers: {request.headers}")  # Print headers for debugging
        print(f"Request body: {request.data}")        # Print raw request body

        # Extract JSON data from the request body
        data = request.json
        text = data.get('text', None)
        
        if not text:
            print("No text provided in the request.")
            return jsonify({"error": "No text provided"}), 400

        # Process the text using spaCy
        tokens, entities, tokenized_text, entity_mapping = process_text_with_spacy(text)
        
        # Create a document to store in MongoDB
        document = {
            "original_text": text,
            "tokenized_text": tokenized_text,
            "entity_mapping": entity_mapping,
            "tokens": tokens,
            "entities": entities
        }
        
        # Store the document in the collection
        result = collection.insert_one(document)

        # Prepare the response data with the inserted ObjectId as a string
        document['_id'] = str(result.inserted_id)

        # Return a success message with the processed data
        return jsonify({
            "message": "Text processed, tokenized, and stored successfully",
            "data": document
        }), 200
    except Exception as e:
        print(f"Error: {e}")
        return jsonify({"error": str(e)}), 500

if __name__ == "__main__":
    app.run(host="0.0.0.0", debug=True)  # Bind to all interfaces

