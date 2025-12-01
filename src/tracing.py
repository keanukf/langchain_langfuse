"""Langfuse tracing setup and callback handler."""

import os
from langfuse.langchain import CallbackHandler
from config import config


def get_langfuse_handler(trace_name: str) -> CallbackHandler:
    """
    Create and configure a Langfuse callback handler for tracing.

    Args:
        trace_name: Name to identify this trace in Langfuse UI

    Returns:
        Configured CallbackHandler instance

    Raises:
        ValueError: If Langfuse credentials are not configured
    """
    config.validate()

    # Set environment variables for Langfuse authentication
    # CallbackHandler reads these automatically
    os.environ["LANGFUSE_SECRET_KEY"] = config.LANGFUSE_SECRET_KEY
    os.environ["LANGFUSE_HOST"] = config.LANGFUSE_HOST

    # Create handler with public key
    # Trace name and session ID will be set via metadata in the invoke config
    handler = CallbackHandler(
        public_key=config.LANGFUSE_PUBLIC_KEY,
    )

    return handler

