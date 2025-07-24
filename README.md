# AI powered document verifier


This service ingests identification documents and medical records, extracts structured patient fields using Google Gemini and Pydantic schemas, matches them, and flags inconsistencies.
Made for Aidsphere.

## Features

* OCR and PDF parsing via Tesseract and LangChain’s PDF loader
* Field extraction using LangChain + Gemini with PydanticOutputParser
* Inconsistency detection between ID and medical records
* Fully local & free-tier compatible (except Gemini API)
* Persists raw outputs, parsed JSON, and in MongoDB for auditability and later retrieval

## Prerequisites

* **Python 3.10+**
* **Tesseract OCR** installed and on your `PATH`
* **Google Gemini API Key** (set `GEMINI_API_KEY`)
* Internet access for Gemini API calls

## Installation

1. **Clone the repository**

   ```bash
   git clone <REPO_URL>
   cd <REPO_DIR>
   ```
2. **Create and activate a virtual environment**

   ```bash
   python -m venv venv
   source venv/bin/activate   # On Windows: venv\Scripts\activate
   ```
3. **Install dependencies**

   ```bash
   pip install -r requirements.txt
   ```

## Environment Variables

* `GEMINI_API_KEY`: Your Google Gemini API key
* **Optional**: If `tesseract` is not on your PATH, export:

  ```bash
  export TESSERACT_CMD="/path/to/tesseract"
  ```
* MONGO_URI: MongoDB connection string for persisting insights and embeddings (e.g., mongodb://username:password@host:port/dbname)


MongoDB Setup

You can run MongoDB locally or use MongoDB Atlas.

## Usage

Run the agent with your ID and medical document paths:

```bash
python agent_service.py \
  --id_path "/path/to/id_image_or_pdf" \
  --med_path "/path/to/medical_pdf"
```

The agent will:

1. Load & OCR/parse both files
2. Extract structured JSON with Gemini
3. Compare fields and print final JSON with `match_issues`

### Example

```bash
python agent_service.py \
  --id_path "test_data/id_image_test.png" \
  --med_path "test_data/med_doc_test.pdf"
```


## Customization

* Edit Pydantic schemas in `schemas.py` to add/remove fields
* Swap in alternative OCR/PDF loaders
* Modify or extend Tools in `agent_service.py` for new functionality

