"""
Analysis Agent with stream_writer for custom events.
Deploy with: langgraph dev --port 8002
"""
from langchain_openai import ChatOpenAI
from langchain_core.tools import tool
from langgraph.prebuilt import create_react_agent
from langgraph.config import get_stream_writer
import json


@tool
def market_analysis(company_or_sector: str) -> str:
    """Analyze market trends for a company or sector."""
    
    # Collect custom events to return
    custom_events = []
    
    stream_writer = get_stream_writer()
    if stream_writer:
        events = [
            {"custom_event": "market_analysis_started", "target": company_or_sector},
            {"custom_event": "data_collection", "sources": ["financial_reports", "market_data", "news"]},
            {"custom_event": "trend_analysis", "trend_direction": "bullish", "confidence": 0.78},
            {"custom_event": "risk_assessment", "risk_level": "moderate", "key_risks": 3},
            {"custom_event": "market_analysis_completed", "recommendation": "buy", "target_price": 125.50}
        ]
        
        for event in events:
            stream_writer(event)
            custom_events.append(event)
    
    # Return both the analysis and custom events
    result = f"Market analysis for {company_or_sector}: Bullish trend with 78% confidence. Recommendation: BUY with target price $125.50. Identified 3 key risks."
    
    # Add custom events to the result for supervisor to use
    result += f"\n\n__CUSTOM_EVENTS__: {json.dumps(custom_events)}"
    
    return result

@tool
def technical_analysis(symbol: str) -> str:
    """Perform technical analysis on a stock symbol."""
    
    # Collect custom events to return
    custom_events = []
    
    stream_writer = get_stream_writer()
    if stream_writer:
        events = [
            {"custom_event": "technical_analysis_started", "symbol": symbol},
            {"custom_event": "indicator_calculated", "indicator": "RSI", "value": 65.4},
            {"custom_event": "indicator_calculated", "indicator": "MACD", "signal": "bullish_crossover"},
            {"custom_event": "support_resistance", "support": 118.20, "resistance": 127.80},
            {"custom_event": "pattern_detected", "pattern": "ascending_triangle", "breakout_probability": 0.72},
            {"custom_event": "technical_analysis_completed", "signal": "strong_buy", "confidence": 0.85}
        ]
        
        for event in events:
            stream_writer(event)
            custom_events.append(event)
    
    # Return both the analysis and custom events
    result = f"Technical analysis for {symbol}: Strong BUY signal with 85% confidence. RSI at 65.4, MACD shows bullish crossover. Ascending triangle pattern detected with 72% breakout probability."
    
    # Add custom events to the result for supervisor to use
    result += f"\n\n__CUSTOM_EVENTS__: {json.dumps(custom_events)}"
    
    return result

# Create the agent
llm = ChatOpenAI(model="gpt-4o")
tools = [market_analysis, technical_analysis]

graph = create_react_agent(llm, tools)