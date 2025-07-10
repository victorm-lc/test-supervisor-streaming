"""
Test RemoteGraph + Supervisor setup with custom event streaming.
This reproduces the customer's first use case.
"""
import os
from typing import Dict, Any
from dotenv import load_dotenv

from langchain_openai import ChatOpenAI
from langgraph_supervisor import create_supervisor
from langgraph.graph import RemoteGraph
from langgraph.types import StreamWriter

load_dotenv()



llm = ChatOpenAI(model="gpt-4o")
    
research_agent = RemoteGraph(url="http://localhost:8001")
analysis_agent = RemoteGraph(url="http://localhost:8002")
    
supervisor = create_supervisor(
        model=llm,
        agents= [research_agent, analysis_agent]
    )
    
