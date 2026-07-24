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

from vectorstore.fusion.fusion_retriever import FusionRetriever

from vectorstore.reranker.cross_encoder import CrossEncoderReranker

from vectorstore.pdf.pdf_loader import PDFLoader
from vectorstore.pdf.chunker import PDFChunker



def index_node(state):

    mode = state.get(
        "mode",
        "rag"
    )


    result = {}

    retriever = None



    # =================================================
    # Dense Vector Index
    # =================================================

    if mode in [
        "rag",
        "hybrid"
    ]:

        retriever = Retriever(
            backend="qdrant"
        )


        retriever.build_index(
            state["papers"]
        )


        result["retriever"] = retriever



    # =================================================
    # Graph Index
    # =================================================

    if mode in [
        "hipporag",
        "hybrid"
    ]:


        extractor = OpenIEExtractor()

        parser = TripleParser()

        loader = PDFLoader()

        chunker = PDFChunker()



        triples = []

        chunks = []


        chunk_index = 0



        for paper in state["papers"]:


            print("=" * 50)
            print(
                paper["title"]
            )



            # -------------------------------
            # PDF Load
            # -------------------------------

            text = loader.load(
                paper["pdf_path"]
            )


            if not text:

                print(
                    "Skip empty PDF"
                )

                continue



            # -------------------------------
            # Chunk
            # -------------------------------

            paper_chunks = chunker.split(
                text
            )



            for chunk in paper_chunks:


                if not chunk.strip():

                    continue



                chunk_id = (
                    f"chunk_{chunk_index}"
                )



                # -------------------------------
                # OpenIE
                # -------------------------------

                raw = extractor.extract(
                    chunk
                )


                print(
                    "RAW OPENIE RESULT"
                )

                print(raw)

                print("="*50)



                paper_triples = parser.parse(
                    raw
                )



                entities = set()



                for triple in paper_triples:


                    # 空除外
                    if not triple.subject:
                        continue

                    if not triple.object:
                        continue



                    entities.add(
                        triple.subject.strip()
                    )

                    entities.add(
                        triple.object.strip()
                    )



                    triple.chunk_id = chunk_id


                    triples.append(
                        triple
                    )



                chunks.append(
                    {
                        "chunk_id": chunk_id,

                        "text": chunk,

                        "entities": list(
                            entities
                        )
                    }
                )


                chunk_index += 1




        # =================================================
        # Graph Build
        # =================================================

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



        # =================================================
        # Entity Embedding
        # =================================================

        entities = list(
            store.nodes()
        )


        # 空文字除外
        entities = [
            e.strip()
            for e in entities
            if isinstance(e, str)
            and e.strip()
        ]



        print(
            f"Entity Count : {len(entities)}"
        )



        entity_embedder = EntityEmbedder(
            batch_size=500
        )


        entity_embeddings = (
            entity_embedder.embed(
                entities
            )
        )



        entity_store = EntityStore(
            entities,
            entity_embeddings
        )



        entity_linker = EntityLinker(
            entity_store,
            entity_embedder
        )




        # =================================================
        # Graph Retriever
        # =================================================

        ppr = PersonalizedPageRank(
            store
        )



        graph_retriever = GraphRetriever(
            store,
            ppr,
            entity_linker
        )



        result[
            "graph_retriever"
        ] = graph_retriever




        # =================================================
        # Hybrid Fusion
        # =================================================

        if mode == "hybrid":


            fusion_method = state.get(
                "fusion_method",
                "rrf"
            )


            fusion_alpha = state.get(
                "fusion_alpha",
                0.6
            )



            reranker = CrossEncoderReranker(

                model_name=state.get(

                    "reranker_model",

                    "BAAI/bge-reranker-base"

                )

            )



            fusion_retriever = FusionRetriever(

                dense_retriever=retriever,

                graph_retriever=graph_retriever,

                method=fusion_method,

                alpha=fusion_alpha,

                reranker=reranker

            )



            result[
                "fusion_retriever"
            ] = fusion_retriever



    return result