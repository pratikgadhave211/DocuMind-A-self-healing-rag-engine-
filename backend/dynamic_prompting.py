"""
Dynamic Few-Shot Learning Module

Learns from successful query-answer pairs and retrieves them as examples
for similar future queries, enabling continuous improvement.
"""

from llama_index.core import VectorStoreIndex, Document
from llama_index.core.prompts import PromptTemplate
from typing import List, Tuple, Optional
import json
from datetime import datetime


class LearningManager:
    """
    Manages dynamic few-shot learning from successful interactions
    """
    
    def __init__(self, similarity_top_k: int = 2):
        """
        Initialize learning manager
        
        Args:
            similarity_top_k: Number of similar examples to retrieve
        """
        self.good_examples: List[Document] = []
        self.index: Optional[VectorStoreIndex] = None
        self.similarity_top_k = similarity_top_k
        self.example_metadata: List[dict] = []
        
        print("✓ Learning Manager initialized")
    
    def add_good_example(
        self,
        query: str,
        answer: str,
        feedback_score: float = 1.0,
        metadata: dict = None
    ):
        """
        Add successful query-answer pair to learning system
        
        Called when user gives positive feedback (thumbs up)
        
        Args:
            query: Original user query
            answer: Successful answer
            feedback_score: User rating (0-1)
            metadata: Additional context (techniques used, processing time, etc.)
        """
        print(f"📚 Adding good example to learning system")
        
        # Create document with structured format
        example_text = f"""Query: {query}

Answer: {answer}

---
This is a successful example that received positive user feedback.
"""
        
        # Prepare metadata
        example_meta = {
            "query": query,
            "answer": answer,
            "feedback_score": feedback_score,
            "timestamp": datetime.now().isoformat(),
            "example_id": len(self.good_examples),
            **(metadata or {})
        }
        
        doc = Document(text=example_text, metadata=example_meta)
        self.good_examples.append(doc)
        self.example_metadata.append(example_meta)
        
        # Rebuild index (in production, use incremental update)
        self._rebuild_index()
        
        print(f"  ✓ Example added. Total examples: {len(self.good_examples)}")
    
    def _rebuild_index(self):
        """Rebuild the vector index from examples"""
        if self.good_examples:
            self.index = VectorStoreIndex.from_documents(self.good_examples)
    
    def get_dynamic_prompt(self, current_query: str) -> str:
        """
        Retrieve similar successful examples for current query
        
        Args:
            current_query: User's current question
            
        Returns:
            Formatted few-shot context string
        """
        if not self.index:
            return ""
        
        print(f"🧠 Retrieving similar past successes for: '{current_query}'")
        
        try:
            # Retrieve similar successful cases
            retriever = self.index.as_retriever(similarity_top_k=self.similarity_top_k)
            nodes = retriever.retrieve(current_query)
            
            if not nodes:
                print("  ℹ No similar examples found")
                return ""
            
            # Format examples
            examples_text = "\n\n".join([
                f"Example {i+1}:\n{node.text}"
                for i, node in enumerate(nodes)
            ])
            
            prompt_prefix = f"""Here are {len(nodes)} example(s) of how to answer similar questions correctly:

{examples_text}

Now, use these examples as guidance to answer the current question."""
            
            print(f"  ✓ Retrieved {len(nodes)} relevant example(s)")
            return prompt_prefix
            
        except Exception as e:
            print(f"  ⚠ Error retrieving examples: {e}")
            return ""
    
    def get_example_stats(self) -> dict:
        """
        Get statistics about learned examples
        
        Returns:
            Dict with learning statistics
        """
        if not self.good_examples:
            return {
                "total_examples": 0,
                "avg_feedback_score": 0.0,
                "example_queries": []
            }
        
        avg_score = sum(
            meta.get("feedback_score", 1.0)
            for meta in self.example_metadata
        ) / len(self.example_metadata)
        
        return {
            "total_examples": len(self.good_examples),
            "avg_feedback_score": round(avg_score, 2),
            "example_queries": [
                meta.get("query", "")[:50] + "..."
                for meta in self.example_metadata[:5]
            ],
            "oldest_example": self.example_metadata[0].get("timestamp") if self.example_metadata else None,
            "newest_example": self.example_metadata[-1].get("timestamp") if self.example_metadata else None
        }
    
    def clear_examples(self):
        """Clear all learned examples"""
        self.good_examples.clear()
        self.example_metadata.clear()
        self.index = None
        print("🗑 All examples cleared")
    
    def export_examples(self, filepath: str):
        """
        Export learned examples to JSON file
        
        Args:
            filepath: Path to save examples
        """
        with open(filepath, 'w') as f:
            json.dump(self.example_metadata, f, indent=2)
        print(f"💾 Exported {len(self.example_metadata)} examples to {filepath}")
    
    def import_examples(self, filepath: str):
        """
        Import examples from JSON file
        
        Args:
            filepath: Path to load examples from
        """
        with open(filepath, 'r') as f:
            loaded_metadata = json.load(f)
        
        for meta in loaded_metadata:
            self.add_good_example(
                query=meta["query"],
                answer=meta["answer"],
                feedback_score=meta.get("feedback_score", 1.0),
                metadata={k: v for k, v in meta.items() if k not in ["query", "answer", "feedback_score"]}
            )
        
        print(f"📥 Imported {len(loaded_metadata)} examples from {filepath}")


class PromptOptimizationTracker:
    """
    Tracks prompt performance for optimization insights
    """
    
    def __init__(self):
        self.prompt_history: List[dict] = []
    
    def log_prompt_performance(
        self,
        prompt_template: str,
        query: str,
        answer: str,
        feedback_score: float,
        techniques_used: List[str]
    ):
        """
        Log prompt performance for analysis
        
        Args:
            prompt_template: Template used
            query: User query
            answer: Generated answer
            feedback_score: User rating
            techniques_used: List of techniques applied
        """
        self.prompt_history.append({
            "timestamp": datetime.now().isoformat(),
            "prompt_template": prompt_template,
            "query": query,
            "answer": answer,
            "feedback_score": feedback_score,
            "techniques_used": techniques_used
        })
    
    def get_best_performing_prompts(self, top_k: int = 5) -> List[dict]:
        """
        Get best performing prompt patterns
        
        Args:
            top_k: Number of top prompts to return
            
        Returns:
            List of best prompts with scores
        """
        sorted_prompts = sorted(
            self.prompt_history,
            key=lambda x: x["feedback_score"],
            reverse=True
        )
        return sorted_prompts[:top_k]
    
    def get_technique_performance(self) -> dict:
        """
        Analyze which techniques correlate with good feedback
        
        Returns:
            Dict mapping techniques to average scores
        """
        technique_scores = {}
        technique_counts = {}
        
        for entry in self.prompt_history:
            score = entry["feedback_score"]
            for tech in entry["techniques_used"]:
                if tech not in technique_scores:
                    technique_scores[tech] = 0
                    technique_counts[tech] = 0
                technique_scores[tech] += score
                technique_counts[tech] += 1
        
        return {
            tech: round(technique_scores[tech] / technique_counts[tech], 2)
            for tech in technique_scores
        }
