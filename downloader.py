# downloader.py

import instaloader
from config import SOURCE_USERNAME, IMAGE_DIR
import os

def download_new_posts():
    L = instaloader.Instaloader(download_pictures=True, download_video_thumbnails=False,
                                 download_video=False, save_metadata=False, post_metadata_txt_pattern='')
    profile = instaloader.Profile.from_username(L.context, SOURCE_USERNAME)

    os.makedirs(IMAGE_DIR, exist_ok=True)
    new_images = []

    for post in profile.get_posts():
        if post.typename != "GraphImage":
            continue
        filename = f"{IMAGE_DIR}{post.shortcode}.jpg"
        if os.path.exists(filename):
            continue
        L.download_post(post, target=IMAGE_DIR)
        new_images.append(filename)

    return new_images
