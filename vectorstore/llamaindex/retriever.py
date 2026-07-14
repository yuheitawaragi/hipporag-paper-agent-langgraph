class LlamaRetriever:

    def __init__(self, index):

        self.retriever = index.as_retriever(
            similarity_top_k=5
        )


    def retrieve(self, query: str):

        nodes = self.retriever.retrieve(query)

        results = []

        for node in nodes:

            results.append(
                {
                    "title": node.metadata.get(
                        "title",
                        ""
                    ),

                    "authors": node.metadata.get(
                        "authors",
                        ""
                    ),

                    "published": node.metadata.get(
                        "published",
                        ""
                    ),

                    "pdf_url": node.metadata.get(
                        "pdf_url",
                        ""
                    ),

                    "page": node.metadata.get(
                        "page",
                        ""
                    ),

                    "chunk_id": node.metadata.get(
                        "chunk_id",
                        ""
                    ),

                    "text": node.text,
                    
                    "score": node.score,
                }
            )

        return results