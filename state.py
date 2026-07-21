from typing import TypedDict, Any, Annotated
from operator import add


class AgentState(TypedDict):

    # ======================
    # User
    # ======================

    query: str
    question: str

    # rag / hipporag / hybrid
    mode: str

    # ======================
    # Search
    # ======================

    papers: list

    # ======================
    # Summary
    # ======================

    summary: str

    # ======================
    # Index
    # ======================

    retriever: Any

    # ======================
    # Graph Retrieval
    # ======================

    graph_retriever: Any

    # ======================
    # Retrieval
    # ======================

    retrieved: Annotated[list, add]

    # ======================
    # Answer
    # ======================

    answer: str