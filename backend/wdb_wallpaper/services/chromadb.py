import logging

import chromadb


def add_description(key, description):
    chroma_client = chromadb.PersistentClient()
    collection = chroma_client.get_or_create_collection(name="wallpaper_descriptions")
    collection.add(documents=[description], ids=[key])
    
