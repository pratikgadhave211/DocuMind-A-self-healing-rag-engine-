"""
Complete Self-Healing RAG System

Integrates all components: HyDE, Query Decomposition, CRAG, Cross-Encoder Reranking,
and Dynamic Learning into a unified self-healing RAG system.
"""

import os
from typing import List, Dict, Any, Optional
from datetime import datetime
from langchain_core.documents import Document

# Import all components
from hyde import build_hyde_engine, configure_hyde_llm
from query_decomposition import QueryDecomposer
from corrective_rag import CRAGSystem
from reranker import Reranker
from dynamic_prompting import LearningManager, PromptOptimizationTracker

# Core dependencies
from llama_index.core import VectorStoreIndex, Document as LlamaDocument, Settings
from llama_index.llms.openai import OpenAI
from llama_index.embeddings.openai import OpenAIEmbedding


class SelfHealingRAGSystem:
    """
    Complete self-healing RAG system with all advanced techniques
    """
    
    def __init__(
        self,
        openai_api_key: str = None,
        tavily_api_key: str = None,
        enable_web_search: bool = False
    ):
        """
        Initialize RAG system
        
        Args:
            openai_api_key: OpenAI API key
            tavily_api_key: Tavily API key for web search
            enable_web_search: Whether to enable web search fallback
        """
        # API key configuration
        if openai_api_key:
            os.environ["OPENAI_API_KEY"] = openai_api_key
        
        print("🚀 Initializing Self-Healing RAG System...")
        
        # Core LLM configuration
        self.llm = OpenAI(model="gpt-4o-mini", temperature=0.3)
        Settings.llm = self.llm
        Settings.embed_model = OpenAIEmbedding(model="text-embedding-3-small")
        
        # Initialize components
        print("  📦 Loading components...")
        self.query_decomposer = QueryDecomposer(model="gpt-4o-mini")
        self.reranker = Reranker()
        self.learning_manager = LearningManager(similarity_top_k=2)
        self.crag_system = CRAGSystem(
            grader_model="gpt-4o-mini",
            generator_model="gpt-4o-mini",
            web_search_enabled=enable_web_search,
            tavily_api_key=tavily_api_key
        )
        self.optimization_tracker = PromptOptimizationTracker()
        
        # Vector index (will be built from documents)
        self.vector_index = None
        self.hyde_engine = None
        
        # Statistics
        self.query_stats = {
            "total_queries": 0,
            "hyde_used": 0,
            "decomposed_queries": 0,
            "crag_activated": 0,
            "reranked": 0,
            "learning_applied": 0,
            "avg_processing_time": 0.0
        }
        
        print("✅ System initialized successfully!")
    
    def load_documents(self, documents: List[str] | List[LlamaDocument]):
        """
        Load documents into vector index
        
        Args:
            documents: List of text strings or LlamaDocument objects
        """
        print("📚 Loading documents into vector index...")
        
        # Convert to LlamaDocument if needed
        if documents and isinstance(documents[0], str):
            docs = [
                LlamaDocument(text=text, metadata={"id": i})
                for i, text in enumerate(documents)
            ]
        else:
            docs = documents
        
        # Build index
        self.vector_index = VectorStoreIndex.from_documents(docs)
        self.hyde_engine = build_hyde_engine(self.vector_index)
        
        print(f"  ✅ Loaded {len(docs)} documents")
    
    def load_sample_documents(self):
        """Load demo documents about RAG techniques"""
        sample_texts = [
            """Retrieval-Augmented Generation (RAG) is a technique that combines 
            pre-trained language models with external knowledge retrieval. RAG systems 
            retrieve relevant documents from a knowledge base and use them to generate 
            more accurate and factual responses. The key advantage is grounding LLM 
            outputs in real data rather than relying solely on parametric knowledge.""",
            
            """Corrective RAG (CRAG) introduces a self-correction mechanism that grades 
            retrieved documents for relevance. If documents are deemed irrelevant, the 
            system triggers alternative retrieval strategies like web search. This 
            three-state evaluation (correct/ambiguous/incorrect) enables dynamic 
            recovery from poor retrieval results.""",
            
            """HyDE (Hypothetical Document Embeddings) improves retrieval by generating 
            hypothetical documents that answer the query, then searching for real documents 
            similar to these hypothetical ones. This addresses the modality mismatch between 
            short queries and long documents, improving recall quality.""",
            
            """Cross-encoder reranking provides more accurate document scoring compared 
            to bi-encoder similarity search. It processes query-document pairs together 
            using full cross-attention to produce refined relevance scores. The two-stage 
            approach uses bi-encoders for fast recall and cross-encoders for precision.""",
            
            """DSPy enables automatic prompt optimization by treating prompts as programs 
            that can be compiled and optimized against specific metrics like accuracy 
            or semantic similarity. The MIPROv2 optimizer rewrites instructions and 
            updates few-shot examples based on validation performance.""",
            
            """Self-healing RAG systems implement feedback loops that learn from successful 
            query-answer pairs, storing them as examples for future similar queries to 
            improve performance over time. This dynamic few-shot learning enables 
            continuous improvement without retraining.""",
            
            """Query decomposition breaks complex multi-part questions into atomic 
            sub-queries that can be individually processed and then combined for 
            comprehensive answers. This handles questions comparing multiple entities 
            or requiring information from disparate sources.""",
            
            """Vector databases enable semantic search by converting documents into 
            high-dimensional embeddings that capture semantic meaning rather than 
            just keyword matches. Modern embedding models like text-embedding-3 
            produce rich representations enabling nuanced similarity search.""",
            
            """LangGraph provides a framework for building stateful, multi-step LLM 
            applications as directed graphs. Each node represents a processing step, 
            and conditional edges enable dynamic routing based on intermediate results. 
            This is ideal for implementing CRAG workflows with fallback logic.""",
            
            """The fragility of standard RAG stems from its open-loop architecture where 
            errors propagate unchecked from retrieval to generation. Self-healing systems 
            add closed-loop feedback at each stage: query refinement, relevance validation, 
            document reranking, and answer quality assessment."""
        ]
        
        self.load_documents(sample_texts)
    
    def enhanced_retrieve(
        self,
        query: str,
        use_hyde: bool = True,
        top_k: int = 5
    ) -> List[Document]:
        """
        Enhanced retrieval with optional HyDE
        
        Args:
            query: User query
            use_hyde: Whether to use HyDE transformation
            top_k: Number of documents to retrieve
            
        Returns:
            List of retrieved documents
        """
        print(f"🔍 Retrieving documents for: '{query[:50]}...'")
        
        if use_hyde and self.hyde_engine:
            print("  🧠 Using HyDE transformation...")
            response = self.hyde_engine.query(query)
            nodes = response.source_nodes
            self.query_stats["hyde_used"] += 1
        else:
            print("  📖 Using standard retrieval...")
            retriever = self.vector_index.as_retriever(similarity_top_k=top_k)
            nodes = retriever.retrieve(query)
        
        # Convert to Document objects
        docs = []
        for node in nodes:
            doc = Document(
                page_content=node.text if hasattr(node, 'text') else str(node),
                metadata=node.metadata if hasattr(node, 'metadata') else {}
            )
            docs.append(doc)
        
        print(f"  ✅ Retrieved {len(docs)} documents")
        return docs
    
    def process_query(
        self,
        query: str,
        enable_decomposition: bool = True,
        enable_hyde: bool = True,
        enable_crag: bool = True,
        enable_reranking: bool = True,
        enable_learning: bool = True
    ) -> Dict[str, Any]:
        """
        Process query through complete self-healing pipeline
        
        Args:
            query: User question
            enable_decomposition: Use query decomposition
            enable_hyde: Use HyDE transformation
            enable_crag: Use CRAG validation
            enable_reranking: Use cross-encoder reranking
            enable_learning: Use dynamic few-shot learning
            
        Returns:
            Dict with answer and metadata
        """
        start_time = datetime.now()
        
        print(f"\n{'='*70}")
        print(f"🔄 SELF-HEALING RAG PIPELINE")
        print(f"{'='*70}")
        print(f"Query: {query}")
        print(f"{'='*70}\n")
        
        self.query_stats["total_queries"] += 1
        techniques_used = []
        
        # Step 1: Query Enhancement (Decomposition)
        sub_queries = [query]
        all_documents = []
        
        if enable_decomposition and self.query_decomposer.is_complex_query(query):
            print("📊 STEP 1: Query Decomposition")
            print("-" * 70)
            try:
                sub_queries = self.query_decomposer.decompose(query)
                if len(sub_queries) > 1:
                    print(f"  ✓ Decomposed into {len(sub_queries)} sub-queries:")
                    for i, sq in enumerate(sub_queries, 1):
                        print(f"    {i}. {sq}")
                    
                    # Retrieve for each sub-query
                    for sq in sub_queries:
                        docs = self.enhanced_retrieve(sq, use_hyde=enable_hyde, top_k=3)
                        all_documents.extend(docs)
                    
                    self.query_stats["decomposed_queries"] += 1
                    techniques_used.append("Query Decomposition")
                else:
                    all_documents = self.enhanced_retrieve(query, use_hyde=enable_hyde)
            except Exception as e:
                print(f"  ⚠ Decomposition error: {e}")
                all_documents = self.enhanced_retrieve(query, use_hyde=enable_hyde)
        else:
            print("📊 STEP 1: Standard Retrieval")
            print("-" * 70)
            all_documents = self.enhanced_retrieve(query, use_hyde=enable_hyde)
        
        if enable_hyde:
            techniques_used.append("HyDE")
        
        print(f"\n  📄 Total documents retrieved: {len(all_documents)}\n")
        
        # Step 2: Document Validation (CRAG)
        filtered_docs = all_documents
        if enable_crag and all_documents:
            print("🔍 STEP 2: CRAG Document Validation")
            print("-" * 70)
            try:
                result = self.crag_system.run(query, all_documents)
                filtered_docs = result.get("documents", all_documents)
                
                removed = len(all_documents) - len(filtered_docs)
                if removed > 0:
                    print(f"  🚨 Filtered out {removed} irrelevant document(s)")
                    self.query_stats["crag_activated"] += 1
                    techniques_used.append("CRAG")
                else:
                    print(f"  ✓ All documents passed relevance check")
            except Exception as e:
                print(f"  ⚠ CRAG error: {e}")
                filtered_docs = all_documents
        
        print(f"\n  📄 Documents after CRAG: {len(filtered_docs)}\n")
        
        # Step 3: Precision Reranking
        final_docs = filtered_docs
        if enable_reranking and len(filtered_docs) > 1:
            print("🎯 STEP 3: Cross-Encoder Reranking")
            print("-" * 70)
            try:
                doc_texts = [doc.page_content for doc in filtered_docs]
                reranked_texts = self.reranker.rerank(query, doc_texts, top_k=min(5, len(doc_texts)))
                
                # Map back to Document objects
                final_docs = []
                for text in reranked_texts:
                    for doc in filtered_docs:
                        if doc.page_content == text:
                            final_docs.append(doc)
                            break
                
                print(f"  ✓ Reranked to top {len(final_docs)} documents")
                self.query_stats["reranked"] += 1
                techniques_used.append("Cross-Encoder Reranking")
            except Exception as e:
                print(f"  ⚠ Reranking error: {e}")
                final_docs = filtered_docs[:5]
        
        print(f"\n  📄 Final documents: {len(final_docs)}\n")
        
        # Step 4: Dynamic Few-Shot Learning
        few_shot_context = ""
        if enable_learning:
            print("🧠 STEP 4: Dynamic Few-Shot Learning")
            print("-" * 70)
            try:
                few_shot_context = self.learning_manager.get_dynamic_prompt(query)
                if few_shot_context:
                    self.query_stats["learning_applied"] += 1
                    techniques_used.append("Dynamic Learning")
                    print("  ✓ Applied learned examples")
                else:
                    print("  ℹ No relevant past examples found")
            except Exception as e:
                print(f"  ⚠ Learning error: {e}")
        
        print()
        
        # Step 5: Answer Generation
        print("✍️ STEP 5: Answer Generation")
        print("-" * 70)
        answer = self.generate_answer(query, final_docs, few_shot_context)
        print("  ✓ Answer generated\n")
        
        # Calculate processing time
        end_time = datetime.now()
        processing_time = (end_time - start_time).total_seconds()
        
        # Update stats
        n = self.query_stats["total_queries"]
        self.query_stats["avg_processing_time"] = (
            (self.query_stats["avg_processing_time"] * (n - 1) + processing_time) / n
        )
        
        result = {
            "query": query,
            "sub_queries": sub_queries,
            "answer": answer,
            "documents_retrieved": len(all_documents),
            "documents_after_crag": len(filtered_docs),
            "final_documents": len(final_docs),
            "document_contents": [doc.page_content[:200] + "..." for doc in final_docs[:3]],
            "processing_time": round(processing_time, 2),
            "techniques_used": techniques_used,
            "timestamp": datetime.now().isoformat()
        }
        
        print(f"{'='*70}")
        print(f"✅ Pipeline completed in {processing_time:.2f}s")
        print(f"📊 Techniques: {', '.join(techniques_used)}")
        print(f"{'='*70}\n")
        
        return result
    
    def generate_answer(
        self,
        query: str,
        documents: List[Document],
        few_shot_context: str = ""
    ) -> str:
        """
        Generate answer from documents
        
        Args:
            query: User query
            documents: Retrieved and validated documents
            few_shot_context: Optional few-shot examples
            
        Returns:
            Generated answer
        """
        if not documents:
            return "I apologize, but I couldn't find relevant information to answer your question."
        
        # Combine document content
        context = "\n\n".join([
            f"[Document {i+1}]\n{doc.page_content}"
            for i, doc in enumerate(documents[:3])
        ])
        
        # Build prompt
        prompt_parts = []
        
        if few_shot_context:
            prompt_parts.append(few_shot_context)
            prompt_parts.append("\n---\n")
        
        prompt_parts.extend([
            "You are a technical assistant answering questions about RAG systems and AI.",
            "Provide accurate, concise answers based on the context below.\n",
            "Context:",
            context,
            f"\nQuestion: {query}",
            "\nProvide a clear, technical answer:"
        ])
        
        prompt = "\n".join(prompt_parts)
        
        try:
            response = self.llm.complete(prompt)
            return response.text.strip()
        except Exception as e:
            return f"Error generating answer: {e}"
    
    def add_feedback(self, query: str, answer: str, is_positive: bool):
        """
        Add user feedback to learning system
        
        Args:
            query: Original query
            answer: Generated answer
            is_positive: Whether feedback is positive
        """
        if is_positive:
            self.learning_manager.add_good_example(
                query=query,
                answer=answer,
                feedback_score=1.0
            )
            print("📚 ✓ Added to learning system")
    
    def get_statistics(self) -> Dict[str, Any]:
        """Get system performance statistics"""
        stats = self.query_stats.copy()
        stats["learning_examples"] = len(self.learning_manager.good_examples)
        
        # Calculate rates
        total = max(1, stats["total_queries"])
        stats["hyde_rate"] = f"{(stats['hyde_used'] / total * 100):.1f}%"
        stats["decomposition_rate"] = f"{(stats['decomposed_queries'] / total * 100):.1f}%"
        stats["crag_rate"] = f"{(stats['crag_activated'] / total * 100):.1f}%"
        stats["reranking_rate"] = f"{(stats['reranked'] / total * 100):.1f}%"
        stats["learning_rate"] = f"{(stats['learning_applied'] / total * 100):.1f}%"
        stats["avg_processing_time"] = f"{stats['avg_processing_time']:.2f}s"
        
        return stats
