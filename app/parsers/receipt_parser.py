import re
from dateutil import parser as dateparser
from rapidfuzz import process

# ----- Predefined constants -----
GAS_STATION_BRANDS = [
    "Petro-Canada", "Shell", "Esso", "Canadian Tire",
    "Costco Gas", "Ultramar", "Husky", "Pioneer", "Mobil"
]

FUEL_TYPES = ["Regular", "Premium", "Diesel", "Unleaded", "Super"]

PAYMENT_KEYWORDS = {
    "credit": "Credit Card",
    "debit": "Debit",
    "cash": "Cash",
    "visa": "Credit Card",
    "mastercard": "Credit Card",
    "amex": "Credit Card"
}

# ----- Utility Functions -----
def fuzzy_match(text, choices, score_cutoff=50):
    if not isinstance(text, str) or not text.strip():
        return "N/A"
    match = process.extractOne(text, choices, score_cutoff=score_cutoff)
    return match[0] if match else "N/A"

def detect_brand(lines):
    for line in lines:
        clean_line = re.sub(r"[^A-Z\- ]", "", line.upper())
        brand = fuzzy_match(clean_line, [b.upper() for b in GAS_STATION_BRANDS], score_cutoff=50)
        if brand != "N/A":
            return brand.title()
    return "N/A"

def extract_date(text):
    date_patterns = [
        r"\b\d{1,2}[-/]\d{1,2}[-/]\d{2,4}\b",
        r"\b\d{4}[-/]\d{1,2}[-/]\d{1,2}\b"
    ]
    for pattern in date_patterns:
        match = re.search(pattern, text)
        if match:
            try:
                dt = dateparser.parse(match.group(), dayfirst=True, fuzzy=True)
                return dt.strftime("%Y-%m-%d")
            except Exception:
                continue
    return "N/A"

def extract_phone(text):
    phone_match = re.search(r"\(?\d{3}\)?[-.\s]?\d{3}[-.\s]?\d{4}", text)
    return phone_match.group() if phone_match else "N/A"

def extract_payment(text):
    text_lower = text.lower()
    for key, value in PAYMENT_KEYWORDS.items():
        if key in text_lower:
            return value
    return "N/A"

def parse_receipt(ocr_text) -> dict:
    if not isinstance(ocr_text, str):
        try:
            ocr_text = str(ocr_text)
        except Exception:
            ocr_text = ""

    lines = [line.strip() for line in ocr_text.splitlines() if line.strip()]
    full_text = " ".join(lines)

    data = {
        "brand": detect_brand(lines),
        "address": "N/A",
        "phone": extract_phone(full_text),
        "date": extract_date(full_text),
        "time": "N/A",
        "terminal": "N/A",
        "pump": "N/A",
        "fuel_type": "N/A",
        "litres": "N/A",
        "price_per_litre": "N/A",
        "total": "N/A",
        "payment_type": extract_payment(full_text)
    }

    # Address detection
    for line in lines:
        if any(word in line for word in ["Ave", "St", "Rd", "Blvd", "Drive", "Ontario", "QC", "AB", "BC"]):
            data["address"] = line
            break

    # Terminal
    term_match = re.search(r"TERMINAL[:\s]*#?\s*(\d+)", full_text, re.IGNORECASE)
    if term_match:
        data["terminal"] = term_match.group(1)

    # Pump
    pump_match = re.search(r"PUMP[:\s]*#?\s*(\d+)", full_text, re.IGNORECASE)
    if pump_match:
        data["pump"] = pump_match.group(1)

    # Fuel type
    for line in lines:
        fuel = fuzzy_match(line, FUEL_TYPES)
        if fuel != "N/A":
            data["fuel_type"] = fuel
            break

    # Litres, Price per litre, Total
    for line in lines:
        numbers = re.findall(r"\d+\.\d+", line)
        if len(numbers) >= 3:
            data["litres"] = numbers[0]
            data["price_per_litre"] = numbers[1]
            data["total"] = numbers[2]
            break

    # Time detection
    time_match = re.search(r"([01]?\d|2[0-3]):[0-5]\d", full_text)
    if time_match:
        data["time"] = time_match.group()

    return data
