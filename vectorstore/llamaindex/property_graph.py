from llama_index.core import (
    Document,
    PropertyGraphIndex,
)


class PropertyGraphStore:

    def __init__(self):

        self.index = None


    def build(self, chunks):

        documents = []

        for chunk in chunks:

            documents.append(
                Document(
                    text=chunk["text"],
                    metadata={
                        "page": chunk["page"],
                        "chunk_id": chunk["chunk_id"],
                    },
                )
            )


        self.index = PropertyGraphIndex.from_documents(
            documents
        )


        return self.index


    def as_retriever(self, top_k=5):

        return self.index.as_retriever(
            similarity_top_k=top_k
        )


    def search(
        self,
        query,
        k=5,
    ):

        retriever = self.as_retriever(
            top_k=k
        )

        results = retriever.retrieve(
            query
        )


        return results