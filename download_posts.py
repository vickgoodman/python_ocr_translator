# Download posts from an instagram account
import os
import json
import time
import random
import instaloader
from datetime import datetime
from dotenv import load_dotenv
from config import SOURCE_USERNAME, TARGET_USERNAME

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
        save_metadata=False,
        filename_pattern="{shortcode}"
    )

    # Create posts directory
    os.makedirs(POSTS_DIR, exist_ok=True)

    # Load tracking data
    try:
        with open(TRACKING_FILE, 'r') as f:
            tracking_data = json.load(f)
            downloaded_posts = set(tracking_data.get('shortcodes', []))
            last_check = tracking_data.get('last_check')
            total_downloaded = tracking_data.get('total_downloaded', 0)
    except FileNotFoundError:
        downloaded_posts = set()
        last_check = None
        total_downloaded = 0
        print("First run - will download latest 20 posts")

    # Login
    try:
        L.load_session_from_file(SOURCE_USERNAME)
        print("Loaded existing session")
    except FileNotFoundError:
        print("No existing session found, logging in...")

        source_password = os.getenv('SOURCE_PASSWORD')
        L.login(SOURCE_USERNAME, source_password)

        print("Login successful, session saved")

    print("-" * 50)

    # Get profile
    profile = instaloader.Profile.from_username(L.context, TARGET_USERNAME)
    print(f"Profile: {profile.username}, Posts: {profile.mediacount}")

    print("-" * 50)
    # Get posts
    posts = profile.get_posts()
    new_posts = []
    download_count = 0
    max_initial_posts = 5

    for post in posts:
        # Skip if already downloaded
        if post.shortcode in downloaded_posts:
            if last_check:  # If not first run, stop when we hit old posts
                print(f"Reached previously downloaded post: {post.shortcode}")
                break
            continue

		# Skip posts with multiple photos (carousels/albums)
        if post.typename == 'GraphSidecar':
            print(f"Skipping multi-photo post: {post.shortcode}")
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
        print("-" * 50)

    # Update tracking file
    tracking_data = {
        'shortcodes': list(downloaded_posts),
        'last_check': datetime.now().isoformat(),
        'total_downloaded': total_downloaded + len(new_posts)  # Only increment by new downloads
    }

    with open(TRACKING_FILE, 'w') as f:
        json.dump(tracking_data, f, indent=2)

    print(f"Downloaded {len(new_posts)} new posts")
    print("-" * 50)
    return new_posts
