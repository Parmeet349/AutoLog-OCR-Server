import re
from typing import Dict, Any, Optional

def parse_receipt(text: str) -> Dict[str, Any]:
    """
    Extracts structured data from OCR receipt text.
    Returns a dictionary with vendor, date, litres, price_per_litre, total_amount.
    """

    data = {
        "vendor": None,
        "date": None,
        "litres": None,
        "price_per_litre": None,
        "total_amount": None
    }

    # --- Vendor (first line assumption) ---
    lines = [line.strip() for line in text.split("\n") if line.strip()]
    if lines:
        data["vendor"] = lines[0]

    # --- Date extraction (YYYY-MM-DD or DD/MM/YYYY or MM-DD-YYYY) ---
    date_pattern = re.search(r"(\d{4}[-/]\d{2}[-/]\d{2}|\d{2}[-/]\d{2}[-/]\d{4})", text)
    if date_pattern:
        data["date"] = date_pattern.group(1)

    # --- Litres / Gallons ---
    litres_pattern = re.search(r"(\d+\.\d+|\d+)\s*(L|Litres|Liters|Gallons)", text, re.IGNORECASE)
    if litres_pattern:
        data["litres"] = float(litres_pattern.group(1))

    # --- Price per litre ---
    ppl_pattern = re.search(r"(\d+\.\d+)\s*/?\s*(L|litre|liter)", text, re.IGNORECASE)
    if ppl_pattern:
        data["price_per_litre"] = float(ppl_pattern.group(1))

    # --- Total amount (look for $ or CAD or TOTAL) ---
    total_pattern = re.search(r"(TOTAL|Amount|CAD|USD)[^\d]*(\d+\.\d{2})", text, re.IGNORECASE)
    if total_pattern:
        data["total_amount"] = float(total_pattern.group(2))

    return data
