import wdb_wallpaper.services.chromadb
import wdb_wallpaper.services.wallpaper
from django.core.management.base import BaseCommand
from wdb_wallpaper.models import Wallpaper


class Command(BaseCommand):

    def handle(self, *args, **kwargs):
        # tags = wdb_wallpaper.services.llm.generate_image_tags(
        #     provider='deepinfra',
        #     image_file_path='Wallpaper/1920_1200_Anno_1800_Botanica_wallpaper.jpg'
        # )
        # print(tags)


        description = wdb_wallpaper.services.llm.generate_description(
            provider='deepinfra',
            image_file_path='Wallpaper/1920_1200_Anno_1800_Botanica_wallpaper.jpg'
        )
        print(description)


        # self.readd_chromadb()


        # w = Wallpaper.objects.first()

        # wdb_wallpaper.services.ollama_.generate_description(image_file_path=w.image.path)

        # import chromadb
        # from chromadb.api.types import Documents, IDs
        # from chromadb.config import Settings

        # # Create a ChromaDB client in in-memory mode
        # chroma_client = chromadb.PersistentClient()
        # collection = chroma_client.get_or_create_collection(name="wallpaper_descriptions")

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
        # query = "holiday festive banana"
        # results = collection.query(
        #     query_texts=[query],
        #     n_results=3
        # )

        # # Print the results
        # from pprint import pprint
        # pprint(results)
        # print("Query:", query)
        # print("Results:")
        # for result in results['documents'][0]:
        #     print("-", result)

    # def readd_chromadb(self):
    #     for wallpaper in Wallpaper.objects.all():
    #         wdb_wallpaper.services.chromadb.add_description(
    #             key=str(wallpaper.id), 
    #             description=wallpaper.chromadb_description
    #         )
