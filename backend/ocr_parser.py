from PIL import Image
import pytesseract
import pdfplumber

def extract_text_from_image(file, language="eng"):
    img = Image.open(file)
    try:
        return pytesseract.image_to_string(img, lang=language)
    except pytesseract.TesseractError as e:
        return f"[OCR Error: {e}]"

def extract_text_from_pdf(file, language="eng"):
    text = ""
    with pdfplumber.open(file) as pdf:
        for page in pdf.pages:
            page_text = page.extract_text()
            if page_text:
                text += page_text + "\n"
    return text
