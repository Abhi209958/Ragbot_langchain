#!/bin/bash

# Enhanced RAG Bot Startup Script

echo "🤖 Starting Enhanced RAG Bot with Multi-PDF Support..."

# Check if virtual environment exists
if [ ! -d "/home/abhishek/Project24/.venv" ]; then
    echo "❌ Virtual environment not found. Please create one first."
    exit 1
fi

# Activate virtual environment
source /home/abhishek/Project24/.venv/bin/activate

# Check if requirements are installed
if ! python -c "import fastapi" 2>/dev/null; then
    echo "📦 Installing requirements..."
    pip install -r requirements.txt
fi

# Check if OpenAI API key is set
if [ -z "$OPENAI_API_KEY" ]; then
    echo "⚠️  Warning: OPENAI_API_KEY not found in environment variables."
    echo "Please set your OpenAI API key in the .env file or as an environment variable."
    echo "You can get your API key from: https://platform.openai.com/api-keys"
fi

# Display new features
echo ""
echo "✨ Enhanced Features:"
echo "   📚 Multi-PDF support - Upload multiple documents at once"
echo "   🏗️  Modular architecture - Better code organization"
echo "   🔍 Improved search - Better chunk management and retrieval"
echo "   📊 Document statistics - Track your uploaded documents"
echo "   🎯 Enhanced sources - Better source attribution"
echo ""

# Start the application
echo "🚀 Starting Enhanced RAG Bot on http://localhost:8000"
echo "📱 Open your browser and navigate to http://localhost:8000"
echo "Press Ctrl+C to stop the server"

python main.py
