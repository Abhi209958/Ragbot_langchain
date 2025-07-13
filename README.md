# 🤖 RAG Bot - Enhanced Multi-Document Q&A Assistant

A sophisticated RAG (Retrieval-Augmented Generation) bot built with LangChain and FastAPI that supports multiple PDF documents with a beautiful, modular architecture.

## ✨ Enhanced Features

- 📄 **Multi-PDF Upload**: Upload multiple PDF documents simultaneously
- 💬 **Intelligent Chat**: Advanced question answering across all uploaded documents
- 🔍 **Enhanced Search**: Improved chunking and retrieval with better source attribution
- 🏗️ **Modular Architecture**: Clean, maintainable code structure
- 📊 **Document Statistics**: Track and manage your uploaded documents
- 🎨 **Modern UI**: Beautiful, responsive interface with smooth animations
- 📱 **Mobile Responsive**: Works perfectly on all devices
- 🚀 **High Performance**: Built with FastAPI for maximum speed

## 🏗️ Project Structure

```
RagBot/
├── main.py                    # Application entry point
├── app/
│   ├── __init__.py
│   ├── main.py               # FastAPI app configuration
│   ├── api/
│   │   ├── __init__.py
│   │   └── routes.py         # API endpoints
│   ├── models/
│   │   ├── __init__.py
│   │   └── schemas.py        # Pydantic models
│   └── services/
│       ├── __init__.py
│       ├── document_processor.py  # PDF processing service
│       └── retrieval.py           # RAG and vector store service
├── templates/
│   └── index.html            # Frontend interface
├── static/                   # Static assets
├── uploads/                  # Temporary upload directory
├── requirements.txt          # Python dependencies
├── .env                     # Environment variables
├── start.sh                 # Enhanced startup script
└── README.md               # This file
```

## 🔧 Technical Details

### Backend Components:
- **FastAPI**: Web framework for the API
- **LangChain**: Framework for building AI applications
- **OpenAI GPT-3.5-turbo**: Language model for generating responses
- **FAISS**: Vector store for document similarity search
- **PyPDF2**: PDF text extraction

### Frontend Components:
- **Vanilla JavaScript**: No frameworks, pure JS for simplicity
- **Modern CSS**: Responsive design with gradients and animations
- **Drag & Drop API**: Modern file upload interface

## 🌟 Features in Detail

### Document Processing:
- Extracts text from PDF files
- Splits text into manageable chunks
- Creates vector embeddings using OpenAI
- Stores embeddings in FAISS vector database

### Chat System:
- Real-time question answering
- Source document attribution
- Context-aware responses
- Error handling and user feedback

### UI/UX:
- Beautiful gradient design
- Smooth animations and transitions
- Mobile-responsive layout
- Loading states and progress indicators

## 🚨 Troubleshooting

### Common Issues:

1. **Import errors when starting:**
   - Make sure you're in the virtual environment: `source /home/abhishek/Project24/.venv/bin/activate`
   - Install requirements: `pip install -r requirements.txt`

2. **OpenAI API errors:**
   - Check your API key in the `.env` file
   - Ensure you have credits in your OpenAI account
   - Verify your API key has the necessary permissions

3. **PDF upload issues:**
   - Only PDF files are supported
   - Make sure the PDF contains extractable text (not just images)
   - Check file size limitations

4. **Chat not working:**
   - Ensure documents are uploaded first
   - Check the browser console for JavaScript errors
   - Verify the backend is running properly

## 🔐 Security Notes

- Keep your OpenAI API key secure and never commit it to version control
- The `.env` file is included in `.gitignore` (if you add one)
- Uploaded files are processed temporarily and not permanently stored

## 🎯 Future Enhancements

- Support for multiple document formats (Word, TXT, etc.)
- Document management (view, delete uploaded docs)
- Chat history persistence
- User authentication
- Advanced search filters
- Export chat conversations

## 📄 License

This project is for educational and personal use.

---

Enjoy using your RAG Bot! 🤖✨
