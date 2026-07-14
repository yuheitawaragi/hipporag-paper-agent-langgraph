import faiss
import numpy as np


class FaissStore:

    def __init__(self):

        self.index = None
        self.metadata = []

    def build(
        self,
        embeddings,
        documents,
    ):

        vectors = np.array(
            embeddings,
            dtype=np.float32,
        )

        dimension = vectors.shape[1]

        self.index = faiss.IndexFlatL2(
            dimension
        )

        self.index.add(vectors)

        self.metadata = documents

    def search(
        self,
        query_vector,
        k=3,
    ):

        query = np.array(
            [query_vector],
            dtype=np.float32,
        )

        distance, index = self.index.search(
            query,
            k,
        )

        results = []

        for idx in index[0]:
            if idx == -1:
                continue

            results.append(
                self.metadata[idx]
            )

        return results