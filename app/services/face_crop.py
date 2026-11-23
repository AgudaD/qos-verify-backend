import cv2
import os
from retinaface import RetinaFace


def crop_face(image_path: str) -> str | None:
    img = cv2.imread(image_path)
    if img is None:
        return None

    h, w = img.shape[:2]
    detect_path = image_path

    # Upscale small images so RetinaFace can detect small passport faces
    if max(h, w) < 1600:
        scale = 1600 / max(h, w)
        img = cv2.resize(img, (int(w * scale), int(h * scale)), interpolation=cv2.INTER_CUBIC)
        detect_path = image_path + "_upscaled.jpg"
        cv2.imwrite(detect_path, img)

    try:
        faces = RetinaFace.detect_faces(detect_path)
    finally:
        if detect_path != image_path:
            try: os.remove(detect_path)
            except: pass

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