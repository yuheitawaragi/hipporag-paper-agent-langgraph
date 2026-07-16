import networkx as nx


class PersonalizedPageRank:


    def __init__(
        self,
        graph_store
    ):

        self.graph_store = graph_store



    def rank(
        self,
        seed_entities,
        alpha=0.85
    ):
        """
        Personalized PageRank実行

        seed_entities:
            質問に関連するentity

        alpha:
            damping factor
        """


        graph = self.graph_store.graph


        if graph is None:
            raise ValueError(
                "Graph is empty"
            )


        personalization = {}



        # 初期entityの重み
        for node in graph.nodes:

            if node in seed_entities:

                personalization[node] = 1.0

            else:

                personalization[node] = 0.0



        scores = nx.pagerank(
            graph,
            alpha=alpha,
            personalization=personalization
        )


        return scores



    def top_k(
        self,
        seed_entities,
        k=10
    ):
        """
        重要entity上位取得
        """


        scores = self.rank(
            seed_entities
        )


        ranked = sorted(
            scores.items(),
            key=lambda x:x[1],
            reverse=True
        )


        return ranked[:k]