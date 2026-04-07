import json
import os
from openai import OpenAI
import truststore, httpx
truststore.inject_into_ssl()

client_openai = OpenAI(
    api_key=os.environ["OPENAI_API_KEY"].strip()
)

import json

def extract_fields(doc_type, pdf_text):

    prompt = f"""
Extract the key fields based on the document type.

Return ONLY the relevant fields for the detected document type using the EXACT field names defined below.
If any field is not present, return null.

Respond STRICTLY in VALID JSON.
Do NOT include markdown, explanation, or extra text.

FIELD DEFINITIONS:

Invoice:
invoice_number
vendor_name
invoice_date
total_amount
currency

Resume:
name
email
phone
skills
experience

Receipt:
merchant_name
transaction_date
total_amount
payment_method
currency

Payslip:
employee_name
employee_id
gross_pay
net_pay
month
designation

Bank Statement:
bank_name
account_holder
opening_balance
closing_balance
statement_period

Offer Letter:
candidate_name
position
employer_name
salary
start_date

Generic:
"Extract most Suitable data points based on the file"

Document Type: {doc_type}

Content:
\"\"\"
{pdf_text}
\"\"\"

Return JSON format EXACTLY like this (use correct fields based on document type):

Example for Payslip:
{{
  "document_type": "Payslip",
  "employee_name": "...",
  "employee_id": "...",
  "gross_pay": "...",
  "net_pay": "...",
  "month": "...",
  "designation": "..."
}}

Example for Invoice:
{{
  "document_type": "Invoice",
  "invoice_number": "...",
  "vendor_name": "...",
  "invoice_date": "...",
  "total_amount": "...",
  "currency": "..."
}}
"""

    try:
        response = client_openai.chat.completions.create(
            model="gpt-4o",
            messages=[
                {"role": "system", "content": "You are a strict JSON extractor."},
                {"role": "user", "content": prompt}
            ],
            temperature=0
        )

        output = response.choices[0].message.content.strip()

        # ✅ Clean markdown if present
        if "```" in output:
            output = output.replace("```json", "").replace("```", "").strip()

        print("[DEBUG LLM OUTPUT]:", output)

        json_output = json.loads(output)

        return json_output

    except Exception as e:
        print("[ERROR] Extraction failed:", str(e))

        # ✅ fallback response
        return {
            "document_type": doc_type,
            "primary_field_1": None,
            "primary_field_2": None,
            "primary_field_3": None,
            "primary_field_4": None,
            "primary_field_5": None
        }