from tools.retriever import Retriever


def index_node(state):

    #retriever = Retriever(backend="llamaindex")
    retriever = Retriever(backend="qdrant")

    retriever.build_index(
        state["papers"]
    )

    return {
        "retriever": retriever
    }