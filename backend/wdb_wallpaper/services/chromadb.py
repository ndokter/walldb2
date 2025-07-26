import logging

import chromadb


def add_description(key, description):
    chroma_client = chromadb.PersistentClient()
    collection = chroma_client.get_or_create_collection(
        name="wallpaper_descriptions", 
        metadata={"hnsw:space": "cosine"}
    )
    collection.add(documents=[description], ids=[key])
    

def remove_key(key):
    chroma_client = chromadb.PersistentClient()
    collection = chroma_client.get_or_create_collection(
        name="wallpaper_descriptions", 
        metadata={"hnsw:space": "cosine"}
    )
    collection.delete(ids=[key])  


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

    # Lower (more strict) for short queries
    # threshold = 0.8 if len(query.split()) > 1 else 0.7
    threshold = 0.8

    from pprint import pprint as pp; pp(results)
    filtered_keys = [
        key for key, doc, dist in zip(results['ids'][0], results['documents'][0], results['distances'][0])
        if dist < threshold  
    ]

    return filtered_keys
