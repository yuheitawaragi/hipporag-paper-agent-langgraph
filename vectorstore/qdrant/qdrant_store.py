from qdrant_client import QdrantClient
from qdrant_client.models import (
    Distance,
    VectorParams,
    PointStruct,
)


class QdrantStore:

    def __init__(
        self,
        collection_name="papers",
    ):

        # ローカル保存
        self.client = QdrantClient(
            path="./qdrant_db"
        )

        self.collection_name = collection_name

    def build(
        self,
        embeddings,
        documents,
    ):

        dimension = len(
            embeddings[0]
        )

        collections = self.client.get_collections()

        names = [
            c.name
            for c in collections.collections
        ]

        if self.collection_name not in names:

            self.client.create_collection(
                collection_name=self.collection_name,
                vectors_config=VectorParams(
                    size=dimension,
                    distance=Distance.COSINE,
                ),
            )

        points = []

        for idx, (
            vector,
            doc,
        ) in enumerate(
            zip(
                embeddings,
                documents,
            )
        ):

            points.append(

                PointStruct(
                    id=idx,
                    vector=vector,
                    payload=doc,
                )

            )

        self.client.upsert(
            collection_name=self.collection_name,
            points=points,
        )

    def search(
        self,
        query_vector,
        k=3,
    ):

        hits = self.client.query_points(
            collection_name=self.collection_name,
            query=query_vector,
            limit=k,
        ).points

        results = []

        for hit in hits:

            results.append(
                hit.payload
            )

        return results