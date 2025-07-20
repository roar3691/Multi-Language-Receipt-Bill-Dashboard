# Multi-Language Receipt/Bill Dashboard

## Overview

A full-stack application to upload, extract, and summarize receipts/bills from images and PDFs.  
Supports English, Hindi, Telugu, French, Spanish, German, etc.  
Key fields are robustly extracted using rule-based logic and OCR.  
Duplicate protection (by invoice/order/bill/receipt number or file hash).

## Setup

1. **Clone repo**

    ```
    git clone roar3691/Multi-Language-Receipt-Bill-Dashboard
    cd Multi-Language-Receipt-Bill-Dashboard
    ```

2. **Install requirements**

    ```
    pip install -r requirements.txt
    ```

3. **Install Tesseract & Language Packs**

    - macOS:
        ```
        brew install tesseract
        brew install tesseract-lang
        ```
    - Ubuntu:
        ```
        sudo apt install tesseract-ocr
        sudo apt install tesseract-ocr-eng tesseract-ocr-hin tesseract-ocr-tel ...
        ```

4. **Configure MongoDB**

    - Edit `backend/db.py` and supply your MongoDB URI.

5. **Run the Streamlit app**

    ```
    streamlit run frontend/app.py
    ```

## Design Choices / Architecture

- **Modular**: All parsing, OCR, keywords, and DB logic are separated in back-end modules.
- **Multi-language field detection**: Handles key fields (invoice no, date, total) in 6 languages.
- **Auto-dedupe and reset on each app run**.
- **Aggregations and exports** with Pandas and Streamlit UI.

## Limitations

- "Wipes" table on each run for demo/testing.
- Multi-language depends on installed Tesseract language data and keyword completeness.

## Assumptions

- Invoice/order/bill/receipt number is present; otherwise file hash is used.
- MongoDB URI is valid.
- Uploaded files are actual receipts/bills.
