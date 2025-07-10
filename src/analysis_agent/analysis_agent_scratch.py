"""
Analysis Agent built from scratch with stream_writer for custom events.
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

# Define the tools
tools = [market_analysis, technical_analysis]
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