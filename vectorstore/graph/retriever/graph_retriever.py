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



    def retrieve_from_entities(
        self,
        entities,
        top_k=5
    ):
        """
        HippoRAG style retrieval

        Query entities
            ↓
        Personalized PageRank
            ↓
        Related entities
            ↓
        Triple retrieval
            ↓
        Chunk retrieval
        """

        triples = []

        chunks = []


        # ==================================
        # 1. PPR entity ranking
        # ==================================

        ranked_entities = self.ppr.top_k(
            entities,
            k=top_k
        )


        # ==================================
        # 2. Entityから情報取得
        # ==================================

        for entity, entity_score in ranked_entities:


            # ------------------------------
            # Triple retrieval
            # ------------------------------

            neighbors = (
                self.graph_store.neighbors(
                    entity
                )
            )


            for neighbor in neighbors:


                relations = (
                    self.graph_store.relations(
                        entity,
                        neighbor
                    )
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



            # ------------------------------
            # Entity -> Chunk retrieval
            # HippoRAG2 style
            # ------------------------------

            if hasattr(
                self.graph_store,
                "get_chunks"
            ):


                entity_chunks = (
                    self.graph_store.get_chunks(
                        entity
                    )
                )


                for chunk in entity_chunks:


                    chunks.append(
                        {
                            "text": chunk["text"],

                            "chunk_id": chunk.get(
                                "id",
                                None
                            ),

                            "entity": entity,

                            "score": entity_score,

                            "source": "graph"
                        }
                    )



        return {
            "triples": triples,

            "chunks": chunks
        }




    def retrieve(
        self,
        query_entities,
        top_k=5
    ):
        """
        Query entity retrieval

        query_entities:
            list[str]

        Example:
            [
                "Agentic RAG",
                "query decomposition"
            ]
        """



        # ==================================
        # Entity linking
        # ==================================

        if self.entity_linker:


            linked_entities = []


            for entity in query_entities:


                linked = (
                    self.entity_linker.link_entity(
                        entity
                    )
                )


                linked_entities.append(
                    linked
                )


            query_entities = linked_entities



        return self.retrieve_from_entities(
            query_entities,
            top_k
        )