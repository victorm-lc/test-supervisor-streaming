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
from langgraph.graph import MessagesState

load_dotenv()

# TODO: Replace with your own deployment URL or local URL if you're running langgraph dev 
DEPLOYMENT_URL = "http://localhost:2024"

llm = ChatOpenAI(model="gpt-4o")
    
research_agent = RemoteGraph("research_agent", url=DEPLOYMENT_URL)
analysis_agent = RemoteGraph("analysis_agent", url=DEPLOYMENT_URL)

prompt = """
You are a supervisor agent. You are responsible for coordinating the research and analysis agents.
"""

# Try with explicit state_schema and other parameters to work around schema union issues
try:
    supervisor = create_supervisor(
        model=llm,
        agents=[research_agent, analysis_agent],
        prompt=prompt
    )
    
    graph = supervisor.compile()
    print("✓ Successfully created supervisor with RemoteGraph agents")
    
except Exception as e:
    print(f"✗ Failed to create supervisor: {e}")
    print("This confirms the schema union issue with RemoteGraph objects")
    
    # Document the specific error for the customer investigation
    with open("supervisor_error_log.txt", "w") as f:
        f.write(f"Error creating supervisor with RemoteGraph:\n{str(e)}\n")
        f.write(f"Error type: {type(e)}\n")
        import traceback
        f.write(f"Traceback:\n{traceback.format_exc()}\n")
    
    raise  # Re-raise to see the full error