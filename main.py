import instaloader
import os
import json
from datetime import datetime
import time
import random
from config import SOURCE_USERNAME, TARGET_USERNAME, DEVELOPER_PROMPT
import pytesseract
from PIL import Image, ImageDraw, ImageFont
from openai import OpenAI
from pathlib import Path


def download_posts():
    # Configuration
    POSTS_DIR = "downloaded_posts"
    TRACKING_FILE = "downloaded_posts.json"

    L = instaloader.Instaloader(
        sleep=True,                 # Add automatic delays
        request_timeout=60,
        max_connection_attempts=3,  # Retry on connection errors
        download_pictures=True,
        download_videos=False,
        download_video_thumbnails=False,
        save_metadata=False
    )

    # Create posts directory
    os.makedirs(POSTS_DIR, exist_ok=True)

    # Load tracking data
    try:
        with open(TRACKING_FILE, 'r') as f:
            tracking_data = json.load(f)
            downloaded_posts = set(tracking_data.get('downloaded_posts', []))
            last_check = tracking_data.get('last_check')
    except FileNotFoundError:
        downloaded_posts = set()
        last_check = None
        print("First run - will download latest 20 posts")

    # Login
    try:
        L.load_session_from_file(SOURCE_USERNAME)
        print("Loaded existing session")
    except FileNotFoundError:
        print("No existing session found, logging in...")
        L.interactive_login(SOURCE_USERNAME)
        print("Login successful, session saved")

    # Get profile
    profile = instaloader.Profile.from_username(L.context, TARGET_USERNAME)
    print(f"Profile: {profile.username}, Posts: {profile.mediacount}")

    # Get posts
    posts = profile.get_posts()
    new_posts = []
    download_count = 0
    max_initial_posts = 20

    for post in posts:
        # Skip if already downloaded
        if post.shortcode in downloaded_posts:
            if last_check:  # If not first run, stop when we hit old posts
                print(f"Reached previously downloaded post: {post.shortcode}")
                break
            continue

        # Download the post
        try:
            print(f"Downloading post: {post.shortcode}")
            L.download_post(post, target=POSTS_DIR)

            # Track the new post
            downloaded_posts.add(post.shortcode)
            new_posts.append({
                'shortcode': post.shortcode,
                'date': post.date.isoformat(),
                'caption': post.caption[:100] if post.caption else ""
            })
            download_count += 1

            # Limit initial download to 20 posts
            if not last_check and download_count >= max_initial_posts:
                print(f"Downloaded {max_initial_posts} posts on first run")
                break

            time.sleep(random.uniform(1, 3))  # Random delay

        except Exception as e:
            print(f"Error downloading {post.shortcode}: {e}")
            continue

    # Update tracking file
    tracking_data = {
        'downloaded_posts': list(downloaded_posts),
        'last_check': datetime.now().isoformat(),
        'total_downloaded': len(downloaded_posts)
    }

    with open(TRACKING_FILE, 'w') as f:
        json.dump(tracking_data, f, indent=2)

    print(f"Downloaded {len(new_posts)} new posts")
    return new_posts


def wrap_text(text, font, max_width, draw):
    """
    Wraps text to fit within the max_width.
    """
    words = text.split()
    lines = [] # Holds each line in the text box
    current_line = [] # Holds each word in the current line under evaluation.

    for word in words:
        # Check the width of the current line with the new word added
        test_line = ' '.join(current_line + [word])
        width = draw.textlength(test_line, font=font)
        if width <= max_width:
            current_line.append(word)
        else:
            # If the line is too wide, finalize the current line and start a new one
            lines.append(' '.join(current_line))
            current_line = [word]

    # Add the last line
    if current_line:
        lines.append(' '.join(current_line))

    return lines


def create_post():
    image_path = "/home/goodman/acs/projects/python_ocr_translator/test2.jpg"

    # Load the image file
    img = Image.open(image_path)

    # Use pytesseract to extract text from the image
    text = pytesseract.image_to_string(img, lang='eng')

    prompt = "traduce coerent in romana:\"" + text + "\""

    # Translate the text to a different language (coherently, with AI)
    client = OpenAI()

    completion = client.chat.completions.create(
        model="gpt-4.1",
        messages=[
            {"role": "developer", "content": DEVELOPER_PROMPT},
            {"role": "user", "content": prompt}
        ]
    )

    translated_text = completion.choices[0].message.content

    # Print text
    print('Original text:\n', text)
    print('Translated text:\n', translated_text)

    # Place text on square(1080x1080) black image
    # Open Image
    img = Image.open('black_square.png')

    # Call draw Method to add 2D graphics in an image
    draw = ImageDraw.Draw(img)

    # Custom font style and font size
    font = ImageFont.truetype('FreeMono.ttf', 30)

    max_width = 780 # Width for the text box

    # Wrap text into lines
    wrapped_lines = wrap_text(translated_text, font, max_width, draw)

    # Calculate positions
    x, y = 150, 450  # Starting position for the text box
    end_x, end_y = x + max_width, y + (24 * int(len(wrapped_lines))) # Ending position for the text box

    # Dimensions for the background box
    background_box = [(x, y), (end_x, end_y)]

    # Draw background box
    draw.rectangle(background_box, fill="black")

    description = ""
    for line in wrapped_lines:
        description += line + "\n"

    # Draw multiline text.
    draw.multiline_text((x, y), description, font=font, fill="white", spacing=6)

    # Display edited image
    img.show()

    # Save edited image
    # img.save('')


if __name__ == "__main__":
    # Download posts from Instagram
    downloaded_posts = download_posts()

    # Create posts with the downloaded images
    new_posts = create_post(downloaded_posts)
