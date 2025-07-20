import re
import hashlib
from datetime import datetime
from pydantic import BaseModel, Field
from typing import Optional
from .keywords import KEYWORDS

class ReceiptRecord(BaseModel):
    invoice_number: Optional[str] = Field(default="")
    vendor: str = Field(..., max_length=100)
    date: str = Field(..., min_length=4)
    amount: float = Field(..., ge=0)
    currency: Optional[str] = Field(default="INR", max_length=8)
    category: Optional[str] = Field(default="")
    file_hash: Optional[str] = Field(default="")

def keyword_regex(lang_keywords, after=r"[:\s#]*([\w\-\/]+)"):
    return r"(?i)\b(" + "|".join(lang_keywords) + r")" + after

def file_hash(file):
    pos = file.tell()
    file.seek(0)
    hash_val = hashlib.sha256(file.read()).hexdigest()
    file.seek(pos)
    return hash_val

def parse_receipt_fields(text):
    currency = "INR"
    if re.search(r"(₹|INR)", text): currency = "INR"
    elif "$" in text and "USD" in text: currency = "USD"
    elif "$" in text: currency = "USD"
    elif "€" in text: currency = "EUR"
    elif "EUR" in text: currency = "EUR"

    lines = [line.strip() for line in text.splitlines() if line.strip()]
    full_text = ' '.join(lines)

    # Invoice/Order/Bill/Receipt Number (multi-language)
    invoice_number = ""
    invno_regex = keyword_regex(KEYWORDS["invoice_number"])
    m = re.search(invno_regex, full_text)
    if m: invoice_number = m.group(2).strip()

    # Vendor
    vendor = None
    for regex in [
        r"(?i)invoice issued by[ :]*([A-Za-z0-9 .,&()\\-]+)",
        r"(?i)issued by[ :]*([A-Za-z0-9 .,&()\\-]+)",
        r"(?i)sold by[ :]*([A-Za-z0-9 .,&()\\-]+)"
    ]:
        for line in lines:
            m = re.search(regex, line)
            if m:
                vendor = m.group(1).strip()[:100]
                break
        if vendor: break
    if not vendor:
        for line in lines:
            if "amazon.in" in line.lower():
                vendor = line.strip()
                break
    if not vendor:
        vendor = lines[0][:35] if lines else ""

    # Date
    date = None
    date_line_val = ""
    date_regex = keyword_regex(KEYWORDS["date"], after=r"[:\s#]*([A-Za-z0-9, \-/]+)")
    m = re.search(date_regex, full_text)
    if m: date_line_val = m.group(2).strip()
    if date_line_val:
        for fmt in ("%d %b %Y", "%d %B %Y", "%d %b %y", "%d %B %y", "%d-%m-%Y", "%d/%m/%Y", "%Y-%m-%d", "%a %d %b %Y"):
            try:
                dt = datetime.strptime(date_line_val.replace(",", ""), fmt)
                date = dt.strftime("%Y-%m-%d")
                break
            except:
                continue
    if not date:
        date_pattern2 = r"(\d{1,2} [A-Za-z]{3,9} \d{2,4})|(\d{4}-\d{2}-\d{2})|(\d{2}/\d{2}/\d{2,4})"
        matches = re.findall(date_pattern2, full_text)
        potential_dates = [item for tup in matches for item in tup if item]
        for dt_str in potential_dates:
            for fmt in ("%d %b %Y", "%d %B %Y", "%Y-%m-%d", "%d/%m/%Y"):
                try:
                    dt = datetime.strptime(dt_str, fmt)
                    date = dt.strftime("%Y-%m-%d")
                    break
                except:
                    continue
            if date: break
    if not date: date = ""

    # Amount/Total (multi-language aware)
    amount = None
    total_regex = re.compile(r"(?i)\b(" + "|".join(KEYWORDS["total"]) + r")\b")
    total_lines = []
    for i, line in enumerate(lines):
        if total_regex.search(line) and not re.search(
            r"(?i)before tax|due date|before GST|taxable", line
        ):
            total_lines.append((i, line))
    candidates = []
    for idx, line in total_lines:
        found = re.findall(r"([0-9]+(?:\.[0-9]{2}))", line)
        if found: candidates.extend(found)
        for offset in [1, 2]:
            if idx + offset < len(lines):
                found2 = re.findall(r"([0-9]+(?:\.[0-9]{2}))", lines[idx+offset])
                if found2: candidates.extend(found2)
    if not candidates:
        fallback_totals = re.findall(r"(?i)total[^\\d]*([0-9]+(?:\.[0-9]{2}))", full_text)
        candidates.extend(fallback_totals)
    try:
        amount = float(max([float(x) for x in candidates])) if candidates else 0.0
    except:
        amount = 0.0

    return {
        "invoice_number": invoice_number,
        "vendor": vendor,
        "date": date,
        "amount": amount,
        "currency": currency,
        "category": ""
    }
