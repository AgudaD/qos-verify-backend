import pytesseract
from fastapi import FastAPI, File, Form, HTTPException, UploadFile
from fastapi.middleware.cors import CORSMiddleware

from app.config import settings
from app.schemas import DocumentResponse, FaceResponse, HealthResponse
from app.services import face, nin, passport
from app.utils import b64_to_tempfile, bytes_to_tempfile, cleanup, is_pdf

pytesseract.pytesseract.tesseract_cmd = settings.tesseract_cmd

app = FastAPI(title="QOS Identity Verification API", version="0.1.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=[o.strip() for o in settings.cors_origins.split(",")],
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/health", response_model=HealthResponse)
def health():
    return {"status": "ok"}


@app.post("/verify/document", response_model=DocumentResponse)
async def verify_document(doc_type: str, file: UploadFile = File(...)):
    if doc_type not in ("nin", "passport"):
        raise HTTPException(400, "doc_type must be 'nin' or 'passport'")

    data = await file.read()
    suffix = ".pdf" if is_pdf(file.filename or "") else ".jpg"
    path = bytes_to_tempfile(data, suffix)
    try:
        if doc_type == "nin":
            fields, face_b64 = nin.verify_nin(path)
        else:
            fields, face_b64 = passport.verify_passport(path)
    finally:
        cleanup(path)

    return {"doc_type": doc_type, "fields": fields, "face_image_b64": face_b64}


@app.post("/verify/face", response_model=FaceResponse)
async def verify_face(
    id_face_b64: str = Form(...),
    selfie: UploadFile = File(...),
):
    if not id_face_b64:
        raise HTTPException(400, "id_face_b64 is required (from /verify/document)")

    id_path = b64_to_tempfile(id_face_b64)
    selfie_path = bytes_to_tempfile(await selfie.read())
    try:
        result = face.compare_faces(id_path, selfie_path)
    except Exception as e:
        raise HTTPException(500, f"Face comparison failed: {e}")
    finally:
        cleanup(id_path)
        cleanup(selfie_path)

    return result