"""CLI entry point for the summarization agent."""

from datetime import datetime
from pathlib import Path
from typing import Optional

import typer
from rich.console import Console
from rich.panel import Panel

from config import config
from src.agent import summarize as summarize_text
from src.tracing import get_langfuse_handler

app = typer.Typer(help="LangChain summarization agent with Langfuse tracing")
console = Console()


def generate_trace_name(prefix: Optional[str] = None) -> str:
    """Generate a trace name with optional prefix and timestamp."""
    timestamp = datetime.now().strftime("%Y%m%d-%H%M%S")
    if prefix:
        return f"{prefix}-{timestamp}"
    return f"summarization-{timestamp}"


@app.command(name="summarize")
def summarize_cmd(
    text: Optional[str] = typer.Option(None, "--text", "-t", help="Text to summarize"),
    file: Optional[str] = typer.Option(None, "--file", "-f", help="Path to text file"),
    trace_name: Optional[str] = typer.Option(None, "--trace-name", help="Custom trace name"),
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
    trace_id = trace_name if trace_name else generate_trace_name()

    if verbose:
        console.print(f"[dim]Using trace name: {trace_id}[/dim]")
        console.print(f"[dim]Ollama model: {config.OLLAMA_MODEL}[/dim]")
        console.print(f"[dim]Ollama URL: {config.OLLAMA_BASE_URL}[/dim]")
        console.print(f"[dim]Langfuse host: {config.LANGFUSE_HOST}[/dim]")

    # Initialize Langfuse handler
    try:
        langfuse_handler = get_langfuse_handler(trace_id)
    except ValueError as e:
        console.print(f"[red]Langfuse Error: {e}[/red]")
        raise typer.Exit(1)

    # Perform summarization
    console.print("[yellow]Summarizing text...[/yellow]")
    try:
        summary = summarize_text(input_text, langfuse_handler)
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


if __name__ == "__main__":
    app()

