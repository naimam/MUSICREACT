"""genius.py: uses genius api to get a song's lyrics given song name"""
import os
from dotenv import find_dotenv, load_dotenv
import requests

load_dotenv(find_dotenv())

GENIUS_TOKEN = os.getenv("GENIUS_TOKEN")


def get_lyrics(track_name):
    """get_lyrics(track_name):returns a track name's genius lyrics url"""
    genius_response = requests.get(
        "https://api.genius.com/search",
        headers={"Authorization": f"Bearer {GENIUS_TOKEN}"},
        params={"q": track_name},
    )
    genius_response_json = genius_response.json()
    lyrics_url = genius_response_json["response"]["hits"][0]["result"]["url"]
    return lyrics_url
