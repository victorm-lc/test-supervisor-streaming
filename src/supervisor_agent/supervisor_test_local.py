"""
Test create_supervisor with LOCAL agents to verify prebuilt functionality.
This helps isolate whether the issue is specifically with RemoteGraph.
"""
import os
from dotenv import load_dotenv

from langchain_openai import ChatOpenAI
from langchain_core.tools import tool
from langgraph_supervisor import create_supervisor
from langgraph.prebuilt import create_react_agent
from langgraph.config import get_stream_writer

load_dotenv()

# Create the same tools as in the remote agents
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

@tool
def market_analysis(company_or_sector: str) -> str:
    """Analyze market trends for a company or sector."""
    
    stream_writer = get_stream_writer()
    if stream_writer:
        stream_writer({"custom_event": "market_analysis_started", "target": company_or_sector})
        stream_writer({"custom_event": "data_collection", "sources": ["financial_reports", "market_data", "news"]})
        stream_writer({"custom_event": "trend_analysis", "trend_direction": "bullish", "confidence": 0.78})
        stream_writer({"custom_event": "risk_assessment", "risk_level": "moderate", "key_risks": 3})
        stream_writer({"custom_event": "market_analysis_completed", "recommendation": "buy", "target_price": 125.50})
    
    return f"Market analysis for {company_or_sector}: Bullish trend with 78% confidence. Recommendation: BUY with target price $125.50. Identified 3 key risks."

@tool
def technical_analysis(symbol: str) -> str:
    """Perform technical analysis on a stock symbol."""
    
    stream_writer = get_stream_writer()
    if stream_writer:
        stream_writer({"custom_event": "technical_analysis_started", "symbol": symbol})
        stream_writer({"custom_event": "indicator_calculated", "indicator": "RSI", "value": 65.4})
        stream_writer({"custom_event": "indicator_calculated", "indicator": "MACD", "signal": "bullish_crossover"})
        stream_writer({"custom_event": "support_resistance", "support": 118.20, "resistance": 127.80})
        stream_writer({"custom_event": "pattern_detected", "pattern": "ascending_triangle", "breakout_probability": 0.72})
        stream_writer({"custom_event": "technical_analysis_completed", "signal": "strong_buy", "confidence": 0.85})
    
    return f"Technical analysis for {symbol}: Strong BUY signal with 85% confidence. RSI at 65.4, MACD shows bullish crossover. Ascending triangle pattern detected with 72% breakout probability."

# Create LOCAL agents (same as the remote ones)
llm = ChatOpenAI(model="gpt-4o")

research_agent = create_react_agent(
    llm, 
    tools=[google_search, academic_search],
    name="research_agent"
)

analysis_agent = create_react_agent(
    llm, 
    tools=[market_analysis, technical_analysis],
    name="analysis_agent"
)

# Test create_supervisor with LOCAL agents
supervisor = create_supervisor(
    model=llm,
    agents=[research_agent, analysis_agent],
    prompt="""
    You are a supervisor agent. You are responsible for coordinating the research and analysis agents.
    """,
    add_handoff_back_messages=True
)

graph = supervisor.compile()