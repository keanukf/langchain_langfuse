"""
Example 3: Sessions

This example demonstrates how to group multiple traces into a session.
Sessions are useful for multi-turn conversations or related operations.

Key concepts:
- Session: Groups multiple traces together
- Session ID: Unique identifier that links traces to the same session
"""

from pathlib import Path
import sys

# Add parent directory to path
sys.path.insert(0, str(Path(__file__).parent.parent))

from config import config
from src.agent import chat
from src.tracing import get_langfuse_handler

# Sample conversation
CONVERSATION = [
    "Hello! What can you help me with?",
    "Can you explain what artificial intelligence is?",
    "What are some applications of AI?",
]


def main():
    """Run sessions example."""
    print("=" * 60)
    print("Example 3: Sessions")
    print("=" * 60)
    print("\nThis example creates multiple traces grouped into a session.")
    print("In Langfuse, you'll see:\n")
    print("  Session")
    print("    ├── Trace 1 (First message)")
    print("    ├── Trace 2 (Second message)")
    print("    └── Trace 3 (Third message)")
    print()

    # Validate configuration
    try:
        config.validate()
    except ValueError as e:
        print(f"Configuration Error: {e}")
        return

    # Use a consistent session ID for all messages
    session_id = "example-03-session"

    print(f"Starting conversation with session ID: {session_id}\n")

    chat_history = []
    for i, message in enumerate(CONVERSATION, 1):
        print(f"--- Message {i} ---")
        print(f"User: {message}")

        # Create handler with session ID
        handler = get_langfuse_handler(
            trace_name=f"example-03-session-message-{i}",
            session_id=session_id,
        )

        try:
            response, chat_history = chat(
                message,
                handler,
                chat_history=chat_history,
                trace_name=f"example-03-session-message-{i}",
                session_id=session_id,
            )
            print(f"Assistant: {response}\n")
        except Exception as e:
            print(f"Error: {e}")
            break

    print("=" * 60)
    print(f"✓ Session created! View it in Langfuse: {config.LANGFUSE_HOST}/sessions")
    print(f"  Session ID: {session_id}")
    print("=" * 60)


if __name__ == "__main__":
    main()

