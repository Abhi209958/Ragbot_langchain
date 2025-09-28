# 🤖 RAG Bot - Enhanced Multi-Document Q&A System

A sophisticated Retrieval-Augmented Generation (RAG) bot built with FastAPI, LangChain, and OpenAI. This bot can process multiple PDF documents and provide intelligent answers based on their content with **full multi-user session support**.

## 🚀 Key Features

- **🔒 Multi-User Session Management**: Each user has isolated document storage - no data leakage between users
- **� Improved UI/UX**: Compact sidebar for uploads, large chat area, clear step-by-step instructions
- **📁 Multi-PDF Support**: Upload and process multiple PDF documents simultaneously
- **🧠 Intelligent Chunking**: Smart text splitting with overlap for better context preservation
- **🔍 Vector Search**: FAISS-powered vector search for relevant document retrieval
- **📝 Source Attribution**: Responses include references to source documents
- **💻 Modern Web Interface**: Clean, responsive UI with drag-and-drop file upload
- **⚡ Real-time Processing**: Live feedback during document processing
- **📊 Document Management**: View, track, and manage uploaded documents per user
- **🌐 RESTful API**: Well-documented API endpoints for integration

## 🛠️ Recent Fixes & Improvements

### Multi-User Security Issues Fixed ✅
- **Session Isolation**: Each user now has their own document storage
- **No Cross-User Access**: Users can only see and query their own uploaded documents
- **Session Management**: Automatic session creation and management for each user

### UI/UX Improvements ✅
- **Better Layout**: Compact sidebar (320px) + large chat area layout
- **Clear Instructions**: Step-by-step guide with visual indicators
- **Smart Upload Panel**: Smaller, more efficient upload area
- **Welcome Screen**: Helpful onboarding for new users
- **Status Indicators**: Real-time feedback on document processing
- **Responsive Design**: Works well on desktop and mobile devices

## 🏗️ Project Structure

```
Ragbot_langchain/
├── main.py                    # Legacy entry point (use app/main.py instead)
├── app/
│   ├── __init__.py
│   ├── main.py               # FastAPI app with session middleware
│   ├── api/
│   │   ├── __init__.py
│   │   └── routes.py         # Session-aware API endpoints
│   ├── models/
│   │   ├── __init__.py
│   │   └── schemas.py        # Pydantic models
│   ├── services/
│   │   ├── __init__.py
│   │   ├── document_processor.py  # PDF processing per user session
│   │   └── retrieval.py           # Vector search per user session
│   ├── static/              # Static files (CSS, JS) - currently empty
│   └── templates/
│       └── index.html       # Modern responsive web interface
├── requirements.txt          # Python dependencies
├── .env                     # Environment variables
├── start.sh                 # Linux/Mac startup script
├── docker-compose.yml       # Docker compose configuration
├── Dockerfile              # Docker build configuration
└── README.md               # This file
```

## 🔧 Technical Details

### Backend Components:
- **FastAPI**: Web framework with session middleware for multi-user support
- **LangChain**: Framework for building AI applications with RAG capabilities
- **OpenAI GPT-3.5-turbo**: Language model for generating responses
- **FAISS**: Vector store for document similarity search per user session
- **PyPDF2**: PDF text extraction with metadata preservation
- **SessionMiddleware**: Secure session management for user isolation

### Frontend Components:
- **Vanilla JavaScript**: No frameworks, pure JS for simplicity and performance
- **Modern CSS**: Responsive design with sidebar + main chat area layout
- **Drag & Drop API**: Modern file upload interface with visual feedback
- **Session Management**: Automatic session handling for multi-user support

## 📦 Installation & Setup

### Prerequisites
- Python 3.8+
- OpenAI API key

### Quick Start
1. **Set up environment**:
   ```bash
   # Clone and navigate to project
   cd Ragbot_langchain
   
   # Create virtual environment
   python -m venv venv
   
   # Activate virtual environment
   # Windows:
   venv\Scripts\activate
   # Linux/Mac:
   source venv/bin/activate
   ```

2. **Install dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

3. **Set up environment variables**:
   ```bash
   # Create .env file or set environment variable
   # Windows:
   set OPENAI_API_KEY=your-openai-api-key
   
   # Linux/Mac:
   export OPENAI_API_KEY="your-openai-api-key"
   ```

4. **Run the application**:
   ```bash
   python app/main.py
   ```

5. **Access the application**:
   Open your browser and navigate to `http://localhost:8000`

## � How to Use

### Step-by-Step Guide
1. **📁 Upload Documents**: 
   - Drag & drop PDF files to the upload area (left sidebar)
   - Or click the upload area to browse files
   - Wait for processing completion

2. **💬 Start Chatting**: 
   - Once documents are processed, the chat input becomes active
   - Ask any questions about your uploaded documents
   - Get answers with source references

3. **📊 Monitor Status**: 
   - View your uploaded documents in the sidebar
   - See processing status and document count
   - Each user only sees their own documents

### Multi-User Testing
- Open multiple browser windows/tabs
- Each window represents a different user session
- Upload different documents in each window
- Verify users can't see each other's documents

## �🌟 Features in Detail

### Document Processing (Per User Session):
- Extracts text from PDF files with page separation
- Splits text into manageable chunks with context preservation
- Creates vector embeddings using OpenAI per user
- Stores embeddings in isolated FAISS vector databases
- Document metadata tracking (upload time, size, page count)

### Session Management:
- Automatic session creation for each user
- Cryptographically signed session cookies
- Complete isolation between user sessions
- Memory-efficient per-user resource allocation

### Chat System:
- Real-time question answering using user's documents only
- Source document attribution with page references
- Context-aware responses with conversation memory
- Comprehensive error handling and user feedback

### Modern UI/UX:
- Responsive sidebar + main chat area layout
- Clear step-by-step user guidance
- Visual feedback for all user actions
- Mobile-responsive design with touch support
- Loading states and progress indicators

## � API Endpoints

All endpoints support session-based isolation:

- `POST /api/upload` - Upload PDF documents (per user session)
- `POST /api/chat` - Send chat messages (uses user's documents only)
- `GET /api/status` - Get user's document status
- `GET /api/documents` - List user's uploaded documents
- `DELETE /api/documents/{id}` - Delete user's specific document
- `DELETE /api/reset` - Clear user's documents
- `GET /health` - Application health check

## 🔒 Security Features

- **Session Isolation**: Each user's documents are completely isolated
- **Secure Sessions**: Cryptographically signed session cookies
- **No Data Leakage**: Users cannot access other users' documents or chat history
- **Memory Management**: Efficient per-user resource allocation
- **API Key Security**: Environment variable-based API key management
- **Temporary Processing**: Files are processed in memory and not stored permanently

## �🚨 Troubleshooting

### Common Issues:

1. **Import errors when starting:**
   - Make sure you're in the virtual environment: `venv\Scripts\activate` (Windows) or `source venv/bin/activate` (Linux/Mac)
   - Install requirements: `pip install -r requirements.txt`
   - Use `python app/main.py` not just `python main.py`

2. **OpenAI API errors:**
   - Check your API key is set: `echo %OPENAI_API_KEY%` (Windows) or `echo $OPENAI_API_KEY` (Linux/Mac)
   - Ensure you have credits in your OpenAI account
   - Verify your API key has the necessary permissions

3. **PDF upload issues:**
   - Only PDF files are supported
   - Make sure the PDF contains extractable text (not just images)
   - Check file size limitations in your browser

4. **Chat not working:**
   - Ensure documents are uploaded first (follow the step-by-step guide)
   - Check the browser console for JavaScript errors
   - Verify the backend is running properly on `http://localhost:8000`

5. **Multi-user issues:**
   - Each browser window/tab represents a different user session
   - Clear browser cookies if sessions get mixed up
   - Use different browsers or incognito mode to test multiple users

### Multi-User Testing
- Use different browsers (Chrome, Firefox, Edge) to test multiple users
- Use incognito/private browsing modes
- Each session should be completely isolated

## 🐳 Docker Support

```bash
# Build and run
docker build -t ragbot .
docker run -p 8000:8000 -e OPENAI_API_KEY=your-key ragbot

# Or use Docker Compose
docker-compose up --build
```

## 📄 License

This project is for educational and personal use.

---

Enjoy using your RAG Bot! 🤖✨
