import os
import tempfile
from typing import List, Dict, Any
import PyPDF2
from datetime import datetime
from fastapi import HTTPException, UploadFile

class Document:
    """Simple Document class for compatibility"""
    def __init__(self, page_content: str, metadata: dict = None):
        self.page_content = page_content
        self.metadata = metadata or {}

class DocumentProcessor:
    """Handles PDF document processing and text extraction"""
    
    def __init__(self):
        self.uploaded_documents: List[Dict[str, Any]] = []
        self.document_id_counter = 0
    
    async def process_uploaded_files(self, files: List[UploadFile]) -> tuple[List[str], List[Dict[str, Any]]]:
        """Process multiple uploaded PDF files and extract text"""
        if not files:
            raise HTTPException(status_code=400, detail="No files uploaded")
        
        texts = []
        document_info = []
        
        for file in files:
            if not file.filename.endswith('.pdf'):
                raise HTTPException(status_code=400, detail=f"File {file.filename} is not a PDF. Only PDF files are supported")
            
            # Save uploaded file temporarily
            with tempfile.NamedTemporaryFile(delete=False, suffix='.pdf') as tmp_file:
                content = await file.read()
                tmp_file.write(content)
                tmp_file_path = tmp_file.name
            
            try:
                # Extract text from PDF
                text, page_count = self.extract_text_from_pdf(tmp_file_path)
                texts.append(text)
                
                # Store document information with unique ID and text
                self.document_id_counter += 1
                doc_info = {
                    "id": self.document_id_counter,
                    "filename": file.filename,
                    "page_count": page_count,
                    "text_length": len(text),
                    "upload_time": datetime.now().isoformat(),
                    "size": len(content),
                    "text": text  # Store the extracted text for rebuilding
                }
                document_info.append(doc_info)
                self.uploaded_documents.append(doc_info)
                
            finally:
                # Clean up temporary file
                os.unlink(tmp_file_path)
        
        if not texts:
            raise HTTPException(status_code=400, detail="No text could be extracted from the uploaded files")
        
        return texts, document_info
    
    def extract_text_from_pdf(self, file_path: str) -> tuple[str, int]:
        """Extract text from PDF file and return text with page count"""
        text = ""
        page_count = 0
        
        try:
            with open(file_path, 'rb') as file:
                pdf_reader = PyPDF2.PdfReader(file)
                page_count = len(pdf_reader.pages)
                
                for page_num, page in enumerate(pdf_reader.pages):
                    page_text = page.extract_text()
                    # Add page separator for multi-page documents
                    text += f"\n--- Page {page_num + 1} ---\n{page_text}\n"
                    
        except Exception as e:
            raise HTTPException(status_code=400, detail=f"Error reading PDF: {str(e)}")
        
        return text, page_count
    
    def get_document_stats(self) -> Dict[str, Any]:
        """Get statistics about uploaded documents"""
        total_pages = sum(doc["page_count"] for doc in self.uploaded_documents)
        total_text_length = sum(doc["text_length"] for doc in self.uploaded_documents)
        
        return {
            "total_documents": len(self.uploaded_documents),
            "total_pages": total_pages,
            "total_text_length": total_text_length,
            "documents": self.uploaded_documents
        }
    
    def clear_documents(self):
        """Clear all uploaded documents"""
        self.uploaded_documents.clear()
    
    def delete_document(self, document_id: int) -> bool:
        """Delete a specific document by ID"""
        for i, doc in enumerate(self.uploaded_documents):
            if doc["id"] == document_id:
                deleted_doc = self.uploaded_documents.pop(i)
                print(f"Deleted document: {deleted_doc['filename']}")
                return True
        return False
    
    def get_document_by_id(self, document_id: int) -> Dict[str, Any]:
        """Get document information by ID"""
        for doc in self.uploaded_documents:
            if doc["id"] == document_id:
                return doc
        return None
    
    def get_remaining_document_names(self) -> List[str]:
        """Get list of remaining document filenames"""
        return [doc["filename"] for doc in self.uploaded_documents]
    
    def get_remaining_texts_and_names(self) -> tuple[List[str], List[str]]:
        """Get remaining document texts and names after deletion"""
        texts = [doc["text"] for doc in self.uploaded_documents]
        names = [doc["filename"] for doc in self.uploaded_documents]
        return texts, names
    
    def get_remaining_texts_and_names_for_rebuilding(self) -> tuple[List[str], List[str]]:
        """Get remaining document texts and names for vector store rebuilding"""
        texts = [doc["text"] for doc in self.uploaded_documents]
        names = [doc["filename"] for doc in self.uploaded_documents]
        return texts, names
