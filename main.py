# Main entry point
import os
import shutil

from download_posts import download_posts
from create_posts import create_posts

# Clean up old directories and files for testing
os.remove('downloaded_posts.json') if os.path.exists('downloaded_posts.json') else None
shutil.rmtree('downloaded_posts', ignore_errors=True)
shutil.rmtree('new_posts', ignore_errors=True)

# Download posts from Instagram
downloaded_posts = download_posts()

# Create posts with the downloaded images
if downloaded_posts:
    create_posts(downloaded_posts)
else:
    print("No new posts to create.")
