"""
Test RemoteGraph + Supervisor setup with custom event streaming.
This reproduces the customer's first use case.
"""
import os
from typing import Dict, Any
from dotenv import load_dotenv

from langchain_openai import ChatOpenAI
from langgraph_supervisor import create_supervisor
from langgraph.pregel.remote import RemoteGraph

load_dotenv()

# TODO: Replace with your own deployment URL or local URL if you're running langgraph dev 
# DEPLOYMENT_URL = "https://streaming-debugging-vz-73d732f1d7fc5ef4a1a86ce794e31132.us.langgraph.app"
DEPLOYMENT_URL = "http://localhost:2024"


llm = ChatOpenAI(model="gpt-4o")
    
research_agent = RemoteGraph("research_agent", url=DEPLOYMENT_URL, name="research_agent")
analysis_agent = RemoteGraph("analysis_agent", url=DEPLOYMENT_URL, name="analysis_agent")

prompt = """
You are a supervisor agent. You are responsible for coordinating the research and analysis agents.
"""

# Try with explicit state_schema and other parameters to work around schema union issues

supervisor = create_supervisor(
    model=llm,
    agents=[research_agent, analysis_agent],
    prompt=prompt
)

graph = supervisor.compile()