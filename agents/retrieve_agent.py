def retrieve_node(state):

    results = state["retriever"].retrieve(
    topic=state["query"],
    question=state["question"],
)

    return {
        "retrieved": results
    }