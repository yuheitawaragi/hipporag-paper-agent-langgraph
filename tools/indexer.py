from tools.pdf_parser import PDFParser
from vectorstore.embedding import EmbeddingModel
from vectorstore.faiss_store import FaissStore


class Indexer:

    def __init__(self):

        self.parser = PDFParser()

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

        embeddings = self.embedding_model.embed_documents(
            chunks,
        )

        store = FaissStore()

        store.build(
            embeddings,
            chunks,
        )

        return store, chunks