🚀 DocuIntel AI

AI-Powered Document Intelligence Platform

DocuIntel AI is a full-stack application that enables users to upload documents (PDFs), automatically classify them, extract key structured data, and interact with them using an AI-powered chat interface.

---

✨ Features

- 📄 Upload and process PDF documents
- 🧠 AI-based document classification (Invoice, Payslip, Resume, etc.)
- 📊 Intelligent data extraction (dynamic + structured JSON output)
- 💬 Chat with your document (context-aware AI responses)
- ⚡ FastAPI backend with OpenAI integration
- 🎨 Modern Angular UI with glassmorphism design
- 🔐 Secure API key handling via environment variables

---

🏗️ Project Structure

docuintel-ai/
│
├── frontend/        # Angular UI
├── backend/         # FastAPI backend
├── README.md
└── .gitignore

---

⚙️ Tech Stack

Frontend

- Angular (Standalone Components)
- Tailwind CSS
- Signals API

Backend

- FastAPI
- OpenAI API
- Python

---

📸 Screenshots
<img width="1896" height="992" alt="image" src="https://github.com/user-attachments/assets/df81c6ff-1343-49bc-8423-edfcc9cfe2b3" />







---

🧑‍💻 Local Setup Guide

---

🔹 1. Clone Repository

git clone https://github.com/YOUR_USERNAME/docuintel-ai.git
cd docuintel-ai

---

🧠 BACKEND SETUP (FastAPI)

---

🔹 2. Navigate to backend

cd backend

---

🔹 3. Create Virtual Environment

Windows:

python -m venv env
env\Scripts\activate

Mac/Linux:

python3 -m venv env
source env/bin/activate

---

🔹 4. Install Dependencies

pip install -r requirements.txt

«If "requirements.txt" is missing:»

pip install fastapi uvicorn openai python-multipart numpy

---

🔹 5. Set OpenAI API Key

Option A: Environment Variable (Recommended)

Windows (CMD):

set OPENAI_API_KEY=your_api_key_here

PowerShell:

$env:OPENAI_API_KEY="your_api_key_here"

Mac/Linux:

export OPENAI_API_KEY="your_api_key_here"

---

Option B: ".env" file

Create a ".env" file in "backend/":

OPENAI_API_KEY=your_api_key_here

Then install:

pip install python-dotenv

---

🔹 6. Run Backend Server

python -m uvicorn main:app --reload

👉 Backend runs at:

http://127.0.0.1:8000

👉 Swagger Docs:

http://127.0.0.1:8000/docs

---

🎨 FRONTEND SETUP (Angular)

---

🔹 7. Navigate to frontend

cd ../frontend

---

🔹 8. Install Dependencies

npm install

---

🔹 9. Run Angular App

ng serve

👉 Frontend runs at:

http://localhost:4200

---

🔗 API Endpoints

---

📤 Upload PDF

POST /upload-pdf

- Upload PDF using multipart/form-data
- Returns session_id + classification

---

📊 Extract Data

POST /extract-data

Request:

{
  "session_id": "your_session_id"
}

---

💬 Chat with Document

POST /chat

Request:

{
  "session_id": "your_session_id",
  "query": "What is this document about?"
}

---

🔥 How It Works

1. Upload PDF
2. Backend classifies document
3. Embeddings stored per session
4. Extraction uses AI prompt
5. Chat queries use semantic similarity

---

⚠️ Common Issues & Fixes

---

❌ uvicorn not recognized

python -m uvicorn main:app --reload

---

❌ CORS Error

Ensure backend has:

from fastapi.middleware.cors import CORSMiddleware

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

---

❌ OpenAI API Error

- Check API key is set
- Ensure internet connection
- Verify SSL settings

---

🛡️ Security Notes

- Never commit ".env" files
- Keep API keys secure
- Use ".gitignore" properly

---

🚀 Future Improvements

- PDF highlighting (click field → scroll to location)
- Multi-document support
- Export to Excel / CSV
- Role-based authentication
- Deployment (Docker + Cloud)

---

🤝 Contributing

Pull requests are welcome!
For major changes, please open an issue first.

---

📄 License

This project is licensed under the MIT License.

---

⭐ Support

If you like this project:

⭐ Star the repo
🍴 Fork it
🚀 Build on top of it

---

Built with ❤️ using FastAPI + Angular + OpenAI 
