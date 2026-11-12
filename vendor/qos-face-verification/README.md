# QOS Face Verification

Face verification proof-of-concept for the QOS Identity Verification solution.

The system compares a face extracted from an identity document with a selfie or another facial image to determine whether both images belong to the same person.

## Overview

The current implementation uses:

- **DeepFace** – Face verification framework
- **GhostFaceNet** – Face recognition/embedding model
- **RetinaFace** – Face detection and alignment
- **Cosine Distance** – Measures similarity between face embeddings
- **PyMuPDF** – Converts PDF identity documents to images for processing

The current project is designed as a benchmark/test implementation before integration into the complete QOS Identity Verification workflow.

## Verification Flow

```text
Identity Document / ID Photo
            |
            v
     Face Detection
       (RetinaFace)
            |
            v
      Face Alignment
            |
            v
   Face Embedding Generation
      (GhostFaceNet)
            |
            v
      Cosine Distance
            |
            v
     Match / No Match
```

## Project Structure

```text
qos-face-verification/
│
├── benchmark_test.py
├── requirements.txt
├── README.md
├── .gitignore
│
├── your_id_image_or_pdf
│
└── test_images/
    ├── same_person_1.jpg
    ├── same_person_2.jpg
    ├── different_person_1.jpg
    └── different_person_2.jpg
```

Identity documents and test images are excluded from Git and must be added locally.

## Setup

### 1. Clone the repository

```bash
git clone <repository-url>
cd qos-face-verification
```

### 2. Create a virtual environment

```bash
python -m venv .venv
```

### 3. Activate the environment

Windows Git Bash:

```bash
source .venv/Scripts/activate
```

Windows Command Prompt:

```cmd
.venv\Scripts\activate
```

### 4. Install dependencies

```bash
pip install -r requirements.txt
```

## Adding Your Test Data

Identity documents and face images are not included in this repository for privacy and security reasons.

### 1. Add Your Reference ID

Place your identity document in the project root directory.

Supported reference ID formats:

- `.jpg`
- `.jpeg`
- `.png`
- One-page `.pdf`

The identity document can have any filename.

For example:

```text
passport.jpg
nin.pdf
my_id.png
```

### 2. Set the ID Filename

Open `benchmark_test.py` and locate:

```python
ID_IMAGE = "nin.pdf"
```

Change this value to match the filename of the identity document you placed in the project directory.

For example, if your file is:

```text
passport.jpg
```

change the code to:

```python
ID_IMAGE = "passport.jpg"
```

For a PDF:

```python
ID_IMAGE = "my_nin.pdf"
```

You do not need to rename your identity document to match the original filename in the script. Simply update `ID_IMAGE`.

### 3. Add Comparison Images

Create a `test_images` directory if it does not already exist:

```bash
mkdir -p test_images
```

Place the facial images you want to compare against the identity document inside this folder.

For example:

```text
test_images/
├── same_person_1.jpg
├── same_person_2.jpg
├── different_person_1.jpg
└── different_person_2.jpg
```

The comparison images do **not** have to use these exact filenames.

The benchmark automatically processes all `.jpg`, `.jpeg`, and `.png` files inside the `test_images` directory.

### PDF Identity Documents

The project supports one-page identity documents supplied as PDFs.

PyMuPDF is used to render the PDF page as an image before face detection and verification.

The temporary converted image is automatically removed after the benchmark completes.

## Running the Benchmark

Once you have:

1. Added your identity document
2. Updated `ID_IMAGE` in `benchmark_test.py`
3. Added your comparison images to `test_images/`

Run:

```bash
python benchmark_test.py
```

The system will compare the face detected in the reference identity document against every supported image inside `test_images/`.

Example result:

```text
Image                   Distance      Threshold      Verified
----------------------------------------------------------------
same_person_1.jpg       0.355190      0.650000       True
same_person_2.jpg       0.438518      0.650000       True
different_person_1.jpg  0.655799      0.650000       False
different_person_2.jpg  0.764949      0.650000       False
```

Lower cosine distance indicates greater facial similarity.

A result below the model threshold is classified as a match, while a result above the threshold is classified as a non-match.

## Current Configuration

```text
Face Verification: DeepFace
Recognition Model: GhostFaceNet
Face Detector: RetinaFace
Distance Metric: Cosine
Face Alignment: Enabled
```

## Intended Identity Verification Flow

This component is intended to form part of the wider QOS Identity Verification pipeline:

```text
Document Extraction
        |
        v
Liveness / Anti-Spoofing
        |
        v
Face Verification
        |
        v
Final Verification Result
```

The face-verification component compares the user's live/selfie image with the facial image obtained from the submitted identity document.

## Testing

Testing should include:

- Same-person images under different lighting conditions
- Different-person images
- Similar-looking individuals or relatives
- Different camera devices
- Different facial angles
- Identity document photographs
- Passport photographs
- NIN photographs
- PDF identity documents
- Different image resolutions and quality levels

## Privacy and Security

Do **not** commit real identity documents, NIN documents, passports, selfies, or other personal biometric data to this repository.

The `.gitignore` file excludes local test images and identity documents from Git tracking.

Each tester should use only identity documents and biometric images they are authorized to use for testing.

## Current Status

This repository contains a proof-of-concept/benchmark implementation.

It is intended for internal testing and evaluation and should not currently be treated as a production-ready identity verification system.
