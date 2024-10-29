from flask import Blueprint, jsonify, send_file
from fpdf import FPDF
import os
from bson import ObjectId
from db import db

# Set up a blueprint for PDF generation
parameterized_pdf_generator_bp = Blueprint('parameterized_pdf_generator', __name__)

# Define MongoDB collection for pdf uploads
pdf_uploads_collection = db["pdf_uploads"]

def create_pdf_from_tokenized_data(data, file_path):
    try:
        pdf = FPDF()
        pdf.add_page()
        pdf.set_font("Arial", size=12)

        # Write the title for the tokenized text section
        pdf.cell(200, 10, txt="Tokenized Text:", ln=True)

        # Get the tokenized text without mappings
        tokenized_text = data.get("tokenized_text", "")
        
        # Ensure the tokenized text is displayed without unsupported characters
        cleaned_text = ''.join(char for char in tokenized_text if char.isprintable())

        # Write the cleaned tokenized text, splitting into lines
        for line in cleaned_text.splitlines():
            pdf.multi_cell(0, 10, line)

        # Save the PDF
        pdf.output(file_path)
        return True
    except Exception as e:
        print(f"Error creating PDF: {e}")  # Log the specific error
        return False

@parameterized_pdf_generator_bp.route('/generate_pdf/<doc_id>', methods=['GET'])
def generate_pdf(doc_id):
    try:
        # Fetch the document data from MongoDB using the doc_id
        data = pdf_uploads_collection.find_one({"_id": ObjectId(doc_id)})
        if not data:
            return jsonify({"error": "Document not found"}), 404

        print("Retrieved data for PDF generation:", data)  # Log the retrieved data

        # Use the existing tokenized_text directly from the stored document
        tokenized_text = data.get("tokenized_text", "No tokenized text available.")
        entity_mapping = data.get("entity_mapping", {})

        user_id = data["uploadedby"]
        pdf_path = os.path.join("/Users/vigneshnatarajan/myData/UWindsor/Term_II/ADT/MedRecShield/backend/public", user_id, "generated_pdfs")
        
        if not os.path.exists(pdf_path):
            os.makedirs(pdf_path)
        
        pdf_file_path = os.path.join(pdf_path, f"tokenized_{doc_id}.pdf")

        # Create the PDF with the existing tokenized data
        if create_pdf_from_tokenized_data({
            "tokenized_text": tokenized_text,
            "entity_mapping": entity_mapping
        }, pdf_file_path):
            return send_file(pdf_file_path, as_attachment=True, download_name=f"tokenized_{doc_id}.pdf")
        else:
            return jsonify({"error": "Failed to create PDF"}), 500
    except Exception as e:
        print(f"Error: {e}")
        return jsonify({"error": str(e)}), 500
