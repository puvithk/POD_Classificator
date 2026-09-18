# POD Classificator

An automated pipeline for Proof of Delivery (POD) document extraction and rule-based classification using Qwen Vision-Language Models (VLM).

---

## 📌 Overview

The **POD Classificator** extracts key delivery metadata, verification marks (signatures, stamps, handwriting), and damage/shortage remarks from document images. It then evaluates and classifies each document into a standardized POD category with a confidence score ($0.0 - 1.0$) and reason.

---

## 🏷️ Classification Categories

The classification engine evaluates documents based on a prioritized hierarchy:

| Priority | Category | Description |
|---|---|---|
| **1** | `MANUAL_CHECK_REQUIRED` | Physical paper damage detected (tears, severe occlusion). |
| **2** | `ISSUE_POD_DAMAGED_AND_SHORT` | Both item damage and shortage recorded. |
| **3** | `ISSUE_POD_DAMAGED` | Business/goods damage recorded on the POD. |
| **4** | `ISSUE_POD_SHORT` | Short delivery / missing quantity noted. |
| **5** | `CLEAN_POD_SEAL_AND_SIGNATURE` | Fully verified with valid stamp, signature, and handwriting. |
| **6** | `CLEAN_POD_ONLY_SEAL` | Verified with company stamp/seal only. |
| **7** | `CLEAN_POD_ONLY_SIGNATURE` | Verified with receiver signature only. |
| **8** | `NO_SIGNATURE_NO_STAMP` | Missing both receiver signature and official stamp. |

---

## 📁 Project Structure

```
POD_Classificator/
├── main.py                     # Fast CLI entrypoint
├── requirements.txt            # Project dependencies
├── .env.example                # Environment variables template
├── .gitignore                  # Git ignore rules
│
├── configs/
│   └── config.yaml             # Model and pipeline configurations
│
├── prompts/
│   └── pod_extraction_prompt.txt # Prompt template for VLM extraction
│
├── src/
│   ├── main.py                 # Core package entrypoint
│   ├── enum/
│   │   └── pod_category.py     # POD category enum definitions
│   ├── model/
│   │   └── qwen_client.py      # Qwen Vision-Language API client
│   ├── pipeline/
│   │   ├── preprocessing.py    # Image preprocessing utilities
│   │   ├── extraction.py       # VLM extraction & JSON parsing
│   │   ├── classification.py   # Rule-based classification engine
│   │   └── pipeline.py         # End-to-end orchestration
│   ├── schemas/
│   │   └── pod_schema.py       # Pydantic schemas for data validation
│   └── utils/
│       ├── json_parser.py      # Response cleaning & JSON parsing
│       └── logger.py           # Standardized logger
│
├── data/
│   ├── sample/                 # Sample input images
│   └── outputs/                # Generated output predictions
│
├── evaluation/
│   ├── evaluate.py             # Evaluation benchmark runner
│   └── metrics.py              # Precision, recall, and accuracy metrics
│
└── tests/
    ├── test_classifier.py      # Classifier unit tests
    └── test_schema.py          # Schema validation tests
```

---

## 🚀 Setup & Installation

### 1. Clone & Install Dependencies

```bash
git clone https://github.com/puvithk/POD_Classificator.git
cd POD_Classificator
pip install -r requirements.txt
```

### 2. Environment Variables

Copy `.env.example` to `.env` and configure your Qwen API credentials:

```bash
cp .env.example .env
```

Edit `.env`:
```env
QWEN_API_KEY=your_dashscope_api_key_here
QWEN_API_BASE=https://dashscope.aliyuncs.com/compatible-mode/v1
MODEL_NAME=qwen-vl-max
```

---

## 💻 Usage

### Run on Default Document (`test.jpg`)
```bash
python main.py
```

### Run on a Custom Image
```bash
python main.py path/to/document.jpg
```

### Run with Custom Image and Prompt
```bash
python main.py path/to/document.jpg prompts/pod_extraction_prompt.txt
```

---

## 📊 Sample Output

Running the pipeline returns the classification report as formatted JSON:

```json
{
  "cnNumber": "CN-987654321",
  "hasSignature": true,
  "hasStamp": true,
  "hasHandwriting": true,
  "imageQualityPassed": true,
  "remarksText": null,
  "deliveryDate": "2026-09-18",
  "categoryReason": "Clean POD without any issues with signature and stamp",
  "categoryScore": 0.945,
  "podCategory": "CLEAN_POD_SEAL_AND_SIGNATURE",
  "limit_exceed": false
}
```

---