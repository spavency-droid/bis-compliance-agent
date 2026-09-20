from services.semantic_search import SemanticSearcher


searcher = SemanticSearcher()


texts = [
    "battery powered toy car for children",
    "cotton shirt for adults",
    "plastic food storage container"
]


embeddings = searcher.encode(texts)


print("Number of texts:", len(texts))
print("Embedding shape:", embeddings.shape)