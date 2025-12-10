#!/usr/bin/env python3
"""
Self-Healing RAG System Demo Script

This script demonstrates how to use the RAG system programmatically.
Run this after starting the backend server.
"""

import sys
import os

# Add backend to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'backend'))

from dotenv import load_dotenv
from self_healing_rag import SelfHealingRAGSystem

# Load environment
load_dotenv()


def main():
    print("=" * 70)
    print("Self-Healing RAG System - Demo")
    print("=" * 70)
    print()
    
    # Initialize system
    print("🔧 Initializing system...")
    system = SelfHealingRAGSystem(
        openai_api_key=os.getenv("OPENAI_API_KEY"),
        enable_web_search=False
    )
    
    # Load sample documents
    print("📚 Loading sample documents...")
    system.load_sample_documents()
    print()
    
    # Demo queries
    demo_queries = [
        {
            "query": "What is RAG and how does it work?",
            "description": "Simple query - demonstrates basic pipeline"
        },
        {
            "query": "Compare HyDE and standard retrieval methods",
            "description": "Complex query - triggers decomposition"
        },
        {
            "query": "How does CRAG improve retrieval quality?",
            "description": "Technical query - shows self-correction"
        }
    ]
    
    results = []
    
    for i, item in enumerate(demo_queries, 1):
        query = item["query"]
        desc = item["description"]
        
        print(f"\n{'='*70}")
        print(f"Demo Query {i}/{len(demo_queries)}: {desc}")
        print(f"{'='*70}")
        print(f"Query: {query}")
        print(f"{'='*70}\n")
        
        # Process query
        result = system.process_query(
            query=query,
            enable_hyde=True,
            enable_decomposition=True,
            enable_crag=True,
            enable_reranking=True,
            enable_learning=True
        )
        
        results.append(result)
        
        # Display result
        print(f"\n{'='*70}")
        print("RESULT")
        print(f"{'='*70}")
        print(f"\nAnswer:\n{result['answer']}\n")
        print(f"Processing Time: {result['processing_time']}s")
        print(f"Documents: {result['documents_retrieved']} → {result['final_documents']}")
        print(f"Techniques Used: {', '.join(result['techniques_used'])}")
        print()
        
        # Simulate positive feedback for first query
        if i == 1:
            print("👍 Simulating positive feedback...")
            system.add_feedback(query, result['answer'], is_positive=True)
            print()
    
    # Display statistics
    print(f"\n{'='*70}")
    print("SYSTEM STATISTICS")
    print(f"{'='*70}")
    stats = system.get_statistics()
    
    print(f"\nTotal Queries: {stats['total_queries']}")
    print(f"Average Processing Time: {stats['avg_processing_time']}")
    print(f"Learned Examples: {stats['learning_examples']}")
    print()
    print("Technique Usage Rates:")
    print(f"  • HyDE: {stats['hyde_rate']}")
    print(f"  • Query Decomposition: {stats['decomposition_rate']}")
    print(f"  • CRAG: {stats['crag_rate']}")
    print(f"  • Reranking: {stats['reranking_rate']}")
    print(f"  • Dynamic Learning: {stats['learning_rate']}")
    print()
    
    print(f"{'='*70}")
    print("✅ Demo completed successfully!")
    print(f"{'='*70}")
    print()
    print("Next steps:")
    print("  • Launch the web UI with: ./start.sh")
    print("  • Access playground at: http://localhost:3000")
    print("  • View API docs at: http://localhost:8000/docs")
    print()


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n\n⚠️  Demo interrupted by user")
        sys.exit(0)
    except Exception as e:
        print(f"\n\n❌ Error: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)
