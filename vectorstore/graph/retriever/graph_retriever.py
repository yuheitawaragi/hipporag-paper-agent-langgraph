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
        PPRで重要entityを取得し、
        周辺triplesを取得
        """


        results = []


        # =====================
        # 1. Personalized PageRank
        # =====================

        ranked_entities = self.ppr.top_k(
            entities,
            k=top_k
        )


        # =====================
        # 2. 上位entityからgraph探索
        # =====================

        for entity, score in ranked_entities:


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


                if not relations:
                    continue

                for relation in relations:

                    results.append(
                        {
                            "subject": entity,
                            "relation": relation,
                            "object": neighbor,
                            "score": score
                        }
                    )



                


        return results



    def retrieve(
        self,
        query_entity,
        top_k=5
    ):
        """
        Query entityからGraph Retrieval
        """


        # entity linkerがある場合
        if self.entity_linker:


            query_entity = (
                self.entity_linker.link_entity(
                    query_entity
                )
            )



        return self.retrieve_from_entities(
            [query_entity],
            top_k
        )