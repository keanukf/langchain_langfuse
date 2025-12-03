"""CLI entry point for the summarization agent."""

import json
from datetime import datetime
from pathlib import Path
from typing import Optional, List, Dict, Any

import typer
from rich.console import Console
from rich.panel import Panel

from config import config
from src.agent import (
    summarize as summarize_text,
    analyze_text,
    chat as chat_agent,
    rag_query,
)
from src.tracing import get_langfuse_handler

app = typer.Typer(help="LangChain agent with Langfuse tracing - demonstrating data model features")
console = Console()


def generate_trace_name(prefix: Optional[str] = None) -> str:
    """Generate a trace name with optional prefix and timestamp."""
    timestamp = datetime.now().strftime("%Y%m%d-%H%M%S")
    if prefix:
        return f"{prefix}-{timestamp}"
    return f"trace-{timestamp}"


def parse_metadata(metadata_str: Optional[str]) -> Optional[Dict[str, Any]]:
    """Parse metadata from JSON string."""
    if not metadata_str:
        return None
    try:
        return json.loads(metadata_str)
    except json.JSONDecodeError:
        console.print(f"[red]Error: Invalid JSON in metadata: {metadata_str}[/red]")
        raise typer.Exit(1)


def parse_tags(tags_str: Optional[str]) -> Optional[List[str]]:
    """Parse tags from comma-separated string."""
    if not tags_str:
        return None
    return [tag.strip() for tag in tags_str.split(",") if tag.strip()]


def get_common_options(
    trace_name: Optional[str] = None,
    session_id: Optional[str] = None,
    user_id: Optional[str] = None,
    environment: Optional[str] = None,
    tags: Optional[str] = None,
    metadata: Optional[str] = None,
    release: Optional[str] = None,
) -> Dict[str, Any]:
    """Get common Langfuse attribute options."""
    return {
        "trace_name": trace_name,
        "session_id": session_id,
        "user_id": user_id,
        "environment": environment,
        "tags": parse_tags(tags),
        "metadata": parse_metadata(metadata),
        "release": release,
    }


@app.command(name="summarize")
def summarize_cmd(
    text: Optional[str] = typer.Option(None, "--text", "-t", help="Text to summarize"),
    file: Optional[str] = typer.Option(None, "--file", "-f", help="Path to text file"),
    trace_name: Optional[str] = typer.Option(None, "--trace-name", help="Custom trace name"),
    session_id: Optional[str] = typer.Option(None, "--session-id", help="Session ID for grouping traces"),
    user_id: Optional[str] = typer.Option(None, "--user", help="User ID for tracking"),
    environment: Optional[str] = typer.Option(None, "--env", help="Environment (e.g., production, staging, development)"),
    tags: Optional[str] = typer.Option(None, "--tags", help="Comma-separated tags"),
    metadata: Optional[str] = typer.Option(None, "--metadata", help="JSON metadata (e.g., '{\"key\":\"value\"}')"),
    release: Optional[str] = typer.Option(None, "--release", help="Release/version identifier"),
    verbose: bool = typer.Option(False, "--verbose", "-v", help="Enable verbose output"),
):
    """
    Summarize text using LangChain and Ollama, with Langfuse tracing.

    Either --text or --file must be provided.
    """
    # Validate input
    if not text and not file:
        console.print("[red]Error: Either --text or --file must be provided[/red]")
        raise typer.Exit(1)

    if text and file:
        console.print("[red]Error: Provide either --text or --file, not both[/red]")
        raise typer.Exit(1)

    # Load text input
    input_text = text
    if file:
        file_path = Path(file)
        if not file_path.exists():
            console.print(f"[red]Error: File not found: {file}[/red]")
            raise typer.Exit(1)
        try:
            input_text = file_path.read_text(encoding="utf-8")
        except Exception as e:
            console.print(f"[red]Error reading file: {e}[/red]")
            raise typer.Exit(1)

    # Validate configuration
    try:
        config.validate()
    except ValueError as e:
        console.print(f"[red]Configuration Error: {e}[/red]")
        raise typer.Exit(1)

    # Generate trace name
    trace_id = trace_name if trace_name else generate_trace_name("summarization")

    if verbose:
        console.print(f"[dim]Using trace name: {trace_id}[/dim]")
        console.print(f"[dim]Ollama model: {config.OLLAMA_MODEL}[/dim]")
        console.print(f"[dim]Ollama URL: {config.OLLAMA_BASE_URL}[/dim]")
        console.print(f"[dim]Langfuse host: {config.LANGFUSE_HOST}[/dim]")

    # Get attribute options
    attr_options = get_common_options(
        trace_name=trace_id,
        session_id=session_id,
        user_id=user_id,
        environment=environment,
        tags=tags,
        metadata=metadata,
        release=release,
    )

    # Initialize Langfuse handler
    try:
        langfuse_handler = get_langfuse_handler(**attr_options)
    except ValueError as e:
        console.print(f"[red]Langfuse Error: {e}[/red]")
        raise typer.Exit(1)

    # Perform summarization
    console.print("[yellow]Summarizing text...[/yellow]")
    try:
        summary = summarize_text(input_text, langfuse_handler, trace_name=trace_id)
    except ConnectionError as e:
        console.print(f"[red]Connection Error: {e}[/red]")
        raise typer.Exit(1)
    except ValueError as e:
        console.print(f"[red]Error: {e}[/red]")
        raise typer.Exit(1)
    except Exception as e:
        console.print(f"[red]Unexpected error: {e}[/red]")
        if verbose:
            import traceback
            console.print(f"[dim]{traceback.format_exc()}[/dim]")
        raise typer.Exit(1)

    # Display results
    console.print("\n[bold green]Summary:[/bold green]\n")
    console.print(Panel(summary, border_style="green"))

    # Get trace URL
    try:
        # Try to get trace URL from handler
        trace_url = f"{config.LANGFUSE_HOST}/traces"
        console.print(f"\n[dim]View trace in Langfuse: {trace_url}[/dim]")
        console.print(f"[dim]Trace name: {trace_id}[/dim]")
    except Exception:
        pass

    console.print("\n[green]✓ Summarization complete![/green]")


@app.command(name="analyze")
def analyze_cmd(
    text: Optional[str] = typer.Option(None, "--text", "-t", help="Text to analyze"),
    file: Optional[str] = typer.Option(None, "--file", "-f", help="Path to text file"),
    trace_name: Optional[str] = typer.Option(None, "--trace-name", help="Custom trace name"),
    session_id: Optional[str] = typer.Option(None, "--session-id", help="Session ID for grouping traces"),
    user_id: Optional[str] = typer.Option(None, "--user", help="User ID for tracking"),
    environment: Optional[str] = typer.Option(None, "--env", help="Environment (e.g., production, staging, development)"),
    tags: Optional[str] = typer.Option(None, "--tags", help="Comma-separated tags"),
    metadata: Optional[str] = typer.Option(None, "--metadata", help="JSON metadata (e.g., '{\"key\":\"value\"}')"),
    release: Optional[str] = typer.Option(None, "--release", help="Release/version identifier"),
    verbose: bool = typer.Option(False, "--verbose", "-v", help="Enable verbose output"),
):
    """
    Analyze text using an agent with tools (demonstrates nested observations).

    This command uses a tool-calling agent that will create nested observations
    in Langfuse, showing how tool calls appear as child observations within a trace.
    """
    # Validate input
    if not text and not file:
        console.print("[red]Error: Either --text or --file must be provided[/red]")
        raise typer.Exit(1)

    if text and file:
        console.print("[red]Error: Provide either --text or --file, not both[/red]")
        raise typer.Exit(1)

    # Load text input
    input_text = text
    if file:
        file_path = Path(file)
        if not file_path.exists():
            console.print(f"[red]Error: File not found: {file}[/red]")
            raise typer.Exit(1)
        try:
            input_text = file_path.read_text(encoding="utf-8")
        except Exception as e:
            console.print(f"[red]Error reading file: {e}[/red]")
            raise typer.Exit(1)

    # Validate configuration
    try:
        config.validate()
    except ValueError as e:
        console.print(f"[red]Configuration Error: {e}[/red]")
        raise typer.Exit(1)

    # Generate trace name
    trace_id = trace_name if trace_name else generate_trace_name("analysis")

    if verbose:
        console.print(f"[dim]Using trace name: {trace_id}[/dim]")
        console.print(f"[dim]Ollama model: {config.OLLAMA_MODEL}[/dim]")
        console.print(f"[dim]Ollama URL: {config.OLLAMA_BASE_URL}[/dim]")
        console.print(f"[dim]Langfuse host: {config.LANGFUSE_HOST}[/dim]")

    # Get attribute options
    attr_options = get_common_options(
        trace_name=trace_id,
        session_id=session_id,
        user_id=user_id,
        environment=environment,
        tags=tags,
        metadata=metadata,
        release=release,
    )

    # Initialize Langfuse handler
    try:
        langfuse_handler = get_langfuse_handler(**attr_options)
    except ValueError as e:
        console.print(f"[red]Langfuse Error: {e}[/red]")
        raise typer.Exit(1)

    # Perform analysis
    console.print("[yellow]Analyzing text with tools...[/yellow]")
    try:
        result = analyze_text(
            input_text,
            langfuse_handler,
            trace_name=trace_id,
            session_id=session_id,
        )
    except ConnectionError as e:
        console.print(f"[red]Connection Error: {e}[/red]")
        raise typer.Exit(1)
    except ValueError as e:
        console.print(f"[red]Error: {e}[/red]")
        raise typer.Exit(1)
    except Exception as e:
        console.print(f"[red]Unexpected error: {e}[/red]")
        if verbose:
            import traceback
            console.print(f"[dim]{traceback.format_exc()}[/dim]")
        raise typer.Exit(1)

    # Display results
    console.print("\n[bold green]Analysis:[/bold green]\n")
    console.print(Panel(result["analysis"], border_style="green"))

    # Get trace URL
    try:
        trace_url = f"{config.LANGFUSE_HOST}/traces"
        console.print(f"\n[dim]View trace in Langfuse: {trace_url}[/dim]")
        console.print(f"[dim]Trace name: {trace_id}[/dim]")
        console.print("[dim]Note: Check nested observations for tool calls![/dim]")
    except Exception:
        pass

    console.print("\n[green]✓ Analysis complete![/green]")


@app.command(name="chat")
def chat_cmd(
    message: str = typer.Argument(..., help="Message to send"),
    session_id: Optional[str] = typer.Option(None, "--session-id", help="Session ID (required for session grouping)"),
    trace_name: Optional[str] = typer.Option(None, "--trace-name", help="Custom trace name"),
    user_id: Optional[str] = typer.Option(None, "--user", help="User ID for tracking"),
    environment: Optional[str] = typer.Option(None, "--env", help="Environment (e.g., production, staging, development)"),
    tags: Optional[str] = typer.Option(None, "--tags", help="Comma-separated tags"),
    metadata: Optional[str] = typer.Option(None, "--metadata", help="JSON metadata (e.g., '{\"key\":\"value\"}')"),
    release: Optional[str] = typer.Option(None, "--release", help="Release/version identifier"),
    verbose: bool = typer.Option(False, "--verbose", "-v", help="Enable verbose output"),
):
    """
    Chat with the agent (demonstrates sessions).

    Use the same --session-id across multiple calls to group traces into a session.
    """
    # Validate configuration
    try:
        config.validate()
    except ValueError as e:
        console.print(f"[red]Configuration Error: {e}[/red]")
        raise typer.Exit(1)

    # Generate trace name
    trace_id = trace_name if trace_name else generate_trace_name("chat")

    if not session_id:
        session_id = f"session-{datetime.now().strftime('%Y%m%d-%H%M%S')}"
        if verbose:
            console.print(f"[yellow]No session ID provided, using: {session_id}[/yellow]")

    if verbose:
        console.print(f"[dim]Using trace name: {trace_id}[/dim]")
        console.print(f"[dim]Session ID: {session_id}[/dim]")
        console.print(f"[dim]Ollama model: {config.OLLAMA_MODEL}[/dim]")
        console.print(f"[dim]Langfuse host: {config.LANGFUSE_HOST}[/dim]")

    # Get attribute options
    attr_options = get_common_options(
        trace_name=trace_id,
        session_id=session_id,
        user_id=user_id,
        environment=environment,
        tags=tags,
        metadata=metadata,
        release=release,
    )

    # Initialize Langfuse handler
    try:
        langfuse_handler = get_langfuse_handler(**attr_options)
    except ValueError as e:
        console.print(f"[red]Langfuse Error: {e}[/red]")
        raise typer.Exit(1)

    # Perform chat
    console.print(f"[yellow]Sending message: {message}[/yellow]")
    try:
        response, _ = chat_agent(
            message,
            langfuse_handler,
            chat_history=[],
            trace_name=trace_id,
            session_id=session_id,
        )
    except ConnectionError as e:
        console.print(f"[red]Connection Error: {e}[/red]")
        raise typer.Exit(1)
    except ValueError as e:
        console.print(f"[red]Error: {e}[/red]")
        raise typer.Exit(1)
    except Exception as e:
        console.print(f"[red]Unexpected error: {e}[/red]")
        if verbose:
            import traceback
            console.print(f"[dim]{traceback.format_exc()}[/dim]")
        raise typer.Exit(1)

    # Display results
    console.print("\n[bold green]Response:[/bold green]\n")
    console.print(Panel(response, border_style="green"))

    # Get trace URL
    try:
        trace_url = f"{config.LANGFUSE_HOST}/traces"
        console.print(f"\n[dim]View trace in Langfuse: {trace_url}[/dim]")
        console.print(f"[dim]Trace name: {trace_id}[/dim]")
        console.print(f"[dim]Session ID: {session_id}[/dim]")
        console.print("[dim]Tip: Use the same --session-id for multiple calls to group them![/dim]")
    except Exception:
        pass

    console.print("\n[green]✓ Chat complete![/green]")


@app.command(name="rag")
def rag_cmd(
    question: str = typer.Option(..., "--question", "-q", help="Question to answer"),
    context: Optional[str] = typer.Option(None, "--context", "-c", help="Context/document text"),
    context_file: Optional[str] = typer.Option(None, "--context-file", help="Path to context file"),
    trace_name: Optional[str] = typer.Option(None, "--trace-name", help="Custom trace name"),
    session_id: Optional[str] = typer.Option(None, "--session-id", help="Session ID for grouping traces"),
    user_id: Optional[str] = typer.Option(None, "--user", help="User ID for tracking"),
    environment: Optional[str] = typer.Option(None, "--env", help="Environment (e.g., production, staging, development)"),
    tags: Optional[str] = typer.Option(None, "--tags", help="Comma-separated tags"),
    metadata: Optional[str] = typer.Option(None, "--metadata", help="JSON metadata (e.g., '{\"key\":\"value\"}')"),
    release: Optional[str] = typer.Option(None, "--release", help="Release/version identifier"),
    verbose: bool = typer.Option(False, "--verbose", "-v", help="Enable verbose output"),
):
    """
    Answer a question using RAG (demonstrates retrieval observations).

    This command simulates a RAG workflow where context is retrieved and used
    to answer a question. In a real implementation, retrieval would appear as
    nested observations in Langfuse.
    """
    # Validate input
    if not context and not context_file:
        console.print("[red]Error: Either --context or --context-file must be provided[/red]")
        raise typer.Exit(1)

    if context and context_file:
        console.print("[red]Error: Provide either --context or --context-file, not both[/red]")
        raise typer.Exit(1)

    # Load context
    context_text = context
    if context_file:
        file_path = Path(context_file)
        if not file_path.exists():
            console.print(f"[red]Error: File not found: {context_file}[/red]")
            raise typer.Exit(1)
        try:
            context_text = file_path.read_text(encoding="utf-8")
        except Exception as e:
            console.print(f"[red]Error reading file: {e}[/red]")
            raise typer.Exit(1)

    # Validate configuration
    try:
        config.validate()
    except ValueError as e:
        console.print(f"[red]Configuration Error: {e}[/red]")
        raise typer.Exit(1)

    # Generate trace name
    trace_id = trace_name if trace_name else generate_trace_name("rag")

    if verbose:
        console.print(f"[dim]Using trace name: {trace_id}[/dim]")
        console.print(f"[dim]Ollama model: {config.OLLAMA_MODEL}[/dim]")
        console.print(f"[dim]Ollama URL: {config.OLLAMA_BASE_URL}[/dim]")
        console.print(f"[dim]Langfuse host: {config.LANGFUSE_HOST}[/dim]")

    # Get attribute options
    attr_options = get_common_options(
        trace_name=trace_id,
        session_id=session_id,
        user_id=user_id,
        environment=environment,
        tags=tags,
        metadata=metadata,
        release=release,
    )

    # Initialize Langfuse handler
    try:
        langfuse_handler = get_langfuse_handler(**attr_options)
    except ValueError as e:
        console.print(f"[red]Langfuse Error: {e}[/red]")
        raise typer.Exit(1)

    # Perform RAG query
    console.print("[yellow]Answering question with RAG...[/yellow]")
    try:
        answer = rag_query(
            question,
            context_text,
            langfuse_handler,
            trace_name=trace_id,
            session_id=session_id,
        )
    except ConnectionError as e:
        console.print(f"[red]Connection Error: {e}[/red]")
        raise typer.Exit(1)
    except ValueError as e:
        console.print(f"[red]Error: {e}[/red]")
        raise typer.Exit(1)
    except Exception as e:
        console.print(f"[red]Unexpected error: {e}[/red]")
        if verbose:
            import traceback
            console.print(f"[dim]{traceback.format_exc()}[/dim]")
        raise typer.Exit(1)

    # Display results
    console.print("\n[bold green]Answer:[/bold green]\n")
    console.print(Panel(answer, border_style="green"))

    # Get trace URL
    try:
        trace_url = f"{config.LANGFUSE_HOST}/traces"
        console.print(f"\n[dim]View trace in Langfuse: {trace_url}[/dim]")
        console.print(f"[dim]Trace name: {trace_id}[/dim]")
    except Exception:
        pass

    console.print("\n[green]✓ RAG query complete![/green]")


if __name__ == "__main__":
    app()

