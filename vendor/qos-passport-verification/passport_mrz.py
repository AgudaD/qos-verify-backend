from fastmrz import FastMRZ
import json
import os
import sys


# Read Tesseract path from the environment so the backend's .env can override it.
# Falls back to the original hardcoded Windows path.
TESSERACT_PATH = os.environ.get(
    "TESSERACT_CMD",
    r"C:\Program Files\Tesseract-OCR\tesseract.exe",
)


def extract_mrz(image_path: str) -> dict:
    """
    Detect + parse passport MRZ from an image.

    Returns the same dict that the CLI previously printed, with a 'status' key
    added (SUCCESS / FAILED). On hard failure, returns {"status": "FAILED", "error": ...}
    so the backend can surface a message instead of a 500.
    """
    if not os.path.exists(image_path):
        return {"status": "FAILED", "error": f"Image not found: {image_path}"}

    fast_mrz = FastMRZ(tesseract_path=TESSERACT_PATH)

    try:
        result = fast_mrz.get_details(image_path)
    except Exception as e:
        return {
            "status": "FAILED",
            "error": f"{type(e).__name__}: {e}",
        }

    if not isinstance(result, dict) or not result:
        return {"status": "FAILED", "error": "MRZ extraction returned no data"}

    result.setdefault("status", "SUCCESS")
    return result


def main():
    if len(sys.argv) < 2:
        print("Usage:")
        print("python passport_mrz.py <passport_image>")
        print()
        print("Example:")
        print("python passport_mrz.py passport.jpg")
        return

    image_path = sys.argv[1]

    print("\nQOSPAY PASSPORT MRZ EXTRACTION")
    print("=" * 60)

    data = extract_mrz(image_path)

    if data.get("status") == "FAILED":
        print("\nERROR:")
        print(data.get("error"))
        return

    print(json.dumps(data, indent=4))


if __name__ == "__main__":
    main()