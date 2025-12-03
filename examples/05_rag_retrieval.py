"""
Example 5: RAG Retrieval

This example demonstrates a RAG (Retrieval-Augmented Generation) workflow.
In a real RAG implementation, the retrieval step would appear as a nested
observation within the generation trace.

Key concepts:
- RAG: Retrieval-Augmented Generation combines retrieval with generation
- Retrieval Observations: Document retrieval steps appear as nested observations
- Context: Retrieved documents are used as context for generation
"""

from pathlib import Path
import sys

# Add parent directory to path
sys.path.insert(0, str(Path(__file__).parent.parent))

from config import config
from src.agent import rag_query
from src.tracing import get_langfuse_handler

# Sample context/document
CONTEXT = """
Langfuse is an open-source observability platform for LLM applications. It helps developers
track, debug, and improve their LLM applications by providing detailed traces of all
interactions. Langfuse supports multiple observation types including generations, tool calls,
and retrieval steps. The platform is built on OpenTelemetry and provides a comprehensive
data model with traces, observations, and sessions.
"""

# Sample questions
QUESTIONS = [
    "What is Langfuse?",
    "What observation types does Langfuse support?",
    "What is Langfuse built on?",
]


def main():
    """Run RAG retrieval example."""
    print("=" * 60)
    print("Example 5: RAG Retrieval")
    print("=" * 60)
    print("\nThis example demonstrates a RAG workflow with retrieval.")
    print("In Langfuse, you'll see:\n")
    print("  Trace")
    print("    └── Generation (RAG)")
    print("        └── Retrieval (Document retrieval)")
    print()
    print("Note: This is a simplified example. In a real implementation,")
    print("the retrieval step would be automatically captured as a nested observation.")
    print()

    # Validate configuration
    try:
        config.validate()
    except ValueError as e:
        print(f"Configuration Error: {e}")
        return

    # Create a session for related RAG queries
    session_id = "example-05-rag-session"

    print(f"Context document ({len(CONTEXT)} characters):")
    print("-" * 60)
    print(CONTEXT[:200] + "...")
    print("-" * 60)
    print()

    for i, question in enumerate(QUESTIONS, 1):
        print(f"--- Question {i} ---")
        print(f"Q: {question}")

        # Create handler with session ID
        handler = get_langfuse_handler(
            trace_name=f"example-05-rag-query-{i}",
            session_id=session_id,
            tags=["rag", "retrieval", "example"],
        )

        try:
            answer = rag_query(
                question,
                CONTEXT,
                handler,
                trace_name=f"example-05-rag-query-{i}",
                session_id=session_id,
            )
            print(f"A: {answer}\n")
        except Exception as e:
            print(f"Error: {e}\n")
            break

    print("=" * 60)
    print(f"✓ RAG examples complete! View traces in Langfuse: {config.LANGFUSE_HOST}/traces")
    print(f"  Session ID: {session_id}")
    print("=" * 60)


if __name__ == "__main__":
    main()

