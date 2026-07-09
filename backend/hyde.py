"""
HyDE (Hypothetical Document Embeddings) Module — FAISS edition

HyDE improves retrieval by generating a hypothetical document that answers the
query, then searching for real documents whose embeddings are similar to that
hypothetical document.  This implementation works directly on a LangChain FAISS
retriever so LlamaIndex is no longer required for this step.
"""

from typing import List
from langchain_core.documents import Document


class HyDERetriever:
    """
    Standalone HyDE retriever that wraps any LangChain vectorstore retriever.

    Pipeline:
        1. Use the LLM to generate a short *hypothetical* document that would
           perfectly answer the user query.
        2. Use the hypothetical document text as the search query against the
           FAISS vector store.  Because the hypothetical document uses domain
           vocabulary similar to what real documents contain, the embedding
           similarity is much stronger than a raw short question.
        3. Return the retrieved real documents.
    """

    def __init__(self, vectorstore, llm, top_k: int = 5, include_original: bool = True):
        """
        Args:
            vectorstore: A LangChain FAISS vectorstore instance.
            llm: Any object with a `.complete(prompt) -> SimpleNamespace(text=...)` interface.
            top_k: Number of documents to retrieve.
            include_original: If True, also retrieve using the original query and
                              merge the results (deduplicating by content).
        """
        self.vectorstore = vectorstore
        self.llm = llm
        self.top_k = top_k
        self.include_original = include_original

    def _generate_hypothetical_doc(self, query: str) -> str:
        """Ask the LLM to write a short passage that answers the query."""
        prompt = (
            "Write a short, factual passage (2–4 sentences) that directly answers "
            f"the following question. Do not include the question itself.\n\n"
            f"Question: {query}\n\nPassage:"
        )
        try:
            resp = self.llm.complete(prompt)
            return resp.text.strip()
        except Exception as e:
            print(f"  ⚠ HyDE generation failed: {e}. Falling back to original query.")
            return query

    def retrieve(self, query: str) -> List[Document]:
        """
        Retrieve documents using the HyDE strategy.

        Returns a deduplicated list of LangChain Document objects.
        """
        hyp_doc = self._generate_hypothetical_doc(query)
        print(f"  🧠 HyDE hypothetical doc (truncated): {hyp_doc[:120]}…")

        seen_contents = set()
        results: List[Document] = []

        # Retrieve using the hypothetical document
        for doc in self.vectorstore.similarity_search(hyp_doc, k=self.top_k):
            key = doc.page_content[:200]
            if key not in seen_contents:
                seen_contents.add(key)
                results.append(doc)

        # Optionally also retrieve using the original query
        if self.include_original:
            for doc in self.vectorstore.similarity_search(query, k=self.top_k):
                key = doc.page_content[:200]
                if key not in seen_contents:
                    seen_contents.add(key)
                    results.append(doc)

        return results[: self.top_k * 2]  # cap total


def build_hyde_retriever(vectorstore, llm, top_k: int = 5, include_original: bool = True) -> HyDERetriever:
    """
    Convenience factory for HyDERetriever.

    Args:
        vectorstore: LangChain FAISS vectorstore.
        llm: LLM with `.complete()` interface.
        top_k: Documents per search.
        include_original: Whether to also search with the original query.

    Returns:
        Configured HyDERetriever.
    """
    return HyDERetriever(
        vectorstore=vectorstore,
        llm=llm,
        top_k=top_k,
        include_original=include_original,
    )
