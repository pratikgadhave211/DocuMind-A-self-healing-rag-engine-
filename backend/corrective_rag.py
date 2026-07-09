"""
CRAG (Corrective RAG) Module

Implements self-correction mechanism that grades retrieved documents for relevance.
If documents are deemed irrelevant, the system triggers alternative retrieval strategies.
"""

from typing import List, TypedDict, Literal
from langchain_core.prompts import PromptTemplate
from langchain_core.documents import Document
from langchain_tavily import TavilySearch
from langchain_nvidia_ai_endpoints import ChatNVIDIA
from langgraph.graph import END, StateGraph, START
from langgraph.checkpoint.memory import MemorySaver
from pydantic import BaseModel

# --- State Definition ---
class GraphState(BaseModel):
    """State for CRAG workflow"""
    question: str
    generation: str
    web_search: str  # 'Yes' or 'No' flag
    documents: List[Document]


class GradeScore(BaseModel):
    """Binary relevance score"""
    score: Literal["yes", "no"]


class CRAGSystem:
    """Corrective RAG system with document grading and fallback"""
    
    def __init__(
        self,
        grader_model: str = "meta/llama-3.1-8b-instruct",
        generator_model: str = "meta/llama-3.1-8b-instruct",
        web_search_enabled: bool = True,
        tavily_api_key: str = None
    ):
        """
        Initialize CRAG system
        
        Args:
            grader_model: LLM for document grading
            generator_model: LLM for answer generation
            web_search_enabled: Whether to enable web search fallback
            tavily_api_key: API key for Tavily search (optional)
        """
        self.grader_llm = ChatNVIDIA(model=grader_model, temperature=0)
        self.generator_llm = ChatNVIDIA(model=generator_model, temperature=0)
        self.web_search_enabled = web_search_enabled
        
        if web_search_enabled and tavily_api_key:
            self.web_tool = TavilySearch(max_results=3, api_key=tavily_api_key)
        else:
            self.web_tool = None
            
        # Initialize MemorySaver
        self.memory = MemorySaver()
        
        # Build graph
        self.app = self._build_graph()
    
    def grade_documents(self, state: GraphState) -> GraphState:
        """
        Self-healing core: Filter low-quality documents
        
        Args:
            state: Current graph state
            
        Returns:
            Updated state with filtered documents
        """
        print("---CHECK DOCUMENT RELEVANCE---")
        question = state.question
        documents = state.documents
        
        # Structured output for binary classification
        structured_llm = self.grader_llm.with_structured_output(GradeScore)
        
        prompt = PromptTemplate(
            template="""You are a grader assessing the relevance of a retrieved document to a user query.
            
Document: {context}

Query: {question}

Evaluate if the document contains useful context or evidence related to the user's query. It does not need to answer the question completely on its own, but it should provide relevant information.

Return JSON with a single key 'score':
- 'yes': Document provides useful context or evidence for the query.
- 'no': Document is completely irrelevant or off-topic.""",
            input_variables=["context", "question"],
        )
        chain = prompt | structured_llm
        
        filtered_docs = []
        web_search = "No"
        
        for d in documents:
            try:
                grade = chain.invoke({
                    "question": question,
                    "context": d.page_content
                })
                
                if grade.score == 'yes':
                    print(f"  ✓ Document relevant")
                    filtered_docs.append(d)
                else:
                    print(f"  ✗ Document not relevant - triggering fallback")
                    web_search = "Yes"
            except Exception as e:
                print(f"  ⚠ Error grading document: {e}")
                # On error, keep the document
                filtered_docs.append(d)
        
        return {
            "documents": filtered_docs,
            "question": question,
            "web_search": web_search,
            "generation": getattr(state, "generation", "")
        }
    
    def transform_query(self, state: GraphState) -> GraphState:
        """
        Self-correction: Rewrite query to improve web search effectiveness
        
        Args:
            state: Current graph state
            
        Returns:
            Updated state with rewritten query
        """
        print("---TRANSFORM QUERY FOR WEB SEARCH---")
        question = state.question
        
        prompt = PromptTemplate(
            template="""Rewrite the following query to make it more effective for semantic vector search within a local document database.
Extract the core intent and keywords. Do not optimize for web search engines, optimize for finding relevant text chunks in documents.

Original query: {question}

Rewritten query:""",
            input_variables=["question"]
        )
        
        chain = prompt | self.generator_llm
        better_q = chain.invoke({"question": question}).content
        
        print(f"  Original: {question}")
        print(f"  Rewritten: {better_q}")
        
        return {
            "question": better_q,
            "documents": state.documents,
            "web_search": state.web_search,
            "generation": getattr(state, "generation", "")
        }
    
    def web_search_node(self, state: GraphState) -> GraphState:
        """
        Web search fallback when retrieved documents are insufficient
        
        Args:
            state: Current graph state
            
        Returns:
            Updated state with web search results
        """
        print("---WEB SEARCH FALLBACK---")
        
        if not self.web_tool:
            print("  ⚠ Web search not available")
            return {
                "documents": state.documents,
                "question": state.question,
                "web_search": state.web_search,
                "generation": getattr(state, "generation", "")
            }
        
        try:
            docs = self.web_tool.invoke({"query": state.question})
            web_results = [
                Document(page_content=d["content"], metadata={"source": "web"})
                for d in docs
            ]
            print(f"  ✓ Retrieved {len(web_results)} documents from web")
            
            # Append web results to existing documents
            return {
                "documents": state.documents + web_results,
                "question": state.question,
                "web_search": state.web_search,
                "generation": getattr(state, "generation", "")
            }
        except Exception as e:
            print(f"  ⚠ Web search error: {e}")
            return {
                "documents": state.documents,
                "question": state.question,
                "web_search": state.web_search,
                "generation": getattr(state, "generation", "")
            }
    
    def generate(self, state: GraphState) -> GraphState:
        """
        Generate final answer from documents
        
        Args:
            state: Current graph state
            
        Returns:
            Updated state with generated answer
        """
        print("---GENERATE ANSWER---")
        
        question = state.question
        documents = state.documents
        
        # Combine document content
        context = "\n\n".join([doc.page_content for doc in documents[:5]])
        
        prompt = PromptTemplate(
            template="""Answer the question based on the following context.
Be concise and factual. If the context doesn't contain enough information, say so.

Context:
{context}

Question: {question}

Answer:""",
            input_variables=["context", "question"]
        )
        
        chain = prompt | self.generator_llm
        answer = chain.invoke({"context": context, "question": question}).content
        
        return {
            "question": state.question,
            "documents": state.documents,
            "web_search": state.web_search,
            "generation": answer
        }
    
    def decide_to_generate(self, state: GraphState) -> str:
        """
        Decision node: Generate answer or trigger web search
        
        Args:
            state: Current graph state
            
        Returns:
            Next node name
        """
        if state.web_search == "Yes":
            print("  → Triggering web search")
            return "transform_query"
        else:
            print("  → Proceeding to generation")
            return "generate"
    
    def _build_graph(self) -> StateGraph:
        """Build the CRAG workflow graph"""
        workflow = StateGraph(GraphState)
        
        # Add nodes
        workflow.add_node("grade_documents", self.grade_documents)
        workflow.add_node("transform_query", self.transform_query)
        workflow.add_node("web_search_node", self.web_search_node)
        workflow.add_node("generate", self.generate)
        
        # Add edges
        workflow.add_edge(START, "grade_documents")
        
        # Conditional routing after grading
        workflow.add_conditional_edges(
            "grade_documents",
            self.decide_to_generate,
            {
                "transform_query": "transform_query",
                "generate": "generate"
            }
        )
        
        workflow.add_edge("transform_query", "web_search_node")
        workflow.add_edge("web_search_node", "generate")
        workflow.add_edge("generate", END)
        
        return workflow.compile(checkpointer=self.memory)
    
    def run(self, question: str, documents: List[Document], thread_id: str = "default") -> dict:
        """
        Run CRAG pipeline
        
        Args:
            question: User question
            documents: Retrieved documents to grade
            thread_id: Thread ID for memory saver checkpointing
            
        Returns:
            Final state with answer
        """
        initial_state = GraphState(
            question=question,
            generation="",
            web_search="No",
            documents=documents
        )
        
        config = {"configurable": {"thread_id": thread_id}}
        result = self.app.invoke(initial_state, config=config)
        return result
