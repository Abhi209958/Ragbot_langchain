"""
RAG Bot - Enhanced Multi-Document Q&A System
Entry point for the application
"""

import sys
import os

# Add the current directory to the Python path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from app.main import app

if __name__ == "__main__":
    import uvicorn
    print("🤖 Starting Enhanced RAG Bot...")
    print("📚 Multi-PDF support enabled")
    print("🏗️  Modular architecture loaded")
    print("🚀 Server starting on http://localhost:8000")
    
    # Use import string to avoid reload warning
    uvicorn.run("app.main:app", host="0.0.0.0", port=8000, reload=True)
