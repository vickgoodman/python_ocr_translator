# uploader.py

from instabot import Bot
from config import TARGET_USERNAME, TARGET_PASSWORD

def upload_image(image_path, caption=""):
    bot = Bot()
    bot.login(username=TARGET_USERNAME, password=TARGET_PASSWORD)
    bot.upload_photo(image_path, caption=caption)
