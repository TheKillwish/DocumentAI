<h1 align="center">🚀 DocuIntel AI</h1>

<p align="center">
  <b>AI-Powered Document Intelligence Platform</b><br/>
  Upload • Classify • Extract • Chat • Bulk Process
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
  <li>📦 Bulk document upload with batch processing</li>
  <li>🧠 AI-based document classification (Invoice, Resume, Payslip, etc.)</li>
  <li>🗂️ Automatic class grouping of documents</li>
  <li>📊 Intelligent structured data extraction (dynamic JSON)</li>
  <li>📁 Session-based document processing</li>
  <li>💬 Chat with your document (context-aware AI)</li>
  <li>⚡ Real-time progress tracking for bulk processing</li>
  <li>📥 Export single document data to CSV</li>
  <li>📤 Export all documents data (bulk CSV)</li>
  <li>📊 Export data by document class</li>
  <li>🎯 Dynamic UI updates based on selected document/session</li>
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
  <li>Signals API (Reactive State Management)</li>
  <li>Tailwind CSS (Modern UI)</li>
</ul>

<h3>Backend</h3>
<ul>
  <li>FastAPI</li>
  <li>OpenAI API (Vision + LLM)</li>
  <li>Python</li>
</ul>

<hr/>

<h2>📸 Screenshots</h2>

<p align="center"><b>🏠 Dashboard UI Overview</b></p>
<!-- Add screenshot -->

<p align="center"><b>📤 Single File Upload Flow</b></p>
<!-- Add screenshot -->

<p align="center"><b>📦 Bulk Upload & Processing</b></p>
<!-- Add screenshot -->

<p align="center"><b>📊 Real-time Progress Tracking</b></p>
<!-- Add screenshot -->

<p align="center"><b>🧠 Document Classification Result</b></p>
<!-- Add screenshot -->

<p align="center"><b>📄 Extracted Structured Data View</b></p>
<!-- Add screenshot -->

<p align="center"><b>🗂️ Class-Based Document Grouping</b></p>
<!-- Add screenshot -->

<p align="center"><b>📑 Multi-Document Navigation (Left Panel)</b></p>
<!-- Add screenshot -->

<p align="center"><b>💬 Chat with Document</b></p>
<!-- Add screenshot -->

<p align="center"><b>🔗 API & JSON Response Panel</b></p>
<!-- Add screenshot -->

<p align="center"><b>📥 Export Single File (CSV)</b></p>
<!-- Add screenshot -->

<p align="center"><b>📤 Export All Files (Bulk CSV)</b></p>
<!-- Add screenshot -->

<p align="center"><b>📊 Export by Document Class</b></p>
<!-- Add screenshot -->

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
POST /api/v1/extract/

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
  <li>Upload single or multiple PDFs</li>
  <li>AI classifies each document</li>
  <li>Session created per document</li>
  <li>Structured data extracted dynamically</li>
  <li>Documents grouped by class automatically</li>
  <li>User selects document → UI updates instantly</li>
  <li>Chat works based on selected session</li>
  <li>Export data (single / bulk / class-wise)</li>
</ol>

<hr/>

<h2>⚠️ Common Issues</h2>

<ul>
  <li><b>uvicorn not recognized</b><br/>python -m uvicorn main:app --reload</li>
  <li><b>CORS Error</b> → enable CORSMiddleware in backend</li>
  <li><b>OpenAI Error</b> → check API key & internet</li>
  <li><b>Slow processing</b> → depends on document size & API latency</li>
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
  <li>📌 Field-level PDF highlighting</li>
  <li>📚 Multi-document chat (cross-session)</li>
  <li>📊 Advanced analytics dashboard</li>
  <li>🔐 Authentication & user sessions</li>
  <li>🐳 Docker deployment</li>
  <li>⚡ Background job queue (Celery / Redis)</li>
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