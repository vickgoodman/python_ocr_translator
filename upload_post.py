# Upload post on Instagram

import os
import json
from instagrapi import Client
from dotenv import load_dotenv
from config import SOURCE_USERNAME


def login_insta():
    load_dotenv()

    cl = Client()
    try:
        cl.load_settings("session.json")
        print("Loaded existing session")
    except FileNotFoundError:
        print("No existing session found, logging in...")

        source_password = os.getenv('SOURCE_PASSWORD')
        cl.login(SOURCE_USERNAME, source_password)
        cl.dump_settings("session.json")

        print("Login successful, session saved")

    return cl


def upload_post():
    cl = login_insta()

    # Load downloaded posts
    with open("downloaded_posts.json", "r") as f:
        data = json.load(f)
        shortcodes = data["shortcodes"]

    # Get the first shortcode
    if shortcodes:
        shortcode = shortcodes[0]
    else:
        # Exit function
        print("No post to upload.")
        return

    # Upload post
    print(f"Posting for: {shortcode}")
    print("-" * 50)

    # Get image and caption paths
    img_path = "created_posts/" + shortcode + '.png'
    caption_path = "created_posts/" + shortcode + '.txt'

    # Get caption text
    with open(caption_path, "r") as f:
        caption_text = f.read()

    # Upload photo
    cl.photo_upload(
        path=img_path,
        caption=caption_text
    )

    print("Removing files...")
    print("-" * 50)
    # Remove from downloaded_posts
    os.remove("downloaded_posts/" + shortcode + '.jpg')
    os.remove("downloaded_posts/" + shortcode + '.txt')

    # Remove from created_posts
    os.remove(img_path)
    os.remove(caption_path)

    # Remove from downloaded_posts.json
    data["shortcodes"] = [s for s in data["shortcodes"] if s != shortcode]

    # Save updated data
    with open("downloaded_posts.json", "w") as f:
        json.dump(data, f, indent=2)

    print(f"Post {shortcode} uploaded to Instagram successfully.")


cl = login_insta()
upload_post()
