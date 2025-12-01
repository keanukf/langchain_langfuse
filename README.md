# Langfuse Tracing Test - LangChain Summarization Agent

A minimal Python project to test Langfuse tracing with a simple LangChain summarization chain using Ollama for local LLM inference.

## Overview

This project demonstrates how to integrate Langfuse tracing with LangChain and Ollama to capture and monitor LLM interactions. It provides a CLI tool for summarizing text with full observability through Langfuse.

## Features

- Simple summarization chain using LangChain and Ollama
- Langfuse tracing integration for monitoring LLM calls
- CLI interface with Typer
- Support for inline text or file input
- Structured markdown output
- Error handling for common issues

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

### Summarize inline text

```bash
python main.py summarize --text "Your text here..." --trace-name "test-run-1"
```

### Summarize text from a file

```bash
python main.py summarize --file examples/sample_text.txt --trace-name "test-run-2"
```

### Options

- `--text`, `-t`: Text to summarize (inline)
- `--file`, `-f`: Path to text file to summarize
- `--trace-name`: Custom name for the trace in Langfuse (optional, defaults to timestamp-based name)
- `--verbose`, `-v`: Enable verbose output for debugging

## Project Structure

```
.
├── src/
│   ├── __init__.py          # Package initialization
│   ├── agent.py             # Summarization chain definition
│   ├── tracing.py           # Langfuse callback handler setup
│   └── prompts.py           # System and user prompt templates
├── examples/
│   └── sample_text.txt      # Example input for testing
├── main.py                  # CLI entry point
├── config.py                # Configuration management
├── requirements.txt         # Python dependencies
├── .env.example             # Environment variables template
└── README.md                # This file
```

## Configuration

Configuration is managed through environment variables (loaded from `.env` file):

- `OLLAMA_MODEL`: Ollama model to use (default: `llama3.1:8b`)
- `OLLAMA_BASE_URL`: Ollama API base URL (default: `http://localhost:11434`)
- `LANGFUSE_PUBLIC_KEY`: Langfuse public key (required)
- `LANGFUSE_SECRET_KEY`: Langfuse secret key (required)
- `LANGFUSE_HOST`: Langfuse host URL (default: `https://cloud.langfuse.com`)

## Success Criteria

After running the summarization command:

1. ✅ The summary prints correctly to the console
2. ✅ A trace appears in the Langfuse UI
3. ✅ The trace shows: input prompt, output completion, model used, token counts, latency
4. ✅ Multiple runs create separate traces that can be filtered by trace name

## Testing

Test the implementation with:

```bash
# Test with inline text
python main.py summarize --text "Paste a paragraph here..." --trace-name "test-run-1"

# Test with file
python main.py summarize --file examples/sample_text.txt --trace-name "test-run-2"

# Verbose mode
python main.py summarize --file examples/sample_text.txt --trace-name "test-run-3" --verbose
```

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

## License

This is a test project for validating Langfuse tracing integration.

