# LangGraph Prebuilts Custom Streaming Investigation

## Quick Setup

1. Install dependencies:
```bash
uv sync
```

2. Set up environment:
```bash
uv venv
# Add your OpenAI API key to .env
```

## Testing Files

- `test_supervisor_streaming.py` - Tests RemoteGraph + supervisor setup with existing deployed agents
- `test_react_agent_streaming.py` - Tests create_react_agent with custom streaming via stream_writer

## Goal

Investigate if custom events can stream through:
1. RemoteGraph + supervisor setup (using existing deployed React agents)
2. create_react_agent with custom tool streaming

Update the agent URLs in test files once provided.