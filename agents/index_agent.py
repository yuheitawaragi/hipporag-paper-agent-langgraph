from tools.retriever import Retriever


def index_node(state):

    retriever = Retriever()

    retriever.build_index(
        state["papers"]
    )

    return {
        "retriever": retriever
    }