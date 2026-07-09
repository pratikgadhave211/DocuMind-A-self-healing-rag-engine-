"""
Cross-Encoder Reranking Module

Cross-encoders provide more accurate document scoring compared to bi-encoder similarity search.
They process query-document pairs together to produce refined relevance scores.
"""

from sentence_transformers import CrossEncoder
from typing import List, Tuple


class Reranker:
    """Cross-encoder reranker for precise document scoring"""
    
    def __init__(self, model_name: str = 'cross-encoder/ms-marco-MiniLM-L-6-v2'):
        """
        Initialize reranker with cross-encoder model
        
        Args:
            model_name: HuggingFace model for cross-encoding
                       Default: MS MARCO optimized MiniLM model
        """
        print(f"Loading cross-encoder model: {model_name}")
        self.model = CrossEncoder(model_name)
        print("✓ Cross-encoder loaded successfully")
    
    def rerank(
        self,
        query: str,
        documents: List[str],
        top_k: int = 5,
        return_scores: bool = False
    ) -> List[str] | List[Tuple[str, float]]:
        """
        Rerank documents using cross-encoder
        
        Args:
            query: User query
            documents: List of document texts to rerank
            top_k: Number of top documents to return
            return_scores: Whether to return scores with documents
            
        Returns:
            List of reranked documents (and scores if requested)
        """
        if not documents:
            return []
        
        # Construct query-document pairs
        pairs = [[query, doc] for doc in documents]
        
        # Batch scoring with cross-encoder
        scores = self.model.predict(pairs)
        
        # Sort by score (descending) and take top_k
        ranked = sorted(
            zip(documents, scores),
            key=lambda x: x[1],
            reverse=True
        )[:top_k]
        
        if return_scores:
            return ranked
        else:
            return [doc for doc, score in ranked]
    

