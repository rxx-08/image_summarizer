# # from fastapi import FastAPI, File, UploadFile
# # import pytesseract
# # from PIL import Image
# # from transformers import pipeline

# # pytesseract.pytesseract.tesseract_cmd = r"C:\\Program Files\\Tesseract-OCR\\tesseract.exe"



# # app = FastAPI()
# # summarizer = pipeline("summarization", model="t5-small")

# # @app.post("/summarize_image/")
# # async def summarize_image(file: UploadFile = File(...)):
# #     image = Image.open(file.file)
# #     text = pytesseract.image_to_string(image)


# #     summary = summarizer(text, max_length=130, min_length=30, do_sample=False)

# #     return {
# #         "original_text": text[:300]+"...",
# #         "summary": summary[0]['summary_text']}

# from fastapi import FastAPI, File, UploadFile
# import pytesseract
# from PIL import Image, ImageEnhance, ImageFilter
# from transformers import pipeline
# from db import get_db
# from models import Summary
# from schemas import SummaryResponse
# import os
# # Tesseract path
# pytesseract.pytesseract.tesseract_cmd = r"C:\\Program Files\\Tesseract-OCR\\tesseract.exe"

# # FastAPI app
# app = FastAPI()

# # Summarization model
# summarizer = pipeline("summarization", model="facebook/bart-large-cnn")

# def preprocess_image(image: Image.Image) -> Image.Image:
#     """
#     Preprocess image for better OCR:
#     - Convert to grayscale
#     - Apply sharpening
#     - Increase contrast
#     """
#     # Convert to grayscale
#     image = image.convert("L")
    
#     # Increase contrast
#     enhancer = ImageEnhance.Contrast(image)
#     image = enhancer.enhance(2.0)
    
#     # Sharpen image
#     image = image.filter(ImageFilter.SHARPEN)
    
#     return image

# def clean_text(text: str) -> str:
#     """
#     Clean OCR output:
#     - Remove extra newlines
#     - Collapse multiple spaces
#     """
#     text = text.replace("\n", " ").replace("\r", " ")
#     text = ' '.join(text.split())
#     return text

# @app.post("/summarize_image/")
# async def summarize_image(file: UploadFile = File(...)):
#     # Open uploaded image
#     image = Image.open(file.file)
    
#     # Preprocess for OCR
#     image = preprocess_image(image)
    
#     # Extract text
#     text = pytesseract.image_to_string(image)
    
#     # Clean OCR text
#     text = clean_text(text)
    
#     # Summarize
#     summary = summarizer(text, max_length=130, min_length=30, do_sample=False)
    
#     # Return cleaned output
#     # return {
#     #     "original_text": text[:300]+"...",
#     #     "summary": summary[0]['summary_text']
#     # }

#     db.add(summary)
#     db.commit()
#     db.refresh(summary)

#     return summary



from fastapi import FastAPI, File, UploadFile, Depends
from sqlalchemy.orm import Session
import pytesseract
from PIL import Image, ImageEnhance, ImageFilter
from transformers import pipeline
from serve.db import get_db
from serve.models import Summary
from serve.schemas import SummaryResponse

# ✅ Path to your Tesseract executable
pytesseract.pytesseract.tesseract_cmd = r"C:\\Program Files\\Tesseract-OCR\\tesseract.exe"

# ✅ FastAPI app
app = FastAPI()

# ✅ Summarization model
summarizer = pipeline("summarization", model="facebook/bart-large-cnn")

# --- Preprocessing helpers ---
def preprocess_image(image: Image.Image) -> Image.Image:
    """Enhance image for better OCR accuracy."""
    image = image.convert("L")
    enhancer = ImageEnhance.Contrast(image)
    image = enhancer.enhance(2.0)
    image = image.filter(ImageFilter.SHARPEN)
    return image

def clean_text(text: str) -> str:
    """Clean OCR output by removing noise."""
    text = text.replace("\n", " ").replace("\r", " ")
    text = ' '.join(text.split())
    return text

# --- Endpoint ---
@app.post("/summarize_image/", response_model=SummaryResponse)
async def summarize_image(
    file: UploadFile = File(...),
    db: Session = Depends(get_db)
):
    """Extract text from an uploaded image, summarize it, and store results in DB."""

    # Step 1: Read and preprocess image
    image = Image.open(file.file)
    image = preprocess_image(image)

    # Step 2: Extract text with OCR
    text = pytesseract.image_to_string(image)
    text = clean_text(text)

    # Step 3: Summarize extracted text
    if len(text.strip()) < 50:
        summary_text = "Text too short for summarization."
    else:
        summary = summarizer(text, max_length=130, min_length=30, do_sample=False)
        summary_text = summary[0]['summary_text']

    # Step 4: Save to database
    new_summary = Summary(
        image_name=file.filename,
        extracted_text=text,
        summary=summary_text
    )
    db.add(new_summary)
    db.commit()
    db.refresh(new_summary)

    # Step 5: Return response
    return new_summary
