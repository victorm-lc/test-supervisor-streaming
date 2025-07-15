# LangGraph Supervisor Custom Event Streaming Issue

This repository demonstrates streaming issues with LangGraph 0.3.4 where custom events from RemoteGraphs are not properly streamed when using the documented `stream_subgraphs` parameter.

## The Problem

The Verizon team reported that when using RemoteGraphs with supervisors, custom events don't stream through when using the documented parameter `stream_subgraphs: true`. However, using the undocumented parameter `subgraphs: true` works as a workaround.

## Testing the Issue

### 1. Start LangGraph Dev Server

```bash
# Install dependencies with LangGraph 0.3.4
uv sync

# Start the development server
langgraph dev
```

The server will start at `http://127.0.0.1:2024` and register these graphs:
- `research_agent` - RemoteGraph for research tasks
- `analysis_agent` - RemoteGraph for analysis tasks  
- `local_supervisor_agent` - Local supervisor using create_supervisor
- `remote_supervisor_agent` - Remote supervisor using create_supervisor

### 2. Test Streaming via Postman/curl

Use this curl command to test the streaming behavior:

```bash
curl --location 'http://127.0.0.1:2024/runs/stream' \
--header 'X-Api-Key: ...' \
--header 'Content-Type: application/json' \
--data '{
    "assistant_id": "remote_supervisor_agent",
    "input": {
        "messages": [
            {
                "type": "human",
                "content": "research the number of academic papers on gaming"
            }
        ]
    },
    "stream_mode": [
        "values",
        "custom"
    ],
    "stream_subgraphs": true
}'
```

### 3. Test the Workaround

To test the undocumented workaround, change `stream_subgraphs` to `subgraphs`:

```bash
curl --location 'http://127.0.0.1:2024/runs/stream' \
--header 'X-Api-Key: ...' \
--header 'Content-Type: application/json' \
--data '{
    "assistant_id": "remote_supervisor_agent",
    "input": {
        "messages": [
            {
                "type": "human",
                "content": "research the number of academic papers on gaming"
            }
        ]
    },
    "stream_mode": [
        "values",
        "custom"
    ],
    "subgraphs": true
}'
```

## Expected Results

- **With `stream_subgraphs: true`**: ❌ Custom events from RemoteGraphs are missing
- **With `subgraphs: true`**: ✅ Custom events from RemoteGraphs stream correctly

## Repository Structure

```
├── src/                           # Example agents for testing
│   ├── research_agent/           # RemoteGraph research agent
│   ├── analysis_agent/           # RemoteGraph analysis agent
│   └── supervisor_agent/         # Local and remote supervisors
├── langgraph.json                # LangGraph configuration
└── test_streaming.py             # Streaming test script
```

## Issue Summary

This demonstrates a critical API parameter naming issue in LangGraph 0.3.4:
1. The documented `stream_subgraphs` parameter doesn't work for RemoteGraphs
2. The undocumented `subgraphs` parameter works as a workaround
3. This affects any team using RemoteGraphs with custom events in supervisors

**✅ This issue has been fixed since LangGraph 0.5.0** - the `stream_subgraphs` parameter now works correctly. Teams using 0.3.4 need to use the `subgraphs` workaround until they can upgrade.
