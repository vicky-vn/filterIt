import pdfplumber

def extract_text_from_pdf(file_path):
    try:
        with pdfplumber.open(file_path) as pdf:
            pdf_text = '\n'.join(page.extract_text() for page in pdf.pages if page.extract_text())
        return pdf_text
    except Exception as e:
        print(f"Error extracting text from PDF: {e}")
        return None