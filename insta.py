# insta.py
from instagrapi import Client
from dotenv import load_dotenv
import os
from instagrapi.types import StoryLink
import asyncio
from test import async_add_text_box
client = Client()

async def login():
    load_dotenv()
    id = os.getenv("ID")
    secret = os.getenv("PW")

    await asyncio.to_thread(client.login, id, secret)
    print("Logged in")

async def upload(img_link, caption, article_link):
    await asyncio.to_thread(client.photo_upload, img_link, caption)
    print("Feed Uploaded")
    story_img = await async_add_text_box(img_link)
    
    await asyncio.to_thread(client.photo_upload_to_story, path=story_img, links=[StoryLink(webUri=article_link)])
    os.remove(story_img)
    print("Story Uploaded")