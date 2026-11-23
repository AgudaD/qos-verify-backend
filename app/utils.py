import base64
import binascii
import os
import tempfile
from pathlib import Path
import fitz  # PyMuPDF

def bytes_to_tempfile(data: bytes, suffix: str = ".jpg") -> str:
    if not data:
        raise ValueError("Empty file")
    tmp = tempfile.NamedTemporaryFile(delete=False, suffix=suffix)
    try:
        tmp.write(data)
    finally:
        tmp.close()
    return tmp.name

def b64_to_tempfile(b64: str, suffix: str = ".jpg") -> str:
    if b64.startswith("data:") and "," in b64:
        b64 = b64.split(",", 1)[1]
    try:
        data = base64.b64decode(b64, validate=True)
    except (binascii.Error, ValueError):
        raise ValueError("Invalid base64 image data")
    return bytes_to_tempfile(data, suffix)

def file_to_b64(path: str) -> str:
    with open(path, "rb") as f:
        return base64.b64encode(f.read()).decode("ascii")

def cleanup(*paths: str | None) -> None:
    for path in paths:
        if not path:
            continue
        try:
            os.unlink(path)
        except OSError:
            pass

def is_pdf(filename: str) -> bool:
    return Path(filename or "").suffix.lower() == ".pdf"

def pdf_to_image(pdf_path: str) -> str:
    """Convert the first page of a PDF to a high-res JPEG for OCR."""
    doc = fitz.open(pdf_path)
    page = doc.load_page(0)
    pix = page.get_pixmap(dpi=300) # High DPI for good OCR
    out_path = pdf_path + "_converted.jpg"
    pix.save(out_path)
    doc.close()
    return out_path