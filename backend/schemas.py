from pydantic import BaseModel
import truststore, httpx
truststore.inject_into_ssl()

class DocumentRequest(BaseModel):
    text: str

class UploadDocumentRequest(BaseModel):
    text: str

class UploadDocumentResponse(BaseModel):
    session_id: str
    classification_result: dict

class ExtractionRequest(BaseModel):
    session_id: str

class ExtractionResponse(BaseModel):
    extracted_data: dict

class ChatRequest(BaseModel):
    session_id: str
    query: str

class ChatResponse(BaseModel):
    response: str
