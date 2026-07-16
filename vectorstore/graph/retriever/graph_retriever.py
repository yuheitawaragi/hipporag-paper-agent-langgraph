class GraphRetriever:


    def __init__(
        self,
        graph_store,
        entity_linker=None
    ):

        self.graph_store = graph_store

        self.entity_linker = entity_linker



    def retrieve_entity(
        self,
        entity,
        depth=1
    ):
        """
        entity周辺探索
        """


        results = []


        if entity not in self.graph_store.graph:

            return results



        current_nodes = [
            entity
        ]


        visited = set()



        for _ in range(depth):

            next_nodes=[]


            for node in current_nodes:


                if node in visited:
                    continue


                visited.add(node)



                neighbors = (
                    self.graph_store.neighbors(
                        node
                    )
                )


                for neighbor in neighbors:


                    relation = (
                        self.graph_store.relations(
                            node,
                            neighbor
                        )
                    )


                    results.append(
                        {
                            "subject": node,
                            "relation": relation[0],
                            "object": neighbor
                        }
                    )


                    next_nodes.append(
                        neighbor
                    )


            current_nodes = next_nodes



        return results



    def retrieve(
        self,
        query_entity,
        depth=1
    ):

        """
        Query entityからgraph検索
        """


        return self.retrieve_entity(
            query_entity,
            depth
        )