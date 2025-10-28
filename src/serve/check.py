import pytesseract

# Set the exact path to the Tesseract executable
pytesseract.pytesseract.tesseract_cmd = r"C:\\Program Files\\Tesseract-OCR\\tesseract.exe"
print(pytesseract.get_tesseract_version())