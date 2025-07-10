"""
Test script for the manual supervisor with RemoteGraph agents.
"""
import os
from dotenv import load_dotenv

load_dotenv()

def test_manual_supervisor():
    print("Testing Manual Supervisor with RemoteGraph agents...")
    
    # Import the manual supervisor
    from src.supervisor_agent.supervisor_manual import graph
    
    # Test with a research task
    print("\n1. Testing research task delegation:")
    result = graph.invoke({
        "messages": [{"role": "user", "content": "Research the latest developments in artificial intelligence"}]
    })
    
    print(f"Final response: {result['messages'][-1].content}")
    
    # Test with an analysis task  
    print("\n2. Testing analysis task delegation:")
    result = graph.invoke({
        "messages": [{"role": "user", "content": "Perform market analysis on Tesla stock"}]
    })
    
    print(f"Final response: {result['messages'][-1].content}")
    
    print("\n✓ Manual supervisor test completed successfully")

if __name__ == "__main__":
    test_manual_supervisor() 