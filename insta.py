from instagrapi import Client
# import .env file
from dotenv import load_dotenv
import os
from instagrapi.types import StoryMention, StoryMedia, StoryLink, StoryHashtag, StorySticker, StoryStickerLink

# Load .env file
load_dotenv()
id = os.getenv("ID")
secret = os.getenv("PW")
print(id, secret)
# Create a client instance
client = Client()
client.login(id, secret)
# sticker = client.sticker_tray()
# print(sticker)
# client.photo_upload("0.jpg", "test")
client.photo_upload_to_story(path="images/1.jpg", stickers=[StorySticker(x=50, y=50, width=100, height=100, type="story_link", story_link=StoryStickerLink(url="https://www.google.com"))])
