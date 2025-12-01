"""Langfuse tracing setup and callback handler."""

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

    handler = CallbackHandler(
        public_key=config.LANGFUSE_PUBLIC_KEY,
        secret_key=config.LANGFUSE_SECRET_KEY,
        host=config.LANGFUSE_HOST,
        trace_name=trace_name,
        session_id=trace_name,  # Use trace_name as session_id for grouping
    )

    return handler

