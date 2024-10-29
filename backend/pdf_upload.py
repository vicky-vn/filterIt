from flask import Blueprint, jsonify, request, current_app, send_from_directory
from werkzeug.utils import secure_filename
import os
import time
import jwt
from db import db  # Assuming db is initialized here for MongoDB
from tokenization import process_text_with_spacy  # Import tokenization function
from pdf_text_extractor import extract_text_from_pdf  # Import the new PDF text extractor

# Set up a blueprint for PDF uploads and serving
pdf_upload_bp = Blueprint('pdf_upload', __name__)

# Define MongoDB collection for pdf uploads
pdf_uploads_collection = db["pdf_uploads"]

# Base folder for all uploads
#BASE_UPLOAD_FOLDER = ""
BASE_UPLOAD_FOLDER = "/Users/vigneshnatarajan/myData/UWindsor/Term_II/ADT/MedRecShield/backend/public"
MAX_CONTENT_LENGTH = 16 * 1024 * 1024  # Limit to 16MB

# Helper function to generate a custom filename
def generate_custom_filename():
    existing_files = [f for f in os.listdir(BASE_UPLOAD_FOLDER) if f.endswith('.pdf')]
    next_index = len(existing_files) + 1
    timestamp = int(time.time())
    return f"{timestamp}.pdf"

# PDF upload and tokenization route
@pdf_upload_bp.route('/upload_pdf', methods=['POST'])
def upload_pdf():
    try:
        token = request.headers.get('Authorization', '').replace('Bearer ', '')
        if not token:
            return jsonify({"error": "Token is missing!"}), 403
        
        decoded_token = jwt.decode(token, current_app.config['JWT_SECRET_KEY'], algorithms=["HS256"])
        user_id = decoded_token["user_id"]

        user_upload_folder = os.path.join(BASE_UPLOAD_FOLDER, user_id, "uploads")
        if not os.path.exists(user_upload_folder):
            os.makedirs(user_upload_folder)

        if 'file' not in request.files:
            return jsonify({"error": "No file part in the request"}), 400

        file = request.files['file']
        if file.filename == '':
            return jsonify({"error": "No selected file"}), 400

        if file and file.filename.lower().endswith('.pdf'):
            # Save the uploaded PDF
            filename = generate_custom_filename()
            file_path = os.path.join(user_upload_folder, filename)
            file.save(file_path)

            # Extract text using the new function
            pdf_text = extract_text_from_pdf(file_path)
            if not pdf_text:
                return jsonify({"error": "Failed to extract text from PDF."}), 500
            
            # Tokenize the extracted text
            tokens, corrected_entities, tokenized_text, entity_mapping = process_text_with_spacy(pdf_text)

            # Insert details into the pdf_uploads collection
            pdf_uploads_collection.insert_one({
                "docname": filename,
                "uploadedby": user_id,
                "filepath": file_path,
                "url": f"/view_pdf/{user_id}/{filename}",
                "original_text": pdf_text,
                "tokenized_text": tokenized_text,
                "entity_mapping": entity_mapping,
                "tokens": tokens,
                "entities": corrected_entities
            })

            # Return success response with file path and tokenized URL
            return jsonify({
                "message": "File uploaded and tokenized successfully",
                "filename": filename,
                "file_path": file_path,
                "url": request.host_url[:-1] + f"/view_pdf/{user_id}/{filename}",  # URL to view the PDF
                "tokenized_text": tokenized_text  # Optionally, show tokenized text in the response
            }), 200
        else:
            return jsonify({"error": "Invalid file format. Only PDF files are allowed."}), 400
    except Exception as e:
        print(f"Error: {e}")
        return jsonify({"error": str(e)}), 500
