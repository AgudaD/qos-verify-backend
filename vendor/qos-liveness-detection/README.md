# QOS Liveness Detection

Liveness detection and anti-spoofing proof-of-concept for the QOS Identity Verification solution.

The system combines randomized active liveness challenges with passive facial anti-spoofing to help determine whether the person interacting with the camera is physically present.

## Overview

The current implementation combines:

- **MediaPipe** – Facial landmark detection
- **OpenCV** – Webcam capture and image processing
- **Active Liveness Challenges** – Blink, mouth-open, and head-movement actions
- **Randomized Challenge Sequences** – Randomizes the actions requested from the user
- **MiniFASNet** – Secondary passive anti-spoofing check
- **PyTorch** – Runs the MiniFASNet models

MiniFASNet source files and the required model weights are included directly in this repository.

## Liveness Flow

```text
Webcam / Live Face
        |
        v
Face Landmark Detection
     (MediaPipe)
        |
        v
Randomized Active Challenge
        |
        +---- Blink
        |
        +---- Mouth Open
        |
        +---- Head Movement
        |
        v
Challenge Validation
        |
        v
MiniFASNet Passive
 Anti-Spoofing Check
        |
        v
Final Liveness Result
```

## Active Liveness

The active liveness component generates randomized challenges involving:

- Blinking
- Opening the mouth
- Turning the head

The user must perform the requested actions in the required sequence.

The current implementation includes:

- Randomized challenge generation
- Ordered action validation
- Exact blink-count validation
- Mouth-open detection
- Head-movement detection
- Neutral head calibration
- Challenge timing
- Landmark-based head movement detection
- Secondary yaw-based head-pose support

## Passive Anti-Spoofing

After the active liveness challenge is successfully completed, MiniFASNet performs a secondary passive anti-spoofing check.

The current implementation combines predictions from two models:

```text
2.7_80x80_MiniFASNetV2.pth
4_0_0_80x80_MiniFASNetV1SE.pth
```

MiniFASNet produces a passive classification of:

```text
REAL
or
FAKE
```

The final prototype result combines the active challenge result with the passive anti-spoofing result.

## Project Structure

```text
qos-liveness-detection/
│
├── LivenessDetection_random_challenges.py
├── minifasnet_liveness.py
├── requirements.txt
├── README.md
├── .gitignore
│
└── minifasnet/
    │
    ├── resources/
    │   ├── anti_spoof_models/
    │   │   ├── 2.7_80x80_MiniFASNetV2.pth
    │   │   └── 4_0_0_80x80_MiniFASNetV1SE.pth
    │   │
    │   └── detection_model/
    │       ├── deploy.prototxt
    │       └── Widerface-RetinaFace.caffemodel
    │
    └── src/
        ├── anti_spoof_predict.py
        ├── generate_patches.py
        ├── utility.py
        ├── data_io/
        └── model_lib/
```

The MiniFASNet source and required model files are included in the repository, so a separate MiniFASNet project is not required.

## Setup

### 1. Clone the Repository

```bash
git clone <repository-url>
cd qos-liveness-detection
```

### 2. Create a Virtual Environment

```bash
python -m venv .venv
```

### 3. Activate the Environment

Windows Git Bash:

```bash
source .venv/Scripts/activate
```

Windows Command Prompt:

```cmd
.venv\Scripts\activate
```

### 4. Install Dependencies

```bash
pip install -r requirements.txt
```

The first installation may take some time because the project includes dependencies such as MediaPipe, OpenCV and PyTorch.

## Running the Liveness Test

Run:

```bash
python LivenessDetection_random_challenges.py
```

The application will initialize the facial landmark and MiniFASNet models and display the available challenge modes.

Example:

```text
Initializing MiniFASNet anti-spoofing models...
MiniFASNet: READY

Choose my liveness detection challenge:

1. RANDOM Challenge (all categories)
2. Blink Detection with Head Movement - 20 random challenges
3. Mouth Open with Head Movement - 20 random challenges
4. End Test
```

Select a challenge and follow the instructions displayed by the application.

## Example Result

A successful test may produce output similar to:

```text
============================================================
LIVENESS VERIFICATION
============================================================

ACTIVE PASS:
sequence=TURN RIGHT -> BLINK EXACTLY 1

Running MiniFASNet...

MiniFASNet: REAL

FINAL RESULT: PERSON IS LIKELY REAL
============================================================
```

The exact MiniFASNet confidence score will vary between tests.

## How the Two Checks Work Together

The prototype uses two complementary liveness approaches:

```text
        ACTIVE LIVENESS
Randomized facial challenges
              |
              v
         Active Pass
              |
              v
       PASSIVE LIVENESS
    MiniFASNet anti-spoofing
              |
              v
    Final Liveness Decision
```

Active liveness checks whether the user can respond to dynamically requested facial actions.

MiniFASNet then provides an additional passive anti-spoofing classification.

A successful active challenge alone does not automatically mean that the complete liveness verification has passed.

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

The face-verification component can subsequently compare the user's live/selfie image with the facial image obtained from the submitted identity document.

## Testing

The prototype should be evaluated under different conditions, including:

- Different users
- Different lighting conditions
- Different webcams and cameras
- Different distances from the camera
- Different facial angles
- Users wearing glasses
- Printed photograph attempts
- Faces displayed on another screen
- Prerecorded video/replay attempts

Both successful and failed attempts should be recorded during broader evaluation to help identify false accepts and false rejects.

## Limitations

This repository contains a proof-of-concept and is not currently a production-ready biometric security system.

Passing both active and passive checks should not be interpreted as proof that every spoofing technique can be detected.

MiniFASNet is used as an additional anti-spoofing signal rather than as the sole liveness mechanism.

The system requires broader testing across users, devices, lighting conditions and representative presentation attacks before production deployment.

## Privacy and Security

Do **not** commit captured facial images, videos, identity documents, or other personal biometric information to this repository.

Testers should only use biometric data they are authorized to use.

## Current Status

The current prototype supports:

- Randomized active liveness challenges
- Blink detection
- Mouth-open detection
- Head-movement detection
- Ordered challenge validation
- Challenge timing
- MiniFASNet passive anti-spoofing
- Webcam-based testing

This implementation is intended for internal QOS testing, research and further development.