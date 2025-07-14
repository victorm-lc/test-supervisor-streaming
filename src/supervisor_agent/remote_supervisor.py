from langgraph_supervisor import create_supervisor
from langgraph.pregel.remote import RemoteGraph
from langchain_openai import ChatOpenAI 

remote_agent = RemoteGraph(
            "research_agent", 
            url="http://localhost:2024"
        )
        
        # Create supervisor
supervisor = create_supervisor(
            agents=[remote_agent],
            model=ChatOpenAI(model="gpt-4o-mini")
        )

app = supervisor.compile()