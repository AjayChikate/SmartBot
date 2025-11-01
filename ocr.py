import os
import pytesseract
from PIL import Image
from dotenv import load_dotenv

load_dotenv()
tesseract_cmd = os.getenv("TESSERACT_CMD")

def ocr_image(image: Image.Image, lang: str = "eng"):
    try:
        if tesseract_cmd:
            pytesseract.pytesseract.tesseract_cmd = tesseract_cmd
        txt= pytesseract.image_to_string(image, lang=lang)
        return txt
    except:
        return ""