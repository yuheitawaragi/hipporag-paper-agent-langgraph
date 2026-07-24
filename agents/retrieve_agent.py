from vectorstore.query.entity_extractor.hybrid_extractor import (
    HybridQueryEntityExtractor
)


def retrieve_node(state):

    mode = state.get("mode", "rag")

    contexts = []

    # ==========================================
    # Query Entity Extraction
    # ==========================================

    extractor = HybridQueryEntityExtractor()

    query_entities = extractor.extract(
        state["question"]
    )

    print("=" * 60)
    print("Query")
    print(state["question"])
    print()

    print("Extracted Entities")
    print(query_entities)
    print("=" * 60)

    # =====================================================
    # RAG (Dense Retrieval)
    # =====================================================

    if mode == "rag":

        results = state["retriever"].retrieve(
            topic=state["query"],
            question=state["question"],
        )

        for node in results:

            # ------------------------------------------
            # Qdrant / FAISS
            # ------------------------------------------

            if isinstance(node, dict):

                contexts.append(
                    {
                        "text": node.get("text", ""),
                        "title": node.get("title", "Unknown"),
                        "authors": node.get("authors", []),
                        "published": node.get("published", ""),
                        "page": node.get("page", ""),
                        "pdf_url": node.get("pdf_url", ""),
                        "score": node.get("score", 0),
                        "source": "vector",
                    }
                )

            # ------------------------------------------
            # LlamaIndex
            # ------------------------------------------

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

    # =====================================================
    # HippoRAG2
    # =====================================================

    elif mode == "hipporag":

        graph_results = state[
            "graph_retriever"
        ].retrieve(
            query_entities=query_entities
        )

        # ------------------------------
        # Chunk Retrieval
        # ------------------------------

        for chunk in graph_results.get(
            "chunks",
            []
        ):

            contexts.append(
                {
                    "text": chunk.get(
                        "text",
                        ""
                    ),

                    "chunk_id": chunk.get(
                        "chunk_id",
                        ""
                    ),

                    "entity": chunk.get(
                        "entity",
                        ""
                    ),

                    "score": chunk.get(
                        "score",
                        0
                    ),

                    "source": "graph",
                }
            )

    # =====================================================
    # Hybrid
    # Dense + Graph Fusion
    # =====================================================

    elif mode == "hybrid":

        fusion_results = state[
            "fusion_retriever"
        ].retrieve(

            query=state["question"],

            query_entities=query_entities,

            top_k=10

        )

        contexts.extend(
            fusion_results
        )

    # =====================================================
    # Sort
    # =====================================================

    contexts = sorted(

        contexts,

        key=lambda x: x.get(
            "score",
            0
        ),

        reverse=True

    )

    return {

        "retrieved": contexts

    }