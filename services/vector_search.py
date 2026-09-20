import faiss
import numpy as np


class VectorSearcher:

    def __init__(self, embeddings):
        self.embeddings = np.asarray(
            embeddings,
            dtype="float32"
        )

        dimension = self.embeddings.shape[1]

        self.index = faiss.IndexFlatIP(dimension)

        self.index.add(self.embeddings)

    def search(
        self,
        query_embedding,
        top_k=3
    ):
        query = np.asarray(
            [query_embedding],
            dtype="float32"
        )

        scores, indices = self.index.search(
            query,
            top_k
        )

        return scores[0], indices[0]