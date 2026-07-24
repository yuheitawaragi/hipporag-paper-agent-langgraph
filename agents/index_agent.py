from tools.retriever import Retriever

from vectorstore.graph.openie.extractor import OpenIEExtractor
from vectorstore.graph.openie.parser import TripleParser

from vectorstore.graph.graph_builder.builder import GraphBuilder
from vectorstore.graph.graph_store.store import GraphStore

from vectorstore.graph.entity_linker.store import EntityStore
from vectorstore.graph.entity_linker.linker import EntityLinker
from vectorstore.graph.entity_linker.embedder import EntityEmbedder

from vectorstore.graph.ppr.pagerank import PersonalizedPageRank
from vectorstore.graph.retriever.graph_retriever import GraphRetriever

from vectorstore.pdf.pdf_loader import PDFLoader
from vectorstore.pdf.chunker import PDFChunker


def index_node(state):

    mode = state.get("mode", "rag")

    result = {}

    # =====================================
    # Vector Index
    # =====================================

    if mode in ["rag", "hybrid"]:

        retriever = Retriever(
            backend="qdrant"
        )

        retriever.build_index(
            state["papers"]
        )

        result["retriever"] = retriever

    # =====================================
    # Graph Index
    # =====================================

    if mode in ["hipporag", "hybrid"]:

        extractor = OpenIEExtractor()

        parser = TripleParser()

        loader = PDFLoader()

        chunker = PDFChunker()

        triples = []

        chunks = []

        chunk_index = 0

        for paper in state["papers"]:

            print("=" * 50)
            print(paper["title"])

            # ----------------------------
            # PDF全文取得
            # ----------------------------

            text = loader.load(
                paper["pdf_path"]
            )

            # ----------------------------
            # Chunk分割
            # ----------------------------

            paper_chunks = chunker.split(
                text
            )

            # ----------------------------
            # ChunkごとにOpenIE
            # ----------------------------

            for chunk in paper_chunks:

                chunk_id = f"chunk_{chunk_index}"

                chunks.append(
                    {
                        "chunk_id": chunk_id,
                        "text": chunk
                    }
                )

                raw = extractor.extract(
                    chunk
                )

                paper_triples = parser.parse(
                    raw
                )

                for triple in paper_triples:

                    triple.chunk_id = chunk_id

                    triples.append(
                        triple
                    )

                chunk_index += 1

        # =====================================
        # Graph構築
        # =====================================

        builder = GraphBuilder()

        graph = builder.build(
            triples,
            chunks
        )

        print(
            f"Graph Nodes : {graph.number_of_nodes()}"
        )

        print(
            f"Graph Edges : {graph.number_of_edges()}"
        )

        store = GraphStore()

        store.add_graph(
            graph
        )

        # =====================================
        # Entity Index
        # =====================================

        entities = store.nodes()

        print(
            f"Entity Count : {len(entities)}"
        )

        entity_embedder = EntityEmbedder()

        entity_embeddings = entity_embedder.embed(
            entities
        )

        entity_store = EntityStore(
            entities,
            entity_embeddings
        )

        entity_linker = EntityLinker(
            entity_store,
            entity_embedder
        )

        # =====================================
        # Personalized PageRank
        # =====================================

        ppr = PersonalizedPageRank(
            store
        )

        graph_retriever = GraphRetriever(
            store,
            ppr,
            entity_linker
        )

        result["graph_retriever"] = graph_retriever

    return result