from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.routers import ocr

app = FastAPI(title="AutoLog OCR API - Step 1")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(ocr.router, prefix="/api")

@app.get("/health")
async def health():
    return {"status": "ok"}