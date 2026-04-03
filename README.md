<h1 align="center">🚀 DocuIntel AI</h1>

<p align="center">
  <b>AI-Powered Document Intelligence Platform</b><br/>
  Upload • Classify • Extract • Chat
</p>

<p align="center">
  <img src="https://img.shields.io/badge/FastAPI-Backend-0ea5e9?style=for-the-badge"/>
  <img src="https://img.shields.io/badge/Angular-Frontend-6366f1?style=for-the-badge"/>
  <img src="https://img.shields.io/badge/OpenAI-AI-22d3ee?style=for-the-badge"/>
</p>

<hr/>

<h2>✨ Features</h2>

<ul>
  <li>📄 Upload and process PDF documents</li>
  <li>🧠 AI-based document classification (Invoice, Payslip, Resume, etc.)</li>
  <li>📊 Intelligent structured data extraction (dynamic JSON)</li>
  <li>💬 Chat with your document (context-aware AI)</li>
  <li>⚡ FastAPI backend with OpenAI integration</li>
  <li>🎨 Modern Angular UI with glassmorphism design</li>
  <li>🔐 Secure API key handling via environment variables</li>
</ul>

<hr/>

<h2>🏗️ Project Structure</h2>

<pre>
frontend/        # Angular UI
backend/         # FastAPI backend
README.md
.gitignore
</pre>

<hr/>

<h2>⚙️ Tech Stack</h2>

<h3>Frontend</h3>
<ul>
  <li>Angular (Standalone Components)</li>
  <li>Tailwind CSS</li>
  <li>Signals API</li>
</ul>

<h3>Backend</h3>
<ul>
  <li>FastAPI</li>
  <li>OpenAI API</li>
  <li>Python</li>
</ul>

<hr/>

<h2>📸 Screenshots</h2>

<p align="center"><b>UI</b></p>
<p align="center">
  <img src="https://github.com/user-attachments/assets/02047218-6291-4cfc-a460-bc45d8bfcb58" width="800"/>
</p>

<p align="center"><b>Upload Document</b></p>
<p align="center">
  <img src="https://github.com/user-attachments/assets/30e07f17-abe3-4830-a90f-006e6ee8a498" width="800"/>
</p>

<p align="center"><b>Classification & Extraction</b></p>
<p align="center">
  <img src="https://github.com/user-attachments/assets/3a8d0266-7041-4b6b-98aa-eb6b6928ba79" width="800"/>
</p>

<p align="center"><b>Chat Bot</b></p>
<p align="center">
  <img src="https://github.com/user-attachments/assets/06305a98-b9e3-43b1-8b7b-32f43a2733ec" width="800"/>
</p>

<p align="center"><b>API Integration</b></p>
<p align="center">
  <img src="https://github.com/user-attachments/assets/3381d736-06ef-4f42-a8c3-c1b4a93d1c60" width="800"/>
</p>

<hr/>

<h2>🧑‍💻 Local Setup Guide</h2>

<h3>🔹 1. Clone Repository</h3>

<pre>
git clone https://github.com/TheKillwish/DocumentAI
cd DocumentAI
</pre>

<hr/>

<h2>🧠 Backend Setup (FastAPI)</h2>

<h3>🔹 Navigate</h3>

<pre>cd backend</pre>

<h3>🔹 Create Virtual Environment</h3>

<pre>
python -m venv env
env\Scripts\activate     (Windows)

source env/bin/activate  (Mac/Linux)
</pre>

<h3>🔹 Install Dependencies</h3>

<pre>pip install -r requirements.txt</pre>

<h3>🔹 Set OpenAI API Key</h3>

<pre>
export OPENAI_API_KEY="your_api_key_here"
</pre>

<h3>🔹 Run Server</h3>

<pre>python -m uvicorn main:app --reload</pre>

<p>
Backend: <a href="http://127.0.0.1:8000">http://127.0.0.1:8000</a><br/>
Docs: <a href="http://127.0.0.1:8000/docs">Swagger UI</a>
</p>

<hr/>

<h2>🎨 Frontend Setup (Angular)</h2>

<h3>🔹 Navigate</h3>

<pre>cd frontend</pre>

<h3>🔹 Install</h3>

<pre>npm install</pre>

<h3>🔹 Run</h3>

<pre>ng serve</pre>

<p>
Frontend: <a href="http://localhost:4200">http://localhost:4200</a>
</p>

<hr/>

<h2>🔗 API Endpoints</h2>

<h3>📤 Upload PDF</h3>
<pre>POST /upload-pdf</pre>

<h3>📊 Extract Data</h3>
<pre>
POST /extract-data

{
  "session_id": "your_session_id"
}
</pre>

<h3>💬 Chat</h3>
<pre>
POST /chat

{
  "session_id": "your_session_id",
  "query": "What is this document about?"
}
</pre>

<hr/>

<h2>🔥 How It Works</h2>

<ol>
  <li>Upload PDF</li>
  <li>AI classifies document</li>
  <li>Embeddings stored per session</li>
  <li>Data extracted using prompts</li>
  <li>Chat uses semantic similarity</li>
</ol>

<hr/>

<h2>⚠️ Common Issues</h2>

<ul>
  <li><b>uvicorn not recognized</b><br/>python -m uvicorn main:app --reload</li>
  <li><b>CORS Error</b> → enable CORSMiddleware in backend</li>
  <li><b>OpenAI Error</b> → check API key & internet</li>
</ul>

<hr/>

<h2>🛡️ Security</h2>

<ul>
  <li>Never commit <code>.env</code></li>
  <li>Keep API keys secure</li>
  <li>Use <code>.gitignore</code></li>
</ul>

<hr/>

<h2>🚀 Future Improvements</h2>

<ul>
  <li>PDF field highlighting</li>
  <li>Multi-document chat</li>
  <li>Excel export</li>
  <li>Authentication system</li>
  <li>Docker deployment</li>
</ul>

<hr/>

<h2>🤝 Contributing</h2>

<p>Pull requests are welcome! Open an issue first for major changes.</p>

<hr/>

<h2>⭐ Support</h2>

<p align="center">
  ⭐ Star the repo &nbsp; | &nbsp; 🍴 Fork &nbsp; | &nbsp; 🚀 Build on top
</p>

<hr/>

<p align="center">
  Built with ❤️ using FastAPI + Angular + OpenAI
</p>
