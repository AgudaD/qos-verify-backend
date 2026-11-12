from paddleocr import PaddleOCR
import re
import os
import sys


def mask_keep_first(text, visible_chars=3, mask_char="*"):
    """
    Show only the first few characters of sensitive values.
    """
    if not text:
        return text

    if len(text) <= visible_chars:
        return text

    return text[:visible_chars] + mask_char * (len(text) - visible_chars)


def extract_field(pattern, text):
    match = re.search(pattern, text, re.IGNORECASE)
    return match.group(1).strip() if match else None


def extract_fields(image_path: str) -> dict:
    """
    Run PaddleOCR on the NIN image and return extracted fields as a dict.

    Keys are snake_case so the API can consume them directly.
    Missing fields are omitted. Returns {"status": "FAILED", ...} on hard failure.
    """
    if not os.path.exists(image_path):
        return {"status": "FAILED", "error": f"Image not found: {image_path}"}

    ocr = PaddleOCR(
        use_angle_cls=True,
        lang="en",
        show_log=False,
    )

    try:
        result = ocr.ocr(image_path, cls=True)
    except Exception as e:
        return {"status": "FAILED", "error": f"OCR ERROR: {e}"}

    # Collect OCR text
    all_text = []
    for line in result:
        if not line:
            continue
        for word_info in line:
            all_text.append(word_info[1][0])

    full_text = " ".join(all_text)

    data = {}

    # --------------------------------------------------
    # NAME FIELDS
    # --------------------------------------------------
    surname = extract_field(r"Surname:\s*([A-Z'-]+)", full_text)
    first_name = extract_field(r"First Name:\s*([A-Z'-]+)", full_text)
    middle_name = extract_field(r"Middle Name:\s*([A-Z'-]+)", full_text)

    if surname:
        data["surname"] = surname
    if first_name:
        data["first_name"] = first_name
    if middle_name:
        data["middle_name"] = middle_name

    # --------------------------------------------------
    # NIN
    # --------------------------------------------------
    nin = extract_field(r"\b(\d{11})\b", full_text)
    if nin:
        data["nin"] = nin

    # --------------------------------------------------
    # TRACKING ID
    # --------------------------------------------------
    tracking_id = extract_field(r"Tracking ID:\s*([A-Z0-9]+)", full_text)
    if tracking_id:
        data["tracking_id"] = tracking_id

    # --------------------------------------------------
    # GENDER
    # --------------------------------------------------
    gender = extract_field(r"Gender:\s*([MF])", full_text)
    if gender:
        data["gender"] = gender.upper()

    # --------------------------------------------------
    # ADDRESS
    # Capture Address only until another known NIN field.
    # --------------------------------------------------
    address_match = re.search(
        r"Address:\s*(.*?)"
        r"(?=\s+(?:Gender|Tracking ID|"
        r"Date of Birth|DOB|State of Origin|"
        r"LGA|Issue Date|Issued Date|Expiry Date)\s*:|$)",
        full_text,
        re.IGNORECASE,
    )
    if address_match:
        data["address"] = address_match.group(1).strip(" ,")

    if not data:
        return {"status": "FAILED", "error": "No expected NIN fields were extracted."}

    data["status"] = "SUCCESS"
    return data


def main():
    if len(sys.argv) < 2:
        print("Usage:")
        print("python nin_ocr.py <nin_image>")
        print()
        print("Example:")
        print("python nin_ocr.py nin_card.png")
        return

    image_path = sys.argv[1]

    print("\nQOSPAY NIN OCR EXTRACTION")
    print("=" * 60)

    data = extract_fields(image_path)

    if data.get("status") == "FAILED":
        print(f"\nERROR: {data.get('error')}")
        return

    print("\nEXTRACTED NIN DATA")
    print("=" * 60)

    # Preserve the original CLI presentation (masking, Title Case labels).
    # The dict returned by extract_fields() is unmasked for API use.
    display_map = {
        "surname": "Surname",
        "first_name": "First Name",
        "middle_name": "Middle Name",
        "nin": "NIN",
        "tracking_id": "Tracking ID",
        "gender": "Gender",
        "address": "Address",
    }
    sensitive_keys = {"nin", "tracking_id", "address"}

    for key, label in display_map.items():
        value = data.get(key)
        if not value:
            continue
        if key in sensitive_keys:
            value = mask_keep_first(value, visible_chars=3)
        print(f"{label}: {value}")


if __name__ == "__main__":
    main()