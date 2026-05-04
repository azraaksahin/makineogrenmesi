import pdfplumber
import fitz
from bs4 import BeautifulSoup

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

    
    try:
        with open(path, "r", encoding="utf-8", errors="ignore") as f:
            html = f.read()

        if "<html" in html.lower():
            soup = BeautifulSoup(html, "html.parser")
            text = soup.get_text(separator=" ")
            return text
    except:
        pass

    return ""