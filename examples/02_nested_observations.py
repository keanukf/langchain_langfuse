"""
Example 2: Nested Observations

This example demonstrates nested observations by using a tool-calling agent.
When the agent calls tools, those tool calls appear as nested observations
within the trace.

Key concepts:
- Nested Observations: Child observations within a parent observation
- Tool Calls: When an agent uses tools, each tool call is a nested observation
"""

from pathlib import Path
import sys

# Add parent directory to path
sys.path.insert(0, str(Path(__file__).parent.parent))

from config import config
from src.agent import analyze_text
from src.tracing import get_langfuse_handler

# Sample text to analyze
SAMPLE_TEXT = """
Artificial intelligence has revolutionized numerous industries, from healthcare to finance, 
by enabling machines to process and analyze vast amounts of data at unprecedented speeds. 
Machine learning algorithms can now identify patterns in medical imaging that might escape 
human detection, predict market trends with remarkable accuracy, and automate complex 
decision-making processes. However, this rapid advancement raises important ethical questions 
about privacy, bias, and the future of human employment.
"""


def main():
    """Run nested observations example."""
    print("=" * 60)
    print("Example 2: Nested Observations")
    print("=" * 60)
    print("\nThis example uses a tool-calling agent that creates nested observations.")
    print("In Langfuse, you'll see:\n")
    print("  Trace")
    print("    └── Generation (Agent)")
    print("        ├── Tool Call (count_words)")
    print("        └── Tool Call (extract_keywords)")
    print()

    # Validate configuration
    try:
        config.validate()
    except ValueError as e:
        print(f"Configuration Error: {e}")
        return

    # Create Langfuse handler
    handler = get_langfuse_handler(
        trace_name="example-02-nested-observations",
    )

    # Perform analysis with tools
    print("Analyzing text with tools...")
    try:
        result = analyze_text(
            SAMPLE_TEXT,
            handler,
            trace_name="example-02-nested-observations",
        )
        print("\n" + "=" * 60)
        print("Analysis Result:")
        print("=" * 60)
        print(result["analysis"])
        print("\n" + "=" * 60)
        print(f"✓ Trace created! View it in Langfuse: {config.LANGFUSE_HOST}/traces")
        print("  Look for nested tool call observations!")
        print("=" * 60)
    except Exception as e:
        print(f"Error: {e}")


if __name__ == "__main__":
    main()

