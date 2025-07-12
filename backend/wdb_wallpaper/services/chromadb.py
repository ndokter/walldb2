import logging

import chromadb


def add_description(key, description):
    chroma_client = chromadb.PersistentClient()
    collection = chroma_client.get_or_create_collection(
        name="wallpaper_descriptions", 
        metadata={"hnsw:space": "cosine"}
    )
    collection.add(documents=[description], ids=[key])
    

def search(query, max_results: int = 50):
    chroma_client = chromadb.PersistentClient()
    collection = chroma_client.get_or_create_collection(
        name="wallpaper_descriptions", 
        metadata={"hnsw:space": "cosine"}
    )

    results = collection.query(
        query_texts=[query], 
        n_results=max_results,
        include=["documents", "distances"]
    )

    # best_match = min(results['distances'][0])
    # threshold = best_match + 0.2

    filtered_keys = [
        key for key, doc, dist in zip(results['ids'][0], results['documents'][0], results['distances'][0])
        # if dist <= threshold and dist < 0.8
        if dist < 0.8  # lower is more strict
    ]

    return filtered_keys
