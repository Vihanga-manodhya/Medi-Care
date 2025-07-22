# File: src/ocr.py
import pytesseract
from PIL import Image

# ----------------- ADD THIS LINE -----------------
# Tell pytesseract where to find the Tesseract-OCR executable.
# The 'r' before the string is important. It means "raw string".
pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'
# -------------------------------------------------

def extract_text_with_ocr(preprocessed_image_path):
    """
    Uses Tesseract OCR to extract text from the preprocessed image.
    """
    print(f"[INFO] Extracting text from: {preprocessed_image_path}")
    try:
        # Open the image and use pytesseract to extract the text
        text = pytesseract.image_to_string(Image.open(preprocessed_image_path))
        print("--- OCR Text Found ---")
        print(text)
        print("----------------------")
        return text
    except Exception as e:
        # This will now give a more specific error if something else is wrong
        print(f"Error during OCR: {e}")
        return ""