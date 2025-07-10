import instaloader
import time
import random
from config import SOURCE_USERNAME, DEVELOPER_PROMPT, TARGET_USERNAME
import pytesseract
from PIL import Image, ImageDraw, ImageFont
from openai import OpenAI


def download_posts():
    L = instaloader.Instaloader(
        sleep=True,  # Add automatic delays
        request_timeout=60,  # Increase timeout
        max_connection_attempts=3  # Retry on connection errors
    )

    try:
        L.load_session_from_file(SOURCE_USERNAME)
        print("Loaded existing session")
    except FileNotFoundError:
        print("No existing session found, logging in...")
        L.interactive_login(SOURCE_USERNAME)
        print("Login successful, session saved")

    profile = instaloader.Profile.from_username(L.context, TARGET_USERNAME)

    print(profile.followers)
    L.download_profiles(profiles={profile}, max_count=5)


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
    download_posts()
    # create_post()
