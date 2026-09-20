from services.semantic_search import SemanticSearcher
from services.vector_search import VectorSearcher


texts = [
    "battery powered toy car for children",
    "cotton shirt for adults",
    "plastic food storage container"
]


searcher = SemanticSearcher()

embeddings = searcher.encode(texts)

vector_searcher = VectorSearcher(embeddings)


query = "rechargeable toy car for kids"

query_embedding = searcher.encode([query])[0]

scores, indices = vector_searcher.search(
    query_embedding,
    top_k=3
)


print("\nQuery:")
print(query)

print("\nResults:")

for score, index in zip(scores, indices):
    print(
        round(float(score), 3),
        "->",
        texts[index]
    )