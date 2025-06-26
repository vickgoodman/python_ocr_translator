# main.py

from downloader import download_new_posts
from ocr import extract_text
from translator import translate_text
from image_editor import draw_translations
from uploader import upload_image
from utils import load_log, save_log
from config import TARGET_LANG, IMAGE_DIR
import os

def process_images():
    log = load_log()
    new_images = download_new_posts()

    for img_path in new_images:
        post_id = os.path.basename(img_path).split('.')[0]
        if post_id in log:
            continue

        ocr_data = extract_text(img_path)
        if not ocr_data:
            continue

        translations = [translate_text(text, TARGET_LANG) for (text, _) in ocr_data]
        out_path = f"{IMAGE_DIR}{post_id}_translated.jpg"
        draw_translations(img_path, ocr_data, translations, out_path)
        upload_image(out_path, caption="Automated translation 🌍")

        log.add(post_id)
        save_log(log)

if __name__ == "__main__":
    process_images()
