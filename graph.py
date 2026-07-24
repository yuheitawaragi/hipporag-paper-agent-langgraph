from langgraph.graph import StateGraph, START, END

from state import AgentState

from agents.search_agent import search_node
from agents.summary_agent import summary_node
from agents.retrieve_agent import retrieve_node
from agents.answer_agent import answer_node
from agents.index_agent import index_node

from agents.download_agent import download_node


workflow = StateGraph(AgentState)

# Nodes
workflow.add_node("search", search_node)
workflow.add_node(
    "download",
    download_node
)
workflow.add_node("summarizer", summary_node)
workflow.add_node("retrieve", retrieve_node)
workflow.add_node("generate_answer", answer_node)
workflow.add_node("index", index_node)

# Flow
workflow.set_entry_point("search")

workflow.add_edge("search", "download")
workflow.add_edge(
    "download",
    "summarizer"
)
workflow.add_edge("summarizer", "index")
workflow.add_edge("index", "retrieve")
workflow.add_edge("retrieve", "generate_answer")
workflow.add_edge("generate_answer", END)

graph = workflow.compile()