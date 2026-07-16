from vectorstore.graph.graph_builder.builder import GraphBuilder
from vectorstore.graph.graph_store.store import GraphStore
from vectorstore.graph.ppr.pagerank import PersonalizedPageRank
from vectorstore.graph.retriever.graph_retriever import GraphRetriever


class Triple:

    def __init__(
        self,
        subject,
        predicate,
        object
    ):
        self.subject=subject
        self.predicate=predicate
        self.object=object



triples=[

Triple(
    "GPT-4",
    "uses",
    "Transformer"
),

Triple(
    "Transformer",
    "contains",
    "Attention"
)

]


# graph作成

builder=GraphBuilder()

graph=builder.build(
    triples
)



# store

store=GraphStore()

store.add_graph(
    graph
)



# PPR

ppr=PersonalizedPageRank(
    store
)



# Retriever

retriever=GraphRetriever(
    store,
    ppr
)



result=retriever.retrieve(
    "GPT-4"
)


print(result)