import pdfplumber

def extract_text_from_pdf(pdf_path):
    """
    Extracts text from a PDF resume (one or more pages).
    """
    text = ""
    with pdfplumber.open(pdf_path) as pdf:
        for page in pdf.pages:
            page_text = page.extract_text()
            if page_text:
                text += page_text + "\n"
    return text

def extract_text_from_txt(txt_path):
    """
    Extracts text from a plain text resume file (.txt).
    """
    with open(txt_path, 'r', encoding='utf-8') as f:
        text = f.read()
    return text

def extract_resume_text(filepath):
    """
    Unified resume text extractor for PDF (.pdf) and TXT (.txt) files.
    """
    if filepath.lower().endswith('.pdf'):
        return extract_text_from_pdf(filepath)
    elif filepath.lower().endswith('.txt'):
        return extract_text_from_txt(filepath)
    else:
        raise ValueError("Unsupported resume file format. Use PDF or TXT.")

# Example usage:
if __name__ == "__main__":
    resume_path = "your_resume.pdf"  # Or "your_resume.txt"
    extracted_text = extract_resume_text(resume_path)
    print("Extracted Resume Text:\n", extracted_text)
