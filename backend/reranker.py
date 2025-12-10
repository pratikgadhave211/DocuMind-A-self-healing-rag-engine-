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
    
    def rerank_with_metadata(
        self,
        query: str,
        documents: List[dict],
        text_key: str = 'text',
        top_k: int = 5
    ) -> List[dict]:
        """
        Rerank documents with metadata preservation
        
        Args:
            query: User query
            documents: List of document dicts with text and metadata
            text_key: Key for document text in dict
            top_k: Number of top documents to return
            
        Returns:
            List of reranked document dicts with added 'rerank_score'
        """
        if not documents:
            return []
        
        # Extract texts
        texts = [doc.get(text_key, '') for doc in documents]
        
        # Construct pairs
        pairs = [[query, text] for text in texts]
        
        # Score
        scores = self.model.predict(pairs)
        
        # Combine with original documents
        for doc, score in zip(documents, scores):
            doc['rerank_score'] = float(score)
        
        # Sort and return top_k
        ranked_docs = sorted(
            documents,
            key=lambda x: x['rerank_score'],
            reverse=True
        )[:top_k]
        
        return ranked_docs
    
    def score_pairs(self, query_doc_pairs: List[Tuple[str, str]]) -> List[float]:
        """
        Score multiple query-document pairs
        
        Args:
            query_doc_pairs: List of (query, document) tuples
            
        Returns:
            List of relevance scores
        """
        pairs = [[q, d] for q, d in query_doc_pairs]
        scores = self.model.predict(pairs)
        return scores.tolist()


class BiEncoderVsCrossEncoderDemo:
    """
    Demonstration comparing Bi-Encoder and Cross-Encoder architectures
    """
    
    @staticmethod
    def explain_difference() -> dict:
        """
        Explain the architectural difference between bi-encoder and cross-encoder
        
        Returns:
            Dict with explanations and trade-offs
        """
        return {
            "bi_encoder": {
                "description": "Encodes query and documents separately into fixed-size vectors",
                "architecture": "Query Encoder → [768d] ← Document Encoder",
                "search": "Cosine similarity between pre-computed embeddings",
                "pros": [
                    "Fast: O(n) for n documents after pre-computation",
                    "Scalable: Can index millions of documents",
                    "Efficient: Documents encoded once and cached"
                ],
                "cons": [
                    "Limited accuracy: No interaction between query and doc",
                    "Semantic details lost in fixed vector",
                    "Asymmetric relevance hard to capture"
                ],
                "use_case": "Initial coarse retrieval (Top 50-100)"
            },
            "cross_encoder": {
                "description": "Encodes query and document together as single input",
                "architecture": "[CLS] Query [SEP] Document [SEP] → BERT → Relevance Score",
                "search": "Full attention between all query and document tokens",
                "pros": [
                    "High accuracy: Full token-level interaction",
                    "Rich semantics: Captures complex relevance patterns",
                    "Direct prediction: No vector comparison needed"
                ],
                "cons": [
                    "Slow: O(n*m) for n queries and m documents",
                    "Not scalable: Must encode each pair separately",
                    "Expensive: Can't pre-compute or cache"
                ],
                "use_case": "Precision reranking (Top 5-10 from coarse retrieval)"
            },
            "two_stage_strategy": {
                "stage_1": "Bi-encoder rapid recall → Top 50 candidates",
                "stage_2": "Cross-encoder precision rerank → Top 5 final results",
                "benefit": "Combines speed of bi-encoder with accuracy of cross-encoder"
            }
        }
