import base64
import binascii
import os
import tempfile
from pathlib import Path


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
    # Accept both raw base64 and "data:image/...;base64,<payload>"
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
    """Delete any number of temp files; ignores None and missing files."""
    for path in paths:
        if not path:
            continue
        try:
            os.unlink(path)
        except OSError:
            pass


def is_pdf(filename: str) -> bool:
    return Path(filename or "").suffix.lower() == ".pdf"