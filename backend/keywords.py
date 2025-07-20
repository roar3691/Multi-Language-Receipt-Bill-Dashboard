KEYWORDS = {
    "invoice_number": [
        r"invoice[\s_\-]*(number|no|id)",    # English
        r"order[\s_\-]*(id|number)", 
        r"bill[\s_\-]*no", 
        r"receipt[\s_\-]*no",
        r"booking[\s_\-]*id",
        r"reference[\s_\-]*number",
        r"इनवॉइस\s*संख्या",                  # Hindi
        r"चालान\s*संख्या",
        r"आदेश\s*संख्या",
        r"ఫైనల్[\s_\-]*ఇన్వాయిస్[\s_\-]*(నంబర్|సంఖ్య)",  
        r"ఇన్వాయిస్[\s_\-]*(నంబర్|సంఖ్య)",
        r"పరిచయం\s*సంఖ్య",
        r"num[eé]ro[\s_\-]*(de)?[\s_\-]*facture",         
        r"num[eé]ro[\s_\-]*(de)?[\s_\-]*r[eé]ception",
        r"rechnungsnummer",
        r"bestellnummer",
        r"nummer[\s_\-]*de[\s_\-]*factura",
        r"n[uú]mero[\s_\-]*de[\s_\-]*pedido",
    ],
    "total": [
        r"grand total", r"total amount", r"amount payable", r"total",
        r"montant total", "importe total", "gesamt",
        r"कुल", r"फाइनल टोटल", r"మొత్తం", r"ఫైనల్ ఆటో టల్"
    ],
    "date": [
        r"date of issue", r"statement date", r"bill date", r"order placed", r"date", r"issue date",
        r"दिनांक", r"जारी\s*दिनांक", r"తేదీ", r"విడుదల[\s_-]*తేదీ",
        r"ausstellungsdatum",
        r"fecha[\s_\-]*(de)?[\s_\-]*(emisi[oó]n|factura|pedido|orden)",
        r"date[\s_\-]*d[eé][\s_\-]*facture"
    ]
}
