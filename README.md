# AutoLog OCR — Step 1


## Run locally (system must have Tesseract installed)


1. Create virtualenv


```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt

2. Run the script
uvicorn app.main:app --reload --port 8000

3. Trust the endpoint
curl -X POST "http://127.0.0.1:8000/api/ocr" -F "file=@./sample_receipt.jpg"

Docker
docker build -t autolog-ocr:step1 .
docker run -p 8000:8000 autolog-ocr:step1

---


## Next actions (Step 2 candidates)
1. Add EasyOCR fallback + language autodetect
2. Add `/ocr/receipt` structured parser and tests (regex-based)
3. Add Celery async worker + `/ocr/pdf-async` with status polling
4. Add API key auth + rate limiting
5. Add S3 storage option (MinIO/localstack for dev)


Pick one and I’ll start implementing it immediately.