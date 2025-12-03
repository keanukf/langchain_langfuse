# Langfuse Data Model Examples

This directory contains standalone example scripts that demonstrate different aspects of the Langfuse data model. Each example is self-contained and can be run independently.

## Prerequisites

Before running the examples, ensure you have:

1. **Environment configured**: Set up your `.env` file with Langfuse credentials
2. **Ollama running**: Start Ollama with `ollama serve`
3. **Model available**: Pull the required model with `ollama pull llama3.1:8b`

## Running Examples

Each example can be run directly:

```bash
python examples/01_basic_trace.py
python examples/02_nested_observations.py
python examples/03_sessions.py
python examples/04_attributes.py
python examples/05_rag_retrieval.py
```

## Example Overview

### 01_basic_trace.py
**Concepts**: Traces, Observations

Demonstrates the simplest use case - a single trace with one generation observation. This is the foundation of Langfuse tracing.

**What you'll see in Langfuse:**
```
Trace
  └── Generation (LLM call)
```

### 02_nested_observations.py
**Concepts**: Nested Observations, Tool Calls

Shows how tool-calling agents create nested observations. When an agent uses tools, each tool call appears as a child observation.

**What you'll see in Langfuse:**
```
Trace
  └── Generation (Agent)
      ├── Tool Call (count_words)
      └── Tool Call (extract_keywords)
```

### 03_sessions.py
**Concepts**: Sessions, Multi-turn Conversations

Demonstrates how to group multiple traces into a session. Sessions are essential for multi-turn conversations or related operations.

**What you'll see in Langfuse:**
```
Session
  ├── Trace 1 (First message)
  ├── Trace 2 (Second message)
  └── Trace 3 (Third message)
```

### 04_attributes.py
**Concepts**: Environments, Tags, Users, Metadata, Releases

Comprehensive demonstration of all trace attributes. Shows how to add metadata to traces for filtering and analysis.

**Attributes covered:**
- **Environment**: Separate dev/staging/prod data
- **Tags**: Categorize traces (e.g., `["summarization", "example"]`)
- **User**: Track which user triggered the trace
- **Metadata**: Custom key-value pairs
- **Release**: Track application versions

### 05_rag_retrieval.py
**Concepts**: RAG, Retrieval Observations

Demonstrates a RAG (Retrieval-Augmented Generation) workflow. In production, retrieval steps appear as nested observations.

**What you'll see in Langfuse:**
```
Trace
  └── Generation (RAG)
      └── Retrieval (Document retrieval)
```

## Understanding the Data Model

### Observations
Observations are individual steps within a trace. Types include:
- **Generations**: LLM calls
- **Tool Calls**: Function/tool invocations
- **Retrieval**: Document retrieval steps
- **Spans**: Custom operations

Observations can be nested - a generation can contain tool calls as children.

### Traces
A trace represents a single request or operation. It contains:
- Overall input and output
- All observations (nested structure)
- Metadata and attributes

### Sessions
Sessions group related traces together. Use cases:
- Multi-turn conversations
- Related operations in a workflow
- User interactions over time

### Attributes
Attributes help you organize and analyze traces:

| Attribute | Purpose | Example |
|-----------|---------|---------|
| **Environment** | Separate deployment contexts | `production`, `staging`, `development` |
| **Tags** | Flexible categorization | `["feature-a", "api", "high-priority"]` |
| **User** | Track end-users | `user-123` |
| **Metadata** | Custom key-value data | `{"source": "api", "endpoint": "/chat"}` |
| **Release** | Version tracking | `v1.2.3` |

## Next Steps

After running the examples:

1. **Explore in Langfuse UI**: Open each trace to see the structure
2. **Try filtering**: Use attributes to filter traces
3. **Combine concepts**: Mix and match attributes in your own code
4. **Read the docs**: See [Langfuse Data Model Documentation](https://langfuse.com/docs/observability/data-model)

## Integration with CLI

These examples demonstrate the same concepts available through the CLI:

```bash
# Basic trace
python main.py summarize --text "..." --trace-name "my-trace"

# Nested observations
python main.py analyze --text "..." --tags "analysis,demo"

# Sessions
python main.py chat "Hello" --session-id "my-session"
python main.py chat "Follow up" --session-id "my-session"

# All attributes
python main.py summarize --text "..." \
  --env production \
  --tags "summarization,api" \
  --user user-123 \
  --metadata '{"source":"api"}' \
  --release v1.0.0
```

