import networkx as nx

from .schema import (
    GraphNode,
    GraphEdge
)



class GraphBuilder:


    def __init__(self):

        # MultiDiGraph:
        # 同じentity間に複数relationを許可
        self.graph = nx.MultiDiGraph()



    def add_entity(
        self,
        node: GraphNode
    ):
        """
        Entity node追加
        """


        self.graph.add_node(
            node.id,
            name=node.name,
            entity_type=node.entity_type,
            **node.metadata
        )



    def add_relation(
        self,
        edge: GraphEdge
    ):
        """
        Relation追加
        """


        self.graph.add_edge(
            edge.source,
            edge.target,
            relation=edge.relation,
            **edge.metadata
        )



    def add_triple(
        self,
        triple
    ):
        """
        EntityLinker後のTripleをGraphへ追加
        """


        subject = triple.subject

        obj = triple.object

        predicate = triple.predicate



        # node追加

        self.add_entity(
            GraphNode(
                id=subject,
                name=subject
            )
        )


        self.add_entity(
            GraphNode(
                id=obj,
                name=obj
            )
        )


        # edge追加

        self.add_relation(
            GraphEdge(
                source=subject,
                target=obj,
                relation=predicate
            )
        )



    def build(
        self,
        triples
    ):
        """
        Triple listからGraph生成
        """


        for triple in triples:

            self.add_triple(
                triple
            )


        return self.graph