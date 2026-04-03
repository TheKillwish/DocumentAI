import chromadb
from datetime import datetime
import uuid
import os
from openai import OpenAI
import truststore, httpx
truststore.inject_into_ssl()

client_openai = OpenAI(
    api_key=os.environ["OPENAI_API_KEY"].strip()
)

client = chromadb.Client()

collection = client.get_or_create_collection(
    name="documents"
)

def store_document(document_type, extracted_data):
    doc_id = str(uuid.uuid4())
    embedding = client_openai.embeddings.create(
        model="text-embedding-3-small",
        input=str(extracted_data)
    ).data[0].embedding

    collection.add(
        documents=[str(extracted_data)],
        embeddings=[embedding],
        metadatas=[{
            "document_id": doc_id,
            "document_type": document_type,
            "timestamp": str(datetime.utcnow())
        }],
        ids=[doc_id]
    )
    return doc_id

def _chunk_text(text, chunk_size=500, overlap=100):
    words = text.split()
    chunks = []
    start = 0
    while start < len(words):
        chunk = words[start:start+chunk_size]
        if chunk:
            chunks.append(" ".join(chunk))
        start += chunk_size - overlap
    return chunks

def store_session_embedding(session_id, text, document_type, classification_result):
    print(f"Saving session embedding for ID: {session_id!r}")
    chunks = _chunk_text(text)
    ids = []
    embeddings = []
    docs = []
    metadatas = []
    timestamp = str(datetime.utcnow())
    for idx, chunk in enumerate(chunks):
        chunk_id = f"{session_id}_chunk_{idx}"
        ids.append(chunk_id)
        docs.append(chunk)
        emb = client_openai.embeddings.create(
            model="text-embedding-3-small",
            input=chunk
        ).data[0].embedding
        embeddings.append(emb)
        metadatas.append({
            "session_id": session_id,
            "document_type": document_type,
            "classification_result": classification_result,
            "timestamp": timestamp,
            "text": chunk
        })
    try:
        res = collection.add(
            documents=docs,
            embeddings=embeddings,
            metadatas=metadatas,
            ids=ids
        )
        print("[DEBUG] Saved session embedding CHUNKS. ids:", ids)
        all_collection = collection.get(include=["metadatas"])
        print("[DEBUG] All IDs in collection:", all_collection.get("ids", []))
        print("[DEBUG] Collection total count:", len(all_collection.get("ids", [])))
    except Exception as e:
        print(f"[ERROR] Exception during collection.add: {e}")

def get_session_embedding(session_id):
    print(f"[DEBUG] Looking up session embedding for ID: {session_id!r}")
    try:
        results = collection.get(
            ids=[str(session_id)],
            include=["metadatas"]
        )
        print("[DEBUG] Chroma returned results:", results)
        metadatas = results.get("metadatas", [])
        if metadatas and len(metadatas) > 0:
            print("[DEBUG] Returning metadata:", metadatas[0])
            return metadatas[0]
        print("[DEBUG] No metadata found for id", session_id)
        return None
    except Exception as e:
        print(f"[ERROR] Exception getting session_id ({session_id!r}):", str(e))
        return None

def search_session_embedding(session_id, query, top_k=4):
    # Embed the user query
    query_emb = client_openai.embeddings.create(
        model="text-embedding-3-small",
        input=query
    ).data[0].embedding

    # Search chromadb for the session's relevant chunks
    results = collection.query(
        query_embeddings=[query_emb],
        n_results=top_k,
        where={"session_id": session_id}
    )
    relevant_chunks = results.get("documents", [[]])[0]
    if not relevant_chunks:
        return "No relevant context found in the document for your query."

    context = "\n\n".join(relevant_chunks)

    prompt = f"""
You are an intelligent assistant for PDF Q&A. Use ONLY the following extracted document content to answer the user's question.
Be strictly factual and cite the facts from the document text below:
-----------------------------
{context}
-----------------------------

User question:
{query}

If the answer is not clearly in the document context, reply: "Not available in the document."
"""
    completion = client_openai.chat.completions.create(
        model="gpt-4o",
        messages=[
            {"role": "system", "content": "Only use the document context provided below to answer the user."},
            {"role": "user", "content": prompt}
        ],
        temperature=0,
        max_tokens=512
    )
    return completion.choices[0].message.content
