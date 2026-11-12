# QOS NIN Verification

This repository contains a **Nigerian National Identification Number (NIN) OCR and Field Extraction Proof of Concept (PoC)** developed as part of the QOSPAY identity verification workflow.

The purpose of this project is to automatically read information from a Nigerian NIN document image and convert the detected information into structured identity data that can be used during customer onboarding and identity verification.

The solution uses:

- **PaddleOCR** for Optical Character Recognition (OCR)
- **PaddlePaddle** as the underlying deep-learning framework
- **Python** for processing OCR results
- **Regular Expressions (Regex)** for extracting expected NIN fields
- **Data Masking** for reducing exposure of sensitive information during testing

---

## What Does This Project Do?

The application accepts an image of a Nigerian NIN document and uses PaddleOCR to detect and recognize the text contained in the document.

The detected text is then processed to extract identity fields such as:

- Surname
- First Name
- Middle Name
- NIN
- Tracking ID
- Gender
- Address

Sensitive fields such as the NIN, Tracking ID, and Address are masked before being displayed in the terminal.

For example:

```bash
python nin_ocr.py nin_card.png
```

The program can produce output similar to:

```text
QOSPAY NIN OCR EXTRACTION
============================================================

EXTRACTED NIN DATA
============================================================
Surname: SAMPLE
First Name: USER
Middle Name: TEST
NIN: 123********
Tracking ID: ABC************
Gender: M
Address: Sam********************
```

---

# How It Works

The NIN processing flow is:

```text
NIN Document Image
        |
        v
PaddleOCR
        |
        v
Text Detection
        |
        v
Text Recognition
        |
        v
OCR Text Processing
        |
        v
Field Extraction
        |
        v
Sensitive Data Masking
        |
        v
Structured Identity Information
```

### 1. NIN Document Image

The application receives the path to a NIN document image.

Example:

```bash
python nin_ocr.py nin_card.png
```

### 2. OCR Processing

PaddleOCR analyzes the image and detects text regions within the NIN document.

It then performs text recognition on the detected regions.

### 3. Text Processing

The detected text is combined and processed by the Python application.

### 4. Field Extraction

Regular expressions are used to search the OCR result for expected NIN fields such as:

- Surname
- First Name
- Middle Name
- NIN
- Tracking ID
- Gender
- Address

### 5. Sensitive Data Masking

Sensitive values are masked before being displayed.

For example, an 11-digit NIN such as:

```text
12345678901
```

may be displayed as:

```text
123********
```

This reduces unnecessary exposure of sensitive identity information during testing.

---

# Project Structure

```text
qos-nin-verification/
│
├── nin_ocr.py
├── requirements.txt
├── README.md
└── .gitignore
```

Real NIN documents are intentionally **not included** in this repository.

---

# Installation

## 1. Install Python

Python must be installed on the computer.

Check whether Python is installed:

```bash
python --version
```

If Python is installed, the command should display the installed Python version.

---

## 2. Clone the Repository

Clone the repository:

```bash
git clone <repository-url>
```

Enter the project directory:

```bash
cd qos-nin-verification
```

---

## 3. Create a Virtual Environment

Create a Python virtual environment:

```bash
python -m venv .venv
```

### Windows - Git Bash

Activate the environment using:

```bash
source .venv/Scripts/activate
```

### Windows - Command Prompt

Use:

```cmd
.venv\Scripts\activate
```

### Windows - PowerShell

Use:

```powershell
.venv\Scripts\Activate.ps1
```

After activation, the terminal should show something similar to:

```text
(.venv)
```

---

## 4. Install the Dependencies

With the virtual environment activated, run:

```bash
pip install -r requirements.txt
```

The current tested environment uses:

```text
numpy==1.26.4
paddleocr==2.8.1
paddlepaddle==2.6.2
opencv-contrib-python==4.11.0.86
protobuf==3.20.2
```

### Important Dependency Note

The NumPy version is intentionally pinned to:

```text
numpy==1.26.4
```

This PaddleOCR environment was tested successfully with NumPy 1.26.4.

Upgrading to NumPy 2.x may cause compatibility problems with this version of the OCR stack.

---

# Running the Project

Unlike the passport repository, this repository does not contain a sample NIN document because NIN documents contain sensitive personal identity information.

Use a local NIN image for testing.

The general command is:

```bash
python nin_ocr.py <path-to-nin-image>
```

For example, if the image is in the current directory:

```bash
python nin_ocr.py nin_card.png
```

If the image is stored in the Downloads folder and you are using Git Bash:

```bash
python nin_ocr.py ~/Downloads/nin_card.png
```

You can also provide another image path:

```bash
python nin_ocr.py path/to/nin_card.jpg
```

---

# Expected Output

When OCR and field extraction are successful, the program should display something similar to:

```text
QOSPAY NIN OCR EXTRACTION
============================================================

EXTRACTED NIN DATA
============================================================
Surname: SAMPLE
First Name: USER
Middle Name: TEST
NIN: 123********
Tracking ID: ABC************
Gender: M
Address: Sam********************
```

The exact fields returned depend on the NIN document, image quality, OCR result, and document layout.

---

# Supported Fields

The current implementation attempts to extract:

| Field | Description |
|---|---|
| Surname | Holder's surname |
| First Name | Holder's first name |
| Middle Name | Holder's middle name |
| NIN | 11-digit National Identification Number |
| Tracking ID | NIN document tracking identifier |
| Gender | Gender value detected from the document |
| Address | Address detected from the document |

Not every field is guaranteed to be detected successfully.

---

# Sensitive Data Masking

The application masks selected sensitive information before printing it to the terminal.

Currently masked fields include:

- NIN
- Tracking ID
- Address

For example:

```text
NIN: 123********
Tracking ID: ABC************
Address: Sam********************
```

Names and gender are currently displayed normally for development and testing purposes.

Additional masking and secure handling should be implemented for production environments.

---

# Role in the QOSPAY Identity Verification Workflow

NIN OCR is one component of the broader QOSPAY identity verification Proof of Concept.

The intended architecture is:

```text
                    CUSTOMER ONBOARDING
                           |
                           v
                    Identity Document
                           |
              +------------+------------+
              |                         |
              v                         v
      Passport Processing         NIN Processing
      FastMRZ + Tesseract           PaddleOCR
              |                         |
              +------------+------------+
                           |
                           v
                  Identity Information
                           |
                           v
                   Liveness Detection
                           |
                           v
                    Face Verification
                           |
                           v
                  Verification Result
```

Each component is currently maintained as a separate PoC so that it can be developed and tested independently before integration.

---

# Related QOSPAY Identity Verification PoCs

## QOS NIN Verification

This repository.

Responsible for:

- NIN OCR
- Text recognition
- NIN field extraction
- Sensitive-data masking

## QOS Passport Verification

Responsible for:

- Passport MRZ detection
- Tesseract OCR
- Passport field extraction
- MRZ parsing and validation

## QOS Liveness Detection

Responsible for:

- Randomized active liveness challenges
- Blink detection
- Mouth-open detection
- Head movement detection
- MiniFASNet passive anti-spoofing

## QOS Face Verification

Responsible for:

- Comparing an identity-document photograph with a selfie
- DeepFace
- GhostFaceNet
- RetinaFace
- Cosine-distance face comparison

---

# Privacy and Security

NIN information is sensitive identity information.

Do **not** commit any real identity documents or customer information to this repository.

This includes:

- Real NIN images
- Customer NIN documents
- Passport images
- Customer selfies
- Biometric images
- Customer personal information
- API keys
- Passwords
- Credentials
- Production data

The `.gitignore` file blocks common image and document formats:

```text
*.jpg
*.jpeg
*.png
*.pdf
*.webp
*.tif
*.tiff
```

This helps reduce the risk of accidentally uploading identity documents to GitHub.

---

# Current Limitations

This repository is currently a **Proof of Concept / Research and Development implementation**.

Current limitations include:

- OCR accuracy depends on image quality.
- Poor lighting may reduce text-recognition accuracy.
- Blur may cause incorrect OCR results.
- Different NIN document layouts may require additional extraction rules.
- Address extraction can vary depending on OCR text ordering.
- Field labels must generally match the patterns expected by the extraction logic.
- Some fields may not be detected if OCR recognition is inaccurate.
- The system does not independently establish whether a NIN document is genuine.
- The system does not currently query an official NIN validation service.
- Broader testing is required before production deployment.

A production implementation would require additional validation, security controls, secure data handling, API integration, monitoring, error handling, and broader testing.

---

# Troubleshooting

## PaddleOCR Import Error

Make sure the virtual environment is activated:

```bash
source .venv/Scripts/activate
```

Then reinstall the requirements:

```bash
pip install -r requirements.txt
```

---

## NumPy Compatibility Problems

Check the installed NumPy version:

```bash
python -c "import numpy; print(numpy.__version__)"
```

The tested version for this project is:

```text
1.26.4
```

If necessary:

```bash
pip uninstall numpy -y
pip install numpy==1.26.4
```

---

## Check PaddleOCR Version

Run:

```bash
python -c "import paddleocr; print(paddleocr.__version__)"
```

The tested version is:

```text
2.8.1
```

---

## Image Not Found

If you receive:

```text
Image not found
```

check that the path supplied to the script is correct.

For example:

```bash
python nin_ocr.py ~/Downloads/nin_card.png
```

---

# Quick Setup

For Windows using Git Bash:

```bash
git clone <repository-url>
cd qos-nin-verification

python -m venv .venv
source .venv/Scripts/activate

pip install -r requirements.txt

python nin_ocr.py ~/Downloads/nin_card.png
```

Replace the final image path with the location of your own local test NIN document.

---

# Project Status

**Status:** Proof of Concept / Research & Development

The current implementation demonstrates that PaddleOCR can be used to extract selected identity information from a Nigerian NIN document and convert the OCR result into structured fields for potential use within the wider QOSPAY identity verification workflow.