from flask import Blueprint, jsonify, request, send_file
from db import db
from bson import ObjectId
from fpdf import FPDF
import os

pdf_generator_bp = Blueprint('pdf_generator', __name__)

uploads_collection = db["uploads"]

@pdf_generator_bp.route('/generate_pdf/<document_id>', methods=['GET'])
@pdf_generator_bp.route('/generate_pdf/<document_id>', methods=['GET'])
def generate_pdf_endpoint(document_id):
    try:
        # Fetch the document using its ID
        document = uploads_collection.find_one({"_id": ObjectId(document_id)})
        if not document:
            return jsonify({"error": "Document not found"}), 404

        # Get the tokenized text
        tokenized_text = document.get("tokenized_text")
        if not tokenized_text:
            return jsonify({"error": "No tokenized text available to generate PDF"}), 400

        # Generate the PDF and save it to a temporary file
        temp_pdf_path = f"/tmp/{document_id}_parameterized_text.pdf"
        pdf = FPDF()
        pdf.add_page()

        # Add a Unicode font
        pdf.add_font('DejaVu', '', '/Users/vigneshnatarajan/myData/UWindsor/Term_II/ADT/MedRecShield/backend/dejavu-sans/DejaVuSans.ttf', uni=True)  # Ensure the font file is present in your project
        pdf.set_font("DejaVu", size=12)

        # Add the tokenized text to the PDF
        pdf.multi_cell(0, 10, tokenized_text)
        pdf.output(temp_pdf_path)

        response = send_file(
            temp_pdf_path,
            as_attachment=True,
            download_name=f"{document_id}_parameterized_text.pdf",
            mimetype='application/pdf'
        )

        os.remove(temp_pdf_path)

        return response
    except Exception as e:
        print(f"Error generating PDF: {e}")
        return jsonify({"error": str(e)}), 500

pdf_generator_bp.route('/generate_summary_pdf/<document_id>', methods=['GET'])
def generate_summary_pdf(document_id):
    try:
        # Fetch the document using its ID
        document = uploads_collection.find_one({"_id": ObjectId(document_id)})
        if not document:
            return jsonify({"error": "Document not found"}), 404

        demasked_response = document.get("demasked_response")
        if not demasked_response:
            return jsonify({"error": "No demasked summary available to generate PDF"}), 400

        # Generate the PDF and save it to a temporary file
        temp_pdf_path = f"/tmp/{document_id}_demasked_summary.pdf"
        pdf = FPDF()
        pdf.add_page()
        pdf.set_font("Arial", size=12)
        pdf.multi_cell(0, 10, demasked_response)
        pdf.output(temp_pdf_path)  # Save to file

        response = send_file(
            temp_pdf_path,
            as_attachment=True,
            download_name=f"{document_id}_demasked_summary.pdf",
            mimetype='application/pdf'
        )

        os.remove(temp_pdf_path)

        return response
    except Exception as e:
        print(f"Error generating PDF: {e}")
        return jsonify({"error": str(e)}), 500
