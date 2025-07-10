"""
Test RemoteGraph + Supervisor setup with custom event streaming.
This version uses scratch-built agents instead of create_react_agent.
"""
import os
from typing import Dict, Any
from dotenv import load_dotenv

from langchain_openai import ChatOpenAI
from langgraph_supervisor import create_supervisor
from langgraph.pregel.remote import RemoteGraph
from langgraph.graph import MessagesState

load_dotenv()
DEPLOYMENT_URL = "https://streaming-debugging-vz-73d732f1d7fc5ef4a1a86ce794e31132.us.langgraph.app"
# DEPLOYMENT_URL = "http://localhost:2024"

llm = ChatOpenAI(model="gpt-4o")
    
research_agent = RemoteGraph("research_agent_scratch", url=DEPLOYMENT_URL, name="research_agent_scratch")
analysis_agent = RemoteGraph("analysis_agent_scratch", url=DEPLOYMENT_URL, name="analysis_agent_scratch")

prompt = """
You are a supervisor agent. You are responsible for coordinating the research and analysis agents.
"""

supervisor = create_supervisor(
    model=llm,
    agents=[research_agent, analysis_agent],
    prompt=prompt
)

graph = supervisor.compile()

    