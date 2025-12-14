from langgraph.graph import StateGraph, END
from app.agents.nodes import GraphState, retrieve_documents, check_relevance, generate_answer

def should_continue(state: GraphState) -> str:
    """Determine if we should continue or end"""
    if state["relevance_score"] > 0.5:
        return "generate"
    else:
        return "end"

def create_workflow():
    """Create the LangGraph workflow"""
    workflow = StateGraph(GraphState)
    
    # Add nodes
    workflow.add_node("retrieve", retrieve_documents)
    workflow.add_node("check_relevance", check_relevance)
    workflow.add_node("generate", generate_answer)
    
    # Add edges
    workflow.set_entry_point("retrieve")
    workflow.add_edge("retrieve", "check_relevance")
    workflow.add_conditional_edges(
        "check_relevance",
        should_continue,
        {
            "generate": "generate",
            "end": END
        }
    )
    workflow.add_edge("generate", END)
    
    return workflow.compile()

# Create compiled graph
app_graph = create_workflow()
