import os
from dotenv import find_dotenv, load_dotenv
import requests

load_dotenv(find_dotenv())

GENIUS_TOKEN = os.getenv("GENIUS_TOKEN")


def get_lyrics(artist, track):
    search_term = artist, " ", track
    search_url = (
        f"http://api.genius.com/search?q={search_term}&access_token={GENIUS_TOKEN}"
    )

    respose = requests.get(search_url)
    json_data = respose.json()
    lyric_search = json_data["response"]["hits"][0]["result"]["url"]
    return lyric_search
