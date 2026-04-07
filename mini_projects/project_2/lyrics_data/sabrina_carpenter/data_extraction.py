from dotenv import load_dotenv
import os
from lyricsgenius import Genius
load_dotenv() 

token=os.getenv("CLIENT_ACCESS_TOKEN")
genius = Genius(token)
artist = genius.search_artist("Sabrina Carpenter", max_songs=3, sort="title")
print(artist.songs)