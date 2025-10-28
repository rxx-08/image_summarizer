# from fastapi import FastAPI, File, UploadFile
# import pytesseract
# from PIL import Image
# from transformers import pipeline

# pytesseract.pytesseract.tesseract_cmd = r"C:\\Program Files\\Tesseract-OCR\\tesseract.exe"



# app = FastAPI()
# summarizer = pipeline("summarization", model="t5-small")

# @app.post("/summarize_image/")
# async def summarize_image(file: UploadFile = File(...)):
#     image = Image.open(file.file)
#     text = pytesseract.image_to_string(image)


#     summary = summarizer(text, max_length=130, min_length=30, do_sample=False)

#     return {
#         "original_text": text[:300]+"...",
#         "summary": summary[0]['summary_text']}

from fastapi import FastAPI, File, UploadFile
import pytesseract
from PIL import Image, ImageEnhance, ImageFilter
from transformers import pipeline

# Tesseract path
pytesseract.pytesseract.tesseract_cmd = r"C:\\Program Files\\Tesseract-OCR\\tesseract.exe"

# FastAPI app
app = FastAPI()

# Summarization model
summarizer = pipeline("summarization", model="facebook/bart-large-cnn")

def preprocess_image(image: Image.Image) -> Image.Image:
    """
    Preprocess image for better OCR:
    - Convert to grayscale
    - Apply sharpening
    - Increase contrast
    """
    # Convert to grayscale
    image = image.convert("L")
    
    # Increase contrast
    enhancer = ImageEnhance.Contrast(image)
    image = enhancer.enhance(2.0)
    
    # Sharpen image
    image = image.filter(ImageFilter.SHARPEN)
    
    return image

def clean_text(text: str) -> str:
    """
    Clean OCR output:
    - Remove extra newlines
    - Collapse multiple spaces
    """
    text = text.replace("\n", " ").replace("\r", " ")
    text = ' '.join(text.split())
    return text

@app.post("/summarize_image/")
async def summarize_image(file: UploadFile = File(...)):
    # Open uploaded image
    image = Image.open(file.file)
    
    # Preprocess for OCR
    image = preprocess_image(image)
    
    # Extract text
    text = pytesseract.image_to_string(image)
    
    # Clean OCR text
    text = clean_text(text)
    
    # Summarize
    summary = summarizer(text, max_length=130, min_length=30, do_sample=False)
    
    # Return cleaned output
    return {
        "original_text": text[:300]+"...",
        "summary": summary[0]['summary_text']
    }
