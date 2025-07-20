import streamlit as st
import pandas as pd

from backend.db import receipts_collection, reset_receipts
from backend.ocr_parser import extract_text_from_image, extract_text_from_pdf
from backend.logic import parse_receipt_fields, ReceiptRecord, file_hash
from pydantic import ValidationError

st.title("🧾 Multi-Language Receipt/Bill Dashboard")
st.markdown("""
All receipts are reset to zero at app launch.  
Receipts are auto-saved if unique by invoice/order/bill/receipt number (if detected) **or** file hash.
""")

ocr_lang = st.selectbox(
    "Select OCR Language (ensure Tesseract language pack is installed):",
    options=[
        ("English (eng)", "eng"),
        ("Hindi (hin)", "hin"),
        ("Telugu (tel)", "tel"),
        ("French (fra)", "fra"),
        ("Spanish (spa)", "spa"),
        ("German (deu)", "deu")
    ],
    format_func=lambda x: x[0],
    index=0
)[1]

reset_receipts()

uploaded_files = st.file_uploader(
    "Upload receipts (.jpg, .png, .pdf, .txt)",
    type=["jpg", "png", "pdf", "txt"],
    accept_multiple_files=True,
)

if uploaded_files:
    for uploaded in uploaded_files:
        text = ""
        curr_file_hash = file_hash(uploaded)
        try:
            if uploaded.type in ["image/jpeg", "image/png"]:
                text = extract_text_from_image(uploaded, language=ocr_lang)
            elif uploaded.type == "application/pdf":
                text = extract_text_from_pdf(uploaded, language=ocr_lang)
            elif uploaded.type == "text/plain":
                uploaded.seek(0)
                text = uploaded.read().decode("utf-8")
            else:
                st.warning(f"Unsupported file: {uploaded.name}", icon="⚠️")
                continue
        except Exception as e:
            st.error(f"OCR error for {uploaded.name}: {e}")
            continue

        data = parse_receipt_fields(text)
        data["file_hash"] = curr_file_hash

        dedup_query = (
            {"invoice_number": data["invoice_number"]}
            if data["invoice_number"]
            else {"file_hash": curr_file_hash}
        )

        if not receipts_collection.find_one(dedup_query):
            try:
                record = ReceiptRecord(**data)
                receipts_collection.insert_one(record.model_dump())
                st.success(f"Auto-saved extracted data for: {uploaded.name}")
            except ValidationError as e:
                st.error(f"❌ Data validation error for {uploaded.name}:\n{e.json()}")
            except Exception as e:
                st.error(f"❌ Failed to save {uploaded.name}: {e}")
        else:
            st.info(f"Duplicate detected for {uploaded.name}: not added again.")
        st.subheader(f"Auto-Parsed Data for {uploaded.name}")
        st.table(pd.DataFrame([data]))
        st.write("OCR/Text Preview:", text[:800] + '...' if len(text) > 800 else text)

st.markdown("---")

try:
    receipts = list(receipts_collection.find())
    for r in receipts:
        r["_id"] = str(r["_id"])
except Exception as e:
    receipts = []
    st.error(f"Error fetching receipts: {e}")

if receipts:
    df = pd.DataFrame(receipts)
    if "file_hash" in df:
        df = df.drop(columns=["file_hash"])
    if "date" in df.columns:
        df["date"] = pd.to_datetime(df["date"], errors="coerce")
    st.write("### All Receipts", df)
    st.download_button("Export CSV", df.to_csv(index=False), file_name="receipts.csv", mime="text/csv")
    st.download_button("Export JSON", df.to_json(orient="records"), file_name="receipts.json", mime="application/json")
    if "amount" in df.columns and len(df["amount"].dropna()) > 0:
        st.bar_chart(df, x="vendor", y="amount")
        if "date" in df.columns:
            df_valid_dates = df[df["date"].notna()]
            if not df_valid_dates.empty:
                st.line_chart(df_valid_dates.set_index("date")["amount"].sort_index())
    if "date" in df.columns and not df.empty:
        df_month = df.dropna(subset=["date"]).copy()
        if not df_month.empty:
            monthly_spend = df_month.set_index("date").resample('ME')["amount"].sum()
            st.write("#### Monthly Spend Trend")
            st.line_chart(monthly_spend)
else:
    st.info("No receipts found in the database yet.")
