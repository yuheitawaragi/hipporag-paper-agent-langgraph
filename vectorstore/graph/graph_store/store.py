from .serializer import GraphSerializer



class GraphStore:


    def __init__(
        self,
        save_path="data/graph/knowledge_graph.pkl"
    ):

        self.graph = None

        self.save_path = save_path

        self.serializer = GraphSerializer()



    def add_graph(
        self,
        graph
    ):
        """
        GraphBuilderで作ったgraphを登録
        """

        self.graph = graph



    def save(
        self
    ):
        """
        graph保存
        """

        if self.graph is None:
            raise ValueError(
                "Graph is empty"
            )


        self.serializer.save(
            self.graph,
            self.save_path
        )



    def load(
        self
    ):
        """
        graph読み込み
        """

        self.graph = self.serializer.load(
            self.save_path
        )


        return self.graph



    def get_node(
        self,
        node_id
    ):
        """
        node情報取得
        """

        if node_id not in self.graph:
            return None


        return self.graph.nodes[node_id]



    def neighbors(
        self,
        node_id
    ):
        """
        隣接entity取得
        """

        if node_id not in self.graph:
            return []


        return list(
            self.graph.neighbors(node_id)
        )



    def relations(
        self,
        source,
        target
    ):
        """
        entity間のrelation取得

        例:
        GPT-4 -> Transformer
        """

        if not self.graph.has_edge(
            source,
            target
        ):
            return []


        edges = self.graph.get_edge_data(
            source,
            target
        )


        return [
            data["relation"]
            for data in edges.values()
        ]



    def nodes(
        self
    ):
        return list(
            self.graph.nodes()
        )



    def edges(
        self
    ):
        return list(
            self.graph.edges(
                data=True
            )
        )