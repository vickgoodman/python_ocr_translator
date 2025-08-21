# File used to clean up old directories and files for testing
import os
import shutil

# Clean up old directories and files for testing
os.remove('downloaded_posts.json') if os.path.exists('downloaded_posts.json') else None
shutil.rmtree('downloaded_posts', ignore_errors=True)
shutil.rmtree('new_posts', ignore_errors=True)
