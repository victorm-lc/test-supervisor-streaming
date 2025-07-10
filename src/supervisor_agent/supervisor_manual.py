"""
Supervisor using RemoteGraph agents with create_supervisor.
"""
import os
from dotenv import load_dotenv

from langchain_openai import ChatOpenAI
from langgraph.pregel.remote import RemoteGraph
from langgraph_supervisor import create_supervisor

load_dotenv()
DEPLOYMENT_URL = "https://streaming-debugging-vz-73d732f1d7fc5ef4a1a86ce794e31132.us.langgraph.app"

# Create RemoteGraph connections to the deployed agents
# The name parameter is crucial for create_supervisor to identify the agents
research_agent = RemoteGraph(
    "9dc0ca3b-1aa6-547d-93f0-e21597d2011c", 
    url=DEPLOYMENT_URL,
    name="research_agent"  # This name will be used by create_supervisor
)

analysis_agent = RemoteGraph(
    "42b04058-5c00-5325-81b3-6e60ee822c24", 
    url=DEPLOYMENT_URL,
    name="analysis_agent"  # This name will be used by create_supervisor
)

# Create the supervisor
llm = ChatOpenAI(model="gpt-4o", temperature=0)

supervisor = create_supervisor(
    agents=[research_agent, analysis_agent],
    model=llm,
    prompt=(
        "You are a supervisor managing two agents:\n"
        "- research_agent: for information gathering, web searches, and academic research\n" 
        "- analysis_agent: for market analysis, technical analysis, and data interpretation\n"
        "Assign work to one agent at a time, do not call agents in parallel.\n"
        "Do not do any work yourself."
    ),
)

# Compile the graph
graph = supervisor.compile()