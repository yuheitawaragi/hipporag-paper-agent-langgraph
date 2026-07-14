class LlamaRetriever:

    def __init__(self, index):

        self.retriever = index.as_retriever(
            similarity_top_k=5
        )

    def retrieve(self, query: str):

        return self.retriever.retrieve(query)