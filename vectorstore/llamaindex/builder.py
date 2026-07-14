from llama_index.core import Document
from llama_index.core import VectorStoreIndex


class LlamaIndexBuilder:

    def build(self, chunks):

        documents = []

        for chunk in chunks:

            documents.append(
                Document(
                    text=chunk["text"],
                    metadata={
    "page": chunk["page"],
    "chunk_id": chunk["chunk_id"],
    "title": chunk.get("title",""),
    "authors": chunk.get("authors",[]),
    "published": chunk.get("published",""),
    "pdf_url": chunk.get("pdf_url",""),
},
                )
            )

        index = VectorStoreIndex.from_documents(
            documents
        )

        return index

    @staticmethod
    def persist(index, persist_dir):

        index.storage_context.persist(
            persist_dir=persist_dir
        )