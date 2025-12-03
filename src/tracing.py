"""Langfuse tracing setup and callback handler."""

import os
from typing import Optional, List, Dict, Any
from langfuse import Langfuse
from langfuse.langchain import CallbackHandler
from config import config


def get_langfuse_handler(
    trace_name: Optional[str] = None,
    session_id: Optional[str] = None,
    user_id: Optional[str] = None,
    environment: Optional[str] = None,
    tags: Optional[List[str]] = None,
    metadata: Optional[Dict[str, Any]] = None,
    release: Optional[str] = None,
) -> CallbackHandler:
    """
    Create and configure a Langfuse callback handler for tracing with full attribute support.

    Args:
        trace_name: Name to identify this trace in Langfuse UI
        session_id: Session ID for grouping related traces
        user_id: User ID for tracking which end-user triggered the trace
        environment: Environment name (e.g., 'production', 'staging', 'development')
        tags: List of tags for categorizing traces
        metadata: Dictionary of custom key-value metadata
        release: Release/version identifier for tracking application versions

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

    # Build trace configuration with all attributes
    trace_config = {}
    if trace_name:
        trace_config["name"] = trace_name
    if session_id:
        trace_config["session_id"] = session_id
    if user_id:
        trace_config["user_id"] = user_id
    if environment:
        trace_config["environment"] = environment
    if tags:
        trace_config["tags"] = tags
    if metadata:
        trace_config["metadata"] = metadata
    if release:
        trace_config["release"] = release

    # Create handler with trace configuration
    handler = CallbackHandler(
        public_key=config.LANGFUSE_PUBLIC_KEY,
        secret_key=config.LANGFUSE_SECRET_KEY,
        host=config.LANGFUSE_HOST,
        **trace_config,
    )

    return handler

