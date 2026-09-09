import chromadb

# Create a persistent database
client = chromadb.PersistentClient(path="db")

# Create or load collection
collection = client.get_or_create_collection(
    name="medical_collection"
)


def store_embeddings(chunks, embeddings):
    """
    Store chunks and embeddings in ChromaDB.
    """

    ids = [str(i) for i in range(len(chunks))]

    collection.add(
        ids=ids,
        documents=chunks,
        embeddings=embeddings.tolist()
    )

    return len(ids)