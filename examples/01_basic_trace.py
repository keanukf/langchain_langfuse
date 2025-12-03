"""
Example 1: Basic Trace

This example demonstrates the simplest use case - creating a basic trace
with a single observation (generation).

Key concepts:
- Trace: A single request/operation
- Observation: Individual step within a trace (in this case, a generation)
"""

from pathlib import Path
import sys

# Add parent directory to path
sys.path.insert(0, str(Path(__file__).parent.parent))

from config import config
from src.agent import summarize
from src.tracing import get_langfuse_handler

# Sample text to summarize
SAMPLE_TEXT = """
Artificial intelligence has revolutionized numerous industries, from healthcare to finance, 
by enabling machines to process and analyze vast amounts of data at unprecedented speeds. 
Machine learning algorithms can now identify patterns in medical imaging that might escape 
human detection, predict market trends with remarkable accuracy, and automate complex 
decision-making processes.
"""


def main():
    """Run basic trace example."""
    print("=" * 60)
    print("Example 1: Basic Trace")
    print("=" * 60)
    print("\nThis example creates a simple trace with a single generation observation.")
    print("In Langfuse, you'll see:\n")
    print("  Trace")
    print("    └── Generation (LLM call)")
    print()

    # Validate configuration
    try:
        config.validate()
    except ValueError as e:
        print(f"Configuration Error: {e}")
        return

    # Create Langfuse handler with basic trace name
    handler = get_langfuse_handler(
        trace_name="example-01-basic-trace",
    )

    # Perform summarization
    print("Summarizing text...")
    try:
        summary = summarize(SAMPLE_TEXT, handler, trace_name="example-01-basic-trace")
        print("\n" + "=" * 60)
        print("Summary:")
        print("=" * 60)
        print(summary)
        print("\n" + "=" * 60)
        print(f"✓ Trace created! View it in Langfuse: {config.LANGFUSE_HOST}/traces")
        print("=" * 60)
    except Exception as e:
        print(f"Error: {e}")


if __name__ == "__main__":
    main()

