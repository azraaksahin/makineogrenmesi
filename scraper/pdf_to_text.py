import pdfplumber
import fitz  # PyMuPDF

def pdf_to_text(path):

    try:
        text = ""
        with pdfplumber.open(path) as pdf:
            for page in pdf.pages:
                text += page.extract_text() or ""
        if text.strip():
            return text
    except:
        pass
    

    try:
        doc = fitz.open(path)
        text = ""
        for page in doc:
            text += page.get_text()
        if text.strip():
            return text
    except:
        pass
    
    return ""