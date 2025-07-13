from pydantic import BaseModel
from typing import List, Optional

class ChatMessage(BaseModel):
    message: str

class ChatResponse(BaseModel):
    response: str
    source_documents: Optional[List[str]] = []

class UploadResponse(BaseModel):
    message: str
    documents: List[str]
    total_documents: int

class StatusResponse(BaseModel):
    documents_uploaded: int
    documents: List[str]
    ready_for_chat: bool

class DocumentInfo(BaseModel):
    filename: str
    page_count: int
    text_length: int
    upload_time: str

class DocumentWithId(BaseModel):
    id: int
    filename: str
    page_count: int
    text_length: int
    upload_time: str
    size: int

class DeleteResponse(BaseModel):
    message: str
    remaining_documents: List[str]
    total_remaining: int
