import os
from openai import OpenAI
import truststore, httpx
import json
truststore.inject_into_ssl()

client_openai = OpenAI(
    api_key=os.environ["OPENAI_API_KEY"].strip()
)

def classify_document(pdf_text):
    print("pdf:",pdf_text)

    prompt = f"""
You are an intelligent document classifier.

Classify the document into ONLY ONE of the following types:

1.Resume
2.Invoice
3.Receipt
4.Payslip
5.Bank Statement
6.Offer Letter
7.Generic

Respond ONLY in JSON:

{{
 "document_title":"",
 "document_summary:"",
 "document_type":"",
 "confidence_score":""
}}

Content:
\"\"\"
{pdf_text}
\"\"\"
"""
    print("propmt:",prompt)
    response = client_openai.chat.completions.create(
        model="gpt-4o",
        messages=[
            {"role":"system","content":"You are a document classification AI"},
            {"role":"user","content":prompt}
        ],
        temperature=0
    )
    print("response:",json.loads(response.choices[0].message.content.strip("```json\n").strip("\n```")))

    return json.loads(response.choices[0].message.content.strip("```json\n").strip("\n```"))
