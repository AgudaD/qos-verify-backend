import cv2
from retinaface import RetinaFace


def crop_face(image_path: str) -> str | None:
    """Detect the largest/first face in the ID card and save a crop."""
    img = cv2.imread(image_path)
    if img is None:
        return None

    faces = RetinaFace.detect_faces(img)
    if not isinstance(faces, dict) or not faces:
        return None

    first = next(iter(faces.values()))
    x1, y1, x2, y2 = first["facial_area"]
    h, w = img.shape[:2]
    pad = 10
    crop = img[max(0, y1 - pad):min(h, y2 + pad), max(0, x1 - pad):min(w, x2 + pad)]
    if crop.size == 0:
        return None

    out = image_path + "_face.jpg"
    cv2.imwrite(out, crop)
    return out