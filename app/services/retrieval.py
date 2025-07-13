import os
import traceback
from typing import List, Dict, Any
from langchain.text_splitter import CharacterTextSplitter
from langchain_community.vectorstores import FAISS
from langchain_openai import OpenAIEmbeddings, ChatOpenAI
from langchain.chains import RetrievalQA
from dotenv import load_dotenv
from fastapi import HTTPException

from .document_processor import Document

load_dotenv()

class RetrievalService:
    """Handles vector store creation and question answering"""
    
    def __init__(self):
        self.vector_store = None
        self.qa_chain = None
        self.document_count = 0
        
    def create_vector_store(self, texts: List[str], document_names: List[str]) -> FAISS:
        """Create FAISS vector store from texts with improved chunking"""
        try:
            print(f"Creating vector store from {len(texts)} documents...")
            
            # Enhanced text splitter with better parameters
            text_splitter = CharacterTextSplitter(
                chunk_size=1500,  # Larger chunks for better context
                chunk_overlap=300,  # More overlap for continuity
                separator="\n",
                length_function=len,
            )
            
            documents = []
            for i, text in enumerate(texts):
                print(f"Processing document {i+1}: {document_names[i] if i < len(document_names) else 'Unknown'}")
                chunks = text_splitter.split_text(text)
                print(f"  - Created {len(chunks)} chunks")
                
                for chunk_idx, chunk in enumerate(chunks):
                    # Enhanced metadata with more information
                    metadata = {
                        "source": document_names[i] if i < len(document_names) else f"document_{i+1}",
                        "document_id": i,
                        "chunk_id": chunk_idx,
                        "total_chunks": len(chunks)
                    }
                    documents.append(Document(
                        page_content=chunk,
                        metadata=metadata
                    ))
            
            print(f"Total chunks created: {len(documents)}")
            
            # Create embeddings with explicit API key
            embeddings = OpenAIEmbeddings(
                openai_api_key=os.getenv("OPENAI_API_KEY")
            )
            
            # Create vector store
            vector_store = FAISS.from_documents(documents, embeddings)
            print("Vector store created successfully!")
            
            return vector_store
            
        except Exception as e:
            print(f"Error creating vector store: {str(e)}")
            print(f"Traceback: {traceback.format_exc()}")
            raise HTTPException(status_code=500, detail=f"Error creating vector store: {str(e)}")
    
    def create_qa_chain(self, vector_store: FAISS):
        """Create QA chain with the vector store"""
        try:
            print("Creating QA chain...")
            
            llm = ChatOpenAI(
                model="gpt-3.5-turbo",
                temperature=0.7,
                openai_api_key=os.getenv("OPENAI_API_KEY")
            )
            
            # Enhanced retriever with more results
            retriever = vector_store.as_retriever(
                search_type="similarity",
                search_kwargs={"k": 5}  # Get more relevant chunks
            )
            
            qa_chain = RetrievalQA.from_chain_type(
                llm=llm,
                chain_type="stuff",
                retriever=retriever,
                return_source_documents=True,
                verbose=True
            )
            
            print("QA chain created successfully!")
            return qa_chain
            
        except Exception as e:
            print(f"Error creating QA chain: {str(e)}")
            print(f"Traceback: {traceback.format_exc()}")
            raise HTTPException(status_code=500, detail=f"Error creating QA chain: {str(e)}")
    
    def add_documents(self, texts: List[str], document_names: List[str]):
        """Add new documents to existing vector store or create new one"""
        try:
            if self.vector_store is None:
                print("Creating new vector store...")
                self.vector_store = self.create_vector_store(texts, document_names)
                self.document_count = len(texts)
            else:
                print("Adding documents to existing vector store...")
                # Create new vector store for new documents
                new_vector_store = self.create_vector_store(texts, document_names)
                # Merge with existing vector store
                self.vector_store.merge_from(new_vector_store)
                self.document_count += len(texts)
            
            # Create or update QA chain
            self.qa_chain = self.create_qa_chain(self.vector_store)
            
            print(f"Total documents in vector store: {self.document_count}")
            
        except Exception as e:
            print(f"Error adding documents: {str(e)}")
            raise HTTPException(status_code=500, detail=f"Error adding documents: {str(e)}")
    
    def query(self, question: str) -> Dict[str, Any]:
        """Query the documents and return answer with sources"""
        if self.qa_chain is None:
            raise HTTPException(status_code=400, detail="No documents uploaded yet. Please upload PDF documents first.")
        
        try:
            print(f"Processing query: {question}")
            
            # Get response from QA chain
            result = self.qa_chain({"query": question})
            
            # Extract and process source information
            source_docs = []
            source_info = []
            
            if "source_documents" in result:
                for doc in result["source_documents"]:
                    source_name = doc.metadata.get("source", "Unknown")
                    chunk_info = f"Chunk {doc.metadata.get('chunk_id', 0) + 1}/{doc.metadata.get('total_chunks', 1)}"
                    
                    if source_name not in source_docs:
                        source_docs.append(source_name)
                    
                    source_info.append({
                        "source": source_name,
                        "chunk_info": chunk_info,
                        "preview": doc.page_content[:200] + "..." if len(doc.page_content) > 200 else doc.page_content
                    })
            
            print(f"Query processed successfully. Found {len(source_docs)} source documents.")
            
            return {
                "answer": result["result"],
                "sources": source_docs,
                "source_details": source_info,
                "total_documents_searched": self.document_count
            }
            
        except Exception as e:
            print(f"Error processing query: {str(e)}")
            raise HTTPException(status_code=500, detail=f"Error processing message: {str(e)}")
    
    def reset(self):
        """Reset the retrieval service"""
        self.vector_store = None
        self.qa_chain = None
        self.document_count = 0
        print("Retrieval service reset successfully")
    
    def get_status(self) -> Dict[str, Any]:
        """Get current status of the retrieval service"""
        return {
            "has_vector_store": self.vector_store is not None,
            "has_qa_chain": self.qa_chain is not None,
            "document_count": self.document_count,
            "ready_for_queries": self.qa_chain is not None
        }
    
    def rebuild_vector_store_without_document(self, remaining_texts: List[str], remaining_names: List[str]):
        """Rebuild vector store excluding deleted document"""
        if not remaining_texts:
            # No documents left, reset everything
            self.reset()
            return
        
        print(f"Rebuilding vector store with {len(remaining_texts)} remaining documents...")
        
        # Recreate vector store with remaining documents
        self.vector_store = self.create_vector_store(remaining_texts, remaining_names)
        self.qa_chain = self.create_qa_chain(self.vector_store)
        self.document_count = len(remaining_texts)
        
        print(f"Vector store rebuilt successfully with {self.document_count} documents")
