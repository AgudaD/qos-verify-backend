import cv2
from deepface import DeepFace

from app.config import settings


def compare_faces(id_face_path: str, selfie_path: str) -> dict:
    for p in (id_face_path, selfie_path):
        if cv2.imread(p) is None:
            raise ValueError(f"Could not read image: {p}")

    result = DeepFace.verify(
        img1_path=id_face_path,
        img2_path=selfie_path,
        model_name="GhostFaceNet",
        detector_backend="retinaface",
        distance_metric="cosine",
        align=True,
        enforce_detection=True,
    )

    distance = float(result["distance"])
    verified = bool(result["verified"]) and distance <= settings.face_distance_threshold

    return {
        "distance": distance,
        "threshold": settings.face_distance_threshold,
        "verified": verified,
    }