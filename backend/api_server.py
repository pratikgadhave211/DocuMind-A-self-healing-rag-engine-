"""
FastAPI Server for Self-Healing RAG System

Provides REST API and WebSocket endpoints for the RAG system
"""

import os
import sys
from fastapi import FastAPI, WebSocket, WebSocketDisconnect, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from pydantic import BaseModel
from typing import List, Optional, Dict, Any
import asyncio
from dotenv import load_dotenv
import traceback

# Load environment variables
load_dotenv()

# Import RAG system
from self_healing_rag import SelfHealingRAGSystem
from reranker import BiEncoderVsCrossEncoderDemo

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

# Global RAG system instance
rag_system: Optional[SelfHealingRAGSystem] = None


# Pydantic models
class QueryRequest(BaseModel):
    query: str
    enable_hyde: bool = True
    enable_decomposition: bool = True
    enable_crag: bool = True
    enable_reranking: bool = True
    enable_learning: bool = True


class FeedbackRequest(BaseModel):
    query: str
    answer: str
    is_positive: bool


class DocumentUpload(BaseModel):
    documents: List[str]


# Startup event
@app.on_event("startup")
async def startup_event():
    """Initialize RAG system on startup"""
    global rag_system
    
    print("🚀 Starting Self-Healing RAG API Server...")
    
    try:
        # Get API key from environment
        openai_api_key = os.getenv("OPENAI_API_KEY")
        if not openai_api_key:
            print("⚠️  WARNING: OPENAI_API_KEY not found in environment")
        
        # Initialize system
        rag_system = SelfHealingRAGSystem(
            openai_api_key=openai_api_key,
            enable_web_search=False  # Disable by default (requires Tavily key)
        )
        
        # Load sample documents
        rag_system.load_sample_documents()
        
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
            "statistics": "/api/statistics",
            "upload": "/api/upload",
            "architecture": "/api/architecture",
            "websocket": "/ws"
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
        raise HTTPException(status_code=400, detail="No documents loaded")
    
    try:
        result = rag_system.process_query(
            query=request.query,
            enable_decomposition=request.enable_decomposition,
            enable_hyde=request.enable_hyde,
            enable_crag=request.enable_crag,
            enable_reranking=request.enable_reranking,
            enable_learning=request.enable_learning
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


@app.get("/api/statistics")
async def get_statistics():
    """
    Get system performance statistics
    
    Returns:
        Statistics dictionary
    """
    if rag_system is None:
        raise HTTPException(status_code=503, detail="RAG system not initialized")
    
    try:
        stats = rag_system.get_statistics()
        learning_stats = rag_system.learning_manager.get_example_stats()
        
        return {
            "system_stats": stats,
            "learning_stats": learning_stats
        }
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.post("/api/upload")
async def upload_documents(request: DocumentUpload):
    """
    Upload custom documents to the RAG system
    
    Args:
        request: Document upload request
        
    Returns:
        Confirmation
    """
    if rag_system is None:
        raise HTTPException(status_code=503, detail="RAG system not initialized")
    
    try:
        rag_system.load_documents(request.documents)
        
        return {
            "status": "success",
            "message": f"Loaded {len(request.documents)} documents",
            "document_count": len(request.documents)
        }
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/api/architecture")
async def get_architecture_info():
    """
    Get architecture information and comparisons
    
    Returns:
        Architecture details
    """
    try:
        bi_vs_cross = BiEncoderVsCrossEncoderDemo.explain_difference()
        
        return {
            "encoder_comparison": bi_vs_cross,
            "pipeline_stages": {
                "1_query_enhancement": {
                    "techniques": ["HyDE", "Query Decomposition"],
                    "purpose": "Transform raw queries into optimal retrieval requests"
                },
                "2_retrieval": {
                    "techniques": ["Vector Search", "Bi-Encoder"],
                    "purpose": "Fast semantic recall of candidate documents"
                },
                "3_validation": {
                    "techniques": ["CRAG", "Relevance Grading"],
                    "purpose": "Filter irrelevant documents, trigger fallback"
                },
                "4_reranking": {
                    "techniques": ["Cross-Encoder"],
                    "purpose": "Precision scoring for final document selection"
                },
                "5_generation": {
                    "techniques": ["Dynamic Few-Shot", "LLM Generation"],
                    "purpose": "Generate accurate answer from validated context"
                },
                "6_learning": {
                    "techniques": ["Feedback Loop", "Example Storage"],
                    "purpose": "Continuous improvement from successful interactions"
                }
            }
        }
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


# WebSocket endpoint for real-time query processing
@app.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    """
    WebSocket endpoint for streaming query results
    
    Clients can send queries and receive real-time updates
    """
    await websocket.accept()
    
    if rag_system is None:
        await websocket.send_json({
            "type": "error",
            "message": "RAG system not initialized"
        })
        await websocket.close()
        return
    
    try:
        while True:
            # Receive query from client
            data = await websocket.receive_json()
            
            query = data.get("query", "")
            config = data.get("config", {})
            
            if not query:
                await websocket.send_json({
                    "type": "error",
                    "message": "Empty query"
                })
                continue
            
            # Send processing started event
            await websocket.send_json({
                "type": "processing_started",
                "query": query
            })
            
            try:
                # Process query
                result = rag_system.process_query(
                    query=query,
                    enable_decomposition=config.get("enable_decomposition", True),
                    enable_hyde=config.get("enable_hyde", True),
                    enable_crag=config.get("enable_crag", True),
                    enable_reranking=config.get("enable_reranking", True),
                    enable_learning=config.get("enable_learning", True)
                )
                
                # Send result
                await websocket.send_json({
                    "type": "result",
                    "data": result
                })
                
            except Exception as e:
                await websocket.send_json({
                    "type": "error",
                    "message": str(e)
                })
                
    except WebSocketDisconnect:
        print("WebSocket client disconnected")
    except Exception as e:
        print(f"WebSocket error: {e}")
        traceback.print_exc()


if __name__ == "__main__":
    import uvicorn
    
    print("🌟 Starting Self-Healing RAG API Server...")
    print("📚 Loading environment variables...")
    
    # Run server
    uvicorn.run(
        "api_server:app",
        host="0.0.0.0",
        port=8000,
        reload=True,
        log_level="info"
    )
