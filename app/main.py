import os
import pytesseract
from fastapi import FastAPI, File, Form, HTTPException, UploadFile
from fastapi.middleware.cors import CORSMiddleware

from app.config import settings
from app.schemas import DocumentResponse, FaceResponse, HealthResponse
from app.utils import b64_to_tempfile, bytes_to_tempfile, cleanup, is_pdf
from app.services.liveness import LivenessService

# Initialize the liveness engine (loads PyTorch models on startup)
liveness_engine = LivenessService()

pytesseract.pytesseract.tesseract_cmd = settings.tesseract_cmd

app = FastAPI(title="QOS Identity Verification API", version="0.1.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=[o.strip() for o in settings.cors_origins.split(",")],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"], 
)

@app.get("/")
def read_root():
    return {"status": "ok", "message": "QOS Verification API is running"}

@app.get("/health", response_model=HealthResponse)
def health():
    return {"status": "ok"}

@app.post("/verify/document", response_model=DocumentResponse)
async def verify_document(doc_type: str, file: UploadFile = File(...)):
    if doc_type not in ("nin", "passport"):
        raise HTTPException(400, "doc_type must be 'nin' or 'passport'")

    if doc_type == "nin":
        from app.services import nin
        verifier = nin.verify_nin
    else:
        from app.services import passport
        verifier = passport.verify_passport

    data = await file.read()
    suffix = ".pdf" if is_pdf(file.filename or "") else ".jpg"
    path = bytes_to_tempfile(data, suffix)
    try:
        fields, face_b64 = verifier(path)
    finally:
        cleanup(path)

    return {"doc_type": doc_type, "fields": fields, "face_image_b64": face_b64}



@app.post("/verify/face", response_model=FaceResponse)
async def verify_face(
    id_face_b64: str = Form(...),
    selfie: UploadFile = File(...),
):
    if not id_face_b64:
        raise HTTPException(400, "id_face_b64 is required")

    from app.services import face

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


# --- SERVER-SIDE LIVENESS ENDPOINT ---
@app.post("/verify/liveness")
async def verify_liveness(file: UploadFile = File(...)):
    """
    Receives the final frame from the frontend liveness check.
    Runs MiniFASNet server-side to ensure it's not a printed photo or screen.
    """
    data = await file.read()
    
    try:
        result = liveness_engine.check_liveness(data)
        if not result.get("is_real"):
            raise HTTPException(400, f"Liveness failed: {result.get('error', 'Spoof detected')}")
        
        return {"status": "SUCCESS", "message": "Liveness confirmed on server", "score": result["score"]}
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(500, f"Liveness engine error: {e}")