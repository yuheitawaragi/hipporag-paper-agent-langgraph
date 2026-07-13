from tools.pdf_parser import PDFParser
from vectorstore.embedding import EmbeddingModel
from vectorstore.faiss_store import FaissStore


class Retriever:

    def __init__(self):
        self.parser = PDFParser()
        self.embedding_model = EmbeddingModel()
        self.store = FaissStore()

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

        embeddings = self.embedding_model.embed_documents(all_chunks)

        self.store.build(
            embeddings,
            self.documents,
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
        

        query_embedding = self.embedding_model.embed(question)

        results = self.store.search(
            query_embedding,
            k=k,
        )

        return results