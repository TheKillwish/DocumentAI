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
        # Try extracting text directly
        reader = PdfReader(file_path)
        text = ''
        for page in reader.pages:
            page_text = page.extract_text()
            if page_text:
                text += page_text
        if text.strip():  # Regular PDF with extractable text
            return text, "text"
        # Fallback to OCR
        return None, "image"
    except Exception:
        return None, "image"

def ocr_text_from_pdf(file_path):
    # Convert PDF to images and apply OCR
    images = convert_from_path(file_path)
    text = ''
    for img in images:
        text += pytesseract.image_to_string(img)
    return text

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
    raw_text, nature = extract_text_from_pdf(save_path)

    if nature == "text" and raw_text and raw_text.strip():
        text = raw_text
        extraction_method = "standard"
    else:
        # Fallback to OCR
        text = ocr_text_from_pdf(save_path)
        extraction_method = "ocr"
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
