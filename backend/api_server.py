"""
FastAPI Server for Self-Healing RAG System

Provides REST API and WebSocket endpoints for the RAG system
"""

import os
import sys



from fastapi import FastAPI, WebSocket, WebSocketDisconnect, HTTPException, UploadFile, File
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse, FileResponse
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel
from typing import List, Optional, Dict, Any
import asyncio
from dotenv import load_dotenv
import traceback

# Load environment variables
load_dotenv()


# Import RAG system
from self_healing_rag import SelfHealingRAGSystem

# Initialize FastAPI app
app = FastAPI(
    title="Self-Healing RAG API",
    description="Advanced RAG system with HyDE, CRAG, Cross-Encoder Reranking, and Dynamic Learning",
    version="1.0.0"
)

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Mount frontend directory for static files (to be created)
import os
frontend_dir = os.path.join(os.path.dirname(os.path.dirname(__file__)), "frontend")
os.makedirs(frontend_dir, exist_ok=True)
app.mount("/app", StaticFiles(directory=frontend_dir, html=True), name="frontend")


# Global RAG system instance
rag_system: Optional[SelfHealingRAGSystem] = None


# Pydantic models
class QueryRequest(BaseModel):
    query: str
    session_id: str = "default"
    manual_override: bool = False
    enable_hyde: bool = True
    enable_decomposition: bool = True
    enable_crag: bool = True
    enable_reranking: bool = True
    enable_learning: bool = True


class FeedbackRequest(BaseModel):
    query: str
    answer: str
    is_positive: bool





# Startup event
@app.on_event("startup")
async def startup_event():
    """Initialize RAG system on startup"""
    global rag_system
    
    print("🚀 Starting Self-Healing RAG API Server...")
    
    try:
        # Get API key from environment
        nvidia_api_key = os.getenv("NVIDIA_API_KEY")
        if not nvidia_api_key:
            print("⚠️  WARNING: NVIDIA_API_KEY not found in environment")
        tavily_api_key = os.getenv("TAVILY_API_KEY")

        # Initialize system
        rag_system = SelfHealingRAGSystem(
            nvidia_api_key=nvidia_api_key,
            tavily_api_key=tavily_api_key,
            enable_web_search=bool(tavily_api_key)
        )

        
        print("✅ RAG System initialized successfully!")
        
    except Exception as e:
        print(f"❌ Error initializing RAG system: {e}")
        traceback.print_exc()


# Health check endpoint
@app.get("/")
async def root():
    """Root endpoint - health check"""
    return {
        "status": "online",
        "service": "Self-Healing RAG API",
        "version": "1.0.0",
        "endpoints": {
            "query": "/api/query",
            "feedback": "/api/feedback",
            "upload_file": "/api/upload-file"
        }
    }


@app.get("/api/health")
async def health_check():
    """Detailed health check"""
    if rag_system is None:
        raise HTTPException(status_code=503, detail="RAG system not initialized")
    
    return {
        "status": "healthy",
        "system_ready": rag_system.vector_index is not None,
        "components": {
            "query_decomposer": "ready",
            "hyde_engine": "ready" if rag_system.hyde_engine else "not_loaded",
            "crag_system": "ready",
            "reranker": "ready",
            "learning_manager": "ready"
        }
    }


@app.post("/api/query")
async def query_rag(request: QueryRequest):
    """
    Process a query through the RAG pipeline
    
    Args:
        request: Query request with configuration
        
    Returns:
        Query result with answer and metadata
    """
    if rag_system is None:
        raise HTTPException(status_code=503, detail="RAG system not initialized")
    
    if not rag_system.vector_index:
        raise HTTPException(status_code=400, detail="No documents loaded. Please upload your document (e.g. your resume) first before asking questions.")
    
    try:
        result = rag_system.process_query(
            query=request.query,
            manual_override=request.manual_override,
            enable_decomposition=request.enable_decomposition,
            enable_hyde=request.enable_hyde,
            enable_crag=request.enable_crag,
            enable_reranking=request.enable_reranking,
            enable_learning=request.enable_learning,
            thread_id=request.session_id
        )
        
        return JSONResponse(content=result)
        
    except Exception as e:
        print(f"Error processing query: {e}")
        traceback.print_exc()
        raise HTTPException(status_code=500, detail=str(e))


@app.post("/api/feedback")
async def submit_feedback(request: FeedbackRequest):
    """
    Submit user feedback for learning
    
    Args:
        request: Feedback data
        
    Returns:
        Confirmation
    """
    if rag_system is None:
        raise HTTPException(status_code=503, detail="RAG system not initialized")
    
    try:
        rag_system.add_feedback(
            query=request.query,
            answer=request.answer,
            is_positive=request.is_positive
        )
        
        return {
            "status": "success",
            "message": "Feedback recorded"
        }
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))



@app.post("/api/upload-file")
async def upload_file(file: UploadFile = File(...)):
    """
    Upload a file (PDF, DOCX, PPTX, HTML, TXT) to the RAG system.
    """
    import os, tempfile
    
    if rag_system is None:
        raise HTTPException(status_code=503, detail="RAG system not initialized")

    allowed_exts = [".pdf", ".docx", ".pptx", ".html", ".htm", ".txt"]
    ext = os.path.splitext(file.filename.lower())[1]
    if ext not in allowed_exts:
        raise HTTPException(status_code=400, detail=f"Unsupported file format. Allowed: {', '.join(allowed_exts)}")

    try:
        # Save upload to a temp file
        with tempfile.NamedTemporaryFile(delete=False, suffix=ext) as tmp:
            content = await file.read()
            tmp.write(content)
            tmp_path = tmp.name

        chunks = rag_system.load_file(tmp_path, original_filename=file.filename)

        return {
            "status": "success",
            "filename": file.filename,
            "chunks_loaded": chunks,
            "message": f"Indexed {chunks} chunks from '{file.filename}'",
        }

    except Exception as e:
        traceback.print_exc()
        raise HTTPException(status_code=500, detail=str(e))

    finally:
        try:
            os.unlink(tmp_path)
        except Exception:
            pass



if __name__ == "__main__":
    import uvicorn
    
    print("🌟 Starting Self-Healing RAG API Server...")
    print("📚 Loading environment variables...")
    
    import os
    # Run server
    uvicorn.run(
        "api_server:app",
        host="0.0.0.0",
        port=int(os.environ.get("PORT", 8000)),
        reload=True,
        log_level="info"
    )
