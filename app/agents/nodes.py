from typing import TypedDict, List
from langchain_ollama import OllamaLLM
from langchain.prompts import PromptTemplate
from app.config import get_settings
from app.utils.vectorstore import get_vectorstore

settings = get_settings()

class GraphState(TypedDict):
    """State of the graph"""
    question: str
    context: List[str]
    answer: str
    relevance_score: float

def retrieve_documents(state: GraphState) -> GraphState:
    """Retrieve relevant documents from vector store"""
    question = state["question"]
    vectorstore = get_vectorstore()
    
    # Perform similarity search
    docs = vectorstore.similarity_search(question, k=4)
    context = [doc.page_content for doc in docs]
    
    return {**state, "context": context}

def check_relevance(state: GraphState) -> GraphState:
    """Check if retrieved documents are relevant"""
    llm = OllamaLLM(
        model=settings.llm_model,
        base_url=settings.ollama_base_url
    )
    
    prompt = PromptTemplate(
        template="""You are a relevance checker. Determine if the context is relevant to answer the question.
        
Question: {question}
Context: {context}

Rate relevance from 0 to 1. Reply with only the number.
Relevance score:""",
        input_variables=["question", "context"]
    )
    
    chain = prompt | llm
    result = chain.invoke({
        "question": state["question"],
        "context": "\n\n".join(state["context"])
    })
    
    try:
        relevance_score = float(result.strip())
    except:
        relevance_score = 0.5
    
    return {**state, "relevance_score": relevance_score}

def generate_answer(state: GraphState) -> GraphState:
    """Generate answer using LLM"""
    llm = OllamaLLM(
        model=settings.llm_model,
        base_url=settings.ollama_base_url
    )
    
    prompt = PromptTemplate(
        template="""You are a helpful assistant. Answer the question based on the provided context.
        
Context: {context}

Question: {question}

Provide a detailed and accurate answer based only on the context provided. If the context doesn't contain enough information, say so.

Answer:""",
        input_variables=["context", "question"]
    )
    
    chain = prompt | llm
    answer = chain.invoke({
        "context": "\n\n".join(state["context"]),
        "question": state["question"]
    })
    
    return {**state, "answer": answer}
