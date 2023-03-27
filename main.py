# main.py - The __main__ file of this API.

from fastapi import FastAPI
from dbClient import Client

# FastAPI & db_Client Instances.
app, dbClient = FastAPI(), Client()

# API Endpoints.

# A GET endpoint to get a list of all the manga in the database along with it's total number chapters and a thumbnail.
@app.get("/")
def read_manga_list():
    return dbClient.get_manga_list()


# A GET endpoint to get a list of all the available chapters to read for a specific manga.
@app.get("/{mangaName}/")
def read_chapters_list(mangaName: str):
    return dbClient.get_chapters_list(mangaName)


# A GET endpoint to get a specific chapter (whole-chapter) of a specifc manga.
@app.get("/{mangaName}/{chapterNum}")
def read_chapter(mangaName: str, chapterNum: str):
    return dbClient.get_chapter(mangaName, chapterNum)
