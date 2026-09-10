import chromadb

# Create a persistent client
client = chromadb.PersistentClient(path="db")

# Create or load the collection
collection = client.get_or_create_collection(
    name="medical_collection"
)


def store_embeddings(chunks, embeddings):
    """
    Store text chunks and embeddings in ChromaDB.
    """

    # Remove old data (for development)
    existing = collection.get()

    if len(existing["ids"]) > 0:
        collection.delete(ids=existing["ids"])

    ids = [str(i) for i in range(len(chunks))]

    collection.add(
        ids=ids,
        documents=chunks,
        embeddings=embeddings.tolist()
    )

    return len(ids)