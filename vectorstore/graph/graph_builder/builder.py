import networkx as nx

from .schema import (
    GraphNode,
    GraphEdge
)


class GraphBuilder:

    def __init__(self):

        # ---------------------------------
        # Knowledge Graph
        # ---------------------------------

        self.graph = nx.MultiDiGraph()

    # --------------------------------------------------
    # Entity
    # --------------------------------------------------

    def add_entity(
        self,
        node: GraphNode
    ):

        if node.id not in self.graph:

            self.graph.add_node(
                node.id,
                name=node.name,
                entity_type=node.entity_type,
                chunks=[]
            )

    # --------------------------------------------------
    # Relation
    # --------------------------------------------------

    def add_relation(
        self,
        edge: GraphEdge
    ):

        self.graph.add_edge(
            edge.source,
            edge.target,
            relation=edge.relation,
            **edge.metadata
        )

    # --------------------------------------------------
    # Chunk Memory
    # --------------------------------------------------

    def add_chunk(
        self,
        entity,
        chunk
    ):

        if entity not in self.graph:

            self.graph.add_node(
                entity,
                name=entity,
                entity_type="entity",
                chunks=[]
            )

        node = self.graph.nodes[entity]

        if "chunks" not in node:

            node["chunks"] = []

        # ---------------------------------
        # 重複防止
        # ---------------------------------

        exists = any(

            c["chunk_id"] == chunk["chunk_id"]

            for c in node["chunks"]

        )

        if not exists:

            node["chunks"].append(chunk)

    # --------------------------------------------------
    # Triple
    # --------------------------------------------------

    def add_triple(
        self,
        triple,
        chunk_dict
    ):

        subject = triple.subject
        obj = triple.object
        predicate = triple.predicate

        # -----------------------------
        # Entity
        # -----------------------------

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

        # -----------------------------
        # Relation
        # -----------------------------

        self.add_relation(

            GraphEdge(
                source=subject,
                target=obj,
                relation=predicate
            )

        )

        # -----------------------------
        # HippoRAG2
        # Entity -> Chunk Memory
        # -----------------------------

        chunk_id = getattr(
            triple,
            "chunk_id",
            None
        )

        if chunk_id is not None:

            chunk = chunk_dict.get(
                chunk_id
            )

            if chunk is not None:

                self.add_chunk(
                    subject,
                    chunk
                )

                self.add_chunk(
                    obj,
                    chunk
                )

    # --------------------------------------------------
    # Build
    # --------------------------------------------------

    def build(
        self,
        triples,
        chunks=None
    ):

        chunk_dict = {}

        if chunks:

            chunk_dict = {

                chunk["chunk_id"]: chunk

                for chunk in chunks

            }

        for triple in triples:

            self.add_triple(
                triple,
                chunk_dict
            )

        return self.graph