from typing import TypedDict, Any


class AgentState(TypedDict):

    # User Input
    query: str
    question: str

    # Search
    papers: list

    # Summary
    summary: str

    # Index
    retriever: Any

    # Retrieve
    retrieved: list

    # Final Answer
    answer: str