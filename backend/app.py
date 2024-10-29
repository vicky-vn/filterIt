from flask import Flask, jsonify, request
from flask_cors import CORS
from db import collection  # MongoDB connection setup in `db.py`
import os

from tokenization import process_text_with_spacy  # Import the spaCy processing function
from auth_decorator import token_required  # Import the JWT decorator
from user_signup import user_signup_bp
from user_signin import user_signin_bp
from pdf_upload import pdf_upload_bp  # Import the pdf upload blueprint
from pdf_upload import send_from_directory  # Ensure send_from_directory is imported
from parameterized_pdf_generator import parameterized_pdf_generator_bp  # Import the new PDF generator blueprint
from settings import settings_bp


app = Flask(__name__)
CORS(app, resources={r"/*": {"origins": "*"}})  # Enable CORS for all routes

# JWT
app.config['JWT_SECRET_KEY'] = 'rasenshuriken_007'  # Replace with a secure key

# Register blueprints for signup and signin
app.register_blueprint(user_signup_bp)
app.register_blueprint(user_signin_bp)

# Register the PDF upload blueprint
app.register_blueprint(pdf_upload_bp)

# Register the PDF generator blueprint
app.register_blueprint(parameterized_pdf_generator_bp)

app.register_blueprint(settings_bp)

# Index route (welcome message)
@app.route('/', methods=['GET'])
def index():
    return "Welcome to the MedRecShield Database Viewer!", 200

# GET API to retrieve all stored records from MongoDB
@app.route('/get_patient_records', methods=['GET'])
@token_required
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
        print("Received POST request.")
        print(f"Request headers: {request.headers}")  # Print headers for debugging
        print(f"Request body: {request.data}")        # Print raw request body

        data = request.json
        
        if data is None:
            print("No JSON data received.")
            return jsonify({"error": "Invalid JSON"}), 400
        
        result = collection.insert_one(data)

        data['_id'] = str(result.inserted_id)

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
        print("Received POST request for text processing.")
        print(f"Request headers: {request.headers}")  # Print headers for debugging
        print(f"Request body: {request.data}")        # Print raw request body

        data = request.json
        text = data.get('text', None)
        
        if not text:
            print("No text provided in the request.")
            return jsonify({"error": "No text provided"}), 400

        tokens, entities, tokenized_text, entity_mapping = process_text_with_spacy(text)
        
        document = {
            "original_text": text,
            "tokenized_text": tokenized_text,
            "entity_mapping": entity_mapping,
            "tokens": tokens,
            "entities": entities
        }
        
        result = collection.insert_one(document)

        document['_id'] = str(result.inserted_id)

        return jsonify({
            "message": "Text processed, tokenized, and stored successfully",
            "data": document
        }), 200
    except Exception as e:
        print(f"Error: {e}")
        return jsonify({"error": str(e)}), 500

# View PDF Route
@app.route('/view_pdf/<user_id>/<filename>', methods=['GET'])
def view_pdf(user_id, filename):
    user_folder = os.path.join('/Users/vigneshnatarajan/myData/UWindsor/Term_II/ADT/MedRecShield/backend/public', user_id, "uploads")
    return send_from_directory(user_folder, filename)

if __name__ == "__main__":
    app.run(host="0.0.0.0", debug=True, port=8000)  # Bind to all interfaces
