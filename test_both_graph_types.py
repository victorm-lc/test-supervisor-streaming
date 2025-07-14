"""
Test to confirm custom event streaming issue affects both local and remote graphs.
"""
import asyncio
from langchain_openai import ChatOpenAI
from langgraph.prebuilt import create_react_agent
from langgraph_supervisor import create_supervisor
from langgraph.config import get_stream_writer
from langchain_core.tools import tool
from langgraph.pregel.remote import RemoteGraph

# Create a tool that emits custom events
@tool
def analyze_data(query: str) -> str:
    """Analyze data and emit progress events."""
    stream_writer = get_stream_writer()
    if stream_writer:
        stream_writer({"progress": "Starting analysis", "step": 1})
        stream_writer({"progress": "Processing data", "step": 2})
        stream_writer({"progress": "Complete", "step": 3})
    return f"Analysis complete for: {query}"

async def test_local_graph():
    """Test with local create_react_agent."""
    print("\n🔧 Testing LOCAL graph (create_react_agent)")
    print("-" * 50)
    
    # Create local agent
    agent = create_react_agent(
        model=ChatOpenAI(model="gpt-4o-mini"),
        tools=[analyze_data],
        name="local_analyst"
    )
    
    # Create supervisor
    supervisor = create_supervisor(
        agents=[agent],
        model=ChatOpenAI(model="gpt-4o-mini")
    )
    app = supervisor.compile()
    
    # Stream and show ALL output
    print("\n📋 ALL STREAMING OUTPUT:")
    custom_events = []
    chunk_count = 0
    async for chunk in app.astream(
        {"messages": [{"role": "user", "content": "analyze the market"}]},
        stream_mode=["custom", "updates"],
        subgraphs=True
    ):
        chunk_count += 1
        # When using stream_mode with a list, chunk is a tuple of (mode, data)
        if isinstance(chunk, tuple) and len(chunk) == 2:
            mode, data = chunk
            print(f"\n  [{chunk_count}] Mode: {mode}")
            print(f"      Content: {data}")
            
            if mode == "custom":
                custom_events.append(data)
        else:
            # Handle the (namespace, mode, data) format from subgraphs
            print(f"\n  [{chunk_count}] Raw chunk: {chunk}")
            if isinstance(chunk, tuple) and len(chunk) == 3:
                namespace, mode, data = chunk
                if mode == "custom":
                    custom_events.append(data)
                    print(f"      ✅ CUSTOM EVENT DETECTED!")
    
    print(f"\n📊 Summary: {chunk_count} total chunks streamed")
    if custom_events:
        print(f"✅ Received {len(custom_events)} custom events")
    else:
        print("❌ No custom events received from LOCAL graph")
    
    return len(custom_events)

async def test_remote_graph():
    """Test with RemoteGraph (if available)."""
    print("\n🌐 Testing REMOTE graph (RemoteGraph)")
    print("-" * 50)
    
    try:
        # Try to connect to a RemoteGraph
        remote_agent = RemoteGraph(
            "research_agent", 
            url="http://localhost:2024",
            name="research_agent"
        )
        
        # Create supervisor
        supervisor = create_supervisor(
            agents=[remote_agent],
            model=ChatOpenAI(model="gpt-4o-mini")
        )
        app = supervisor.compile()
        
        # Stream and show ALL output
        print("\n📋 ALL STREAMING OUTPUT:")
        custom_events = []
        chunk_count = 0
        async for chunk in app.astream(
            {"messages": [{"role": "user", "content": "research AI trends"}]},
            stream_mode=["custom", "updates"],
            subgraphs=True
        ):
            chunk_count += 1
            # When using stream_mode with a list, chunk is a tuple of (mode, data)
            if isinstance(chunk, tuple) and len(chunk) == 2:
                mode, data = chunk
                print(f"\n  [{chunk_count}] Mode: {mode}")
                print(f"      Content: {data}")
                
                if mode == "custom":
                    custom_events.append(data)
            else:
                # Handle the (namespace, mode, data) format from subgraphs
                print(f"\n  [{chunk_count}] Raw chunk: {chunk}")
                if isinstance(chunk, tuple) and len(chunk) == 3:
                    namespace, mode, data = chunk
                    if mode == "custom":
                        custom_events.append(data)
                        print(f"      ✅ CUSTOM EVENT DETECTED!")
        
        print(f"\n📊 Summary: {chunk_count} total chunks streamed")
        if custom_events:
            print(f"✅ Received {len(custom_events)} custom events")
        else:
            print("❌ No custom events received from REMOTE graph")
        
        return len(custom_events)
        
    except Exception as e:
        print(f"⚠️  Could not test RemoteGraph: {e}")
        print("   (This is OK if you don't have a LangGraph server running)")
        return -1

async def main():
    """Run all tests."""
    print("=" * 70)
    print("Testing Custom Event Streaming with Original langgraph-supervisor")
    print("=" * 70)
    
    # Test local graph
    local_events = await test_local_graph()
    
    # Test remote graph
    remote_events = await test_remote_graph()
    
    # Summary
    print("\n" + "=" * 70)
    print("SUMMARY:")
    print("=" * 70)
    print(f"Local graph custom events:  {local_events} {'❌ BUG!' if local_events == 0 else '✅'}")
    print(f"Remote graph custom events: {remote_events if remote_events >= 0 else 'N/A'} {'❌ BUG!' if remote_events == 0 else '✅' if remote_events > 0 else ''}")

if __name__ == "__main__":
    asyncio.run(main()) 