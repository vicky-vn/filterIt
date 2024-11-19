from docx import Document

def extract_text_from_docx(file_path):
    try:
        doc = Document(file_path)
        text = "\n".join(paragraph.text for paragraph in doc.paragraphs)
        return text
    except Exception as e:
        print(f"Error extracting text from DOCX: {e}")
        return None