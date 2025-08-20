from PIL import Image
import io
import pytesseract
from app.utils.preprocess import preprocess_pil

pytesseract.pytesseract.tesseract_cmd = r"C:\Program Files\Tesseract-OCR\tesseract.exe"

def ocr_image_bytes(image_bytes: bytes) -> str:
    pil = Image.open(io.BytesIO(image_bytes)).convert("RGB")
    pil = preprocess_pil(pil)
    text = pytesseract.image_to_string(pil)
    return text.strip()