"""
Intent Analyzer Module

Classifies user queries into specific intents to route them to the most
effective retrieval and generation pipeline.
"""

from typing import Literal
from pydantic import BaseModel
from langchain_core.prompts import PromptTemplate
from langchain_nvidia_ai_endpoints import ChatNVIDIA

class IntentClassification(BaseModel):
    intent: Literal["qa", "global_review"]

class IntentAnalyzer:
    """Analyzes query intent for dynamic RAG pipeline routing."""
    
    def __init__(self, model: str = "meta/llama-3.1-8b-instruct"):
        self.llm = ChatNVIDIA(
            model=model,
            temperature=1,
            top_p=1,
            max_tokens=16384,
            seed=42
        )
        self.structured_llm = self.llm.with_structured_output(IntentClassification)
        
        self.prompt = PromptTemplate(
            template="""You are an AI routing assistant for a Document Analysis system.
Analyze the user's query and classify it into one of two categories:

1. 'global_review': The user is asking for a document-wide analysis, summary, review, critique, or rating. 
   Examples: "Rate my resume", "Summarize this document", "What are the main themes?", "Review this file".
2. 'qa': The user is asking a specific factual question that can be answered by finding a specific piece of information.
   Examples: "What is the applicant's GPA?", "Where did the author go to school?", "What does section 3 say?".

Query: {query}

Return JSON with a single key 'intent' containing either 'global_review' or 'qa'.""",
            input_variables=["query"]
        )
        self.chain = self.prompt | self.structured_llm

    def analyze(self, query: str) -> str:
        """
        Analyze the query and return the intent.
        Falls back to 'qa' on error.
        """
        try:
            result = self.chain.invoke({"query": query})
            return result.intent
        except Exception as e:
            print(f"  ⚠ Intent analysis failed: {e}. Defaulting to 'qa'.")
            return "qa"
