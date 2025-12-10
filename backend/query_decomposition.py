"""
Query Decomposition Module

Breaks down complex queries into atomic sub-queries that can be
individually processed and then combined for comprehensive answers.
"""

from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate
from pydantic import BaseModel, Field
from typing import List


class SubQueries(BaseModel):
    """Collection of sub-queries to retrieve"""
    questions: List[str] = Field(description="List of atomic sub-questions.")


class QueryDecomposer:
    """Decomposes complex queries into simpler sub-queries"""
    
    def __init__(self, model: str = "gpt-4o-mini", temperature: float = 0):
        """
        Initialize query decomposer
        
        Args:
            model: LLM model to use for planning
            temperature: Temperature for generation (0 for deterministic)
        """
        self.llm = ChatOpenAI(model=model, temperature=temperature)
        
        system_prompt = """You are an expert researcher. Break down the user's complex query 
into simple, atomic sub-queries that a search engine can answer independently.

Guidelines:
- Each sub-query should be self-contained and answerable on its own
- Aim for 2-4 sub-queries for complex questions
- Keep sub-queries concise and focused
- For simple questions, return just the original query"""

        self.prompt = ChatPromptTemplate.from_messages([
            ("system", system_prompt),
            ("human", "{query}")
        ])
        
        # Build processing chain with structured output
        self.planner = self.prompt | self.llm.with_structured_output(SubQueries)
    
    def decompose(self, query: str) -> List[str]:
        """
        Decompose query into sub-queries
        
        Args:
            query: Complex user query
            
        Returns:
            List of atomic sub-queries
        """
        result = self.planner.invoke({"query": query})
        return result.questions
    
    def is_complex_query(self, query: str) -> bool:
        """
        Determine if query needs decomposition
        
        Args:
            query: User query
            
        Returns:
            True if query should be decomposed
        """
        # Heuristics for complex queries
        complexity_indicators = [
            " and ",
            " vs ",
            " versus ",
            " compare ",
            " difference between ",
            " both ",
            "?",  # Multiple question marks
        ]
        
        query_lower = query.lower()
        
        # Check for multiple clauses or comparison patterns
        return any(indicator in query_lower for indicator in complexity_indicators)


# Convenience function
def plan_query(query: str, model: str = "gpt-4o-mini") -> List[str]:
    """
    Quick function to decompose a query
    
    Args:
        query: User query to decompose
        model: LLM model to use
        
    Returns:
        List of sub-queries
    """
    decomposer = QueryDecomposer(model=model)
    return decomposer.decompose(query)
