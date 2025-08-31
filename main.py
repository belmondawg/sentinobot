import os
import tweepy
import requests 
import time 
import logging
import random

from dotenv import load_dotenv

from src.image_gen import ImageGen 
from src.song import Song

load_dotenv()

API_KEY                 = os.environ['API_KEY']
API_KEY_SECRET          = os.environ['API_KEY_SECRET']

ACCESS_TOKEN            = os.environ['ACCESS_TOKEN']
ACCESS_TOKEN_SECRET     = os.environ['ACCESS_TOKEN_SECRET']

BEARER_TOKEN            = os.environ['BEARER_TOKEN']

auth = tweepy.OAuth1UserHandler(API_KEY, API_KEY_SECRET, ACCESS_TOKEN, ACCESS_TOKEN_SECRET)
api = tweepy.API(auth)

client = tweepy.Client(BEARER_TOKEN, API_KEY, API_KEY_SECRET, ACCESS_TOKEN, ACCESS_TOKEN_SECRET)

logging.basicConfig(
    filename='sentino.log',
    format='%(asctime)s %(message)s',
    filemode='w'
)

logger = logging.getLogger()
logger.setLevel(logging.INFO)

def main():
    """Main loop"""

    while True:
        song = Song()

        image_data = requests.get(song.image_url).content
        album_image_data = requests.get(song.album_image_url).content

        image_gen = ImageGen(
            song.title,
            song.artist,
            song.album,
            song.get_random_line(),
            image_data,
            album_image_data,
            song.primary_color,
            song.secondary_color,
            song.text_color
        )

        image = image_gen.generate()
        image.save('data/image.png')

        logger.info('posting...')
        
        try:
            media = api.media_upload('data/image.png')
            tweet = client.create_tweet(media_ids=[media.media_id])
        except tweepy.errors.TooManyRequests:
            logging.info('done for today')
  
        time.sleep((60 * 60) * random.randint(1, 3))

if __name__ == '__main__':
    main()
