import wdb_wallpaper.services.ollama_
from django.core.management.base import BaseCommand
from wdb_wallpaper.models import Wallpaper


class Command(BaseCommand):

    def handle(self, *args, **kwargs):
        # w = Wallpaper.objects.first()

        # wdb_wallpaper.services.ollama_.generate_description(image_file_path=w.image.path)

        import chromadb
        from chromadb.api.types import Documents, IDs
        from chromadb.config import Settings

        # Create a ChromaDB client in in-memory mode
        chroma_client = chromadb.PersistentClient()
        collection = chroma_client.get_or_create_collection(name="wallpaper_descriptions")

        # # Define some documents and their IDs
        # documents: Documents = [
        #     "The cat sat on the mat.",
        #     "The dog chased the squirrel.",
        #     "The bird flew in the sky.",
        #     "The fish swam in the ocean."
        # ]
        # ids: IDs = ["doc1", "doc2", "doc3", "doc4"]

        # # Add the documents to the collection
        # collection.add(
        #     documents=documents,
        #     ids=ids
        # )

        # Perform a semantic search
        query = "holiday festive banana"
        results = collection.query(
            query_texts=[query],
            n_results=3
        )

        # Print the results
        from pprint import pprint
        pprint(results)
        print("Query:", query)
        print("Results:")
        for result in results['documents'][0]:
            print("-", result)