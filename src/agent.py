"""Summarization chain using LangChain and Ollama."""

from typing import Optional
from langchain_ollama import ChatOllama
from langfuse.langchain import CallbackHandler
from config import config
from src.prompts import get_summarization_prompt


def create_summarization_chain():
    """
    Create a summarization chain using ChatOllama.

    Returns:
        RunnableSequence configured for summarization
    """
    prompt = get_summarization_prompt()
    llm = ChatOllama(
        model=config.OLLAMA_MODEL,
        base_url=config.OLLAMA_BASE_URL,
    )

    chain = prompt | llm

    return chain


def summarize(text: str, langfuse_handler: CallbackHandler) -> str:
    """
    Summarize the provided text using the summarization chain.

    Args:
        text: Input text to summarize
        langfuse_handler: Langfuse callback handler for tracing

    Returns:
        Summary string in markdown format

    Raises:
        ConnectionError: If Ollama is not accessible
        ValueError: If input text is empty
    """
    if not text or not text.strip():
        raise ValueError("Input text cannot be empty")

    chain = create_summarization_chain()

    try:
        result = chain.invoke(
            {"text": text},
            config={"callbacks": [langfuse_handler]},
        )

        # Extract content from AIMessage
        summary = result.content if hasattr(result, "content") else str(result)

        return summary
    except Exception as e:
        if "connection" in str(e).lower() or "refused" in str(e).lower():
            raise ConnectionError(
                f"Failed to connect to Ollama at {config.OLLAMA_BASE_URL}. "
                "Please ensure Ollama is running and the base URL is correct."
            ) from e
        raise

