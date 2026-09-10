import chromadb

client = chromadb.PersistentClient(path="db")

collection = client.get_or_create_collection(
    name="medical_collection"
)


def retrieve_chunks(question, embedding_model, top_k=3):

    # Convert question into embedding
    query_embedding = embedding_model.encode(question)

    # Search database
    results = collection.query(
        query_embeddings=[query_embedding.tolist()],
        n_results=top_k
    )

    return results["documents"][0]