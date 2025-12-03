"""Summarization chain using LangChain and Ollama."""

from typing import Optional, List, Dict, Any
from langchain_ollama import ChatOllama
from langchain_core.messages import HumanMessage, AIMessage, SystemMessage
from langchain.agents import AgentExecutor, create_tool_calling_agent
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langfuse.langchain import CallbackHandler
from config import config
from src.prompts import get_summarization_prompt
from src.tools import get_tools


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


def summarize(text: str, langfuse_handler: CallbackHandler, trace_name: str = None) -> str:
    """
    Summarize the provided text using the summarization chain.

    Args:
        text: Input text to summarize
        langfuse_handler: Langfuse callback handler for tracing
        trace_name: Optional trace name for Langfuse (default: None)

    Returns:
        Summary string in markdown format

    Raises:
        ConnectionError: If Ollama is not accessible
        ValueError: If input text is empty
    """
    if not text or not text.strip():
        raise ValueError("Input text cannot be empty")

    chain = create_summarization_chain()

    # Prepare config with callbacks and metadata
    invoke_config = {"callbacks": [langfuse_handler]}
    if trace_name:
        invoke_config["metadata"] = {
            "trace_name": trace_name,
            "session_id": trace_name,
        }

    try:
        result = chain.invoke(
            {"text": text},
            config=invoke_config,
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


def create_analysis_agent():
    """
    Create an agent that can use tools to analyze text.

    Returns:
        AgentExecutor configured with tools
    """
    llm = ChatOllama(
        model=config.OLLAMA_MODEL,
        base_url=config.OLLAMA_BASE_URL,
    )

    tools = get_tools()

    prompt = ChatPromptTemplate.from_messages([
        ("system", """You are a helpful text analysis assistant. 
You have access to tools that can help you analyze text in detail.
When analyzing text, use the available tools to gather information, then provide a comprehensive analysis.

Available tools:
- count_words: Count words, characters, and sentences
- extract_keywords: Extract the most important keywords

Use the tools to gather information, then provide your analysis."""),
        MessagesPlaceholder(variable_name="chat_history"),
        ("human", "{input}"),
        MessagesPlaceholder(variable_name="agent_scratchpad"),
    ])

    agent = create_tool_calling_agent(llm, tools, prompt)
    agent_executor = AgentExecutor(agent=agent, tools=tools, verbose=False)

    return agent_executor


def analyze_text(
    text: str,
    langfuse_handler: CallbackHandler,
    trace_name: str = None,
    session_id: Optional[str] = None,
) -> Dict[str, Any]:
    """
    Analyze text using an agent with tools (demonstrates nested observations).

    Args:
        text: Input text to analyze
        langfuse_handler: Langfuse callback handler for tracing
        trace_name: Optional trace name for Langfuse
        session_id: Optional session ID for grouping traces

    Returns:
        Dictionary with analysis results

    Raises:
        ConnectionError: If Ollama is not accessible
        ValueError: If input text is empty
    """
    if not text or not text.strip():
        raise ValueError("Input text cannot be empty")

    agent = create_analysis_agent()

    # Prepare config with callbacks and metadata
    invoke_config = {"callbacks": [langfuse_handler]}
    metadata = {}
    if trace_name:
        metadata["trace_name"] = trace_name
    if session_id:
        metadata["session_id"] = session_id
    if metadata:
        invoke_config["metadata"] = metadata

    try:
        result = agent.invoke(
            {
                "input": f"Analyze this text in detail: {text}",
                "chat_history": [],
            },
            config=invoke_config,
        )

        return {
            "analysis": result.get("output", ""),
            "text_length": len(text),
        }
    except Exception as e:
        if "connection" in str(e).lower() or "refused" in str(e).lower():
            raise ConnectionError(
                f"Failed to connect to Ollama at {config.OLLAMA_BASE_URL}. "
                "Please ensure Ollama is running and the base URL is correct."
            ) from e
        raise


def create_chat_agent():
    """
    Create a chat agent for multi-turn conversations.

    Returns:
        ChatOllama instance configured for chat
    """
    llm = ChatOllama(
        model=config.OLLAMA_MODEL,
        base_url=config.OLLAMA_BASE_URL,
    )

    return llm


def chat(
    message: str,
    langfuse_handler: CallbackHandler,
    chat_history: List[tuple] = None,
    trace_name: str = None,
    session_id: Optional[str] = None,
) -> tuple[str, List[tuple]]:
    """
    Conduct a chat conversation (demonstrates sessions).

    Args:
        message: User message
        langfuse_handler: Langfuse callback handler for tracing
        chat_history: Previous conversation history as list of (user, assistant) tuples
        trace_name: Optional trace name for Langfuse
        session_id: Session ID for grouping related traces (required for sessions)

    Returns:
        Tuple of (response, updated_chat_history)

    Raises:
        ConnectionError: If Ollama is not accessible
        ValueError: If message is empty
    """
    if not message or not message.strip():
        raise ValueError("Message cannot be empty")

    if chat_history is None:
        chat_history = []

    llm = create_chat_agent()

    # Convert chat history to LangChain messages
    messages = [
        SystemMessage(content="You are a helpful assistant. Have a natural conversation with the user.")
    ]
    for user_msg, assistant_msg in chat_history:
        messages.append(HumanMessage(content=user_msg))
        messages.append(AIMessage(content=assistant_msg))
    messages.append(HumanMessage(content=message))

    # Prepare config with callbacks and metadata
    invoke_config = {"callbacks": [langfuse_handler]}
    metadata = {}
    if trace_name:
        metadata["trace_name"] = trace_name
    if session_id:
        metadata["session_id"] = session_id
    if metadata:
        invoke_config["metadata"] = metadata

    try:
        result = llm.invoke(messages, config=invoke_config)

        response = result.content if hasattr(result, "content") else str(result)
        updated_history = chat_history + [(message, response)]

        return response, updated_history
    except Exception as e:
        if "connection" in str(e).lower() or "refused" in str(e).lower():
            raise ConnectionError(
                f"Failed to connect to Ollama at {config.OLLAMA_BASE_URL}. "
                "Please ensure Ollama is running and the base URL is correct."
            ) from e
        raise


def create_rag_chain():
    """
    Create a simple RAG chain with document retrieval simulation.

    Returns:
        RunnableSequence configured for RAG
    """
    from langchain_core.prompts import ChatPromptTemplate

    llm = ChatOllama(
        model=config.OLLAMA_MODEL,
        base_url=config.OLLAMA_BASE_URL,
    )

    # Simple RAG prompt that simulates retrieval
    prompt = ChatPromptTemplate.from_messages([
        ("system", """You are a helpful assistant that answers questions based on retrieved documents.
When you receive a question, you will first see retrieved context, then answer based on that context."""),
        ("human", """Retrieved context:
{context}

Question: {question}

Answer the question based on the retrieved context above.""")
    ])

    chain = prompt | llm
    return chain


def rag_query(
    question: str,
    context: str,
    langfuse_handler: CallbackHandler,
    trace_name: str = None,
    session_id: Optional[str] = None,
) -> str:
    """
    Answer a question using RAG (demonstrates retrieval observations).

    Args:
        question: User question
        context: Retrieved context/document
        langfuse_handler: Langfuse callback handler for tracing
        trace_name: Optional trace name for Langfuse
        session_id: Optional session ID for grouping traces

    Returns:
        Answer string

    Raises:
        ConnectionError: If Ollama is not accessible
        ValueError: If question or context is empty
    """
    if not question or not question.strip():
        raise ValueError("Question cannot be empty")
    if not context or not context.strip():
        raise ValueError("Context cannot be empty")

    chain = create_rag_chain()

    # Prepare config with callbacks and metadata
    invoke_config = {"callbacks": [langfuse_handler]}
    metadata = {}
    if trace_name:
        metadata["trace_name"] = trace_name
    if session_id:
        metadata["session_id"] = session_id
    if metadata:
        invoke_config["metadata"] = metadata

    try:
        result = chain.invoke(
            {"question": question, "context": context},
            config=invoke_config,
        )

        answer = result.content if hasattr(result, "content") else str(result)
        return answer
    except Exception as e:
        if "connection" in str(e).lower() or "refused" in str(e).lower():
            raise ConnectionError(
                f"Failed to connect to Ollama at {config.OLLAMA_BASE_URL}. "
                "Please ensure Ollama is running and the base URL is correct."
            ) from e
        raise

