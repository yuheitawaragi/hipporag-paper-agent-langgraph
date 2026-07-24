class GraphRetriever:

    def __init__(
        self,
        graph_store,
        ppr,
        entity_linker=None
    ):

        self.graph_store = graph_store
        self.ppr = ppr
        self.entity_linker = entity_linker

    # ===================================================
    # HippoRAG2 Retrieval
    # ===================================================

    def retrieve_from_entities(
        self,
        entities,
        top_k=5
    ):

        triples = []
        chunks = []

        # -------------------------------
        # Personalized PageRank
        # -------------------------------

        ranked_entities = self.ppr.top_k(
            entities,
            k=top_k
        )

        visited_chunks = set()

        for entity, entity_score in ranked_entities:

            # ==========================================
            # Triple Retrieval
            # ==========================================

            neighbors = self.graph_store.neighbors(
                entity
            )

            for neighbor in neighbors:

                relations = self.graph_store.relations(
                    entity,
                    neighbor
                )

                for relation in relations:

                    triples.append(
                        {
                            "subject": entity,
                            "relation": relation,
                            "object": neighbor,
                            "entity_score": entity_score,
                            "source": "graph"
                        }
                    )

            # ==========================================
            # Chunk Retrieval (HippoRAG2)
            # ==========================================

            entity_chunks = self.graph_store.get_chunks(
                entity
            )

            for chunk in entity_chunks:

                chunk_id = chunk.get(
                    "chunk_id"
                )

                if chunk_id in visited_chunks:
                    continue

                visited_chunks.add(
                    chunk_id
                )

                chunks.append(
                    {
                        "chunk_id": chunk_id,
                        "entity": entity,
                        "score": entity_score,
                        "source": "graph"
                    }
                )

        chunks = sorted(
            chunks,
            key=lambda x: x["score"],
            reverse=True
        )

        return {
            "triples": triples,
            "chunks": chunks
        }

    # ===================================================
    # Query
    # ===================================================

    def retrieve(
        self,
        query_entities,
        top_k=5
    ):

        if self.entity_linker:

            linked_entities = []

            for entity in query_entities:

                linked = self.entity_linker.link_entity(
                    entity
                )

                linked_entities.append(
                    linked
                )

            query_entities = linked_entities

        return self.retrieve_from_entities(
            query_entities,
            top_k
        )