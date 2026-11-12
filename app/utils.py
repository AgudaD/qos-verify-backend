import base64
import os
import tempfile
from pathlib import Path


def bytes_to_tempfile(data: bytes, suffix: str = ".jpg") -> str:
    tmp = tempfile.NamedTemporaryFile(delete=False, suffix=suffix)
    tmp.write(data)
    tmp.close()
    return tmp.name


def b64_to_tempfile(b64: str, suffix: str = ".jpg") -> str:
    return bytes_to_tempfile(base64.b64decode(b64), suffix)


def file_to_b64(path: str) -> str:
    with open(path, "rb") as f:
        return base64.b64encode(f.read()).decode("ascii")


def cleanup(path: str) -> None:
    try:
        os.unlink(path)
    except OSError:
        pass


def is_pdf(filename: str) -> bool:
    return Path(filename or "").suffix.lower() == ".pdf"