import os
import uuid
import json
from fastapi import FastAPI, HTTPException, UploadFile, File
from fastapi.responses import JSONResponse
import requests
import truststore, httpx
truststore.inject_into_ssl()
from schemas import (
    UploadDocumentResponse,
    ExtractionRequest,
    ExtractionResponse,
    ChatRequest,
    ChatResponse,
)
from vector_store import store_session_embedding, get_session_embedding, search_session_embedding
from vector_store import collection,client_openai,client
from classifier import classify_document
from extractor import extract_fields
import certifi
import io
import pytesseract

import asyncio

os.environ['SSL_CERT_FILE']=certifi.where()

# For PDF text extraction
from PyPDF2 import PdfReader
from pdf2image import convert_from_path
import pytesseract
from PIL import Image
from fastapi.middleware.cors import CORSMiddleware
origins = [
    "http://localhost:4200",   # Angular (Vite)
    "http://127.0.0.1:5173",
]



UPLOAD_FOLDER = "uploads"
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,  # or ["*"] for dev
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


def extract_text_from_pdf(file_path):
    try:
        import fitz  # PyMuPDF
        import base64
        from openai import OpenAI
        from concurrent.futures import ThreadPoolExecutor, as_completed

        client = OpenAI()
        doc = fitz.open(file_path)

        # -------------------------
        # 🧠 LOCAL MERGE FUNCTION
        # -------------------------
        def merge_locally(text, visual):
            combined = (text or "").strip() + "\n\n" + (visual or "").strip()

            lines = combined.splitlines()
            seen = set()
            result = []

            for line in lines:
                clean = line.strip()
                key = clean.lower()
                if clean and key not in seen:
                    seen.add(key)
                    result.append(clean)

            return "\n".join(result)

        # -------------------------
        # 🚀 PAGE PROCESSOR
        # -------------------------
        def process_page(page_number):
            page = doc[page_number]

            # TEXT extraction
            text_content = page.get_text("text") or ""

            # IMAGE detection
            image_list = page.get_images(full=True)
            has_images = len(image_list) > 0

            visual_content = ""

            # 🔥 SMART OCR CONDITION (cost + speed optimized)
            if has_images and len(text_content.strip()) < 800:

                pix = page.get_pixmap(matrix=fitz.Matrix(1.2, 1.2))
                img_bytes = pix.tobytes("png")

                img_base64 = base64.b64encode(img_bytes).decode()

                try:
                    response = client.responses.create(
                        model="gpt-4o",
                        input=[
                            {
                                "role": "user",
                                "content": [
                                    {
                                        "type": "input_text",
                                        "text": """
Extract meaningful structured information from this document image.

Focus on:
- tables (convert to readable format)
- charts/graphs (summarize insights)
- scanned text
- important numbers

Do NOT repeat normal paragraph text.
Keep output clean and structured.
"""
                                    },
                                    {
                                        "type": "input_image",
                                        "image_url": f"data:image/png;base64,{img_base64}"
                                    }
                                ]
                            }
                        ],
                        max_output_tokens=1200
                    )

                    visual_content = response.output_text or ""

                except Exception as e:
                    print(f"OCR ERROR (page {page_number}):", str(e))

            # 🔥 MERGE
            return merge_locally(text_content, visual_content)

        # -------------------------
        # ⚡ PARALLEL EXECUTION
        # -------------------------
        final_text = ""
        results = {}

        with ThreadPoolExecutor(max_workers=3) as executor:
            futures = {
                executor.submit(process_page, i): i
                for i in range(len(doc))
            }

            for future in as_completed(futures):
                page_number = futures[future]
                try:
                    results[page_number] = future.result()
                except Exception as e:
                    print(f"PAGE ERROR {page_number}:", str(e))
                    results[page_number] = ""

        # -------------------------
        # 📄 ORDERED OUTPUT
        # -------------------------
        for i in range(len(doc)):
            final_text += f"\n\n--- PAGE {i+1} ---\n\n"
            final_text += results.get(i, "")

        return final_text.strip()

    except Exception as e:
        print("PDF EXTRACTION ERROR:", str(e))
        return ""
# def extract_text_from_pdf(file_path):
#     try:
#         import fitz  # PyMuPDF
#         import base64
#         from openai import OpenAI

#         client = OpenAI()
#         doc = fitz.open(file_path)

#         final_text = ""

#         for page_number, page in enumerate(doc):

#             # -------------------------
#             # 🧾 1. Extract TEXT layer
#             # -------------------------
#             text_content = page.get_text("text") or ""

#             # -------------------------
#             # 🖼️ 2. Detect images
#             # -------------------------
#             image_list = page.get_images(full=True)
#             has_images = len(image_list) > 0

#             visual_content = ""

#             # -------------------------
#             # 🤖 3. AI Vision for visuals
#             # -------------------------
#             if has_images:
#                 pix = page.get_pixmap(matrix=fitz.Matrix(2, 2))
#                 img_bytes = pix.tobytes("png")
#                 img_base64 = base64.b64encode(img_bytes).decode()

#                 response = client.responses.create(
#                     model="gpt-4o",
#                     input=[
#                         {
#                             "role": "user",
#                             "content": [
#                                 {
#                                     "type": "input_text",
#                                     "text": """
# You are analyzing a document page.

# Extract ONLY meaningful structured information from visual elements such as:
# - tables
# - charts/graphs (summarize key insights)
# - scanned sections
# - logos, stamps (if relevant)

# Rules:
# - Do NOT repeat plain paragraph text already visible
# - Convert tables into readable structured format
# - Summarize graphs into key insights (e.g. trends, totals)
# - Keep output clean and human-readable
# """
#                                 },
#                                 {
#                                     "type": "input_image",
#                                     "image_url": f"data:image/png;base64,{img_base64}"
#                                 }
#                             ]
#                         }
#                     ],
#                     max_output_tokens=1500
#                 )

#                 visual_content = response.output_text or ""

#             # -------------------------
#             # 🧠 4. SMART MERGE USING AI
#             # -------------------------
#             merge_response = client.responses.create(
#                 model="gpt-4o",
#                 input=f"""
# You are given two sources from the same document page:

# 1. Extracted text:
# {text_content}

# 2. Visual analysis (tables, charts, OCR):
# {visual_content}

# Task:
# - Combine both into ONE clean, structured output
# - Remove duplicates
# - Preserve meaning
# - Keep important numbers and facts
# - Format tables clearly
# - Keep it concise but complete

# Output clean readable content only.
# """,
#                 max_output_tokens=1500
#             )

#             page_output = merge_response.output_text or ""

#             final_text += f"\n\n--- PAGE {page_number + 1} ---\n\n"
#             final_text += page_output.strip()

#         return final_text.strip()

#     except Exception as e:
#         print("PDF EXTRACTION ERROR:", str(e))
#         return ""
def deduplicate_text(text):
    lines = text.splitlines()
    seen = set()
    unique_lines = []

    for line in lines:
        clean = line.strip()
        if clean and clean.lower() not in seen:
            seen.add(clean.lower())
            unique_lines.append(clean)

    return "\n".join(unique_lines)

# Health Check API
@app.get("/")
def home():
    # url="https://api.openai.com/v1/models"
    url="https://google.com/"
    r=requests.get(url)
    api_key=os.environ["OPENAI_API_KEY"].strip()
    return {"message": "Backend Running Successfully","open_api_key":api_key,"status":r.status_code}

# OpenAI test API
@app.post("/openai-test")
async def openai_test(query: str = "Say hello, OpenAI!"):
    from openai import OpenAI
    import os
    try:
        client = OpenAI(api_key=os.environ["OPENAI_API_KEY"].strip())
        resp = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[
                {"role": "system", "content": "Quick test for OpenAI API."},
                {"role": "user", "content": query}
            ],
            temperature=0
        )
        return {"result": resp.choices[0].message.content}
    except Exception as e:
        return {"error": str(e)}

# Upload PDF API
@app.post("/upload-pdf", response_model=UploadDocumentResponse)
async def upload_pdf(file: UploadFile = File(...)):
    if not file.filename.lower().endswith(".pdf"):
        raise HTTPException(status_code=400, detail="Only PDF files are allowed.")
    
    session_id = str(uuid.uuid4())
    save_path = os.path.join(UPLOAD_FOLDER, f"{session_id}_{file.filename}")
    content = await file.read()

    with open(save_path, "wb") as f:
        f.write(content)

    # Try simple text extraction first
    text= extract_text_from_pdf(save_path)
    if not text or not text.strip():
        raise HTTPException(status_code=422, detail="Could not extract usable text from PDF.")

    # Classify document
    classification_json = classify_document(text)
    try:
        print("AMAN")
        classification_result = dict(classification_json)
        print(classification_result)
        doc_type = classification_result.get("document_type", "Generic")
        print(doc_type)
    except Exception:
        raise HTTPException(status_code=500, detail="Classification failed")

    # Store embedding/session info
    store_session_embedding(
        session_id=session_id,
        text=text,
        document_type=doc_type,
        classification_result=str(classification_result)
    )
    return UploadDocumentResponse(
        session_id=session_id,
        classification_result=classification_result
    )

# Extraction API: extract info for given session using per-type prompt
from fastapi import HTTPException

@app.post("/api/v1/extract", response_model=ExtractionResponse)
async def extract_data(req: ExtractionRequest):

    session_id = req.session_id or "current_session_id_placeholder"

    # ✅ Step 1: Create query embedding (generic extraction query)
    query_text = "Extract key structured fields from this document"

    query_embedding = client_openai.embeddings.create(
        model="text-embedding-3-small",
        input=query_text
    ).data[0].embedding

    # ✅ Step 2: Fetch most relevant chunks (RAG)
    results = collection.query(
        query_embeddings=[query_embedding],
        n_results=5,
        where={"session_id": session_id},
        include=["documents", "metadatas"]
    )

    documents = results.get("documents", [[]])[0]
    metadatas = results.get("metadatas", [[]])[0]

    if not documents:
        raise HTTPException(status_code=404, detail="Embedding/session not found")

    # ✅ Step 3: Combine relevant chunks only
    context_text = " ".join(documents)

    # ✅ Step 4: Get doc_type from metadata
    doc_type = "Generic"
    if metadatas and len(metadatas) > 0:
        doc_type = metadatas[0].get("document_type", "Generic")

    # ✅ Step 5: Extract fields
    extracted = extract_fields(doc_type, context_text)

    return ExtractionResponse(extracted_data=extracted)

# Chat API: chat based on session's embedding
@app.post("/chat", response_model=ChatResponse)
async def chat(req: ChatRequest):
    chat_result = search_session_embedding(session_id=req.session_id, query=req.query)
    return ChatResponse(response=chat_result)
