def retrieve_node(state):

    results = state["retriever"].retrieve(
        topic=state["query"],
        question=state["question"],
    )


    contexts = []

    for node in results:

        contexts.append(
            {
                "text": node.node.text,
                "title": node.node.metadata.get(
                    "title",
                    "Unknown"
                ),
                "authors": node.node.metadata.get(
                    "authors",
                    []
                ),
                "published": node.node.metadata.get(
                    "published",
                    ""
                ),
                "page": node.node.metadata.get(
                    "page",
                    ""
                ),
                "pdf_url": node.node.metadata.get(
                    "pdf_url",
                    ""
                ),
                "score": node.score
            }
        )


    return {
        "retrieved": contexts
    }