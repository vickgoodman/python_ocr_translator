# image_editor.py

import cv2
from PIL import ImageFont, ImageDraw, Image
import numpy as np

def draw_translations(image_path, ocr_data, translations, output_path):
    img = cv2.imread(image_path)
    img_pil = Image.fromarray(img)
    draw = ImageDraw.Draw(img_pil)
    font = ImageFont.truetype("arial.ttf", 24)

    for ((text, box), translated) in zip(ocr_data, translations):
        box = np.array(box).astype(int)
        x, y = box[0]
        draw.rectangle([tuple(box[0]), tuple(box[2])], fill=(255,255,255))  # Optional blur/cover
        draw.text((x, y), translated, fill=(0, 0, 0), font=font)

    img_pil.save(output_path)
