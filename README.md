# LangGraph Supervisor Custom Event Streaming Issue

This repository demonstrates an issue with `create_supervisor` in langgraph-supervisor where custom events from sub-agents are not forwarded to the parent stream.

## The Problem

When using `create_supervisor` with agents that emit custom events (via `stream_writer`), these events are lost because the supervisor uses `agent.invoke()` instead of `agent.astream()`. This affects:

- ❌ Custom events from tools
- ❌ LLM token streaming  
- ❌ Debug information
- ❌ Both local graphs (create_react_agent) and RemoteGraphs

## Quick Test

```bash
# Install dependencies
uv sync

# Test the issue with current langgraph-supervisor
python test_mre.py
# Output: ❌ No custom events received (this is the bug!)

# Test both local and remote graphs
python test_both_graph_types.py
```

## Repository Structure

```
├── test_mre.py                    # Minimal reproducible example
├── test_both_graph_types.py       # Test showing issue affects all graph types
├── SUPERVISOR_CUSTOM_EVENTS_PR.md # PR description with proposed fix
├── src/                           # Example agents for testing
│   ├── research_agent/           
│   └── analysis_agent/           
└── langgraph.json                # LangGraph configuration
```

## The Fix

The proposed fix modifies `_make_call_agent` in langgraph-supervisor to use `agent.astream()` when available, forwarding all streaming modes to sub-agents. See `SUPERVISOR_CUSTOM_EVENTS_PR.md` for details.

## Testing with LangGraph Server (Optional)

If you want to test with RemoteGraphs:

```bash
# Start LangGraph server
langgraph dev

# In another terminal, run tests
python test_both_graph_types.py
```
