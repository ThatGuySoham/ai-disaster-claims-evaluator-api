def store_chunks(chunks):
    """
    Minimal local store: append chunks to a local file so the app doesn't error.
    Replace with your real vector DB storage (FAISS, Pinecone, etc.).
    """
    with open("chunks_store.txt", "a", encoding="utf-8") as f:
        for i, c in enumerate(chunks):
            f.write(f"--- chunk {i} ---\n{c}\n")
