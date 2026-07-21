def retrieve_node(state):

    contexts = []

    # ======================
    # 1. Vector Retrieval
    # ======================

    if "retriever" in state:

        results = state["retriever"].retrieve(
            topic=state["query"],
            question=state["question"],
        )

        for node in results:

            # ======================
            # Qdrant / FAISS形式
            # ======================

            if isinstance(node, dict):

                contexts.append(
                    {
                        "text": node.get(
                            "text",
                            ""
                        ),

                        "title": node.get(
                            "title",
                            "Unknown"
                        ),

                        "authors": node.get(
                            "authors",
                            []
                        ),

                        "published": node.get(
                            "published",
                            ""
                        ),

                        "page": node.get(
                            "page",
                            ""
                        ),

                        "pdf_url": node.get(
                            "pdf_url",
                            ""
                        ),

                        "score": node.get(
                            "score",
                            0
                        ),

                        "source": "vector",
                    }
                )

            # ======================
            # LlamaIndex形式
            # ======================

            else:

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

                        "score": node.score,

                        "source": "vector",
                    }
                )

    # ======================
    # 2. Graph Retrieval
    # ======================

    if "graph_retriever" in state:

        graph_results = (
            state["graph_retriever"].retrieve(
                state["query"]
            )
        )

        for triple in graph_results:

            contexts.append(
                {
                    "text":
                    f"""
{triple["subject"]}
 -- {triple["relation"]} -->
{triple["object"]}
""",

                    "score":
                    triple.get(
                        "entity_score",
                        0
                    ),

                    "source": "graph",
                }
            )

    # ======================
    # Sort by score
    # ======================

    contexts = sorted(
        contexts,
        key=lambda x: x.get("score", 0),
        reverse=True,
    )

    return {
        "retrieved": contexts
    }