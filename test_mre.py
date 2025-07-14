import asyncio
from langchain_openai import ChatOpenAI
from langgraph.prebuilt import create_react_agent
from langgraph_supervisor import create_supervisor
from langgraph.config import get_stream_writer
from langchain_core.tools import tool

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

# Create agent with the tool
agent = create_react_agent(
    model=ChatOpenAI(model="gpt-4o"),
    tools=[analyze_data],
    name="analyst"
)

# Create supervisor
supervisor = create_supervisor(
    agents=[agent],
    model=ChatOpenAI(model="gpt-4o")
)
app = supervisor.compile()

async def main():
    """Run the streaming test."""
    print("Testing custom event streaming...")
    print("=" * 50)

# Stream with custom events - BEFORE FIX: No custom events appear!
    custom_events = []
async for mode, chunk in app.astream(
    {"messages": [{"role": "user", "content": "analyze the market"}]},
    stream_mode=["custom", "updates"]
):
    if mode == "custom":
            print(f"Custom event: {chunk}")
            custom_events.append(chunk)
    
    if not custom_events:
        print("\n❌ No custom events received (this is the bug!)")
    else:
        print(f"\n✅ Received {len(custom_events)} custom events")

if __name__ == "__main__":
    asyncio.run(main())