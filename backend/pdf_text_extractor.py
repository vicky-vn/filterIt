import os
from flask import Blueprint, jsonify, request
import pdfplumber

pdf_extractor_bp = Blueprint("process_pdf", __name__)

def extract_text_from_pdf(file_path):
    try:
        with pdfplumber.open(file_path) as pdf:
            pdf_text = '\n'.join(page.extract_text() for page in pdf.pages if page.extract_text())
        return pdf_text
    except Exception as e:
        print(f"Error extracting text from PDF: {e}")
        return None

@pdf_extractor_bp.route("/process_pdf", methods=["POST"])
def process_pdf():
    try:
        # Check if a file is included in the request
        if 'file' not in request.files:
            return jsonify({"error": "No file provided"}), 400

        file = request.files['file']

        # Validate that the file is a PDF
        if not file.filename.lower().endswith('.pdf'):
            return jsonify({"error": "File must be a PDF"}), 400

        # Save the file temporarily for processing
        temp_file_path = os.path.join("/tmp", file.filename)
        file.save(temp_file_path)

        # Extract text from the PDF
        extracted_text = extract_text_from_pdf(temp_file_path)

        # Remove the temporary file
        os.remove(temp_file_path)

        if not extracted_text:
            return jsonify({"error": "Failed to extract text from the PDF"}), 500

        return jsonify({"extracted_text": extracted_text}), 200

    except Exception as e:
        print(f"Error processing PDF: {e}")
        return jsonify({"error": str(e)}), 500