# Multi-Language Receipt/Bill Dashboard

## Overview

The **Multi-Language Receipt/Bill Dashboard** is a modular, full-stack Python application enabling upload, OCR, structured extraction, deduplication, storage, and analytics for receipts/bills in multiple languages.  
It supports invoice parsing in **English, Hindi, Telugu, French, German, and Spanish** (and is easily extensible to others) and includes smart duplicate protection by invoice/order number or file content hash.

Built for quick deployment and maintainable as a real production or assignment-grade project, it features clean code separation, Pydantic model validation, MongoDB flexible storage, and a modern Streamlit dashboard UI.

## Features

- **Language-Aware OCR**: Supports English, Hindi, Telugu, French, Spanish, and German. Easily extended!
- **Automatic Field Extraction**: Robust recognition for invoice/order/bill/receipt number, vendor, date, total/amount, and currency in multiple languages.
- **Smart Deduplication**: Ensures receipts are only saved once, based on detected number or file hash, even if re-uploaded in a different language scan.
- **Streamlit Analytics UI**: Upload and review receipts, visualize spend by vendor/month, and export data as CSV/JSON with a single click.
- **Modular Design**: Decoupled backend modules for DB, OCR, parsing logic, and language dictionaries.

## Folder Structure

```plaintext
receipt-dashboard/
├── backend/
│   ├── __init__.py          # Python package marker
│   ├── db.py                # MongoDB connection & reset helpers
│   ├── ocr_parser.py        # OCR utilities for images and PDFs
│   ├── keywords.py          # All multi-language regex keywords ("total", "date", ...)
│   └── logic.py             # Pydantic schema, parsing, deduplication
├── frontend/
│   ├── __init__.py
│   └── app.py               # Main Streamlit dashboard/UI
├── requirements.txt         # Python dependencies
└── README.md                # Project documentation (this file)
```

## Setup Instructions

**1. Clone the repository**
```bash
git clone https://github.com/roar3691/Multi-Language-Receipt-Bill-Dashboard.git
cd Multi-Language-Receipt-Bill-Dashboard
```

**2. Install Python requirements**
```bash
pip install -r requirements.txt
```

**3. Install Tesseract OCR and Language Packs**

- **macOS:**
  ```bash
  brew install tesseract
  brew install tesseract-lang
  ```
- **Ubuntu:**
  ```bash
  sudo apt-get install tesseract-ocr
  sudo apt-get install tesseract-ocr-eng tesseract-ocr-hin tesseract-ocr-tel tesseract-ocr-fra tesseract-ocr-deu tesseract-ocr-spa
  ```
  *See [official docs](https://tesseract-ocr.github.io/tessdoc/Data-Files-in-different-versions.html) for other languages.*

**4. Configure MongoDB**
- Use [MongoDB Atlas](https://www.mongodb.com/cloud/atlas) or a local DB.
- Update your URI inside `backend/db.py` in `MONGO_URI`.

**5. Run the Streamlit Dashboard**
```bash
streamlit run frontend/app.py
```
*The app will launch at [http://localhost:8501](http://localhost:8501).*

## How It Works

- **Choose OCR Language:** Select the document language before upload (matching your scanned bill's language and Tesseract install).
- **Upload receipts/bills:** Accepts `.jpg`, `.png`, `.pdf`, and `.txt`.
- **Automatic Parsing:** Extracts all core fields using multi-language-aware regex.
- **Smart Storage:** Prevents duplicates using robust ID/hash logic.
- **Immediate Analytics:** Tables, bar/line charts, and monthly trends.
- **Export:** Download all your parsed data as CSV/JSON.

## Code Structure Details

### **backend/**
- **db.py:** Manages MongoDB connection (`receipts_collection`) and helper for table reset.
- **ocr_parser.py:** Image/PDF OCR with Tesseract, supports many languages.
- **keywords.py:** Central dictionary of regex label translations, e.g., for "total", "date", "invoice number".
- **logic.py:** Main parsing logic and field extraction, includes:
    - `parse_receipt_fields(text)`: multi-language robust parser
    - `safe_group_strip()`: prevents errors from missing regex groups
    - `ReceiptRecord`: Pydantic model for validation
    - Deduplication by invoice number or file hash

### **frontend/**
- **app.py:** Streamlit dashboard UI with multi-language OCR selection, file upload, parsed/validated data preview, analytics, and export. Imports backend modules for business logic.

## Design Choices

- **Separation of concerns:** Each backend module is testable and upgradable in isolation.
- **Regex and dictionary-driven parsing:** Easy to add new field names or languages.
- **Pydantic for validation:** Data integrity on insert.
- **Deduplication:** Critical for production or analytics environments.
- **Immediate feedback:** All user actions (upload, error, parse, export) result in instant UI updates.

## Limitations

- The demo version wipes stored receipts on each app run (change `reset_receipts()` to preserve records).
- Matching quality depends on completeness of language keyword dictionaries and OCR accuracy.
- Multi-language OCR requires Tesseract to be built/installed with the desired language data.

## Assumptions

- Invoice/order/bill/receipt number or hash is available for deduplication.
- Valid MongoDB URI and relevant database privileges are configured.
- Uploaded files are actual receipts or bills.

## Extensibility

- **New languages?** Add translations in `backend/keywords.py` and install that language pack for Tesseract.
- **New fields?** Expand `parse_receipt_fields()` and JSON/Pydantic model.
- **Run in production:** Remove `reset_receipts()` from app.py for data persistence.

## Example Usage

1. Select “Hindi” as OCR language.
2. Upload a Hindi PDF electricity bill and a Telugu supermarket receipt.
3. The table shows both, with correct fields parsed.
4. Export as CSV for further financial analysis.

## License

MIT License

## Issues and Contributions

Found an issue? Want to contribute?  
Open an issue or pull request at [GitHub Issues](https://github.com/roar3691/Multi-Language-Receipt-Bill-Dashboard/issues).
