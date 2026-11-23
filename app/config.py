import os
import shutil

from pydantic_settings import BaseSettings, SettingsConfigDict


def _default_tesseract() -> str:
    found = shutil.which("tesseract")
    if found:
        return found
    if os.name == "nt":
        return r"C:\Program Files\Tesseract-OCR\tesseract.exe"
    return "/usr/bin/tesseract"


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env", extra="ignore")

    tesseract_cmd: str = _default_tesseract()
    face_distance_threshold: float = 0.65
    cors_origins: str = "http://localhost:5173"


settings = Settings()

# The vendored passport module reads TESSERACT_CMD straight from os.environ,
# but pydantic-settings does not export .env values there. Do it explicitly
# so the path is configured in exactly one place.
os.environ["TESSERACT_CMD"] = settings.tesseract_cmd