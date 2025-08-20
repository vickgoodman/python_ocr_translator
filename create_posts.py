# Create posts from downloaded posts
import os
import pytesseract
from openai import OpenAI
from config import DEVELOPER_PROMPT
from PIL import Image, ImageDraw, ImageFont


def is_mostly_black(image_path, threshold=30, ratio=0.9):
    img = Image.open(image_path).convert("L")  # Convert to grayscale
    pixels = list(img.getdata())

    dark_pixels = sum(p < threshold for p in pixels)
    total_pixels = len(pixels)

    return dark_pixels / total_pixels >= ratio


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
        post_text = pytesseract.image_to_string(img, lang='eng')

        # Read the caption text from the corresponding text file
        with open("downloaded_posts/" + post['shortcode'] + '.txt', 'r') as f:
            caption_text = f.read()

        # Create prompts for translation
        post_prompt = "Traduce coerent in română:\" " + post_text + "\""
        caption_prompt = "Traduce coerent in română:\" " + caption_text + "\". Nu tradu cuvintele care încep cu '#' și lasă-le neatinse."

        # Translate the post text and caption to a different language (coherently, with AI)
        client = OpenAI()

        post_completion = client.chat.completions.create(
            model="gpt-4.1",
            messages=[
                {"role": "developer", "content": DEVELOPER_PROMPT},
                {"role": "user", "content": post_prompt}
            ]
        )

        translated_post_text = post_completion.choices[0].message.content

        caption_completion = client.chat.completions.create(
            model="gpt-4.1",
            messages=[
                {"role": "developer", "content": DEVELOPER_PROMPT},
                {"role": "user", "content": caption_prompt}
            ]
        )

        translated_caption_text = caption_completion.choices[0].message.content

        # Place text on square(1080x1080) black image
        # Open Image
        img = Image.open('black_square.png')

        # Call draw Method to add 2D graphics in an image
        draw = ImageDraw.Draw(img)

        # Custom font style and font size
        font = ImageFont.truetype('Lato-Light.ttf', 45)

        # Width for the text box
        max_width = 780

        # Wrap text into lines
        wrapped_lines = wrap_text(translated_post_text, font, max_width, draw)

        # Starting position for the text box
        x = 150
        y = 540 - 55 * int(len(wrapped_lines)) // 2 # A line occupies around 55 pixels
        end_x, end_y = x + max_width, 930 # Ending position for the text box

        # Dimensions for the background box
        background_box = [(x, y), (end_x, end_y)]

        # Draw background box
        draw.rectangle(background_box, fill="black")

        description = ""
        for line in wrapped_lines:
            description += line + "\n"

        # Draw multiline text.
        draw.multiline_text((x, y), description, font=font, fill="white", spacing=4)

        if is_mostly_black(image_path):
            # Save the post
            img.save("new_posts/" + post['shortcode'] + '.png')
            # Save caption
            with open("new_posts/" + post['shortcode'] + '.txt', 'w') as f:
                f.write(translated_caption_text)

        print(f"Created post for {post['shortcode']}")
        print("-" * 50)
