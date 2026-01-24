from pdfminer.high_level import extract_text as pdf_extract
import docx
import os

def parse_pdf(path):
    try:
        return pdf_extract(path)
    except Exception as e:
        print("PDF parse error:", e)
        return ""

def parse_docx(path):
    try:
        doc = docx.Document(path)
        return "\n".join([p.text for p in doc.paragraphs])
    except Exception as e:
        print("DOCX parse error:", e)
        return ""

def parse_txt(path):
    try:
        with open(path, "r", encoding="utf-8", errors="ignore") as f:
            return f.read()
    except Exception as e:
        print("TXT parse error:", e)
        return ""

def parse_file(path, filename=None):
    if filename is None:
        filename = os.path.basename(path)
    filename = filename.lower()
    if filename.endswith(".pdf"):
        return parse_pdf(path)
    if filename.endswith(".docx"):
        return parse_docx(path)
    if filename.endswith(".txt"):
        return parse_txt(path)
    raise ValueError("Unsupported format: " + filename)
