from typing import List
from fastapi import APIRouter, File, UploadFile, HTTPException, status, Request, Depends
from app.models.schemas import ChatMessage, ChatResponse, UploadResponse, StatusResponse, DocumentWithId, DeleteResponse
from app.services.document_processor import DocumentProcessor
from app.services.retrieval import RetrievalService

# Initialize services - now session-based
document_processors = {}  # session_id -> DocumentProcessor
retrieval_services = {}   # session_id -> RetrievalService

router = APIRouter()

def get_session_id(request: Request) -> str:
    """Get session ID from request"""
    return request.session.get("session_id", "default")

def get_user_services(session_id: str = Depends(get_session_id)):
    """Get or create user-specific services"""
    if session_id not in document_processors:
        document_processors[session_id] = DocumentProcessor()
        retrieval_services[session_id] = RetrievalService()
    
    return document_processors[session_id], retrieval_services[session_id]

@router.post("/upload", response_model=UploadResponse)
async def upload_documents(files: List[UploadFile] = File(...), services: tuple = Depends(get_user_services)):
    """Upload and process multiple PDF documents with enhanced support"""
    
    document_processor, retrieval_service = services
    
    try:
        # Process uploaded files
        texts, document_info = await document_processor.process_uploaded_files(files)
        document_names = [info["filename"] for info in document_info]
        
        print(f"Processing {len(files)} files: {document_names}")
        
        # Add documents to retrieval service
        retrieval_service.add_documents(texts, document_names)
        
        # Get document statistics
        stats = document_processor.get_document_stats()
        
        return UploadResponse(
            message=f"Successfully uploaded and processed {len(files)} document(s). Total: {stats['total_documents']} documents, {stats['total_pages']} pages.",
            documents=document_names,
            total_documents=stats['total_documents']
        )
        
    except Exception as e:
        print(f"Error in upload endpoint: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Error processing documents: {str(e)}")

@router.post("/chat", response_model=ChatResponse)
async def chat(message: ChatMessage, services: tuple = Depends(get_user_services)):
    """Process chat message and return response with enhanced source information"""
    
    document_processor, retrieval_service = services
    
    try:
        # Query the documents
        result = retrieval_service.query(message.message)
        
        return ChatResponse(
            response=result["answer"],
            source_documents=result["sources"]
        )
        
    except Exception as e:
        print(f"Error in chat endpoint: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Error processing message: {str(e)}")

@router.get("/status", response_model=StatusResponse)
async def get_status(services: tuple = Depends(get_user_services)):
    """Get current status of the RAG bot with detailed information"""
    
    document_processor, retrieval_service = services
    
    # Get document stats
    doc_stats = document_processor.get_document_stats()
    retrieval_status = retrieval_service.get_status()
    
    document_names = [doc["filename"] for doc in doc_stats["documents"]]
    
    return StatusResponse(
        documents_uploaded=doc_stats["total_documents"],
        documents=document_names,
        ready_for_chat=retrieval_status["ready_for_queries"]
    )

@router.delete("/reset")
async def reset_bot(services: tuple = Depends(get_user_services)):
    """Reset the bot by clearing all uploaded documents"""
    
    document_processor, retrieval_service = services
    
    # Reset both services
    document_processor.clear_documents()
    retrieval_service.reset()
    
    return {"message": "Bot reset successfully. All documents cleared."}

@router.get("/documents/stats")
async def get_document_stats(services: tuple = Depends(get_user_services)):
    """Get detailed statistics about uploaded documents"""
    
    document_processor, retrieval_service = services
    
    doc_stats = document_processor.get_document_stats()
    retrieval_status = retrieval_service.get_status()
    
    return {
        **doc_stats,
        **retrieval_status
    }

@router.get("/documents", response_model=List[DocumentWithId])
async def get_documents(services: tuple = Depends(get_user_services)):
    """Get list of uploaded documents with their IDs"""
    
    document_processor, retrieval_service = services
    
    doc_stats = document_processor.get_document_stats()
    return [
        DocumentWithId(**doc) for doc in doc_stats["documents"]
    ]

@router.delete("/documents/{document_id}", response_model=DeleteResponse)
async def delete_document(document_id: int, services: tuple = Depends(get_user_services)):
    """Delete a specific document by its ID and rebuild the vector store"""
    
    document_processor, retrieval_service = services
    
    try:
        # Check if document exists
        doc_to_delete = document_processor.get_document_by_id(document_id)
        if not doc_to_delete:
            raise HTTPException(status_code=404, detail="Document not found")
        
        # Remove from document processor
        deleted = document_processor.delete_document(document_id)
        if not deleted:
            raise HTTPException(status_code=404, detail="Document not found")
        
        # Get remaining documents
        remaining_texts, remaining_names = document_processor.get_remaining_texts_and_names()
        
        # Rebuild vector store with remaining documents
        retrieval_service.rebuild_vector_store_without_document(remaining_texts, remaining_names)
        
        return DeleteResponse(
            message=f"Document '{doc_to_delete['filename']}' deleted successfully",
            remaining_documents=remaining_names,
            total_remaining=len(remaining_names)
        )
        
    except HTTPException:
        raise
    except Exception as e:
        print(f"Error deleting document: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Error deleting document: {str(e)}")