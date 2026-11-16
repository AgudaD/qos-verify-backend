import os
import sys
import cv2
import numpy as np

MINIFASNET_DIR = os.path.abspath(
    os.path.join(os.path.dirname(__file__), "minifasnet")
)

if MINIFASNET_DIR not in sys.path:
    sys.path.insert(0, MINIFASNET_DIR)

from src.anti_spoof_predict import AntiSpoofPredict
from src.generate_patches import CropImage
from src.utility import parse_model_name


class MiniFASNetLiveness:

    def __init__(self):
        self.model_dir = os.path.join(
            MINIFASNET_DIR,
            "resources",
            "anti_spoof_models"
        )

        self.models = [
            os.path.join(
                self.model_dir,
                "2.7_80x80_MiniFASNetV2.pth"
            ),
            os.path.join(
                self.model_dir,
                "4_0_0_80x80_MiniFASNetV1SE.pth"
            ),
        ]

        for model_path in self.models:
            if not os.path.exists(model_path):
                raise FileNotFoundError(
                    f"MiniFASNet model not found: {model_path}"
                )

        # AntiSpoofPredict uses relative paths internally,
        # so initialize it from the MiniFASNet project directory.
        original_dir = os.getcwd()

        try:
            os.chdir(MINIFASNET_DIR)
            self.predictor = AntiSpoofPredict(0)
        finally:
            os.chdir(original_dir)

        self.cropper = CropImage()

    def predict(self, image, bbox):

        prediction = np.zeros(3, dtype=np.float32)

        for model_path in self.models:

            model_name = os.path.basename(model_path)

            h_input, w_input, model_type, scale = parse_model_name(
                model_name
            )

            param = {
                "org_img": image,
                "bbox": bbox,
                "scale": scale,
                "out_w": w_input,
                "out_h": h_input,
                "crop": True,
            }

            if scale is None:
                param["crop"] = False

            face_crop = self.cropper.crop(**param)

            # AntiSpoofPredict.predict() also uses relative model paths,
            # so temporarily switch to the MiniFASNet project directory.
            original_dir = os.getcwd()

            try:
                os.chdir(MINIFASNET_DIR)
                relative_model_path = os.path.relpath(
                    model_path,
                    MINIFASNET_DIR
                )

                model_prediction = self.predictor.predict(
                    face_crop,
                    relative_model_path
                )
            finally:
                os.chdir(original_dir)

            prediction += model_prediction[0]

        probabilities = prediction / len(self.models)

        label = int(np.argmax(probabilities))

        if label == 1:
            label_name = "REAL"
        else:
            label_name = "FAKE"

        score = float(probabilities[label])

        return {
            "label": label,
            "label_name": label_name,
            "score": score,
            "probabilities": probabilities,
        }
