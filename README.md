# POD Classification

Proof of Delivery (POD) classification and information extraction pipeline using Qwen vision-language models.

## Project Structure

```
pod-classification/
│
├── README.md
├── requirements.txt
├── .env.example
├── .gitignore
│
├── configs/
│   └── config.yaml
│
├── prompts/
│   └── pod_extraction_prompt.txt
│
├── src/
│   ├── __init__.py
│   ├── main.py
│   │
│   ├── model/
│   │   ├── __init__.py
│   │   └── qwen_client.py
│   │
│   ├── pipeline/
│   │   ├── __init__.py
│   │   ├── preprocessing.py
│   │   ├── extraction.py
│   │   └── classification.py
│   │
│   ├── schemas/
│   │   ├── __init__.py
│   │   └── pod_schema.py
│   │
│   └── utils/
│       ├── __init__.py
│       ├── json_parser.py
│       └── logger.py
│
├── data/
│   ├── sample/
│   └── outputs/
│
├── evaluation/
│   ├── evaluate.py
│   └── metrics.py
│
├── tests/
│   ├── test_classifier.py
│   └── test_schema.py
│
└── report/
    └── POD_Classification_Report.pdf
```

## Setup & Installation

1. **Clone repository & install dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

2. **Configure environment**:
   ```bash
   cp .env.example .env
   # Edit .env and set your QWEN_API_KEY
   ```

3. **Run pipeline**:
   ```bash
   python src/main.py
   ```
