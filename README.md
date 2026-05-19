# 🧠 Second Brain AI

> **A local AI-powered personal knowledge operating system.** Upload documents, notes, PDFs, research papers, and text files, then chat with your knowledge using local AI models through Ollama.

[![Version](https://img.shields.io/badge/version-0.2.0-blue.svg)](./package.json)
[![License](https://img.shields.io/badge/license-MIT-green.svg)](./LICENSE)
[![Python](https://img.shields.io/badge/Python-3.9%2B-blue.svg)](https://www.python.org/downloads/)
[![Node.js](https://img.shields.io/badge/Node.js-18%2B-green.svg)](https://nodejs.org/)

---

## ✨ Features

### Core Functionality
- 📄 **Multi-format Support**: Upload PDF, TXT, MD, DOCX files
- 🔍 **Hybrid Search**: Combines vector (semantic) + keyword (BM25) search for best results
- 💾 **Smart Chunking**: Intelligent text extraction and splitting with cleaning
- 🧬 **Embeddings**: Generate embeddings using sentence-transformers
- 🔗 **Vector Storage**: Store and retrieve with ChromaDB
- 💬 **AI Chat**: Ask questions and get context-aware answers
- 🎯 **Semantic Search**: Retrieve relevant chunks using intelligent search
- 📝 **Auto-Summarization**: Automatic summaries for uploaded documents
- 📚 **Chat Memory**: Persistent conversations with rolling summaries
- 🏷️ **Citations**: Every answer includes source file, chunk, and relevance score
- 📊 **Session Management**: Organize chats into sessions with history

### Search & Retrieval
- Hybrid vector + keyword search with configurable weights
- Context ranking by relevance, recency, and diversity
- Automatic query expansion and optimization
- Configurable result filtering and scoring

### API Features
- 7 professional REST endpoints with validation
- Automatic OpenAPI documentation
- Comprehensive error handling
- Type-safe Pydantic models
- CORS support for frontend integration

---

## 🏗️ Architecture

```
┌─────────────────────────────────────────────────────┐
│              Frontend (Next.js)                     │
│  • React Components  • TypeScript  • Tailwind CSS   │
└──────────────────┬──────────────────────────────────┘
                   │ HTTP/REST API
                   ▼
┌─────────────────────────────────────────────────────┐
│           Backend (FastAPI/Python)                  │
├─────────────────────────────────────────────────────┤
│  API Router                                         │
│  ├── Search      │ Hybrid search (vector + BM25)   │
│  ├── Chat        │ RAG chat with memory            │
│  ├── Documents   │ File management & summaries     │
│  ├── Sessions    │ Chat session management         │
│  └── Upload      │ Document processing             │
├─────────────────────────────────────────────────────┤
│  Services Layer                                     │
│  ├── RetrievalService   (Hybrid search)            │
│  ├── RankingService     (Context optimization)     │
│  ├── MemoryService      (Chat persistence)         │
│  ├── CitationService    (Source tracking)          │
│  ├── SummaryService     (Auto-summarization)       │
│  └── EmbeddingService   (Embeddings generation)    │
├─────────────────────────────────────────────────────┤
│  Data Layer                                         │
│  ├── ChromaDB (Vector embeddings)                   │
│  └── SQLite (Metadata & sessions)                  │
├─────────────────────────────────────────────────────┤
│  AI Integration                                     │
│  └── Ollama (Local LLM inference)                  │
└─────────────────────────────────────────────────────┘
```

---

## 🛠️ Tech Stack

### Frontend
- **Framework**: Next.js 14
- **Language**: TypeScript
- **Styling**: Tailwind CSS
- **HTTP Client**: Axios
- **State**: React Hooks

### Backend
- **Framework**: FastAPI
- **Language**: Python 3.9+
- **Server**: Uvicorn

### AI & ML
- **LLM**: Ollama (local models: Qwen, Mistral, Phi-3)
- **Embeddings**: sentence-transformers
- **Search**: rank-bm25
- **Vector DB**: ChromaDB

### Data & Processing
- **Database**: SQLite (metadata)
- **Document Parsing**: PyPDF2, python-docx, Markdown
- **OCR**: EasyOCR (optional)
- **Utilities**: Pydantic, python-multipart

---

## 📂 Project Structure

```
Second Brain AI/
├── frontend/                      # Next.js application
│   ├── app/                       # App routing and pages
│   ├── components/                # Reusable React components
│   ├── services/                  # API client service
│   ├── types/                     # TypeScript interfaces
│   ├── tailwind.config.js
│   ├── package.json
│   └── .env.local
│
├── backend/                       # FastAPI application
│   ├── main.py                    # Application entry point
│   ├── requirements.txt           # Python dependencies
│   ├── .env / .env.example        # Configuration
│   │
│   ├── api/
│   │   └── router.py              # 7 REST endpoints
│   │
│   ├── services/                  # Business logic
│   │   ├── retrieval_service.py   # Hybrid search
│   │   ├── ranking_service.py     # Context ranking
│   │   ├── memory_service.py      # Chat memory
│   │   ├── citation_service.py    # Citations
│   │   ├── summary_service.py     # Auto-summary
│   │   ├── embedding_service.py   # Embeddings
│   │   └── file_service.py        # File handling
│   │
│   ├── embeddings/                # Embedding generation
│   ├── vector_db/                 # ChromaDB wrapper
│   ├── ai/                        # Ollama integration
│   ├── database/                  # SQLite wrapper
│   ├── parsers/                   # Document parsing
│   └── chroma_db/                 # Vector storage
│
├── uploads/                       # Uploaded files
├── README.md                      # This file
├── SETUP.md                       # Detailed setup guide
└── start.bat                      # Quick start script (Windows)
```

---

## 🚀 Quick Start

### Prerequisites
- **Node.js** 18+ ([Download](https://nodejs.org/))
- **Python** 3.9+ ([Download](https://www.python.org/downloads/))
- **Ollama** ([Download](https://ollama.ai/))
- **Git** ([Download](https://git-scm.com/))

### Installation (5 minutes)

#### 1. Clone & Navigate
```bash
git clone https://github.com/RaunakSingh733/Second-Brain-AI.git
cd "Second Brain AI"
```

#### 2. Setup Backend
```bash
cd backend

# Create virtual environment
python -m venv venv
venv\Scripts\activate          # Windows
# source venv/bin/activate    # macOS/Linux

# Install dependencies
pip install -r requirements.txt
```

#### 3. Setup Ollama Model
```bash
# Make sure Ollama is running, then pull a model:
ollama pull qwen:7b            # Recommended
# OR: ollama pull mistral
# OR: ollama pull phi-3
```

#### 4. Start Backend
```bash
cd backend
uvicorn main:app --reload
# Backend runs at http://localhost:8000
```

#### 5. Setup Frontend (new terminal)
```bash
cd frontend
npm install
npm run dev
# Frontend runs at http://localhost:3000
```

#### 6. Access the Application
Open [http://localhost:3000](http://localhost:3000) in your browser

---

## 📡 API Endpoints

| Method | Endpoint | Purpose |
|--------|----------|----------|
| `POST` | `/api/upload` | Upload a document |
| `POST` | `/api/search` | Hybrid search (vector + keyword) |
| `POST` | `/api/chat` | RAG chat with citations |
| `GET` | `/api/documents` | List documents with summaries |
| `GET` | `/api/documents/{id}` | Document details |
| `GET` | `/api/chat/sessions` | List chat sessions |
| `GET` | `/api/chat/sessions/{id}/history` | Session history |

### Example Requests

**Hybrid Search:**
```bash
curl -X POST http://localhost:8000/api/search \
  -H "Content-Type: application/json" \
  -d '{"query": "machine learning", "top_k": 5}'
```

**RAG Chat:**
```bash
curl -X POST http://localhost:8000/api/chat \
  -H "Content-Type: application/json" \
  -d '{"query": "What is this about?", "include_history": true}'
```

---

## 🔄 How It Works

### Document Upload Flow
```
Upload File → Parse Content → Extract Text → Split Chunks → 
Generate Embeddings → Store in ChromaDB → Auto-Summarize → 
Save Metadata to SQLite
```

### Chat & Search Flow
```
User Query → Generate Embedding → Vector Search + Keyword Search → 
Merge Results → Rank by Relevance → Get Chat History → 
Build LLM Prompt → Ollama Generation → Add Citations → 
Store Message → Return Response
```

---

## 🔧 Configuration

### Backend Environment Variables (.env)
```env
# Ollama Configuration
OLLAMA_BASE_URL=http://localhost:11434
OLLAMA_MODEL=qwen:7b

# Search Configuration
VECTOR_WEIGHT=0.6
KEYWORD_WEIGHT=0.4
TOP_K=5

# Context Configuration
MAX_TOKENS=4000
SUMMARY_FREQUENCY=5
```

### Frontend Environment Variables (.env.local)
```env
NEXT_PUBLIC_API_URL=http://localhost:8000
```

---

## 📊 Phase 2 Implementation (Current Version)

### ✅ What's Included

**New Features:**
- ✅ Hybrid search (vector + BM25 keyword search)
- ✅ Smart context ranking (relevance, recency, diversity)
- ✅ Chat memory system with rolling summaries
- ✅ Automatic document summarization
- ✅ Source citations in every response
- ✅ Improved API structure (7 endpoints)

**New Endpoints:**
- ✅ POST `/api/search` - Hybrid search
- ✅ POST `/api/chat` - RAG chat with memory
- ✅ GET `/api/documents` - List with summaries
- ✅ GET `/api/chat/sessions` - Session management

**Code Statistics:**
- 1,600+ lines of new code
- 4 new service modules
- 7 professional API endpoints
- 1 new dependency (rank-bm25)
- 0 breaking changes

---

## 🧪 Testing

### Verify Installation
```bash
# Check backend is running
curl http://localhost:8000/health

# Check API status
curl http://localhost:8000/api/status
```

### Test Workflow
1. Upload a PDF/TXT document via the web interface
2. Check `/api/documents` to see auto-generated summary
3. Ask a question in the chat interface
4. Verify citations appear in the response
5. Check `/api/chat/sessions` for persistent memory

---

## 📚 Documentation

- **[SETUP.md](./SETUP.md)** - Detailed step-by-step setup guide
- **[PHASE2_IMPLEMENTATION.md](./PHASE2_IMPLEMENTATION.md)** - Technical deep-dive
- **[QUICKSTART_PHASE2.md](./QUICKSTART_PHASE2.md)** - Quick reference with examples
- **[PROJECT_SUMMARY.md](./PROJECT_SUMMARY.md)** - Architecture and structure
- **[DELIVERABLES.md](./DELIVERABLES.md)** - Complete feature list

---

## 🔮 Roadmap

### Phase 3: Enhancements (Planned)
- OCR support for scanned documents
- Flashcard auto-generation
- Enhanced UI/UX with animations
- Document tagging and organization
- Advanced filtering and faceted search

### Phase 4: Advanced Features (Planned)
- Knowledge graph visualization
- Smart concept linking
- Export capabilities (PDF, Markdown)
- Multi-user support
- API rate limiting and authentication

---

## ⚙️ Troubleshooting

### Backend Won't Start
```bash
# Check Python version
python --version  # Should be 3.9+

# Verify dependencies
pip list | grep -E "(fastapi|uvicorn|chromadb)"

# Reinstall requirements
pip install -r requirements.txt --upgrade
```

### Ollama Connection Issues
```bash
# Check Ollama is running
curl http://localhost:11434/api/tags

# Pull a model if needed
ollama pull qwen:7b
```

### Frontend Can't Connect to Backend
- Check backend is running on http://localhost:8000
- Verify CORS is enabled in `backend/main.py`
- Check `.env.local` has correct `NEXT_PUBLIC_API_URL`

### No Search Results
- Ensure documents are uploaded first
- Check BM25 index is initialized (see backend logs)
- Verify ChromaDB has document chunks

---

## 📝 License

MIT License - Feel free to use and modify for your personal knowledge management needs.

```
MIT License

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.
```

---

## 🤝 Contributing

Contributions are welcome! Please feel free to:
- Report bugs via GitHub Issues
- Suggest features and improvements
- Submit pull requests
- Improve documentation

---

## 👨‍💻 Development

### Project Status
- **Version**: 0.2.0
- **Status**: Production Ready
- **Quality**: High (with comprehensive error handling and logging)
- **Last Updated**: May 2026

### Maintainers
- Built with ❤️ for smarter knowledge management

---

## 📞 Support

Having issues? Check:
1. [Troubleshooting Section](#-troubleshooting)
2. [SETUP.md](./SETUP.md) for detailed instructions
3. [PHASE2_IMPLEMENTATION.md](./PHASE2_IMPLEMENTATION.md) for technical details
4. GitHub Issues for known problems

---

<div align="center">

**Made with ❤️ for better knowledge management**

[⬆ Back to top](#-second-brain-ai)

</div>