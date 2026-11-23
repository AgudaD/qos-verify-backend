
import sys
from pathlib import Path
from app.services.face_crop import crop_face
from app.utils import file_to_b64

_VENDOR = Path(__file__).resolve().parents[2] / "vendor" / "qos-nin-verification"
if not _VENDOR.exists():
    raise RuntimeError(f"qos-nin-verification not found at {_VENDOR}")

sys.path.insert(0, str(_VENDOR))
from nin_ocr import extract_fields  # noqa: E402

def verify_nin(image_path: str) -> tuple[dict, str]:
    fields = extract_fields(image_path)
    face_path = crop_face(image_path)
    face_b64 = file_to_b64(face_path) if face_path else ""
    return fields, face_b64