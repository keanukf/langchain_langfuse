"""
Example 4: Attributes

This example demonstrates all the different attributes you can add to traces:
- Environments: Separate data from different deployment contexts
- Tags: Flexible labels to categorize traces
- Users: Track which end-user triggered each trace
- Metadata: Custom key-value information
- Releases: Track application versions

Key concepts:
- Attributes help you filter, segment, and analyze traces
- Each attribute type serves a specific purpose
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
"""


def main():
    """Run attributes example."""
    print("=" * 60)
    print("Example 4: Attributes")
    print("=" * 60)
    print("\nThis example demonstrates all trace attributes:")
    print("  - Environment: Separates dev/staging/prod data")
    print("  - Tags: Categorizes traces (e.g., feature, endpoint)")
    print("  - User: Tracks which user triggered the trace")
    print("  - Metadata: Custom key-value information")
    print("  - Release: Tracks application version")
    print()

    # Validate configuration
    try:
        config.validate()
    except ValueError as e:
        print(f"Configuration Error: {e}")
        return

    # Example 1: Environment
    print("--- Example 1: Environment ---")
    handler = get_langfuse_handler(
        trace_name="example-04-attributes-environment",
        environment="development",
    )
    try:
        summarize(SAMPLE_TEXT, handler, trace_name="example-04-attributes-environment")
        print("✓ Created trace with environment='development'")
    except Exception as e:
        print(f"Error: {e}")

    # Example 2: Tags
    print("\n--- Example 2: Tags ---")
    handler = get_langfuse_handler(
        trace_name="example-04-attributes-tags",
        tags=["summarization", "example", "demo"],
    )
    try:
        summarize(SAMPLE_TEXT, handler, trace_name="example-04-attributes-tags")
        print("✓ Created trace with tags=['summarization', 'example', 'demo']")
    except Exception as e:
        print(f"Error: {e}")

    # Example 3: User
    print("\n--- Example 3: User ---")
    handler = get_langfuse_handler(
        trace_name="example-04-attributes-user",
        user_id="user-123",
    )
    try:
        summarize(SAMPLE_TEXT, handler, trace_name="example-04-attributes-user")
        print("✓ Created trace with user_id='user-123'")
    except Exception as e:
        print(f"Error: {e}")

    # Example 4: Metadata
    print("\n--- Example 4: Metadata ---")
    handler = get_langfuse_handler(
        trace_name="example-04-attributes-metadata",
        metadata={
            "source": "cli",
            "feature": "summarization",
            "priority": "high",
            "custom_field": "custom_value",
        },
    )
    try:
        summarize(SAMPLE_TEXT, handler, trace_name="example-04-attributes-metadata")
        print("✓ Created trace with custom metadata")
    except Exception as e:
        print(f"Error: {e}")

    # Example 5: Release
    print("\n--- Example 5: Release ---")
    handler = get_langfuse_handler(
        trace_name="example-04-attributes-release",
        release="v1.2.3",
    )
    try:
        summarize(SAMPLE_TEXT, handler, trace_name="example-04-attributes-release")
        print("✓ Created trace with release='v1.2.3'")
    except Exception as e:
        print(f"Error: {e}")

    # Example 6: All attributes combined
    print("\n--- Example 6: All Attributes Combined ---")
    handler = get_langfuse_handler(
        trace_name="example-04-attributes-all",
        environment="production",
        tags=["summarization", "production"],
        user_id="user-456",
        metadata={"source": "api", "endpoint": "/summarize"},
        release="v2.0.0",
    )
    try:
        summarize(SAMPLE_TEXT, handler, trace_name="example-04-attributes-all")
        print("✓ Created trace with all attributes combined")
    except Exception as e:
        print(f"Error: {e}")

    print("\n" + "=" * 60)
    print(f"✓ All examples complete! View traces in Langfuse: {config.LANGFUSE_HOST}/traces")
    print("  Use filters to find traces by environment, tags, user, etc.")
    print("=" * 60)


if __name__ == "__main__":
    main()

