# Main entry point

from download_posts import download_posts
from create_posts import create_posts
from notify import notify

# Download posts from Instagram
downloaded_posts = download_posts()

# Create posts with the downloaded images
if downloaded_posts:
    create_posts(downloaded_posts)
else:
    print("No new posts to create.")

notify("Download and create completed.")
