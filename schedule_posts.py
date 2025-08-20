# Schedule posts on Instagram

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

def schedule_post():
    cl = login_insta()

    # Create scheduled posts directory
    os.makedirs("scheduled_posts", exist_ok=True)

    with open("downloaded_posts.json", "r") as f:
        data = json.load(f)
        shortcodes = data["shortcodes"]

    if shortcodes:
        shortcode = shortcodes[0]
    else:
        # Exit function
        print("No post to schedule.")
        return

    # Schedule each post
    print(f"Scheduling post for: {shortcode}")

    img_path = "new_posts/" + shortcode + '.png'
    caption_path = "new_posts/" + shortcode + '.txt'

    with open(caption_path, "r") as f:
        caption_text = f.read()

    # Upload photo
    cl.photo_upload(
        path=img_path,
        caption=caption_text
    )

    # Remove from downloaded_posts
    os.remove("downloaded_posts/" + shortcode + '.png')
    os.remove("downloaded_posts/" + shortcode + '.txt')
    # Remove from new_posts
    os.remove(img_path)
    os.remove(caption_path)

    # Remove from shortcodes
    data["shortcodes"] = [s for s in data["shortcodes"] if s != shortcode]

    # Save updated data
    with open("downloaded_posts.json", "w") as f:
        json.dump(data, f, indent=2)

cl = login_insta()
print("This is a test.")
# schedule_post()
