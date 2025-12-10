"""
HyDE (Hypothetical Document Embeddings) Module

HyDE improves retrieval by generating hypothetical documents that answer the query,
then searching for real documents similar to these hypothetical ones.
"""

from llama_index.core import VectorStoreIndex, SimpleDirectoryReader, Settings
from llama_index.core.indices.query.query_transform import HyDEQueryTransform
from llama_index.core.query_engine import TransformQueryEngine
from llama_index.llms.openai import OpenAI


def build_hyde_engine(index, include_original: bool = True, similarity_top_k: int = 5):
    """
    Build HyDE query engine
    
    Args:
        index: VectorStoreIndex to search
        include_original: Whether to search both original query and hypothetical doc
        similarity_top_k: Number of documents to retrieve
    
    Returns:
        TransformQueryEngine with HyDE transformation
    """
    # Initialize HyDE transformation
    hyde = HyDEQueryTransform(include_original=include_original)
    
    # Create base retrieval engine
    base_query_engine = index.as_query_engine(similarity_top_k=similarity_top_k)
    
    # Wrap with TransformQueryEngine
    # This middleware intercepts the query, generates hypothetical document, then searches
    hyde_engine = TransformQueryEngine(base_query_engine, query_transform=hyde)
    
    return hyde_engine


def configure_hyde_llm(model: str = "gpt-4o-mini", temperature: float = 0.7):
    """
    Configure LLM for hypothetical document generation
    
    Args:
        model: OpenAI model to use
        temperature: Creativity level for generation
    """
    Settings.llm = OpenAI(model=model, temperature=temperature)
