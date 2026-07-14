class HybridRetriever:

    def __init__(
        self,
        vector_retriever,
        graph_retriever,
    ):

        self.vector = vector_retriever
        self.graph = graph_retriever

    def retrieve(self, query):

        vector_docs = self.vector.retrieve(query)

        graph_docs = self.graph.retrieve(query)

        return vector_docs + graph_docs