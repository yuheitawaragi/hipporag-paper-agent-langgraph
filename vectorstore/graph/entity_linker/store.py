import faiss
import numpy as np


class EntityStore:


    def __init__(
        self,
        entities,
        embeddings
    ):

        self.entities = entities

        dim = len(
            embeddings[0]
        )

        self.index = faiss.IndexFlatIP(
            dim
        )


        vectors = np.array(
            embeddings,
            dtype="float32"
        )

        # cosine similarity用
        faiss.normalize_L2(
            vectors
        )

        self.index.add(
            vectors
        )


    def search(
        self,
        embedding,
        k=3
    ):

        vector = np.array(
            [embedding],
            dtype="float32"
        )

        faiss.normalize_L2(
            vector
        )

        scores, ids = self.index.search(
            vector,
            k
        )


        results=[]

        for score, idx in zip(
            scores[0],
            ids[0]
        ):

            results.append(
                {
                    "entity":
                        self.entities[idx],
                    "score":
                        float(score)
                }
            )

        return results