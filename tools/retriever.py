from tools.pdf_parser import PDFParser
from vectorstore.faiss.embedding import EmbeddingModel
from vectorstore.faiss.faiss_store import FaissStore


class Retriever:

    def __init__(self, backend="faiss"):
        self.backend = backend
        self.parser = PDFParser()
        if backend == "faiss":
            self.embedding_model = EmbeddingModel()
            self.store = FaissStore()
        elif backend == "llamaindex":
            self.index = None
        elif backend == "property_graph":
            self.index = None
        # 検索結果との対応を保持
        self.documents = []

    def build_index(self, papers):

        all_chunks = []
        self.documents = []

        for i, paper in enumerate(papers):

            filename = f"paper_{i}.pdf"

            pdf_path = self.parser.download_pdf(
                paper["pdf_url"],
                filename,
            )

            pages = self.parser.extract_pages(pdf_path)

            chunks = self.parser.chunk_pages(pages)

            for chunk in chunks:
                embedding_doc = {
        "page": chunk["page"],
        "chunk_id": chunk["chunk_id"],
        "text": f"""
Title:
{paper["title"]}

Abstract:
{paper["summary"]}

Content:
{chunk["text"]}
"""
    }
                # Embedding用
                all_chunks.append(embedding_doc)
                # 検索結果として返すメタデータ
                self.documents.append(
        {
            "title": paper["title"],
            "authors": paper["authors"],
            "published": paper["published"],
            "pdf_url": paper["pdf_url"],
            "entry_id": paper["entry_id"],
            "page": chunk["page"],
            "chunk_id": chunk["chunk_id"],
            "text": chunk["text"],
        }
    )

        if self.backend == "faiss":
            embeddings = self.embedding_model.embed_documents(all_chunks)
            self.store.build(
            embeddings,
            self.documents,
        )
        elif self.backend == "llamaindex":
            from vectorstore.llamaindex.builder import LlamaIndexBuilder
            builder = LlamaIndexBuilder()
            self.index = builder.build(
        all_chunks
    )
        elif self.backend == "property_graph":
            from vectorstore.llamaindex.property_graph import PropertyGraphStore
            store = PropertyGraphStore()
            self.index = store.build(
                all_chunks
            )

    def retrieve(self,
    topic,
    question,
    k=5,):
        query = f"""
Topic:
{topic}

Question:
{question}
"""
        

        if self.backend == "faiss":
            query_embedding = self.embedding_model.embed(query)
            results = self.store.search(
            query_embedding,
            k=k,
        )
            return results
        elif self.backend == "llamaindex":
            from vectorstore.llamaindex.retriever import LlamaRetriever
            retriever = LlamaRetriever(
        self.index,
    )
            return retriever.retrieve(query)
        elif self.backend == "property_graph":
            retriever = self.index.as_retriever(
                similarity_top_k=k
            )
            return retriever.retrieve(
                query
            )