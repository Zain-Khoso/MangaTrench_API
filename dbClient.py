# dbClient.py - Holds the Client class which is used to connect and operate over the Database.

from environs import Env
from pymongo import MongoClient
from pymongo.server_api import ServerApi


class Client:
    def __init__(self) -> None:
        # Reading the .env file.
        env = Env()
        env.read_env()

        # Getting the database-user's username and password from the .env-file.
        db_username = env.str("atlas_username")
        db_user_password = env.str("atlas_user_password")

        # Creating a client object for the Atlas-Cluster.
        client = MongoClient(
            f"mongodb+srv://{db_username}:{db_user_password}@maincluster.bwozlbo.mongodb.net/?retryWrites=true&w=majority",
            server_api=ServerApi("1"),
        )

        # Creating a Database inside the cluster.
        self.Database = client["MangaURLs"]

    def get_manga_list(self) -> list:
        # The list of available-manga.
        output_list = []

        for collectionName in self.Database.list_collection_names():
            # Collection OBJ.
            collection = self.Database.get_collection(collectionName)

            # Dictionary for storing the data for the current manga.
            currMangaDict = {}

            # Collecting MangaName, Total-Number-Chapters-Number, a Thumbnail.
            mangaName = collection.name
            totalChapters = collection.count_documents({})
            thumbnail = collection.find_one(
                {"ChapterNum": "1"}, {"_id": 0, "ChapterNum": 0}
            )["pages"][0]

            # Adding the collected fields to currMangaDict.
            currMangaDict.setdefault("name", mangaName)
            currMangaDict.setdefault("chapters", totalChapters)
            currMangaDict.setdefault("thumbnail", thumbnail)

            # Appending currMangaDict to output_list.
            output_list.append(currMangaDict)

        return output_list

    def get_chapters_list(self, mangaName):
        # Collection Object of the manga.
        collection = self.Database.get_collection(mangaName)

        # List of all the Chapter Numbers.
        chpNumList = []

        for chapterNum in collection.find({}, {"_id": 0, "ChapterNum": 1}):
            chpNumList.append(chapterNum["ChapterNum"])

        return chpNumList

    def get_chapter(self, mangaName, chapterNum):
        # Collection Object of the manga.
        collection = self.Database.get_collection(mangaName)

        # List of all the pages in a chapter.
        chapterPages = collection.find_one(
            {"ChapterNum": chapterNum}, {"_id": 0, "ChapterNum": 0}
        )["pages"]

        return chapterPages
