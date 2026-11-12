from pydantic import BaseModel


class DocumentResponse(BaseModel):
    doc_type: str
    fields: dict
    face_image_b64: str


class FaceResponse(BaseModel):
    distance: float
    threshold: float
    verified: bool


class HealthResponse(BaseModel):
    status: str