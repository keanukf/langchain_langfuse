"""Langfuse tracing setup and callback handler."""

import os
from langfuse import Langfuse
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

    # Initialize Langfuse client first
    # This is required for CallbackHandler to work properly
    langfuse_client = Langfuse(
        public_key=config.LANGFUSE_PUBLIC_KEY,
        secret_key=config.LANGFUSE_SECRET_KEY,
        host=config.LANGFUSE_HOST,
    )

    # Create handler - it will use the initialized client
    handler = CallbackHandler(
        public_key=config.LANGFUSE_PUBLIC_KEY,
    )

    return handler

