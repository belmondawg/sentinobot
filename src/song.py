import json
import random

class Song:
    """
    A class responsible for selecting a random song and managing it's data.

    Attributes:
        data (dict): Song data taken from Genius.
        song (dict): Randomly chosen song data from the dataset.
        title (str): Song's title.
        artist (str): Song's artist.
        album (str): Song's album name.
        primary_color (str): Primary color of the album cover represented in a hex value.
        secondary_color (str): Secondary color of the album cover represented in a hex value.
        text_color (str): Text color of the song represented in a hex value.
        album_image_url (str): Url to the album cover.
        image_url (str): Url to the album song. 

    Methods:
        get_random_line(): Acquires a random line from the song's data.
    """
    def __init__(self):
        self.data = json.load(open('data/Lyrics_Sentino.json', 'r'))
        self.song = random.choice(self.data.get("songs"))

    @property
    def title(self) -> str:
        return self.song.get('title_with_featured')

    @property
    def artist(self) -> str:
        return self.song.get('artist_names')

    @property
    def album(self) -> str:
        album = self.song.get('album')
        return album['name'] if album is not None else "Single"

    @property
    def primary_color(self) -> str:
        return self.song.get('song_art_primary_color')

    @property
    def secondary_color(self) -> str:
        return self.song.get('song_art_secondary_color')

    @property 
    def text_color(self) -> str:
        return self.song.get('song_art_text_color')

    @property
    def album_image_url(self) -> str:
        album = self.song.get('album')
        return album['cover_art_url'] if album is not None else self.song.get('song_art_image_url')

    @property 
    def image_url(self) -> str:
        return self.song.get('song_art_image_url')
           
    def get_random_line(self) -> str:
        lyrics = self.song.get('lyrics')
        line = random.choice(lyrics.split("\n"))
        blacklisted_characters = ['[', ']']

        for character in blacklisted_characters:
            if character in line or line.strip() == "" or len(line) > 40:
                return self.get_random_line()
            
        return line
        