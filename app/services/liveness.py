import os
import cv2
import numpy as np
import importlib.util
from pathlib import Path

# Resolve paths
BASE_DIR = Path(__file__).resolve().parents[2]  # qos-verify-backend/
VENDOR_LIVENESS_PATH = BASE_DIR / "vendor" / "qos-liveness-detection" / "minifasnet_liveness.py"

if not VENDOR_LIVENESS_PATH.exists():
    raise FileNotFoundError(f"minifasnet_liveness.py not found at {VENDOR_LIVENESS_PATH}")

# Load module by path
spec = importlib.util.spec_from_file_location("minifasnet_liveness", VENDOR_LIVENESS_PATH)
minifasnet_module = importlib.util.module_from_spec(spec)
spec.loader.exec_module(minifasnet_module)

MiniFASNetLiveness = minifasnet_module.MiniFASNetLiveness


class LivenessService:
    _instance = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(LivenessService, cls).__new__(cls)
            print("Initializing MiniFASNet Anti-Spoofing models...")
            cls._instance.engine = MiniFASNetLiveness()
        return cls._instance

    def check_liveness(self, image_bytes: bytes) -> dict:
        # 1. Decode image
        np_arr = np.frombuffer(image_bytes, np.uint8)
        frame = cv2.imdecode(np_arr, cv2.IMREAD_COLOR)
        if frame is None:
            return {"is_real": False, "error": "Invalid image format"}

        # 2. Detect face bbox with OpenCV Haar Cascade
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        face_cascade = cv2.CascadeClassifier(
            cv2.data.haarcascades + "haarcascade_frontalface_default.xml"
        )
        faces = face_cascade.detectMultiScale(gray, 1.1, 4)

        if len(faces) == 0:
            return {"is_real": False, "error": "No face detected"}

        # 3. Take the largest face
        x, y, w, h = max(faces, key=lambda r: r[2] * r[3])
        bbox = [x, y, x + w, y + h]

        # 4. Run MiniFASNet
        result = self.engine.predict(frame, bbox)

        return {
            "is_real": result["label_name"] == "REAL",
            "score": result["score"],
            "label": result["label_name"],
        }