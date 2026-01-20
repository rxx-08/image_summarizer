import pytesseract
from PIL import Image
import os
import sys

def extract_text_from_image(image_path: str) -> str:
    
    try:
        # Open the image file
        with Image.open(image_path) as img:
            # Use Tesseract to do OCR on the image
            text = pytesseract.image_to_string(img)
            return text
    except Exception as e:
        print(f"Error extracting text from image: {e}")
        return ""
    

    if __name__ == "__main__":
        if len(sys.argv) != 2:
            print("Usage: python extract.py <image_path>")
            sys.exit(1)

        # image_path = sys.argv[1]
        # if not os.path.isfile(image_path):
        #     print(f"File not found: {image_path}")
        #     sys.exit(1)

        image_path = "C:\\Users\\rasag\\Downloads\\download (4).jpeg"
        if not os.path.isfile(image_path):
            print(f"File not found: {image_path}")
            sys.exit(1)


        extracted_text = extract_text_from_image(image_path)
        with open("output_data.txt", "w", encoding="utf-8") as f:
            f.write(extracted_text)

        print("Text extraction complete. Check output_data.txt for results.")
        print('extracted_text:', extracted_text)