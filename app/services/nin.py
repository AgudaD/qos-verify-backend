def verify_nin(image_path: str) -> tuple[dict, str]:
    # TEMPORARY FOR CLOUD DEMO: PaddleOCR requires >3GB RAM.
    # We return a clean error message instead of crashing the 512MB server.
    return {
        "status": "FAILED",
        "error": "NIN extraction is disabled on the cloud demo due to memory limits. Please use a Passport or run the NIN demo locally."
    }, ""