from tools.pdf_parser import PDFParser
from vectorstore.faiss.embedding import EmbeddingModel
from vectorstore.faiss.faiss_store import FaissStore
from vectorstore.qdrant.qdrant_store import QdrantStore


class Indexer:

    def __init__(self, backend="faiss"):

        self.backend = backend

        self.parser = PDFParser()

        if backend == "faiss":
            self.embedding_model = EmbeddingModel()

    def build_index(
    self,
    pdf_url,
    filename="paper.pdf",
):
        pdf_path = self.parser.download_pdf(
        pdf_url,
        filename,
    )
        pages = self.parser.extract_pages(
        pdf_path,
    )
        chunks = self.parser.chunk_pages(
        pages,
    )
        if self.backend == "faiss":
            embeddings = self.embedding_model.embed_documents(
            chunks,
        )
            store = FaissStore()
            store.build(
            embeddings,
            chunks,
        )
        elif self.backend == "llamaindex":
            from vectorstore.llamaindex.builder import LlamaIndexBuilder
            builder = LlamaIndexBuilder()
            store = builder.build(
        chunks,
    )
        elif self.backend == "qdrant":

            embeddings = self.embedding_model.embed_documents(chunks)

            store = QdrantStore()

            store.build(
                embeddings,
                chunks,
            )
        else:
            raise ValueError(f"Unknown backend: {self.backend}")
        
        return store, chunks