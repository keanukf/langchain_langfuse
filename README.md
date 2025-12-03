# Langfuse Data Model Demonstration

A comprehensive educational project demonstrating the Langfuse data model with LangChain and Ollama. This repository showcases all key concepts of Langfuse's observability platform: observations, traces, sessions, and attributes.

## Overview

This project provides a complete demonstration of how Langfuse structures and captures data from LLM applications. It includes:

- **Multiple agent types**: Summarization, analysis with tools, chat, and RAG
- **Nested observations**: Tool calls and retrieval steps as child observations
- **Session management**: Multi-turn conversations grouped into sessions
- **Full attribute support**: Environments, tags, users, metadata, and releases
- **Standalone examples**: Educational scripts for each concept
- **CLI interface**: Easy-to-use commands for all features

## Langfuse Data Model

Langfuse organizes application data into three core concepts:

### Observations

Observations are individual steps within a trace. They can be nested hierarchically.

**Types of observations:**
- **Generations**: LLM calls (prompts and completions)
- **Tool Calls**: Function/tool invocations
- **Retrieval**: Document retrieval steps (RAG)
- **Spans**: Custom operations

**Nested structure example:**
```
Trace
  └── Generation (Agent)
      ├── Tool Call (count_words)
      └── Tool Call (extract_keywords)
```

### Traces

A trace represents a single request or operation. It contains:
- Overall input and output
- All observations (nested structure)
- Metadata and attributes

**Example:** When a user asks a question to a chatbot, that entire interaction is one trace.

### Sessions

Sessions group multiple traces together. Use cases:
- Multi-turn conversations
- Related operations in a workflow
- User interactions over time

**Example:** A chat thread where multiple messages are grouped into one session.

### Attributes

Attributes help you organize, filter, and analyze traces:

| Attribute | Purpose | Example |
|-----------|---------|---------|
| **Environment** | Separate deployment contexts | `production`, `staging`, `development` |
| **Tags** | Flexible categorization | `["feature-a", "api", "high-priority"]` |
| **User** | Track end-users | `user-123` |
| **Metadata** | Custom key-value data | `{"source": "api", "endpoint": "/chat"}` |
| **Release** | Version tracking | `v1.2.3` |

## Features

- ✅ **Basic Traces**: Simple single-operation traces
- ✅ **Nested Observations**: Tool-calling agents with child observations
- ✅ **Sessions**: Multi-turn conversations grouped together
- ✅ **RAG Workflows**: Retrieval-augmented generation examples
- ✅ **Full Attribute Support**: All attribute types demonstrated
- ✅ **CLI Interface**: Easy-to-use commands for all features
- ✅ **Standalone Examples**: Educational scripts for each concept

## Prerequisites

- Python 3.11+
- Ollama installed and running locally
- Langfuse account (cloud or self-hosted)

## Setup

1. **Clone or navigate to the project directory**

2. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

3. **Set up environment variables:**
   ```bash
   cp .env.example .env
   ```
   Edit `.env` and add your Langfuse credentials:
   - `LANGFUSE_PUBLIC_KEY`: Your Langfuse public key
   - `LANGFUSE_SECRET_KEY`: Your Langfuse secret key
   - `LANGFUSE_HOST`: Langfuse host URL (default: `https://cloud.langfuse.com`)

4. **Ensure Ollama is running:**
   ```bash
   ollama serve
   ```

5. **Pull the required model (if not already available):**
   ```bash
   ollama pull llama3.1:8b
   ```

## Usage

### CLI Commands

The project provides multiple CLI commands to demonstrate different aspects of the data model:

#### 1. Summarize (Basic Trace)

Simple summarization with a single generation observation:

```bash
# Inline text
python main.py summarize --text "Your text here..." --trace-name "my-trace"

# From file
python main.py summarize --file examples/sample_text.txt --trace-name "my-trace"

# With attributes
python main.py summarize --text "..." \
  --env production \
  --tags "summarization,demo" \
  --user user-123 \
  --metadata '{"source":"cli"}' \
  --release v1.0.0
```

#### 2. Analyze (Nested Observations)

Text analysis using a tool-calling agent (demonstrates nested observations):

```bash
python main.py analyze --text "Your text here..." --trace-name "analysis-trace"

# With attributes
python main.py analyze --text "..." \
  --tags "analysis,tools" \
  --env development
```

#### 3. Chat (Sessions)

Multi-turn conversation with session support:

```bash
# First message (creates session)
python main.py chat "Hello!" --session-id "my-session"

# Follow-up messages (same session)
python main.py chat "Tell me more" --session-id "my-session"
python main.py chat "Thanks!" --session-id "my-session"
```

#### 4. RAG (Retrieval Observations)

Answer questions using RAG with context:

```bash
python main.py rag \
  --question "What is Langfuse?" \
  --context "Langfuse is an observability platform..." \
  --trace-name "rag-trace"

# Or from file
python main.py rag \
  --question "What is Langfuse?" \
  --context-file examples/sample_text.txt
```

### CLI Options

All commands support these common options:

- `--trace-name`: Custom name for the trace
- `--session-id`: Session ID for grouping traces
- `--user`: User ID for tracking
- `--env`: Environment (production, staging, development)
- `--tags`: Comma-separated tags
- `--metadata`: JSON metadata (e.g., `'{"key":"value"}'`)
- `--release`: Release/version identifier
- `--verbose`, `-v`: Enable verbose output

### Standalone Examples

The `examples/` directory contains educational scripts demonstrating each concept:

```bash
# Basic trace
python examples/01_basic_trace.py

# Nested observations
python examples/02_nested_observations.py

# Sessions
python examples/03_sessions.py

# Attributes
python examples/04_attributes.py

# RAG retrieval
python examples/05_rag_retrieval.py
```

See [examples/README.md](examples/README.md) for detailed explanations of each example.

## Project Structure

```
.
├── src/
│   ├── __init__.py          # Package initialization
│   ├── agent.py             # Agent implementations (summarize, analyze, chat, rag)
│   ├── tools.py             # Simple tools for agents (word count, keyword extraction)
│   ├── tracing.py           # Langfuse callback handler setup with full attribute support
│   └── prompts.py           # Prompt templates
├── examples/
│   ├── 01_basic_trace.py     # Basic trace example
│   ├── 02_nested_observations.py  # Nested observations example
│   ├── 03_sessions.py        # Sessions example
│   ├── 04_attributes.py      # Attributes example
│   ├── 05_rag_retrieval.py   # RAG retrieval example
│   ├── README.md             # Examples guide
│   └── sample_text.txt       # Sample input text
├── main.py                   # CLI entry point
├── config.py                 # Configuration management
├── requirements.txt          # Python dependencies
└── README.md                 # This file
```

## Configuration

Configuration is managed through environment variables (loaded from `.env` file):

- `OLLAMA_MODEL`: Ollama model to use (default: `llama3.1:8b-instruct-q4_K_M`)
- `OLLAMA_BASE_URL`: Ollama API base URL (default: `http://localhost:11434`)
- `LANGFUSE_PUBLIC_KEY`: Langfuse public key (required)
- `LANGFUSE_SECRET_KEY`: Langfuse secret key (required)
- `LANGFUSE_HOST`: Langfuse host URL (default: `https://cloud.langfuse.com`)

## Understanding the Data Model

### Visual Structure

**Basic Trace:**
```
Trace (summarization-20240101-120000)
  └── Generation
      ├── Input: "Summarize this text..."
      └── Output: "Summary here..."
```

**Nested Observations:**
```
Trace (analysis-20240101-120000)
  └── Generation (Agent)
      ├── Tool Call (count_words)
      │   ├── Input: "text..."
      │   └── Output: {"word_count": 50}
      └── Tool Call (extract_keywords)
          ├── Input: "text..."
          └── Output: {"keywords": {...}}
```

**Session with Multiple Traces:**
```
Session (my-session)
  ├── Trace 1 (chat-message-1)
  │   └── Generation
  ├── Trace 2 (chat-message-2)
  │   └── Generation
  └── Trace 3 (chat-message-3)
      └── Generation
```

### Key Concepts

1. **Observations are nested**: A generation can contain tool calls as children
2. **Traces are atomic**: One trace = one operation/request
3. **Sessions group traces**: Multiple traces can belong to one session
4. **Attributes add context**: Use them to filter and analyze

## Examples Walkthrough

### Example 1: Basic Trace

The simplest use case - a single trace with one generation observation.

**What you'll see in Langfuse:**
- One trace with a generation observation
- Input prompt and output completion
- Token counts and latency metrics

### Example 2: Nested Observations

Demonstrates how tool-calling agents create nested observations.

**What you'll see in Langfuse:**
- One trace with a generation (the agent)
- Child observations for each tool call
- Tool inputs and outputs

### Example 3: Sessions

Shows how to group multiple traces into a session.

**What you'll see in Langfuse:**
- One session containing multiple traces
- Each trace represents one message in the conversation
- Session view showing all related traces

### Example 4: Attributes

Comprehensive demonstration of all trace attributes.

**What you'll see in Langfuse:**
- Multiple traces with different attributes
- Ability to filter by environment, tags, user, etc.
- Metadata visible in trace details

### Example 5: RAG Retrieval

Demonstrates a RAG workflow with retrieval observations.

**What you'll see in Langfuse:**
- Traces with generation observations
- Retrieval steps as nested observations (in production)
- Context and question visible

## Best Practices

1. **Use meaningful trace names**: Help identify traces in the UI
2. **Group related traces**: Use sessions for multi-turn conversations
3. **Add attributes**: Use environments, tags, and metadata for filtering
4. **Track users**: Add user IDs to understand usage patterns
5. **Version your releases**: Use release tags to track changes

## Troubleshooting

### Ollama Connection Error

If you see a connection error:
- Ensure Ollama is running: `ollama serve`
- Check that `OLLAMA_BASE_URL` in `.env` matches your Ollama instance
- Verify the model is available: `ollama list`

### Langfuse Credentials Error

If you see a credentials error:
- Ensure `.env` file exists and contains `LANGFUSE_PUBLIC_KEY` and `LANGFUSE_SECRET_KEY`
- Verify your keys are correct in the Langfuse dashboard
- Check that `LANGFUSE_HOST` is set correctly (cloud or self-hosted)

### Model Not Found

If the model is not available:
- Pull the model: `ollama pull llama3.1:8b`
- Or change `OLLAMA_MODEL` in `.env` to an available model

### Traces Not Appearing

If traces don't appear in Langfuse:
- Check that Langfuse credentials are correct
- Verify network connectivity to Langfuse host
- Check Langfuse logs for errors
- Ensure you're flushing traces (especially in short-lived applications)

## Resources

- [Langfuse Documentation](https://langfuse.com/docs)
- [Langfuse Data Model](https://langfuse.com/docs/observability/data-model)
- [LangChain Integration](https://langfuse.com/docs/integrations/langchain)
- [Python SDK Reference](https://langfuse.com/docs/reference/python-sdk)

## License

This is an educational project demonstrating Langfuse's data model and observability features.
