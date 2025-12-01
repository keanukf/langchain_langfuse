"""Prompt templates for summarization."""

from langchain_core.prompts import ChatPromptTemplate, SystemMessagePromptTemplate, HumanMessagePromptTemplate

SYSTEM_PROMPT = """You are an expert academic summarizer. Your task is to analyze the provided text and create a structured summary.

Instructions:
- Extract 3-5 key points from the text
- Provide a one-sentence takeaway that captures the main message
- Maintain an academic and professional tone
- Format your response as structured markdown

Output Format:
## Key Points
1. [First key point]
2. [Second key point]
3. [Third key point]
[Additional points as needed]

## Takeaway
[One sentence summarizing the main message]"""

USER_PROMPT = "Summarize the following text:\n\n{text}"


def get_summarization_prompt() -> ChatPromptTemplate:
    """
    Create a chat prompt template for summarization.

    Returns:
        ChatPromptTemplate configured for summarization task
    """
    system_message = SystemMessagePromptTemplate.from_template(SYSTEM_PROMPT)
    human_message = HumanMessagePromptTemplate.from_template(USER_PROMPT)

    prompt = ChatPromptTemplate.from_messages([system_message, human_message])

    return prompt

