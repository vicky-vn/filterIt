# pdf_text_extractor.py

import pdfplumber

def extract_text_from_pdf(file_path):
    """Extracts text from a PDF file and returns it as a single string."""
    try:
        with pdfplumber.open(file_path) as pdf:
            # Concatenate text from all pages
            pdf_text = '\n'.join(page.extract_text() for page in pdf.pages if page.extract_text())
        return pdf_text
    except Exception as e:
        print(f"Error extracting text from PDF: {e}")
        return None