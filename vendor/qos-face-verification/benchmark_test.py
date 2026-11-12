import os
import time
import fitz  # PyMuPDF
from deepface import DeepFace

ID_IMAGE = "nin.pdf"
TEST_FOLDER = "test_images"
TEMP_PDF_IMAGE = "_temp_id_page.png"


def prepare_id_image(file_path):
    if not os.path.exists(file_path):
        raise FileNotFoundError(f"ID file not found: {file_path}")

    extension = os.path.splitext(file_path)[1].lower()

    if extension in (".jpg", ".jpeg", ".png"):
        print(f"\nUsing image ID: {file_path}")
        return file_path

    if extension == ".pdf":
        print(f"\nOpening one-page PDF ID: {file_path}")

        pdf = fitz.open(file_path)

        try:
            page_count = len(pdf)

            if page_count != 1:
                raise ValueError(
                    f"Expected a one-page ID PDF, but found {page_count} pages."
                )

            page = pdf[0]
            pix = page.get_pixmap(matrix=fitz.Matrix(3, 3), alpha=False)
            pix.save(TEMP_PDF_IMAGE)

            print(f"PDF converted to image: {TEMP_PDF_IMAGE}")
            return TEMP_PDF_IMAGE

        finally:
            pdf.close()

    raise ValueError(
        "Unsupported ID format. Use .jpg, .jpeg, .png, or a one-page .pdf"
    )


print("=" * 70)
print("       QOSPAY - GhostFaceNet Face Matching Benchmark")
print("=" * 70)

try:
    ID_IMAGE_FOR_MATCHING = prepare_id_image(ID_IMAGE)
except Exception as e:
    print(f"\nERROR preparing ID: {e}")
    raise SystemExit(1)

print("\nLoading GhostFaceNet...")
load_start = time.perf_counter()

DeepFace.build_model("GhostFaceNet")

load_time = time.perf_counter() - load_start
print(f"Model loaded in: {load_time:.2f} seconds")

if not os.path.isdir(TEST_FOLDER):
    print(f"\nTest folder not found: {TEST_FOLDER}")
    raise SystemExit(1)

images = [
    filename
    for filename in os.listdir(TEST_FOLDER)
    if filename.lower().endswith((".jpg", ".jpeg", ".png"))
]

if not images:
    print("\nNo images found in test_images/")
    raise SystemExit(1)

print(f"\nFound {len(images)} test images.\n")

results = []

for filename in sorted(images):
    image_path = os.path.join(TEST_FOLDER, filename)

    print("-" * 70)
    print(f"Testing: {filename}")

    start_time = time.perf_counter()

    try:
        result = DeepFace.verify(
            img1_path=ID_IMAGE_FOR_MATCHING,
            img2_path=image_path,
            model_name="GhostFaceNet",
            detector_backend="retinaface",
            distance_metric="cosine",
            enforce_detection=True,
            align=True,
        )

        elapsed = time.perf_counter() - start_time

        distance = result["distance"]
        threshold = result["threshold"]
        verified = result["verified"]

        results.append({
            "filename": filename,
            "distance": distance,
            "threshold": threshold,
            "verified": verified,
            "time": elapsed,
        })

        print(f"Distance : {distance:.6f}")
        print(f"Threshold: {threshold:.6f}")
        print(f"Match    : {verified}")
        print(f"Time     : {elapsed:.3f} seconds")

    except Exception as e:
        elapsed = time.perf_counter() - start_time

        results.append({
            "filename": filename,
            "distance": None,
            "threshold": None,
            "verified": False,
            "time": elapsed,
            "error": str(e),
        })

        print(f"ERROR: {e}")

print("\n")
print("=" * 70)
print("                         SUMMARY")
print("=" * 70)

print(
    f"{'IMAGE':<30}"
    f"{'DISTANCE':<12}"
    f"{'THRESHOLD':<12}"
    f"{'MATCH':<10}"
    f"{'TIME':<10}"
)

print("-" * 70)

for r in results:
    if r["distance"] is not None:
        print(
            f"{r['filename']:<30}"
            f"{r['distance']:<12.6f}"
            f"{r['threshold']:<12.6f}"
            f"{str(r['verified']):<10}"
            f"{r['time']:<10.2f}"
        )
    else:
        print(
            f"{r['filename']:<30}"
            f"{'ERROR':<12}"
            f"{'-':<12}"
            f"{'False':<10}"
            f"{r['time']:<10.2f}"
        )

print("=" * 70)

if ID_IMAGE.lower().endswith(".pdf") and os.path.exists(TEMP_PDF_IMAGE):
    try:
        os.remove(TEMP_PDF_IMAGE)
    except OSError:
        pass
