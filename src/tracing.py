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
        Configured CallbackHandler instance with trace attributes stored for metadata injection

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

    # Create handler - CallbackHandler constructor only accepts public_key, secret_key, host
    # Trace attributes must be passed via metadata during chain invocation
    handler = CallbackHandler(
        public_key=config.LANGFUSE_PUBLIC_KEY,
        secret_key=config.LANGFUSE_SECRET_KEY,
        host=config.LANGFUSE_HOST,
    )

    # Store trace attributes on the handler object for later use in metadata
    # These will be passed via metadata with langfuse_ prefixes during invocation
    handler._langfuse_trace_name = trace_name
    handler._langfuse_session_id = session_id
    handler._langfuse_user_id = user_id
    handler._langfuse_environment = environment
    handler._langfuse_tags = tags
    handler._langfuse_custom_metadata = metadata
    handler._langfuse_release = release

    return handler


def get_trace_metadata(handler: CallbackHandler) -> Dict[str, Any]:
    """
    Extract trace metadata from a Langfuse handler for use in chain invocation.

    Args:
        handler: CallbackHandler instance with stored trace attributes

    Returns:
        Dictionary of metadata with langfuse_ prefixes for trace attributes
    """
    metadata = {}

    # Add trace attributes with langfuse_ prefixes
    if hasattr(handler, "_langfuse_trace_name") and handler._langfuse_trace_name:
        metadata["langfuse_name"] = handler._langfuse_trace_name
    if hasattr(handler, "_langfuse_session_id") and handler._langfuse_session_id:
        metadata["langfuse_session_id"] = handler._langfuse_session_id
    if hasattr(handler, "_langfuse_user_id") and handler._langfuse_user_id:
        metadata["langfuse_user_id"] = handler._langfuse_user_id
    if hasattr(handler, "_langfuse_environment") and handler._langfuse_environment:
        metadata["langfuse_environment"] = handler._langfuse_environment
    if hasattr(handler, "_langfuse_tags") and handler._langfuse_tags:
        metadata["langfuse_tags"] = handler._langfuse_tags
    if hasattr(handler, "_langfuse_release") and handler._langfuse_release:
        metadata["langfuse_release"] = handler._langfuse_release
    if hasattr(handler, "_langfuse_custom_metadata") and handler._langfuse_custom_metadata:
        # Merge custom metadata (without langfuse_ prefix for user-defined keys)
        metadata.update(handler._langfuse_custom_metadata)

    return metadata

