import sys
from pathlib import Path
from app.utils import file_to_b64

_VENDOR = Path(__file__).resolve().parents[2] / "vendor" / "qos-passport-verification"
if not _VENDOR.exists():
    raise RuntimeError(f"qos-passport-verification not found at {_VENDOR}")

sys.path.insert(0, str(_VENDOR))
from passport_mrz import extract_mrz  # noqa: E402


def verify_passport(image_path: str) -> tuple[dict, str]:
    fields = extract_mrz(image_path)
    
    
    face_b64 = "" 
    
    return fields, face_b64