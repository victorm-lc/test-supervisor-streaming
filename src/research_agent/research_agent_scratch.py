"""
Research Agent built from scratch with stream_writer for custom events.
This version uses StateGraph directly instead of create_react_agent.
"""
from typing import Literal
from typing_extensions import TypedDict

from langchain_openai import ChatOpenAI
from langchain_core.tools import tool
from langchain_core.messages import AIMessage, ToolMessage
from langgraph.graph import StateGraph, MessagesState, START, END
from langgraph.prebuilt import ToolNode
from langgraph.config import get_stream_writer

@tool
def google_search(query: str) -> str:
    """Search Google for information about a topic."""
    
    stream_writer = get_stream_writer()
    if stream_writer:
        stream_writer({"custom_event": "search_started", "query": query, "source": "google"})
        stream_writer({"custom_event": "search_progress", "status": "fetching_results"})
        stream_writer({"custom_event": "search_completed", "results_count": 10, "source": "google"})
    
    return f"Found 10 Google results for '{query}'. Top results include recent news articles and relevant websites."

@tool
def academic_search(topic: str) -> str:
    """Search academic databases for research papers on a topic."""
    
    stream_writer = get_stream_writer()
    if stream_writer:
        stream_writer({"custom_event": "academic_search_started", "topic": topic, "databases": ["arxiv", "pubmed"]})
        stream_writer({"custom_event": "database_queried", "database": "arxiv", "papers_found": 15})
        stream_writer({"custom_event": "database_queried", "database": "pubmed", "papers_found": 8})
        stream_writer({"custom_event": "academic_search_completed", "total_papers": 23})
    
    return f"Found 23 academic papers on '{topic}' from arXiv and PubMed. Recent publications show significant developments in the field."

# Define the tools
tools = [google_search, academic_search]
tool_node = ToolNode(tools)

# Initialize the model
model = ChatOpenAI(model="gpt-4o", temperature=0)
model_with_tools = model.bind_tools(tools)

# Define the agent state
class AgentState(MessagesState):
    pass

def call_model(state: AgentState):
    messages = state['messages']
    response = model_with_tools.invoke(messages)
    return {"messages": [response]}

def should_continue(state: AgentState) -> Literal["tools", "__end__"]:
    messages = state['messages']
    last_message = messages[-1]
    
    # If the LLM makes a tool call, then we route to the "tools" node
    if last_message.tool_calls:
        return "tools"
    # Otherwise, we stop (this is the end of the conversation)
    return "__end__"

# Define the graph
workflow = StateGraph(AgentState)

# Define the two nodes we will cycle between
workflow.add_node("agent", call_model)
workflow.add_node("tools", tool_node)

# Set the entrypoint as `agent`
workflow.add_edge(START, "agent")

# Add conditional edges
workflow.add_conditional_edges(
    "agent",
    should_continue,
    {
        "tools": "tools",
        "__end__": END,
    },
)

# Add normal edge from `tools` to `agent`
workflow.add_edge("tools", "agent")

# Compile the graph
graph = workflow.compile() 