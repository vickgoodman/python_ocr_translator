# Create posts from downloaded posts
import os
import psutil
import pytesseract
from openai import OpenAI
from config import DEVELOPER_PROMPT
from PIL import Image, ImageDraw, ImageFont

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


def create_posts(downloaded_posts):
    # Create new posts directory
    NEW_POSTS_DIR = "new_posts"
    os.makedirs(NEW_POSTS_DIR, exist_ok=True)

    for post in downloaded_posts:
        print(f"Creating post for: {post['shortcode']}")
        image_path = "downloaded_posts/" + post['shortcode'] + '.jpg'

        # Load the image file
        img = Image.open(image_path)

        # Use pytesseract to extract text from the image
        text = pytesseract.image_to_string(img, lang='eng')

        prompt = "traduce coerent in română:\"" + text + "\""

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

        # Place text on square(1080x1080) black image
        # Open Image
        img = Image.open('black_square.png')

        # Call draw Method to add 2D graphics in an image
        draw = ImageDraw.Draw(img)

        # Custom font style and font size
        font = ImageFont.truetype('FreeMono.ttf', 30)

        # Width for the text box
        max_width = 780

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

        # Show the image for validation
        img.show()

        # Validation prompt
        print(f"\n--- Post Validation for {post['shortcode']} ---")
        print("Original text:", text)
        print("Translated text:", translated_text)

        while True:
            user_choice = input("\nDo you want to save this post? (y/n/q to quit): ").lower().strip()

            if user_choice in ['y', 'yes']:
                # Save the post
                img.save("new_posts/" + post['shortcode'] + '.png')
                print(f"✅ Post saved: {post['shortcode']}.png")
                break
            elif user_choice in ['n', 'no']:
                # Skip post
                print(f"❌ Post skipped: {post['shortcode']}")
                break
            elif user_choice in ['q', 'quit']:
                print("Exiting post creation...")
                return
            else:
                print("Please enter 'y' for yes, 'n' for no, or 'q' to quit.")

        # Close images by PID
        for proc in psutil.process_iter():
            if proc.name() == r"display-im6.q16":
                proc.kill()

        print("-" * 50)
