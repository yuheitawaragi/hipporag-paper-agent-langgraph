from tools.retriever import Retriever

from vectorstore.graph.openie.extractor import OpenIEExtractor
from vectorstore.graph.openie.parser import TripleParser

from vectorstore.graph.graph_builder.builder import GraphBuilder
from vectorstore.graph.graph_store.store import GraphStore
from vectorstore.graph.ppr.pagerank import PersonalizedPageRank
from vectorstore.graph.retriever.graph_retriever import GraphRetriever



def index_node(state):


    # =====================
    # Vector Index
    # =====================

    retriever = Retriever(
        backend="qdrant"
    )

    retriever.build_index(
        state["papers"]
    )



    # =====================
    # Graph Index
    # =====================

    extractor = OpenIEExtractor()

    parser = TripleParser()


    triples = []


    for paper in state["papers"]:


        raw = extractor.extract(
            paper["summary"]
        )


        paper_triples = parser.parse(
            raw
        )


        triples.extend(
            paper_triples
        )



    # Graph構築

    builder = GraphBuilder()

    graph = builder.build(
        triples
    )


    store = GraphStore()

    store.add_graph(
        graph
    )


    ppr = PersonalizedPageRank(
        store
    )


    graph_retriever = GraphRetriever(
        store,
        ppr
    )


    return {

        "retriever": retriever,

        "graph_retriever": graph_retriever

    }