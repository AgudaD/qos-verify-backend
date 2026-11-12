from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env", extra="ignore")

    tesseract_cmd: str = r"C:\Program Files\Tesseract-OCR\tesseract.exe"
    face_distance_threshold: float = 0.65
    cors_origins: str = "http://localhost:5173"


settings = Settings()