# from PIL import Image
# import io
# import pytesseract
# from app.utils.preprocess import preprocess_pil

# pytesseract.pytesseract.tesseract_cmd = r"C:\Program Files\Tesseract-OCR\tesseract.exe"

# def ocr_image_bytes(image_bytes: bytes) -> str:
#     pil = Image.open(io.BytesIO(image_bytes)).convert("RGB")
#     pil = preprocess_pil(pil)
#     text = pytesseract.image_to_string(pil)
#     return text.strip()

from PIL import Image
import io
import pytesseract
import easyocr
from app.utils.preprocess import preprocess_pil
import numpy as np
import cv2
import shutil


# pytesseract.pytesseract.tesseract_cmd = r"C:\Program Files\Tesseract-OCR\tesseract.exe"

# Find tesseract in PATH
tesseract_cmd = shutil.which("tesseract")
if not tesseract_cmd:
    raise EnvironmentError("Tesseract is not installed in the container")
pytesseract.pytesseract.tesseract_cmd = tesseract_cmd


# Initialize EasyOCR reader (add languages you expect)
reader = easyocr.Reader(['en', 'fr', 'es', 'de'], gpu=False) # Set gpu=True if available


def ocr_image_bytes(image_bytes: bytes) -> dict:
    pil_img = Image.open(io.BytesIO(image_bytes)).convert("RGB")
    pil_img = preprocess_pil(pil_img)


    # Try Tesseract first
    text = pytesseract.image_to_string(pil_img, lang='eng', config='--oem 3 --psm 6').strip()
    if text:
        return {"engine": "tesseract", "text": text}


    # Fallback to EasyOCR
    img_array = np.array(pil_img)
    img_cv = cv2.cvtColor(img_array, cv2.COLOR_RGB2BGR)


    results = reader.readtext(img_cv, detail=0)
    fallback_text = "\n".join(results).strip()


    if fallback_text:
        return {"engine": "easyocr", "text": fallback_text}
    else:
        raise Exception("OCR processing failed: both Tesseract and EasyOCR returned empty text")