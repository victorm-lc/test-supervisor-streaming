"""
Research Agent with stream_writer for custom events.
Deploy with: langgraph dev --port 8001
"""
from langchain_openai import ChatOpenAI
from langchain_core.tools import tool
from langgraph.prebuilt import create_react_agent
from langgraph.types import StreamWriter
from langgraph.pregel import get_stream_writer

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

# Create the agent
llm = ChatOpenAI(model="gpt-4o")
tools = [google_search, academic_search]
graph = create_react_agent(llm, tools)