"""spotify.py: uses spotipy library to get a spotify artist's info and their track info"""
import os
import random
from dotenv import find_dotenv, load_dotenv
import spotipy
from spotipy.oauth2 import SpotifyClientCredentials

load_dotenv(find_dotenv())
CLIENT_ID = os.getenv("CLIENT_ID")
CLIENT_SECRET = os.getenv("CLIENT_SECRET")

client_credentials_manager = SpotifyClientCredentials(CLIENT_ID, CLIENT_SECRET)
sp = spotipy.Spotify(client_credentials_manager=client_credentials_manager)


def get_artist_info(artist_id):
    """gets information on a spotify artist given a valid id."""
    artist_uri = "spotify:artist:" + artist_id
    artist_tracks = sp.artist_top_tracks(artist_uri)
    artist = sp.artist(artist_uri)

    def get_artist_name(artist):
        return artist["name"]

    def get_artist_img(artist):
        return artist["images"][0]["url"]

    def get_artist_track_info(artist_tracks):
        random_track = random.randint(0, 4)
        track = artist_tracks["tracks"][random_track]
        track_info = []
        track_info.append(track["name"])
        track_info.append(track["preview_url"])
        track_info.append(track["album"]["images"][0]["url"])
        return track_info

    artist_name = get_artist_name(artist)
    artist_img = get_artist_img(artist)
    artist_track_info = get_artist_track_info(artist_tracks)
    return (
        artist_name,
        artist_img,
        artist_track_info,
    )
