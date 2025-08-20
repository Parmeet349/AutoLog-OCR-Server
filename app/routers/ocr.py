import re
from fastapi import APIRouter, UploadFile, File, HTTPException
from fastapi.responses import JSONResponse

from app.parsers.receipt_parser import parse_receipt
from app.services.ocr_service import ocr_image_bytes

router = APIRouter()


def clean_raw_text(raw_text: str) -> str:
    if not raw_text:
        return ""
    text = raw_text.replace("¥", "").replace("#", "")
    text = re.sub(r"[^\x20-\x7E\n]", "", text)
    return "\n".join([line.strip() for line in text.splitlines() if line.strip()])


def format_phone(phone: str) -> str:
    if phone == "N/A":
        return phone
    digits = re.sub(r"[^\d]", "", phone)
    if len(digits) == 10:
        return f"({digits[:3]}) {digits[3:6]}-{digits[6:]}"
    elif len(digits) > 10:
        return " ".join([digits[i:i+3] for i in range(0, len(digits), 3)])
    return phone


def format_receipt_output(raw_text: str, parsed_data: dict, engine: str) -> dict:
    clean_text = clean_raw_text(raw_text)
    phone = format_phone(parsed_data.get("phone", "N/A"))

    # Add GST if available in OCR text
    gst_match = re.search(r"GST(?: INCL\.?|:)?\s*\$?(\d+\.\d+)", clean_text, re.IGNORECASE)
    gst_value = gst_match.group(1) if gst_match else "N/A"

    return {
        "Brand": parsed_data.get("brand", "N/A"),
        "Address": parsed_data.get("address", "N/A"),
        "Phone": phone,
        "Date": parsed_data.get("date", "N/A"),
        "Time": parsed_data.get("time", "N/A"),
        "Terminal": parsed_data.get("terminal", "N/A"),
        "Pump": parsed_data.get("pump", "N/A"),
        "Fuel Type": parsed_data.get("fuel_type", "N/A"),
        "Litres": parsed_data.get("litres", "N/A"),
        "Price per Litre ($)": parsed_data.get("price_per_litre", "N/A"),
        "Total ($)": parsed_data.get("total", "N/A"),
        "Payment Type": parsed_data.get("payment_type", "N/A"),
        "GST ($)": gst_value,
        "OCR Engine": engine,
        "Raw Text": clean_text
    }


@router.post("/ocr")
async def ocr_endpoint(file: UploadFile = File(...)):
    try:
        if file.content_type not in {"image/png", "image/jpeg"}:
            raise HTTPException(415, "Unsupported file type. Only PNG/JPEG allowed.")

        contents = await file.read()
        if not contents:
            raise HTTPException(400, "Uploaded file is empty")

        ocr_result = ocr_image_bytes(contents)

        if isinstance(ocr_result, dict):
            raw_text = ocr_result.get("text", "")
            ocr_engine = ocr_result.get("engine", "unknown")
        elif isinstance(ocr_result, str):
            raw_text = ocr_result
            ocr_engine = "unknown"
        else:
            raw_text = str(ocr_result)
            ocr_engine = "unknown"

        parsed_data = parse_receipt(raw_text)
        formatted_output = format_receipt_output(raw_text, parsed_data, ocr_engine)

        # Return pure JSON
        return JSONResponse(content=formatted_output)

    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(500, f"OCR processing failed: {str(e)}")
